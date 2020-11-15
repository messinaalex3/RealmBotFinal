import GrabScreen
import cv2
import os
import time

enemyList = os.listdir("Resources\\Enemies\\")
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



while True:

    start_time = time.time()
    frame = GrabScreen.captureScreen(gameWindow)
    cv2.imshow("Template Match Enemies",GrabScreen.findEnemies(frame,enemyList))
    print(GrabScreen.findPlayerData(frame))

    print(time.time() - start_time)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break