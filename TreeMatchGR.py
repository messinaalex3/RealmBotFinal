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


frame = cv2.imread("Resources\\TestImages\\Tree1.png")
frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)

outline_mask = cv2.inRange(frame, (1,1,1), (15,15,15))
tree_mask = cv2.inRange(frame, (0,10,30), (3,30,60))

while (True):
    cv2.imshow('frame', frame)
    cv2.imshow('Stumps!', tree_mask)
    cv2.imshow('Outlines!', outline_mask)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

