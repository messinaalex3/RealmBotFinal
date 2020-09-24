import cv2
import numpy as numpy

def cutGameFrame(frame):
    tempFrame = frame.copy()
    cv2.rectangle(tempFrame,(10,30),(600,625),(0,255,0),2)
    cutFrame = tempFrame[30:625,10:600]
    return cutFrame


enemyColorList = [
    [157,157,157], #enemies with swords
    [39,206,164],  #snakes, also all elves
    [191,191,191], #pirate sword
    [189,191,191], #piratess sword
    [0,208,25],    #green cube not working
    [205,22,141],  #purple cube dont think this is either
    [88,204,228],   #little scorpion feller
    [34,19,171],    #big scorpion eyes
    [255,84,175],    #exp
    [29,196,154]    #left elves, right wasnt working even with same values
]

