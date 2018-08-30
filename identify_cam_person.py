from consts import *
from utils import *


def main():

    colorama.init()

    CF.Key.set(subscription_key)
    CF.BaseUrl.set(uri_base)
  
    # source = 'http://localhost:8080/u3.mpg' # Name of the stream or webcam

    source = 0

    while testDevice(source) == False: # Check if stream even works
        pass

    cap = cv2.VideoCapture(source) # Open stream

    print('\n#######################################################\n')
    
    checkIfTrained() # Checking if person_group is trained

    while True :

        print('\n#######################################################\n')

        detected_faces = sendToDetection(cap) # Looking for faces
        print()
        
        identified_faces = sendToIdentification(detected_faces) # Trying to identify faces
        print()

        if len(identified_faces) != 0: # Identified something?            
            for identified_face in identified_faces:                
                front_payload['userData'] = sendDataRequest(identified_face) # Getting user data
                print()

                sendToFront() # Sending to Front

    cap.release()

if __name__ == '__main__':
    main()
