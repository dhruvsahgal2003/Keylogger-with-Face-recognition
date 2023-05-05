import cv2
from simple_facerec import SimpleFacerec

class faceRecognition():
    # faceRecognition constructor
    def __init__(self):
        self.isUnknown= False
        self.cap= cv2.VideoCapture(0) # To capture the real time video from webcamera
        self.sfr = SimpleFacerec() # this class is used for encoding the images and train them
        self.sfr.load_encoding_images("manikantaImages/") # for train the model, ##enter your images folder 
        
    #isUnknow() function is used for
    # knowing that the faces detected are known or unknown.
    def isUnknow(self):
        while True:
            ret, frame = self.cap.read() # this will read the input from webcam
            face_locations,face_names=self.sfr.detect_known_faces(frame) #this will detect the know faces 
            for face_loc, name in zip(face_locations, face_names): # this loop is used to print the box and name of the face detected
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                if(name== "mandala mani" or name=="Mani" or name == "manikanta" or name == "Manikanta" or name=="ManikantaMandala"): #Write your file names here
                    cv2.putText(frame, "Manikanta",(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    isUnknown=False
                else:
                    cv2.putText(frame, "Unknown",(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    isUnknown=True

                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,0,200),4)
            cv2.imshow("Frame",frame) #this will show the frame 
            key=cv2.waitKey(1) # if ESC key is pressed then the videoCapturing will stop and it will return the isUnknown value
            if key == 27:
                break
        self.cap.release()
        cv2.destroyAllWindows()
        return isUnknown # return statement of isUnknow() function

