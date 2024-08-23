import cv2
import HandTrackingModule as htm
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 840, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
volBar=400
volper=0
area=0
frameR = 50
smoothingFactor = 4
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

lastTapTime = 0
selectedFinger = 8
previousF = 8

def is_double_tap(a):
    global previousF
    global lastTapTime
    currentTime = time.time()
    if currentTime - lastTapTime < 0.3 and previousF == a:
        lastTapTime = 0
        return True
    lastTapTime = currentTime
    previousF = a
    return False

detector = htm.handDetector(detectionCon=0.7,maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

def VolumeGesture(img):
    global selectedFinger
    global volper,volBar
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if lmList :

        area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        print(area)

        if 200<area< 1200:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[selectedFinger][1], lmList[selectedFinger][2]
            x8, y8 = lmList[8][1], lmList[8][2]
            x12, y12 = lmList[12][1], lmList[12][2]
            x16, y16 = lmList[16][1], lmList[16][2]
            x20, y20 = lmList[20][1], lmList[20][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            yy = math.hypot(x2 - x1, y2 - y1)
            y8 = math.hypot(x8 - x1, y8 - y1)
            y12 = math.hypot(x12 - x1, y12 - y1)
            y16 = math.hypot(x16 - x1, y16 - y1)
            y20 = math.hypot(x20 - x1, y20 - y1)

            if y8 < 30:
                if is_double_tap(8):
                    selectedFinger = 8
            if y12 < 30:
                if is_double_tap(12):
                    selectedFinger = 12
            if y16 < 30:
                if is_double_tap(16):
                    selectedFinger = 16


            volBar = np.interp(yy, [50, 250], [400, 150])
            volper = np.interp(yy, [50, 250], [0, 100])


            smoothness=10

            volper=smoothness*round(volper/smoothness)
            fingers=detector.fingersUp()


            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volper / 100, None)
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            else:
                cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img,f'{int(volper)} %',(40,450),cv2.FONT_HERSHEY_TRIPLEX,1,(255,0,0),3)



    return img

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = VolumeGesture(frame)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, f' Volume Gesture   FPS:{int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Volume Gesture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()