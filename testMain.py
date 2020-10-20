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


file = open("Resources\\WeaponsImages\\TierTable.txt")
weaponTable = []
for line in file:
    tableItem = line.split()
    weaponTable.append(tableItem)
file.close()
for item in weaponTable:
    temp = "Resources\\WeaponsImages\\" + item[0]
    print(temp)
    item[0] = cv2.imread(temp, cv2.IMREAD_UNCHANGED)
    #item[0] = cv2.cvtColor(tempItem,cv2.COLOR_BGRA2GRAY)

pyautogui.FAILSAFE = True
enemyList = os.listdir("Resources\\WeaponsImages")
enemyList = GrabScreen.enemyListToFileList(enemyList)
print(enemyList)
enemyList = GrabScreen.openEnemyTemplates(enemyList)
gameWindow = GrabScreen.findWindow("RotMGExalt")

def cutWindowItemPickup(frame):
    tempFrame = frame.copy()
    cv2.rectangle(frame,(610,525),(805,630),(0,255,255),2)
    temp = tempFrame[525:630,610:805]
    cv2.rectangle(frame,(635,345),(640,350),(255,255,0),2)
    cv2.imshow("uhhh",temp)
    return temp

def matchTieredItem(frame,itemList):
    tempFrame = frame.copy()
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    for item in itemList:
        rgbEnemy = cv2.cvtColor(item[0],cv2.COLOR_BGRA2RGB)
        result = cv2.matchTemplate(frame, rgbEnemy, cv2.TM_CCOEFF_NORMED)
        location = numpy.where(result >= .7)
        w, h = rgbEnemy.shape[:-1]
        for pt in zip(*location[::-1]):
            cv2.rectangle(tempFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
            print("Hello world weve found a tier", item[1])
            print(pt)


    return tempFrame


while True:
    start_time = time.time()

    playerPos = [0,0]

    #Get window
    frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    itemPickupWindow = cutWindowItemPickup(frame)
    cv2.imshow("0",weaponTable[0][0])
    cv2.imshow("1", weaponTable[1][0])
    cv2.imshow("2", weaponTable[2][0])
    cv2.imshow("3", weaponTable[3][0])
    matchedItems = matchTieredItem(frame,weaponTable)
    cv2.imshow("gameFrame",matchedItems)




    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

