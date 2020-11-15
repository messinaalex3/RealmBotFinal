import pyautogui
import random
import cv2
import Looting

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
    if len(playerPos) > 0 and len(enemyMap) > 0:
        playerPos = playerPos[0]
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

def monitorHealth(health):
    if health < 45:
        pyautogui.press("r")
    elif health < 50:
        pyautogui.press("f")

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
        windowX = window[0] + 15
        windowY = window[1] + 15
        pyautogui.moveTo(closestEnemy[0] + windowX,closestEnemy[1] + windowY)