import pyautogui
import random

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
    if health < 25:
        pyautogui.press("r")
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