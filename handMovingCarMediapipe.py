import cv2 as cv
import mediapipe as mp
import time
import serial
import math

#arduino = serial.Serial('COM8', 9600)
#time.sleep(2)
vid = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]
palm_ids = [0, 1, 5, 9, 13, 17]  # Palm keypoints: wrist (0) and finger bases (1, 5, 9, 13, 17)
Rcenter_x , Rcenter_y , Lcenter_x ,Lcenter_y =0,0,0,0
HandL,HandR = True,True

while True:
    ret, frame = vid.read()
    if not ret:
         break
    frame = cv.flip(frame, 1)
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    

    if results.multi_hand_landmarks:
           
            for handLms in results.multi_hand_landmarks:
                
                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy]) 
                    
                if len(lmList) != 0:
                        
                    HandR = lmList[4][1] < lmList[20][1] # True if right hand exist
                    HandL = lmList[4][1] > lmList[20][1] # True if right hand exist  

                    if HandR == True:
                        #Text Coordinates
                        text_x = lmList[8][1] -40
                        text_y = lmList[8][2]-50
                        #Rectangle Coordinates
                        corner1_x = lmList[4][1] - 20
                        corner1_y = lmList[8][2] - 20
                        corner2_x = lmList[20][1] + 20
                        corner2_y = lmList[1][2] + 20

                        # Palm keypoints: wrist (0) and finger bases (1, 5, 9, 13, 17)
                        Rcenter_x = int(sum([lmList[i][1] for i in palm_ids]) / len(palm_ids))
                        Rcenter_y = int(sum([lmList[i][2] for i in palm_ids]) / len(palm_ids))
                            
                        # Draw a solid dot at the hand center
                        cv.circle(frame, (Rcenter_x, Rcenter_y), 8, (0, 0, 255), cv.FILLED)

                        cv.putText(frame,'Right', (text_x,text_y),cv.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 4)
                        cv.rectangle(frame , (corner1_x,corner1_y) , (corner2_x,corner2_y) , (255, 0, 255) , 3)
            
                    elif HandL == True:   
                        #Text Coordinates
                        text_x = lmList[16][1]-40
                        text_y = lmList[8][2]-50
                        #Rectangle Coordinates
                        corner1_x = lmList[20][1] - 20
                        corner1_y = lmList[8][2] - 20
                        corner2_x = lmList[4][1] + 20
                        corner2_y = lmList[1][2] + 20          

                        # Palm keypoints: wrist (0) and finger bases (1, 5, 9, 13, 17)
                        Lcenter_x = int(sum([lmList[i][1] for i in palm_ids]) / len(palm_ids))
                        Lcenter_y = int(sum([lmList[i][2] for i in palm_ids]) / len(palm_ids))
                            
                        # Draw a solid dot at the hand center
                        cv.circle(frame, (Lcenter_x, Lcenter_y), 8, (0, 0, 255), cv.FILLED) 
                        
                        cv.putText(frame,'Left', (text_x,text_y),cv.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 4)  
                        cv.rectangle(frame , (corner1_x,corner1_y) , (corner2_x,corner2_y) , (255, 0, 255) , 3)

                    # ========= If <2 hands stop ==========
                    if len(results.multi_hand_landmarks) < 2: 
                        cv.putText(frame,'Stop', (20,70),cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3)   #BGR
                        #arduino.write(b"S")
                    else:
                        # ============ Drawing =============
                        CircleCentreX = (Rcenter_x+Lcenter_x)//2
                        CircleCentreY = (Rcenter_y+Lcenter_y)//2
                        Radius = int(math.hypot(Rcenter_x - Lcenter_x, Rcenter_y - Lcenter_y) / 2)  

                        cv.line(frame , (Lcenter_x,Lcenter_y) , (Rcenter_x,Rcenter_y) , (0,0,0) , 5) #wheel Line
                        cv.circle(frame, (CircleCentreX,CircleCentreY), 8,(0,0,255), -1) #Line Middle dot
                        cv.circle(frame , (CircleCentreX,CircleCentreY) , Radius , (0,0,0) , 5) #Wheel Circle

                        # ============= Moving =============
                        if Lcenter_y+30 < Rcenter_y: #Right
                            cv.putText(frame,'Move Right', (20,70),cv.FONT_HERSHEY_COMPLEX,1, (255,0,0), 3)
                           # arduino.write(b"R")
                        elif Lcenter_y > Rcenter_y+30: #Left
                            cv.putText(frame,'Move Left', (20,70),cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3) 
                            #arduino.write(b" L")
                        elif Lcenter_y-30 <= Rcenter_y+30: #Forward 
                            cv.putText(frame,'Move Forward', (20,70),cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)
                           # arduino.write(b"F")
                    
                               

    cv.imshow("Car Controller Window", frame)
    if cv.waitKey(1) == ord('x'):
        break
    



vid.release()
cv.destroyAllWindows()
