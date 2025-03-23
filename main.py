import cv2
from matplotlib import pyplot as plt
import time


cap = cv2.VideoCapture(0)
ret, frame = cap.read()

print(ret)

if ret:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    plt.imshow(rgb_frame)
    plt.pause(5)
    plt.close()

cap.release()
