import cognitive_face as CF

import time
import json
import cv2

from apiconsts import *

def check_if_trained(groupID):

    while (True):
        pass
        try:
            print(CF.person_group.get_status(groupID))
            # print (colored('TRAINED!', color='green'))
            return 0
        except Exception as e:
            print(e)
            time.sleep(5)

def detect(groupID):

    cap = cv2.VideoCapture('http://localhost:8080/u3.mpg')

    pic_dir = 'pics/nameID_' + '0' + '/'
    ensure_dir(pic_dir)
    os.remove(pic_dir+'pic_'+ '0' +'.jpg')

    recognised = False

    while recognised == False :

        try:

            _, frame = cap.read()

            face = pic_dir+'pic_'+ '0' +'.jpg'
            
            cv2.imwrite(face, frame)

            detected = CF.face.detect(face)
            print(detected[0]['faceId'])
            candidate = CF.face.identify([detected[0]['faceId']], groupID)
            person = CF.person.get(groupID, candidate[0]['candidates'][0]['personId'])

            userDataDecoded = json.loads(person['userData'])

            recognised = True
            name = userDataDecoded['name']
            surname = userDataDecoded['surname']
            middlename = userDataDecoded['middlename']
            print ('Detected: ' + name + ' ' + middlename + ' ' + surname)
        except Exception as e:
            print(e)
            time.sleep(5)

    cap.release()

def main():

    CF.Key.set(subscription_key)
    CF.BaseUrl.set(uri_base)

    check_if_trained(groupID)

    detect(groupID)

if __name__ == '__main__':
    main()
