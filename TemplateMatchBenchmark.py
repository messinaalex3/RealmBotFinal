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

GrabScreencaptureScreen = 0
GrabScreenfindEnemies = 0
GrabScreenfindPlayerData = 0
loopTime = 0
count = 0
str_width = 60

trials = 10.0


def printResults():
    functions = []

    functions.append(("GrabScreen.captureScreen(gameWindow)", GrabScreencaptureScreen))
    functions.append(("(TM) GrabScreen.findEnemies(frame,enemyList)", GrabScreenfindEnemies))
    functions.append(("(OCR Health) GrabScreen.findPlayerData(frame)", GrabScreenfindPlayerData))

    print("\n\nTrials: ", f'{int(trials):,}')
    print("\n----------Averages----------\n")

    functions.sort(key=lambda x: x[1], reverse=True)

    total_avg_time = 0

    for function in functions:
        print((function[0] + ":").ljust(str_width, ' '), "{:.10f}".format(function[1] / trials))
        total_avg_time += function[1] / trials

    print("\nTotal Avg Time:".ljust(str_width + 1, ' '), "{:.10f}".format(total_avg_time))
    print("Loop Time:".ljust(str_width, ' '), "{:.10f}".format(loopTime / trials))


while count < trials:

    start_loop = time.time()

    # Capture Screen
    start_time = time.time()
    frame = GrabScreen.captureScreen(gameWindow)
    delta = time.time() - start_time
    print("{0}. GrabScreen.captureScreen(gameWindow):".format(count).ljust(str_width, ' '), delta)
    GrabScreencaptureScreen += delta

    # Find Enemies (Template Match)
    start_time = time.time()
    tempFrame = GrabScreen.findEnemies(frame,enemyList)
    delta = time.time() - start_time
    print("{0}. (TM) GrabScreen.findEnemies(frame,enemyList):".format(count).ljust(str_width, ' '), delta)
    GrabScreenfindEnemies += delta

    # OCR Health
    start_time = time.time()
    health = GrabScreen.findPlayerData(frame)
    delta = time.time() - start_time
    print("{0}. (OCR Health) GrabScreen.findPlayerData(frame):".format(count).ljust(str_width, ' '), delta)
    GrabScreenfindPlayerData += delta

    delta_loop = time.time() - start_loop

    loopTime += delta_loop

    count += 1

    cv2.imshow("Template Match Enemies",tempFrame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

printResults()