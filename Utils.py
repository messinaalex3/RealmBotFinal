import cv2
import numpy as numpy
import pyautogui

def cutGameFrame(frame):
    tempFrame = frame.copy()
    cv2.rectangle(tempFrame,(10,30),(600,625),(0,255,0),2)
    cutFrame = tempFrame[30:625,10:600]
    return cutFrame

#check sword one, has issues with arrrows, may need to change that
enemyColorList = [
    [00, 219, 18] , # healthbar
    [15,16,56]
    ]
redDotMapColor = [2,13,229]
whiteMapColor = [255,255,255]
def getPlayerStatsFromBar(barFrame,fillColor):
    nonStatColorPixels = 0
    fillColor = numpy.array(fillColor)
    for pixel in reversed(barFrame):
        if not numpy.array_equal(pixel,fillColor):
            nonStatColorPixels += 1
        else:
            break
    healthPercent = (len(barFrame) - nonStatColorPixels) / len(barFrame)
    return healthPercent * 100

def moveMouseToPosition(pos,gameWindow):
    newPosX = pos[0]
    newPosY = pos[1]
    newPosX += gameWindow[0]
    newPosY += gameWindow[1]
    pyautogui.moveTo(newPosX,newPosY)

def dragMouseToPosition(pos,gameWindow):
    newPosX = pos[0]
    newPosY = pos[1]
    newPosX += gameWindow[0]
    newPosY += gameWindow[1]
    pyautogui.dragTo(newPosX,newPosY,button='left')

weaponColorToTierList = [
    [[181,181,181],0],
    [[53,74,177],1],
    [[136,98,98],2],
    [[101,212,32],3],
    [[0,212,255],4],
    [[66,66,255],5],
    [[177,26,177],6],
    [[31,0,206],7],
    [[255,60,0],8]
]

robeColorToTierList = [
    [[55,92,134],1],
    [[13,109,177],2],
    [[228,96,96],3],
    [[55,135,102],4],
    [[100,100,100],5],
    [[42,42,42],6],
    [[13,13,176],7],
    [[194,194,194],8]
]

healthPotionRed = [
    [[30,30,168],100]
]

playerItemsPos = [610,325]
lootPos = [610,525]
playerWeaponPos = [635,345]
playerArmorPos = [735,345]
potionLocation = [650,500]

avoidOnMap = [
    [29,74,24],
    [139,74,43]
]

treeMapColor = [29,74,24]
darkWaterColor = [139,74,43]
"""
    [107,221,247], #enemies with swords issues with arrows, gotta change this.
    [39,206,164],  #snakes, also all elves
    [191,191,191], #pirate sword
    [189,191,191], #piratess sword
    [128,255,149],    #green cube
    [234,129,197],  #purple cube
    [0,0,238],      #red cube
    [48,135,235],   #little scorpion feller
    [79,79,79],    #big scorpion tasil
    #[255,84,175],    #exp
    [29,196,154],    #left elves, right wasnt working even with same values
    [91,181,214],   #sandDevil
    [255,179,98],    #Sumo Master
    [202,153,255],  #nice bunnies
    [21,50,217],     #crabs.
    [27,77,132],     #Nymphs
    [79,255,222],    #goblins
    [54,253,249],    #hobbit mage
    [107,216,247],   #bandit leader yellow face
    [77,77,77],      #sandsman hat
    [10,221,38],     #slimes
    [22,188,234],   #wereleopard
    [00,92,158],   #werelion
    [0,68,178],     #warrior bee
    [50,107,124],   #warg
    [45,226,205],   #sludget
    [231,222,124],  #magic sprite
    [52,140,175],   #earth golem test me!
    [209,209,209],  #paper golem
    [127,127,127],  #metal golem
    [255,110,236],  #pink blob
    """
