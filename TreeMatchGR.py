import GrabScreen
import DisplayScreen
import AgentTest
import Utils
import cv2
from matplotlib import pyplot as plt
import numpy
import os
import pyautogui
import time
import threading
import sys
import random


frame = cv2.imread("Resources\\TestImages\\SandBagsBullet.png")
frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)

# for i in range(0,10):                             # Pixel location top left of box
#     for j in range(0, 10):
#         frame[289+i,491+j] = [255, 255, 255]

print(frame[289,491])


outline_mask = cv2.inRange(frame, (1,1,1), (30,30,30))      # Issue with words above character (outlined)
tree_mask = cv2.inRange(frame, (0,10,30), (3,30,60))
arrow_mask = cv2.inRange(frame, (34,100,164), (34,100,164))
edges = cv2.Canny(frame, 50, 100)

while (True):

    cv2.imshow('edges',edges)
    cv2.imshow('Arrows', arrow_mask)
    cv2.imshow('frame', frame)
    cv2.imshow('Stumps!', tree_mask)
    cv2.imshow('Outlines!', outline_mask)

    time.sleep(.5)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

