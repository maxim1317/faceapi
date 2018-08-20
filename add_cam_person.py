import cognitive_face as CF

# import glob
import time
import cv2
import os
import json
import shutil

from transliterate import translit, get_available_language_codes

from termcolor import colored

from apiconsts import *

home = '/home/oberon/Downloads/'
# bak_face_list = glob.glob(home + 'bak/*.jpg')
# mik_face_list = glob.glob(home + 'mik/*.jpg')

# tst_face_list = glob.glob(home + 'tst/*.jpg')
# print(bak_face_list)

def add_cf():
    os.system('ln -s /home/oberon/utilities/Cognitive-Face-Python/cognitive_face .')

def ask_FIO():
    FIO = {}
    FIO['surname'] = input('Фамилия:')
    FIO['name'] = input('Имя:')
    FIO['middlename'] = input('Отчество:')

    return FIO

def add_camera_person(FIO, nameID, groupID):
    try:
        person = CF.person.create(groupID, nameID, json.dumps(FIO))

    except Exception as e:
        print(e)

    cap = cv2.VideoCapture(0)

    watching = False
    pics = 0

    pic_dir = 'pics/nameID_' + nameID + '/'
    ensure_dir(pic_dir)


    pbar = tqdm(total=pics_needed)

    while (watching == False):
        ret, frame = cap.read()

        face = pic_dir+'pic_'+str(pics)+'.jpg'
        cv2.imwrite(face, frame)
        # print(face)

        time.sleep(5)

        try:
            CF.person.add_face(os.path.abspath(face), groupID, person['personId'])
            pics += 1
            pbar.update(1)    
        except Exception as e:
            # print(e)
            pass

        if pics == pics_needed:
            print (colored('READY!', color='green'))
            watching = True

    pbar.close()

    time.sleep(5)

    # train group
    try:
        CF.person_group.train(groupID)
        print (colored('Sent to training!', color='green'))

    except Exception as e:
        print(e)

    shutil.rmtree('pics/', ignore_errors=True, onerror=None)

    while (True):
        pass
        try:
            print(CF.person_group.get_status(groupID))
            print (colored('TRAINED!', color='green'))
            return person['personId']
        except Exception as e:
            print(e)

    cap.release()



def main():
    add_cf()

    CF.Key.set(subscription_key)
    CF.BaseUrl.set(uri_base)

    # Create group with id '1534'
    try:
        CF.person_group.create(groupID, 'important')
    
    except Exception as e:
        print(e)




    # FIO = ask_FIO()

    FIO = {'name' : 'Макс', 'surname' : 'Снес' , 'middlename' : '_'}

    nameID = translit(FIO['name'] + FIO['surname'], 'ru', reversed=True)

    add_camera_person(FIO, str(nameID), groupID)

    os.remove('cognitive_face')


if __name__ == '__main__':
    main()

