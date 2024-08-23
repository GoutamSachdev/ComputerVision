import cv2
import HandTrackingModule as htm
import pyautogui
import numpy as np
import time

cap = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)
wCam, hCam = 840, 480
cap.set(3, wCam)
cap.set(4, hCam)
frameR = 50
smoothingFactor = 4
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wScr, hScr = pyautogui.size()

while True:
    ret, frame = cap.read()
    img = detector.findHands(frame)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        finger = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        if finger[1] == 1 and finger[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothingFactor
            clocY = plocY + (y3 - plocY) / smoothingFactor

            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
            plocY, plocX = clocY, clocX
        if finger[1] == 1 and finger[2] == 1:
            length, img, midpoint = detector.findDistance(lmList[8], lmList[12], img)

            print(length)
            if length < 1280:
                cv2.circle(img, midpoint, 10, (255, 255, 255), cv2.FILLED)


                pyautogui.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    mirrored_frame = cv2.flip(img, 1)
    cv2.putText(mirrored_frame, f'FPS:{int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Virtual Mouse', mirrored_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()