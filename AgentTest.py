import pyautogui
import random
import cv2
import Looting
import win32api

def AttackEnemies(state,window):
    enemies = state[0]
    health = state[1]
    playerPos = state[2]
    enemyMap = state[3]
    if not len(enemies) == 0:
        enemyList = enemies[0]
        point = random.choice(enemyList)
        windowX = window[0]
        windowY = window[1]
        pointX = point[0][0]
        pointY = point[0][1]
        pyautogui.moveTo(pointX + windowX,pointY + windowY)
    print(findClosestEnemy(enemyMap,playerPos))

def findClosestEnemy(enemyMap,playerPos):
    closestPos = [0, 0]
    playerPos = [100,98]
    if len(playerPos) > 0 and len(enemyMap) > 0:
        #rplayerPos = playerPos[0]
        closest = 5000
        for enemy in enemyMap:
            enemy = enemy[0][0]
            enemyDistance = abs(playerPos[0] - enemy[0]) + abs(playerPos[1] - enemy[1])
            if enemyDistance < closest:
                closest = enemyDistance
                closestPos = enemy

    return closestPos

def checkIfOnBag(frame,window):
    meanFrame = frame.copy()
    meanFrame = meanFrame[533:630,613:798]
    mean = sum(cv2.mean(meanFrame)) / 3
    if mean > 70:
        print("bag!!")
        Looting.doLooting(frame,window)

def monitorHealth(health,outOfPotions):
    if not outOfPotions:
        if health < 45:
            pyautogui.press("r")
        elif health < 65:
            pyautogui.press("f")
    else:
        if health < 65:
            pyautogui.press("r")

def Aim(enemies,window,frame):
    if not len(enemies) == 0:
        playerPos = [319,310]
        enemyLocations = []
        for enemy in enemies:
            location  = enemy[0][0]
            enemyLocations.append([location,abs(playerPos[0] - location[0]) + abs(playerPos[1] - location[1])])
        enemyLocations.sort(key=sorter)
        closestEnemy = enemyLocations[0][0]
        windowX = window[0]
        windowY = window[1]
        pyautogui.moveTo(closestEnemy[0] + windowX,closestEnemy[1] + windowY)


        # enemyList = enemies[0]
        # print(enemyLocations)
        # point = random.choice(enemyList)
        # windowX = window[0]
        # windowY = window[1]
        # pointX = point[0][0]
        # pointY = point[0][1]
        #pyautogui.moveTo(pointX + windowX,pointY + windowY)

def sorter(input):
    return input[1]

def Aim1(enemies,window,frame):
    if not len(enemies) == 0:
        playerPos = [297,280]
        enemyLocations = []
        for enemy in enemies:
            enemyLocations.append([enemy,abs(playerPos[0] - enemy[0]) + abs(playerPos[1] - enemy[1])])
        enemyLocations.sort(key=sorter)
        closestEnemy = enemyLocations[0][0]
        windowX = window[0] + 10
        windowY = window[1] + 32
        #pyautogui.moveTo(closestEnemy[0] + windowX, closestEnemy[1] + windowY)
        win32api.SetCursorPos((closestEnemy[0] + windowX, closestEnemy[1] + windowY))

        # pointA = (closestEnemy[0],closestEnemy[1])
        # cv2.drawMarker(frame, pointA, (0, 0, 255), cv2.MARKER_TILTED_CROSS, 20, 2)
        # cv2.imshow("Closest Enemy", frame)
        # cv2.waitKey(1)