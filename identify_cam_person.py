import json
import time
import requests

import cognitive_face as CF
import cv2
from PIL import Image

from apiconsts import *


def testDevice(source):
    '''
        Trying to open webcam/stream
    '''
    cap = cv2.VideoCapture(source) 
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
        cap.release()
        return False
    return True

def checkIfTrained(groupID):
    while (True):
        pass
        try:
            print(CF.person_group.get_status(groupID))
            return 0
            
        except Exception as e:
            print(e)
            time.sleep(wait_time)

def detect(groupID):

    # source = 'http://localhost:8080/u3.mpg' # Name of the stream or webcam

    source = 0

    while testDevice(source) == False: # Check if stream even works
        pass

    cap = cv2.VideoCapture(source) # Open stream

    pic_dir = 'pics/frame/' # I save last frame here for cropping and stuff
    ensure_dir(pic_dir) # check if dir exists
    # os.remove(pic_dir+'pic_'+ '0' +'.jpg') # lil cleanup

    detected_dir = 'pics/detected/'
    ensure_dir(detected_dir)

    while True :

        detected_faces = []

        _, frame = cap.read() # Read next frame

        tmp_pic = pic_dir + 'pic_' + '0' +'.jpg'   
        cv2.imwrite(tmp_pic, frame) # Saving frame for a while

        detected = CF.face.detect(tmp_pic) # Trying to detect faces
        if len(detected) == 0: # Found something?
            continue

        for detected_face in detected:
            detected_faces.append({'faceId' : detected_face['faceId'], 'faceRectangle': detected_face['faceRectangle']}) # Remembering face IDs and rectangles 
        # print(detected[0]['faceId'])

        try:
            identified_faces = CF.face.identify([d_f['faceId'] for d_f in detected_faces], groupID) # Trying to identify faces

        except Exception as e:
            print(e)
            time.sleep(wait_time)
            continue
        
        if len(identified_faces) == 0: # Identified something?
            continue
        
        for identified_face in identified_faces:
            if identified_face['candidates'][0]['confidence'] >= treshold:

                time.sleep(wait_time)
                # for face in detected_faces: # Trying to find bounding box
                #     if face['faceId'] == identified_face['faceId']:
                #         rect = face['faceRectangle']
            
                time.sleep(wait_time)
                person = CF.person.get(groupID, identified_face['candidates'][0]['personId']) # Getting person data

                # print(data)
                # to_front.send(person['userData']) # Sending to front
                r = requests.post("http://localhost:9000/rest/userdata", data={'userData' : person['userData'], 'inHelmet' : False})
                print(r)

        # userDataDecoded = json.loads(person['userData'])

        # name = userDataDecoded['name']
        # surname = userDataDecoded['surname']
        # middlename = userDataDecoded['middlename']
        # print ('Detected: ' + name + ' ' + middlename + ' ' + surname)

    cap.release()

def main():

    CF.Key.set(subscription_key)
    CF.BaseUrl.set(uri_base)

    checkIfTrained(groupID)

    detect(groupID)

if __name__ == '__main__':
    main()
