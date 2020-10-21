import cv2
import mss
import win32gui
import time
import numpy
import pytesseract
import re
import Utils
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
enemyList = ['Bandit Enemy','Bandit Leader','Pirate','Piratess','Poison Scorpion','Purple Gelatinous Cube',\
'Red Gelatinous Cube', 'Scorpion Queen', 'Snake','Green Gelatinous Cube']

def enemyListToFileList(enemyList):
    newList = []
    for enemy in enemyList:
        tempEnemy = "Resources\\" + enemy
        newList.append(tempEnemy)
    return newList

def openEnemyTemplates(enemyList):
    enemies = []
    for enemy in enemyList:
        tempEnemy = cv2.imread(enemy,cv2.IMREAD_UNCHANGED)
        enemies.append(tempEnemy)
    return enemies

def findPlayerData(frame):
    healthFrame = frame.copy()
    expFrame = frame.copy()
    cv2.rectangle(healthFrame,(675,280),(735,305),(0,255,0),2)
    healthFrame = healthFrame[280:300,660:750]
    cv2.rectangle(expFrame,(640,230),(750,260),(0,255,0),2)
    expFrame = expFrame[260:280,665:755]
    expFrame = cv2.cvtColor(expFrame,cv2.COLOR_RGBA2RGB)
    healthFrame = cv2.cvtColor(healthFrame,cv2.COLOR_RGB2GRAY)
    health = pytesseract.image_to_string(healthFrame)
    exp = pytesseract.image_to_string(expFrame)
    health = health[:-2]
    exp = exp[:-2]
    return (health,exp)

def findPlayerDataFromColors(frame):
    tempFrame = frame.copy()
    tempFrame = cv2.cvtColor(tempFrame,cv2.COLOR_RGBA2RGB)
    cv2.rectangle(tempFrame,(610,250),(805,350),(0,255,0),2)
    tempFrame = tempFrame[286:287,620:800]
    health = Utils.getPlayerStatsFromBar(tempFrame[0],[83,77,250])
    return health

def captureScreen(screen):
    sct = mss.mss()
    temp = numpy.asarray(sct.grab(screen))
    return numpy.asarray(sct.grab(screen))
def findWindow(name):
    hWnd = win32gui.FindWindow(None,name)
    window = win32gui.GetWindowRect(hWnd)
    win32gui.SetForegroundWindow(hWnd)
    return window

def convertToGray(enemyList):
    temp = []
    for enemy in enemyList:
        tempEnemy = cv2.cvtColor(enemy,cv2.COLOR_RGBA2GRAY)
        temp.append(tempEnemy)
    return temp

def convertToAlpha(enemyList):
    tempList = []
    for enemy in enemyList:
        newImage = enemy[:,:,0:3]
        alpha = enemy[:,:,1]
        alpha = cv2.merge([alpha,alpha,alpha])
        shape = enemy.shape[:2]
        temp = [newImage,alpha,shape]
        tempList.append(temp)
    return tempList

def newAlphaConvert(enemyList):
    tempList = []
    for enemy in enemyList:
        channels = cv2.split(enemy)
        zero_channel = numpy.zeros_like(channels[0])
        mask = numpy.array(channels[3])
        mask[channels[3] == 0] = 1
        mask[channels[3] == 100] = 0
        transparent_mask = cv2.merge([zero_channel, zero_channel, zero_channel, mask])
        temp = [enemy,transparent_mask]
        tempList.append(temp)
    return tempList

def convertToEdge(enemyList):
    temp = []
    for enemy in enemyList:
        temp.append(frameToEdge(enemy))
    return temp

def frameToEdge(frame):
    return cv2.Canny(frame,100,200)

#Load all photos into a list and pass into here with original photo
#Leave one untouched, and mark up one for return so we can match against
#Unmarked photo
def findEnemies(frame,enemyPhotos):
    tempFrame = frame.copy()
    #testing with blur to try to distort background pixels throwing off matching
    frame = cv2.GaussianBlur(frame,(5,5),0)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGRA2GRAY)
    #frame = frameToEdge(frame)
    enemiesFound = 0
    for enemy in enemyPhotos:
        #rgbEnemy = cv2.cvtColor(enemy[0],cv2.COLOR_RGBA2GRAY)
        result = cv2.matchTemplate(frame,enemy,cv2.TM_CCORR_NORMED)
        location = numpy.where(result >= .85)
        w, h = enemy.shape[::-1]
        for pt in zip(*location[::-1]):
            cv2.rectangle(tempFrame,pt,(pt[0] + w,pt[1] + h), (0,0,255),1)

    return tempFrame

def findEnemiesWithMask(frame,enemies):
    tempFrame = frame.copy()
    frameColorChange = cv2.cvtColor(frame,cv2.COLOR_BGRA2GRAY)
    newEnemies = convertToAlpha(enemies)
    for enemy in newEnemies:
        tempEnemy = cv2.cvtColor(enemy[0],cv2.COLOR_RGBA2GRAY)
        result = cv2.matchTemplate(frameColorChange,tempEnemy,cv2.TM_CCORR_NORMED,mask = enemy[1])
        location = numpy.where(result >= .8)
        w, h = enemy[2]
        for pt in zip(*location[::-1]):
            cv2.rectangle(tempFrame,pt,(pt[0] + w,pt[1] + h), (0,0,255),1)
    return tempFrame

#returns black pixels in map
def getMapExplored(frame):
    tempFrame = frame.copy()
    cv2.rectangle(tempFrame,(607,32),(807,235),(0,255,0),2)
    cutFrame = tempFrame[32:235,607:807]
    return cutFrame
    #return numpy.count_nonzero(cutFrame == [0,0,0])

def findColorsInFrame(frame,colors):
    tempFrame = 0
    for color in colors:
        tempFrame += findColorInFrame(frame,color)
    return tempFrame

def findColorInFrame(frame,color,upperb = None):
    lowerb = numpy.array(color)
    if upperb == None:
        upperb = numpy.array(color)
    else:
        upperb = numpy.array(upperb)
    return cv2.inRange(frame,lowerb,upperb)

def findEnemiesFromMask(mask,frameToDraw,where = "Screen",doPrint = True):
    tempFrame = frameToDraw.copy()
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(tempFrame, contours, -1, (0, 255, 0), 2)
    if doPrint:
        print("Enemies on ",where,": ", len(contours))
    return [tempFrame,contours]
