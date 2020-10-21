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


staffImage = cv2.imread("Resources\\WeaponsImages\\EnergyStaff.png")

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
    temp = tempFrame[525:630,610:805]
    #This is where we need to drag to for weapons
    return temp

def cutWindowPlayerItems(frame):
    tempFrame = frame.copy()
    temp = tempFrame[325:390,610:805]
    return temp


def matchTieredItem(frame,item,offset,window):
    tempFrame = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    rgbEnemy = cv2.cvtColor(item, cv2.COLOR_BGRA2GRAY)
    result = cv2.matchTemplate(frame, rgbEnemy, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= .4)
    w, h = rgbEnemy.shape[::-1]
    windowOffset = [window[0] + offset[0],window[1] + offset[1]]
    tiersFound = []
    for pt in zip(*location[::-1]):
        cv2.rectangle(tempFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        weaponFrame = tempFrame.copy()
        weaponFrame = weaponFrame[pt[1]:(pt[1] + h), pt[0]:(pt[0] + w)]
        for color in Utils.weaponColorToTierList:
            weaponColor = numpy.array(color[0])
            found = cv2.inRange(weaponFrame, weaponColor, weaponColor)
            if numpy.any(found):
                #print("We have found a tier ", color[1])
                tiersFound.append([color[1],[pt[0] + w/2 + windowOffset[0],pt[1] + h/2 + windowOffset[1]]])
    cv2.imshow("hellooo",tempFrame)
    return tiersFound

def sorter(input):
    return input[0]

while True:
    start_time = time.time()

    playerPos = [0,0]

    #Get window
    frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    itemPickupWindow = cutWindowItemPickup(frame)
    playerItemWindow = cutWindowPlayerItems(frame)
    foundItems = matchTieredItem(itemPickupWindow,staffImage,Utils.lootPos,gameWindow)
    playerItems = matchTieredItem(playerItemWindow,staffImage,Utils.playerItemsPos,gameWindow)
    print("Player item tier =", playerItems)

    # if not len(foundItems) == 0:
    #     pyautogui.moveTo(foundItems[0][1])
    wepPosX = Utils.playerWeaponPos[0]
    wepPosY = Utils.playerWeaponPos[1]
    wepPosX += gameWindow[0]
    wepPosY += gameWindow[1]

    if not len(foundItems) == 0:
        if not len(playerItems) == 0:
            foundItems.sort(reverse=True, key=sorter)
            maxTierItem = foundItems[0]
            if maxTierItem[0] > playerItems[0][0]:
                pyautogui.moveTo(maxTierItem[1])
                pyautogui.dragTo(playerItems[0][1][0],playerItems[0][1][1],.25,pyautogui.easeInQuad)


    print("Loot item tier = ", foundItems)

    # if not len(playerItems) == 0:
    #     pyautogui.moveTo(playerItems[0][1])
    #cv2.rectangle(matchedItems,(610,325),(805,390),(0,255,255),2)
    #cv2.imshow("gameFrame",matchedItems)




    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

