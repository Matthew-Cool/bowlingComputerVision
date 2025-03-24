import cv2
import numpy as np

# python counterDebug.py 
# test pin counting system

frameWidth = 1280
frameHeight = 720
camBrightness = 150

cap = cv2.VideoCapture(0)

cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, camBrightness)

while True:
    # COUNTING SYSTEM
    r, frame = cap.read()
    cv2.imshow('Camera View', frame)

    if not r: #something is wrong, cap is not working
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBlue = np.array([100,50,50])
    upperBlue = np.array([130,255,255])

    mask = cv2.inRange(hsv, lowerBlue, upperBlue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    greyResult = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(greyResult, (9, 9), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filterFalsePositives = []
    for c in contours:
        area = cv2.contourArea(c)
        if 500 < area < 2000:
            filterFalsePositives.append(c)

    pins = len(filterFalsePositives)
    #END OF COUNTING SYSTEM
    print(f'pins={pins}')

    cv2.drawContours(result, filterFalsePositives, -1, (255,0,0), 2)

    cv2.imshow('hsv View', hsv)
    cv2.imshow('mask View', mask)
    cv2.imshow('result View', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()