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


staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
pyautogui.FAILSAFE = True
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
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # rgbEnemy = cv2.cvtColor(item, cv2.COLOR_RGBA2GRAY)
    edgeFrame = GrabScreen.frameToEdge(tempFrame)
    edgeEnemy = GrabScreen.frameToEdge(item)
    result = cv2.matchTemplate(edgeFrame, edgeEnemy, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= .7)
    w, h = edgeEnemy.shape[::-1]
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
                # print("We have found a tier ", color[1])
                tiersFound.append([color[1],[pt[0] + w/2 + windowOffset[0],pt[1] + h/2 + windowOffset[1]]])
    cv2.imshow("hellooo",tempFrame)
    return tiersFound

def sorter(input):
    return input[0]

def loot(frame):
    itemPickupWindow = cutWindowItemPickup(frame)
    playerItemWindow = cutWindowPlayerItems(frame)
    foundItems = matchTieredItem(itemPickupWindow, staffImage, Utils.lootPos, gameWindow)
    playerItems = matchTieredItem(playerItemWindow, staffImage, Utils.playerItemsPos, gameWindow)
    print("Player item tier =", playerItems)

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
                pyautogui.dragTo(playerItems[0][1][0], playerItems[0][1][1], .25, pyautogui.easeInQuad)

    print("Loot item tier = ", foundItems)


    #Get window
frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
loot(frame)
#staffImage = GrabScreen.frameToEdge(staffImage)
# while (True):
#     frame = GrabScreen.captureScreen(gameWindow)
#     # Convert window to 3-channel RGB without Alpha
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     lootFrame = cutWindowItemPickup(frame)
#     playerFrame = cutWindowPlayerItems(frame)
#     #playerFrame = GrabScreen.frameToEdge(playerFrame)
#
#     cv2.imshow("Loot",lootFrame)
#     cv2.imshow("PlayerLoot",playerFrame)
#     cv2.imshow("Staff",staffImage)
#     playerItems = matchTieredItem(playerFrame,staffImage,Utils.playerItemsPos,gameWindow)
#     foundItems = matchTieredItem(lootFrame,staffImage,Utils.lootPos,gameWindow)
#     print("player",playerItems)
#     print("loot",foundItems)
#
#     if cv2.waitKey(25) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break


