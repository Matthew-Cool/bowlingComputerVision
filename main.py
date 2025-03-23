import cv2
import numpy as np

frameWidth = 1280
frameHeight = 720
camBrightness = 150

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, camBrightness)

while True:
    _, img = cap.read()
    cv2.imshow('Original', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()