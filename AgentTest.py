import pyautogui
import random

def AttackEnemies(enemies,window,health):
    if not len(enemies) == 0:
        enemy = enemies[0]
        point = random.choice(enemy)
        windowX = window[0]
        windowY = window[1]
        pointX = point[0][0]
        pointY = point[0][1]
        pyautogui.moveTo(pointX + windowX,pointY + windowY)
    if health < 90:
        pyautogui.press("r")