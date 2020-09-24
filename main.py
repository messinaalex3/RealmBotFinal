import GrabScreen
import DisplayScreen
import AgentTest
import Utils
import cv2
from matplotlib import pyplot as plt
import numpy
import os





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


    #cv2.imshow("hi",pi)
    frame = GrabScreen.captureScreen(gameWindow)
    cv2.imshow("dude",GrabScreen.findPlayerData(frame))
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    gameFrame = Utils.cutGameFrame(frame)
    lowerB = numpy.array([39,206,164])
    upperB = numpy.array([39,206,164])
    #cv2.imshow("hi",GrabScreen.findColorsInFrame(gameFrame,Utils.enemyColorList))
    enemyMask = GrabScreen.findColorsInFrame(gameFrame,Utils.enemyColorList)


    contours = GrabScreen.findEnemiesFromMask(enemyMask,frame)
    cv2.imshow("ppp",contours[0])
    AgentTest.AttackEnemies(contours[1],gameWindow)
    miniMap = GrabScreen.getMapExplored(frame)
    print(miniMap)

    #cv2.imshow("hi",GrabScreen.findEnemies(frame,enemyList))
    #cv2.imshow("hi",GrabScreen.findEnemiesWithMask(frame,[snake]))
    #print(playerData)

    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


