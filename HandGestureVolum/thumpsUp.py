import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

detector = htm.handDetector(maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
def is_thumbs_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Ensure the thumb and index finger tips are above the wrist
    thumb_outside = thumb_tip.y < thumb_mcp.y
    index_outside = index_tip.y < index_mcp.y

    # Ensure the middle, ring, and pinky finger tips are inside the hand (not extended)
    middle_inside = middle_tip.y > middle_mcp.y
    ring_inside = ring_tip.y > ring_mcp.y
    pinky_inside = pinky_tip.y > pinky_mcp.y

    return thumb_outside and index_outside and middle_inside and ring_inside and pinky_inside


# Initialize camera
cap = cv2.VideoCapture(0)
selectedFinger = 8
while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for thumbs-up gesture
            if is_thumbs_up(hand_landmarks):
                cv2.putText(frame, 'Thumbs Up!', (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                img = detector.findHands(frame)
                lmList, _ = detector.findPosition(frame)
                if lmList:
                    x1, y1 = lmList[4][1], lmList[4][2]
                    x2, y2 = lmList[selectedFinger][1], lmList[selectedFinger][2]
                    yy = math.hypot(x2 - x1, y2 - y1)
                    vol = np.interp(yy, [50, 280], [volRange[0], volRange[1]])
                    volume.SetMasterVolumeLevel(vol, None)
                    if yy < 50:
                        cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), 15, (0, 255, 0), cv2.FILLED)
    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
