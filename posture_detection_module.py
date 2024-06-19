import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import math
from mediapipe.python.solutions.drawing_utils import DrawingSpec

landmark_drawing_spec = DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)  # Green color for landmarks
connection_drawing_spec = DrawingSpec(color=(0, 255, 0), thickness=2)  # Red color for connections

class poseDetector():
    def __init__(self, mode=False, complexity =1, upBody = True, smooth = True, detectioncon = 0.5, trackcon = 0.5):
        self.mode = mode
        self.complexity = complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectioncon = detectioncon
        self.trackcon = trackcon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.complexity,self.upBody,self.smooth,self.detectioncon ,self.trackcon)

    def findPose(self , img, draw=True):
        
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
    
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS,landmark_drawing_spec,connection_drawing_spec)

        return img

        
    def findPosition(self,img,draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),8,(255,0,0),cv.FILLED)

        return self.lmList
    
    def findAngle(self,img,p1,p2,p3,draw=True):
        # Landmarks
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        x3,y3 = self.lmList[p3][1:]

        # Angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        
        if angle<0:
            angle+=360
        # print(angle)
        # drawing
        if draw:
            cv.line(img,(x1,y1),(x2,y2),(255,255,255),3)
            cv.line(img,(x2,y2),(x3,y3),(255,255,255),3)
            cv.circle(img,(x1,y1),8,(255,0,0),cv.FILLED)
            cv.circle(img,(x1,y1),15,(0,0,255),2)
            cv.circle(img,(x2,y2),8,(255,0,0),cv.FILLED)
            cv.circle(img,(x2,y2),15,(0,0,255),2)
            cv.circle(img,(x3,y3),8,(255,0,0),cv.FILLED)
            cv.circle(img,(x3,y3),15,(0,0,255),2)
            cv.putText(img, str(int(angle)),(x2-50,y2+50),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return angle


def main():
    pTime = 0


    cap = cv.VideoCapture(0)

    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        print(lmList)
        #FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)),(70,50),cv.FONT_HERSHEY_PLAIN,3,(0,255,0), 3)
        cv.imshow("Image",img)
        cv.waitKey(20)


if __name__ == "__main__":
    main()