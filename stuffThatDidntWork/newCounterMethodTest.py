import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

r, frame = cap.read() 

pinImg = cv2.imread('assets/pinImage.jpg', 0)
imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
height, width = pinImg.shape

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
# lets test all methods to see which one works best!

imgGrey = cv2.GaussianBlur(imgGrey, (3,3), 0)

for method in methods:
    imgGrey2 = imgGrey.copy() #so we can draw stuff on here and not the original, so copy

    result = cv2.matchTemplate(imgGrey2, pinImg, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    print(minLoc, maxLoc)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = minLoc
    else:
        location = maxLoc

    bottomRightDraw = (location[0] + width, location[1] + height)
    cv2.rectangle(imgGrey2, location, bottomRightDraw, 255, 5)
    cv2.imshow('match', imgGrey2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



cap.release()
