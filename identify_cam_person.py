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


        detected = []
        while len(detected) == 0:
            time.sleep(wait_time)
            detected = CF.face.detect(tmp_pic) # Trying to detect faces

        for detected_face in detected:
            detected_faces.append({'faceId' : detected_face['faceId'], 'faceRectangle': detected_face['faceRectangle']}) # Remembering face IDs and rectangles 
            print(detected_face['faceId'])

        try:
            time.sleep(wait_time)
            identified_faces = CF.face.identify([d_f['faceId'] for d_f in detected_faces], groupID) # Trying to identify faces
            print(identified_faces)

        except Exception as e:
            print(e)
            # time.sleep(wait_time)
            continue
        
        if len(identified_faces) != 0: # Identified something?
            
        
            for identified_face in identified_faces:
                if identified_face['candidates'][0]['confidence'] >= threshold:

                    # for face in detected_faces: # Trying to find bounding box
                    #     if face['faceId'] == identified_face['faceId']:
                    #         rect = face['faceRectangle']
                
                    time.sleep(wait_time)
                    person = CF.person.get(groupID, identified_face['candidates'][0]['personId']) # Getting person data

                    # print(data)
                    # to_front.send(person['userData']) # Sending to front
                    headers = {
                        'Content-Type': 'application/json',
                    }
                    payload = {
                        'userData' : (person['userData']), 
                        'inHelmet' : False,
                    }

                    r = requests.post("http://localhost:9000/rest/userdata", headers=headers, data=json.dumps(payload))
                    print((person['userData']))
                    print(r.text)
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

    time.sleep(wait_time)

    detect(groupID)

if __name__ == '__main__':
    main()
