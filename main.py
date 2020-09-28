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
while True:
    start_time = time.time()

    #Get window
    frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    #Cut the frame to only include game windows for enemy tracking
    gameFrame = Utils.cutGameFrame(frame)
    #find enemies based on color and create a mask
    enemyMask = GrabScreen.findColorsInFrame(gameFrame,Utils.enemyColorList)

    #find chunks in mask to get enemy positions
    contours = GrabScreen.findEnemiesFromMask(enemyMask,frame)

    #get players health from health bar
    playerHealth = GrabScreen.findPlayerDataFromColors(frame)

    #Get black pixels in map, should convert to percent so less change
    #miniMap = GrabScreen.getMapExplored(frame)
    #qprint(miniMap)

    #run agent
    AgentTest.AttackEnemies(contours[1],gameWindow,playerHealth)

    #show frame with enemies highlighted
    cv2.imshow("CurrentFrame",contours[0])


    #well...this one is obvious right?
    print("FPS: ",1.0 / (time.time() - start_time))

    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


