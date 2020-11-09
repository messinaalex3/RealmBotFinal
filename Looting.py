import GrabScreen
import Utils
import cv2
import numpy
import pyautogui
import time


def cutWindowItemPickup(frame):
    tempFrame = frame.copy()
    temp = tempFrame[525:630, 610:805]
    # This is where we need to drag to for weapons
    return temp


def cutWindowPlayerItems(frame):
    tempFrame = frame.copy()
    temp = tempFrame[325:390, 610:805]
    return temp


def matchTieredItem(frame, item, offset, window, tierList, defaultPos):
    tempFrame = frame.copy()
    edgeFrame = GrabScreen.frameToEdge(tempFrame)
    edgeEnemy = GrabScreen.frameToEdge(item)
    result = cv2.matchTemplate(edgeFrame, edgeEnemy, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= .5)
    w, h = edgeEnemy.shape[::-1]
    windowOffset = [window[0] + offset[0], window[1] + offset[1]]
    tiersFound = []
    if not defaultPos == [0, 0]:
        tiersFound.append([-1, [defaultPos[0] + window[0], defaultPos[1] + window[1]]])
    for pt in zip(*location[::-1]):
        cv2.rectangle(tempFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        weaponFrame = tempFrame.copy()
        weaponFrame = weaponFrame[pt[1]:(pt[1] + h), pt[0]:(pt[0] + w)]
        for color in tierList:
            weaponColor = numpy.array(color[0])
            found = cv2.inRange(weaponFrame, weaponColor, weaponColor)
            if numpy.any(found):
                # print("We have found a tier ", color[1])
                tiersFound.append([color[1], [pt[0] + w / 2 + windowOffset[0], pt[1] + h / 2 + windowOffset[1]]])
    return tiersFound


def sorter(input):
    return input[0]


def loot(frame, image, tierList, defaultPos, window):
    itemPickupWindow = cutWindowItemPickup(frame)
    playerItemWindow = cutWindowPlayerItems(frame)
    playerItems = matchTieredItem(playerItemWindow, image, Utils.playerItemsPos, window, tierList, defaultPos)
    foundItems = matchTieredItem(itemPickupWindow, image, Utils.lootPos, window, tierList, [0, 0])


    wepPosX = Utils.playerWeaponPos[0]
    wepPosY = Utils.playerWeaponPos[1]
    wepPosX += window[0]
    wepPosY += window[1]

    if not len(foundItems) == 0:
        if not len(playerItems) == 0:
            foundItems.sort(reverse=True, key=sorter)
            playerItems.sort(reverse=True, key=sorter)
            maxTierItem = foundItems[0]
            if maxTierItem[0] > playerItems[0][0]:
                pyautogui.moveTo(maxTierItem[1])
                pyautogui.dragTo(playerItems[0][1][0], playerItems[0][1][1], .35, pyautogui.easeInQuad)
    print("Player item tier =", playerItems)
    print("Loot item tier = ", foundItems)


def doLooting(frame,staffImage,robeImage,potionImage, window):
    tempFrame = frame.copy()
    # staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
    # robeImage = cv2.imread("Resources\\WeaponsImages\\T1Robe.png")
    # potionImage = cv2.imread("Resources\\WeaponsImages\\Potion.png")
    loot(tempFrame, staffImage, Utils.weaponColorToTierList, Utils.playerWeaponPos, window)
    loot(tempFrame, robeImage, Utils.robeColorToTierList, Utils.playerArmorPos, window)
    loot(tempFrame,potionImage,Utils.healthPotionRed,Utils.potionLocation,window)
    pyautogui.keyDown('w')
    time.sleep(.1)
    pyautogui.keyUp('w')

def doLootingNoImage(frame,window):
    tempFrame = frame.copy()
    staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
    robeImage = cv2.imread("Resources\\WeaponsImages\\T1Robe.png")
    potionImage = cv2.imread("Resources\\WeaponsImages\\Potion.png")
    loot(tempFrame, staffImage, Utils.weaponColorToTierList, Utils.playerWeaponPos, window)
    loot(tempFrame, robeImage, Utils.robeColorToTierList, Utils.playerArmorPos, window)
    loot(tempFrame,potionImage,Utils.healthPotionRed,Utils.potionLocation,window)
    pyautogui.keyDown('w')
    time.sleep(.1)
    pyautogui.keyUp('w')