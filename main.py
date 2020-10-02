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
import threading
import sys
import random



pyautogui.FAILSAFE = True
enemyList = os.listdir("Resources\\")
enemyList = GrabScreen.enemyListToFileList(enemyList)
print(enemyList)
enemyList = GrabScreen.openEnemyTemplates(enemyList)
#enemyList = GrabScreen.newAlphaConvert(enemyList)
#enemyList = GrabScreen.convertToAlpha(enemyList)
enemyList = GrabScreen.convertToGray(enemyList)
#for testing with edge detection
#testing edge detection is easy just uncomment this
#and also the edge function in findEnemies in GrabScreen file
#enemyList = GrabScreen.convertToEdge(enemyList)
gameWindow = GrabScreen.findWindow("RotMGExalt")
#tempMask = numpy.uint8(tempMask)
params = cv2.SimpleBlobDetector_Params()
params.blobColor = 255
params.minArea = 5
params.filterByColor = False
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
detector = cv2.SimpleBlobDetector_create(params)

g_nearest_enemy=None
g_playerPos = [0,0]

def hold_char(hold_time,char):
    pyautogui.keyDown(char)
    time.sleep(hold_time//1000)
    pyautogui.keyUp(char)

def motionLR():

    motion_keys = ['a','d']

    while True:
        #time.sleep(.1)
        sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
        #sys.stdout.write("   Player Loc: {}".format(g_playerPos))

        if 'numpy.ndarray' in str(type(g_playerPos)):
            distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
            #sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

            key = ''
            random.seed(time.time())

            if distance > 30:
                if g_nearest_enemy[0] > g_playerPos[0]:
                    key = 'd'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)
                if g_nearest_enemy[0] <= g_playerPos[0]:
                    key = 'a'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)

            elif distance < 10:
                if g_nearest_enemy[0] > g_playerPos[0]:
                    key = 'a'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)
                if g_nearest_enemy[0] <= g_playerPos[0]:
                    key = 'd'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)

            else:

                key = motion_keys[random.randint(0, 1)]
                #print(' random press:', key)
                hold_char(random.randint(100, 2000), key)

        sys.stdout.flush()

def motionUD():

    motion_keys = ['w','s']

    while True:
        #time.sleep(.1)
        #sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
        #sys.stdout.write("   Player Loc: {}".format(g_playerPos))

        if 'numpy.ndarray' in str(type(g_playerPos)):
            distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
            sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

            key = ''
            random.seed(time.time())

            if distance > 30:
                if g_nearest_enemy[1] > g_playerPos[1]:
                    key = 's'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)
                if g_nearest_enemy[1] <= g_playerPos[1]:
                    key = 'w'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)


            elif distance < 10:
                if g_nearest_enemy[1] > g_playerPos[1]:
                    key = 'w'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)
                if g_nearest_enemy[1] <= g_playerPos[1]:
                    key = 's'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)

            else:

                key = motion_keys[random.randint(0, 1)]
                #print(' random press:', key)
                hold_char(random.randint(100, 2000), key)

        sys.stdout.flush()


t1 = threading.Thread(target=motionUD)
t2 = threading.Thread(target=motionLR)

t1.start()
t2.start()

while True:
    start_time = time.time()

    playerPos = [0,0]

    #Get window
    frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    #Cut the frame to only include game windows for enemy tracking
    gameFrame = Utils.cutGameFrame(frame)
    #find enemies based on color and create a mask
    enemyMask = GrabScreen.findColorsInFrame(gameFrame,Utils.enemyColorList)

    #find chunks in mask to get enemy positionsrrrrrrrrrrr
    contours = GrabScreen.findEnemiesFromMask(enemyMask,frame)
    enemiesOnScreen = contours[1]
    #get players health from health bar
    playerHealth = GrabScreen.findPlayerDataFromColors(frame)

    #Get black pixels in map, should convert to percent so less change
    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap,[0,0,200],[0,0,255])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask,mapMask,"Map")
    enemiesOnMap = mapFound[1]
    #cv2.imshow("map",mapMask)
    playerMapMask = GrabScreen.findColorInFrame(miniMap,numpy.array(Utils.whiteMapColor),[255,255,255])
    playerMapFound = GrabScreen.findEnemiesFromMask(playerMapMask,playerMapMask,doPrint= False)
    if len(playerMapFound[1]) > 0:
        playerPos = playerMapFound[1][0][0]
    print("Player pos: ",playerPos[0])

    #cv2.imshow("playerMap",playerMapMask)
    #qprint(miniMap)

    state = [enemiesOnScreen,playerHealth,playerPos,enemiesOnMap]

    g_nearest_enemy = AgentTest.findClosestEnemy(enemiesOnMap, playerPos)
    g_playerPos = playerPos[0]

    #run agent
    AgentTest.AttackEnemies(state,gameWindow)

    #show frame with enemies highlighted
    cv2.imshow("CurrentFrame",contours[0])


    #well...this one is obvious right?
    print("FPS: ",1.0 / (time.time() - start_time))

    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


