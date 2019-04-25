import cv2
import array
import numpy as np
import math
#import serial 

gunDistanceFromCapX =10.41
gunDistanceFromCapY =7.293
gunDistanceFromCapZ =29.96

angelConstantOfCamera = 510
distanceOfTwoCameras = 55

rectangleCenterPont = ()
rectangleCenterPont1 = ()
tempHorizontalDistanceFromCap = None
tempHorizontalDistanceFromCap1 = None
tempAbsAngelDiff = None
#cancelPixelFromTwoCaps = ((10000 * 320 / angelConstantOfCamera) - distanceOfTwoCameras) * angelConstantOfCamera / 10000
#cancelExtraPixelFromTwoCaps = 10
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
cap1 = cv2.VideoCapture(1)
cap1.set(3, 320)
cap1.set(4, 240)

#arduino = serial.Serial('COM5', 9600)

while (cap.isOpened() and cap1.isOpened()):
        arrayOfPoints = [[]]
        arrayOfPoints1 = [[]]
        _ , frame= cap.read()
        (width,height,c) = frame.shape

        face_detection=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')   
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_detection.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h) , (0,255,0),2)
                rectangleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
#                if rectangleCenterPont[0] < (640 - cancelPixelFromTwoCaps + cancelExtraPixelFromTwoCaps) :
                arrayOfPoints.append([rectangleCenterPont[0], rectangleCenterPont[1]])
                cv2.circle(frame, rectangleCenterPont, 1, (0, 0, 255), 5)
        
        _ , frame1 = cap1.read()
        (width,height,c) = frame.shape

        face_detection=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        faces1=face_detection.detectMultiScale(gray1,1.3,5)
        for (x,y,w,h) in faces1:
                cv2.rectangle(frame1, (x,y), (x+w,y+h) , (0,255,0),2)
                rectangleCenterPont1 = ((x + x + w) // 2, (y + y + h) // 2)
#                if rectangleCenterPont1[0] > (640 - cancelPixelFromTwoCaps + cancelExtraPixelFromTwoCaps) :
                arrayOfPoints1.append([rectangleCenterPont1[0], rectangleCenterPont1[1]])
                cv2.circle(frame1, rectangleCenterPont1, 1, (0, 0, 255), 5)

        if cv2.waitKey(1) == 27 :
            break
        distancesFromCap = [[]]
        if len(arrayOfPoints) != 0 and len(arrayOfPoints) == len(arrayOfPoints1) :
                for i in range(0, len(arrayOfPoints)) :
                    if len(arrayOfPoints[i]) != 0 :
                        X = arrayOfPoints[i][0]
                        Y = arrayOfPoints[i][1]
                        X1 = arrayOfPoints1[i][0]
                        Y1 = arrayOfPoints1[i][1]
                        absCordinateX = X - cap.get(3)//2
                        absCordinateY = Y - cap.get(4)//2
                        absCordinateX1 = X1 - cap1.get(3)//2
                        absCordinateY1 = Y1 - cap1.get(4)//2
                        horizontalAngel = math.atan(absCordinateX/ angelConstantOfCamera)
                        verticalAngel = math.atan(absCordinateY/ angelConstantOfCamera)
                        horizontalAngel1 = math.atan(absCordinateX1/ angelConstantOfCamera)
                        verticalAngel1 = math.atan(absCordinateY1/ angelConstantOfCamera)
                        # abs = absolute
                        if absCordinateX - absCordinateX1 == 0 :
                                distanceConst = distanceOfTwoCameras/ tempAbsAngelDiff
                        else :
                                tempAbsAngelDiff = absCordinateX - absCordinateX1 
                                distanceConst = distanceOfTwoCameras/ tempAbsAngelDiff
                        # cap1 mustbe at +ve dirrection wrt cap
                        if horizontalAngel == 0 :
                            horizontalDistanceFromCap = tempHorizontalDistanceFromCap
                        else :
                            horizontalDistanceFromCap = distanceConst * absCordinateX / math.sin(horizontalAngel)
                            tempHorizontalDistanceFromCap = horizontalDistanceFromCap
                        totalDistancdFromCap = str(horizontalDistanceFromCap / math.cos(verticalAngel))
                        cv2.putText(frame, totalDistancdFromCap,(X+10, Y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA);
                        distancesFromCap.append([horizontalDistanceFromCap, math.tan(verticalAngel) * horizontalDistanceFromCap, math.tan(horizontalAngel) * horizontalDistanceFromCap])
                        if horizontalAngel1 == 0 :
                            horizontalDistanceFromCap1 = tempHorizontalDistanceFromCap1
                        else :
                            horizontalDistanceFromCap1 = distanceConst * absCordinateX1 / math.sin(horizontalAngel1)
                            tempHorizontalDistanceFromCap1 = horizontalDistanceFromCap1            
                        totalDistancdFromCap1 = str(horizontalDistanceFromCap1 / math.cos(verticalAngel1))
                        cv2.putText(frame1, totalDistancdFromCap1,(X1+10, Y1+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA);
                distancesFromCap.remove([])
                if len(distancesFromCap) > 0 :
                        distanceOfObjFromGunZ = abs(distancesFromCap[0][0] - gunDistanceFromCapZ)
                        distanceOfObjFromGunY = distancesFromCap[0][1] - gunDistanceFromCapY
                        distanceOfObjFromGunX = distancesFromCap[0][2] - gunDistanceFromCapX

                        angelWRTGunAlongX = math.atan(distanceOfObjFromGunX / distanceOfObjFromGunY) *180 / math.pi
                        angelWRTGunAlongY = math.atan(distanceOfObjFromGunZ / distanceOfObjFromGunY) *180 / math.pi
                
#                        arduino.write(str(int(round(angelWRTGunAlongX)) + 90).encode())
#                        arduino.write(str(int(round(angelWRTGunAlongY)) + 90).encode())
                        print('X ',str(int(round(angelWRTGunAlongX)) + 90))
                        print('Y ',str(int(round(angelWRTGunAlongY)) + 90))
        cv2.imshow('iamge',frame)
        cv2.imshow('iamge1',frame1)
cap.release()
cap1.release()
cv2.destroyAllWindows()
