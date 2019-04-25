import cv2
import array
import numpy as np
import math

angelConstantOfCamera = 512
distanceOfTwoCameras = 19.5

minDistanceOfActionLineFromCaps = 20
maxDistanceOfActionLineFromCaps = 200

tempHorizontalDistanceFromCapFor1stForLoop = 5
tempHorizontalDistanceFromCap1For1stForLoop = 5
tempHorizontalDistanceFromCapFor2ndForLoop = 5
tempHorizontalDistanceFromCap1For2ndForLoop = 5
tempAbsAngelDiffFor1stForLoop = 5
tempAbsAngelDiffFor2ndForLoop = 5

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while (cap.isOpened() and cap1.isOpened()):
        ret, img11 = cap.read()
        ret, img21 = cap1.read()
        if cv2.waitKey(10) == 27 :
            break
        ret, img12 = cap.read()
        ret, img22 = cap1.read()
        
        img = cv2.cvtColor(cv2.absdiff(img11, img12), cv2.COLOR_BGR2GRAY)
        retval, img = cv2.threshold(img, 22, 255, cv2.THRESH_BINARY)
    
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        arrayOfPoints = [[]]
        for i in range(0, len(contours)) :
            if len(contours[i]) > 20 :
                x = 0
                y = 0
                for j in range(0, len(contours[i])) :
                    x = x + contours[i][j][0][0]
                    y = y + contours[i][j][0][1]
                cmX = x / (len(contours[i]))
                cmY = y / (len(contours[i]))
                arrayOfPoints.append([cmX , cmY, len(contours[i])])
        arrayOfPoints.remove([])
        arrayOfPoints = sorted(arrayOfPoints, key=lambda x: x[0])
        
        img1 = cv2.cvtColor(cv2.absdiff(img21, img22), cv2.COLOR_BGR2GRAY)
        retval, img1 = cv2.threshold(img1, 22, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        arrayOfPoints1 = [[]]
        for i in range(0, len(contours)) :
            if len(contours[i]) > 20 :
                    x = 0
                    y = 0
                    for j in range(0, len(contours[i])) :
                        x = x + contours[i][j][0][0]
                        y = y + contours[i][j][0][1]
                    cmX = x / (len(contours[i]))
                    cmY = y / (len(contours[i]))
                    arrayOfPoints1.append([cmX , cmY, len(contours[i])])
        arrayOfPoints1.remove([])
        arrayOfPoints1 = sorted(arrayOfPoints1, key=lambda x: x[0])

        modifiedArrayOfPoints = [[]]
        modifiedArrayOfPoints1 = [[]]
        for i in range(0, len(arrayOfPoints)) :
                if i == len(arrayOfPoints1) :
                        break
                else :
                        if abs(arrayOfPoints[i][2] - arrayOfPoints1[i][2]) < 30 :
                                modifiedArrayOfPoints.append([arrayOfPoints[i][0], arrayOfPoints[i][1]])
                                modifiedArrayOfPoints1.append([arrayOfPoints1[i][0], arrayOfPoints1[i][1]])
        modifiedArrayOfPoints.remove([])
        modifiedArrayOfPoints1.remove([])

        
        cmDistanceAreaArray = [[]]
        cmDistanceAreaArray1 = [[]]
        if len(modifiedArrayOfPoints) != 0 and len(modifiedArrayOfPoints) == len(modifiedArrayOfPoints1) :
            for i in range(0, len(modifiedArrayOfPoints)) :
                if len(arrayOfPoints[i]) != 0 :
                    X = modifiedArrayOfPoints[i][0]
                    Y = modifiedArrayOfPoints[i][1]
                    X1 = modifiedArrayOfPoints1[i][0]
                    Y1 = modifiedArrayOfPoints1[i][1]
                    absCordinateX = X - 320
                    absCordinateX1 = X1 - 320
                    horizontalAngel = math.atan((X - 320)/ angelConstantOfCamera)
                    verticalAngel = math.atan((Y - 240)/ angelConstantOfCamera)
                    horizontalAngel1 = math.atan((X1 - 320)/ angelConstantOfCamera)
                    verticalAngel1 = math.atan((Y1 - 240)/ angelConstantOfCamera)
                    if absCordinateX - absCordinateX1 == 0 :
                        distanceConst = distanceOfTwoCameras/ tempAbsAngelDiffFor1stForLoop
                    else :
                        tempAbsAngelDiffFor1stForLoop = absCordinateX - absCordinateX1 
                        distanceConst = distanceOfTwoCameras/ tempAbsAngelDiffFor1stForLoop
                    if horizontalAngel == 0 :
                        horizontalDistanceFromCap = tempHorizontalDistanceFromCapFor1stForLoop
                    else :
                        horizontalDistanceFromCap = distanceConst * absCordinateX / math.sin(horizontalAngel)
                        tempHorizontalDistanceFromCapFor1stForLoop = horizontalDistanceFromCap
                    totalDistancdFromCap = horizontalDistanceFromCap / math.cos(verticalAngel)
                    if horizontalAngel1 == 0 :
                        horizontalDistanceFromCap1 = tempHorizontalDistanceFromCap1For1stForLoop
                    else :
                        horizontalDistanceFromCap1 = distanceConst * absCordinateX1 / math.sin(horizontalAngel1)
                        tempHorizontalDistanceFromCap1For1stForLoop = horizontalDistanceFromCap1            
                    totalDistancdFromCap1 = horizontalDistanceFromCap1 / math.cos(verticalAngel1)
                    cmDistanceAreaArray.append([X, Y, horizontalAngel, verticalAngel, totalDistancdFromCap])
                    cmDistanceAreaArray1.append([X1, Y1, horizontalAngel1, verticalAngel1, totalDistancdFromCap1])
        else :
                print("len(modifiedArrayOfPoints) may be 0 or ERROR in 1st for loop")           
        cmDistanceAreaArray.remove([])
        cmDistanceAreaArray1.remove([])
        cmDistanceAreaArray = sorted(cmDistanceAreaArray, key=lambda x : x[4])
        cmDistanceAreaArray1 = sorted(cmDistanceAreaArray1, key=lambda x : x[4])

        count = 0
        while(True) :
                if count == len(cmDistanceAreaArray) - 2 or len(cmDistanceAreaArray) < 2 :
                        break
                else :
                      if abs(cmDistanceAreaArray[count][4] - cmDistanceAreaArray[count + 1][4]) < 15 :
                                cmDistanceAreaArray[count][0] = (cmDistanceAreaArray[count][0] + cmDistanceAreaArray[count + 1][0]) / 2
                                cmDistanceAreaArray[count][1] = (cmDistanceAreaArray[count][1] + cmDistanceAreaArray[count + 1][1]) / 2
                                cmDistanceAreaArray.remove(cmDistanceAreaArray[count + 1])
                      else :
                              count = count + 1
        count = 0
        while(True) :
                if count == len(cmDistanceAreaArray1) - 2 or len(cmDistanceAreaArray1) < 2 :
                        break
                else :
                      if abs(cmDistanceAreaArray1[count][4] - cmDistanceAreaArray1[count + 1][4]) < 15 :
                                cmDistanceAreaArray1[count][0] = (cmDistanceAreaArray1[count][0] + cmDistanceAreaArray1[count + 1][0]) / 2
                                cmDistanceAreaArray1[count][1] = (cmDistanceAreaArray1[count][1] + cmDistanceAreaArray1[count + 1][1]) / 2
                                cmDistanceAreaArray1.remove(cmDistanceAreaArray1[count + 1])
                      else :
                              count = count + 1

        if len(cmDistanceAreaArray) == len(cmDistanceAreaArray1) and len(cmDistanceAreaArray) != 0 :
            for i in range(0, len(modifiedArrayOfPoints)) :
                if len(arrayOfPoints[i]) != 0 :
                    X = int(round(cmDistanceAreaArray[i][0]))
                    Y = int(round(cmDistanceAreaArray[i][1]))
                    X1 = int(round(cmDistanceAreaArray1[i][0]))
                    Y1 = int(round(cmDistanceAreaArray1[i][1]))
                    absCordinateX = X - 320
                    absCordinateX1 = X1 - 320
                    horizontalAngel = math.atan((X - 320)/ angelConstantOfCamera)
                    verticalAngel = math.atan((Y - 240)/ angelConstantOfCamera)
                    horizontalAngel1 = math.atan((X1 - 320)/ angelConstantOfCamera)
                    verticalAngel1 = math.atan((Y1 - 240)/ angelConstantOfCamera)
                    if absCordinateX - absCordinateX1 == 0 :
                        distanceConst = distanceOfTwoCameras/ tempAbsAngelDiffFor2ndForLoop
                    else :
                        tempAbsAngelDiffFor2ndForLoop = absCordinateX - absCordinateX1 
                        distanceConst = distanceOfTwoCameras/ tempAbsAngelDiffFor2ndForLoop
                    if horizontalAngel == 0 :
                        horizontalDistanceFromCap = tempHorizontalDistanceFromCapFor2ndForLoop
                    else :
                        horizontalDistanceFromCap = distanceConst * absCordinateX / math.sin(horizontalAngel)
                        tempHorizontalDistanceFromCapFor2ndForLoop = horizontalDistanceFromCap
                    totalDistancdFromCap = str(horizontalDistanceFromCap / math.cos(verticalAngel))
                    cv2.circle(img12, (X, Y), 4, (0, 0, 255), -1)
                    cv2.putText(img12, totalDistancdFromCap,(X+10, Y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA);
                    if horizontalAngel1 == 0 :
                        horizontalDistanceFromCap1 = tempHorizontalDistanceFromCap1
                    else :
                        horizontalDistanceFromCap1 = distanceConst * absCordinateX1 / math.sin(horizontalAngel1)
                        tempHorizontalDistanceFromCap1 = horizontalDistanceFromCap1            
                    totalDistancdFromCap1 = str(horizontalDistanceFromCap1 / math.cos(verticalAngel1))
                    if abs(horizontalDistanceFromCap1) > minDistanceOfActionLineFromCaps and abs(horizontalDistanceFromCap1) < maxDistanceOfActionLineFromCaps :
                            cv2.circle(img22, (X1, Y1), 4, (0, 0, 255), -1)
                            cv2.putText(img22, totalDistancdFromCap1,(X1+10, Y1+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA);
                            print('distance ', X1, ' ',Y1 ,' ' , horizontalDistanceFromCap1)
                            cmDistanceAreaArray.append([X, Y, horizontalAngel, verticalAngel, totalDistancdFromCap])
                            cmDistanceAreaArray1.append([X1, Y1, horizontalAngel1, verticalAngel1, totalDistancdFromCap1])
        else :
                print("len(cmDistanceAreaArray1) = 0 or ERROR in 2nd for loop")         
                              
        cv2.imshow('iamge',img12)
        cv2.imshow('iamge1',img22)
        
cap.release()
cap1.release()
cv2.destroyAllWindows()
