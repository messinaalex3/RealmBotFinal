import GrabScreen
import cv2
import pyautogui
import time
import AgentTest


pyautogui.FAILSAFE = True
gameWindow = GrabScreen.findWindow("RotMGExalt")
time.sleep(1)

def hold_char(hold_time,char):
    pyautogui.keyDown(char)
    time.sleep(hold_time//1000)
    pyautogui.keyUp(char)

pressedA = False
pressedD = False
pressedW = False

#FIRST
while (True):
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap, [200, 0, 0], [255, 0, 0])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map",doPrint=False)

    max_pos = -float('inf')

    for points in mapFound[1]:
        #print(points[0][0])
        if points[0][0][1] > 60:
            if points[0][0][0] > max_pos:
                max_pos = points[0][0][0]

    center_diff = 112-max_pos

    #print("Distance to center: ", center_diff)     # 112 is 94 (pos right) + 130 (pos left) / 2 from testing


    if  center_diff > 3 and not pressedA:
        pyautogui.keyDown('a')
        pressedA = True
        #print("Press A")
    elif center_diff < 4 and  pressedA:
        pyautogui.keyUp('a')
        pressedA = False
        #print("Release A")
    elif center_diff < -3 and not pressedD:
        pyautogui.keyDown('d')
        #print("Press D")
        pressedD = True
    elif center_diff > -4 and pressedD:
        pyautogui.keyUp('d')
        pressedD = False
        #print("Release D")

    if -3 <= center_diff <= 3 and not pressedW:
        break



    cv2.imshow("map", mapMask)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break


pyautogui.keyDown('w')
pressedW = True
print("Press W")

time.sleep(2.8)

pyautogui.keyUp('w')
pressedW = False

#SECOND
while (True):
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap, [18, 0, 125], [28, 18, 145])  # red
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map", doPrint=False)

    min_diff = float('inf')
    min_pos = float('inf')

    for points in mapFound[1]:
        #print(points[0][0])
        diff = abs(98-points[0][0][1])
        if diff < min_diff:
            min_diff = diff
            min_pos = points[0][0][1]

    top_diff = 98-min_pos

    #print("Distance to top: ", top_diff)     # 112 is 94 (pos right) + 130 (pos left) / 2 from testing


    if  top_diff > 2 and not pressedW:
        pyautogui.keyDown('w')
        pressedW = True
        #print("Press W")
    elif top_diff < 2 and pressedW:
        pyautogui.keyUp('w')
        pressedW = False
        #print("Release W")

    if top_diff <= 3 and not pressedW:
        break

    cv2.imshow("map", mapMask)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

pressedA = False
pressedD = False

#THIRD
while (True):
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap, [200, 0, 0], [255, 0, 0])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map",doPrint=False)

    nearest_portal = AgentTest.findClosestEnemy(mapFound[1], [[100,98]])

    h_diff = 100 - nearest_portal[0]

    #print("Nearest H Portal: ", h_diff)     # 112 is 94 (pos right) + 130 (pos left) / 2 from testing

    if  h_diff > 3 and not pressedA:
        pyautogui.keyDown('a')
        pressedA = True
        #print("Press A")
    elif h_diff < 4 and  pressedA:
        pyautogui.keyUp('a')
        pressedA = False
        #print("Release A")
    elif h_diff < -3 and not pressedD:
        pyautogui.keyDown('d')
        #print("Press D")
        pressedD = True
    elif h_diff > -4 and pressedD:
        pyautogui.keyUp('d')
        pressedD = False
        #print("Release D")

    mode_frame = frame.copy()[597:600, 640:778]

    mode_mean = sum(cv2.mean(mode_frame)) / 3

    #print(mode_mean)

    if 140 <= mode_mean <= 170:
        if pressedA:
            pyautogui.keyUp('a')
            pressedA=False
        if pressedD:
            pyautogui.keyUp('d')
            pressedD=False
        time.sleep(.1)
        pyautogui.press('space')
        #print("run")
        break


    if -3 <= h_diff <= 3:
       break

    cv2.imshow("map", mode_frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

pressedW = False
pressedS = False

#FOURTH
while (True):
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    #print(mode_mean)

    miniMap = GrabScreen.getMapExplored(frame)[0:130,0:200]
    mapMask = GrabScreen.findColorInFrame(miniMap, [200, 0, 0], [255, 0, 0])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map",doPrint=False)

    nearest_portal = AgentTest.findClosestEnemy(mapFound[1], [[100,98]])

    v_diff = 97 - nearest_portal[1]

    #print("Nearest V Portal: ", v_diff)     # 112 is 94 (pos right) + 130 (pos left) / 2 from testing

    if  v_diff >= -5 and not pressedW:
        pyautogui.keyDown('w')
        pressedW = True
        #print("Press W")
    if v_diff < 3 and pressedW:
        pyautogui.keyUp('w')
        pressedW= False
        #print("Release W")
    if v_diff < -10 and not pressedS:
        pyautogui.keyDown('s')
        #print("Press S")
        pressedS = True
    if (v_diff > -2 or v_diff==97) and pressedS:
        pyautogui.keyUp('s')
        pressedS = False
        #print("Release S")

    mode_frame = frame.copy()[597:600, 640:778]

    mode_mean = sum(cv2.mean(mode_frame)) / 3

    #print(mode_mean)

    if 140 <= mode_mean <= 170:
        if pressedS:
            pyautogui.keyUp('s')
            pressedS=False
        if pressedW:
            pyautogui.keyUp('w')
            pressedW=False
        time.sleep(.1)
        pyautogui.press('space')
        #print("run")
        break

    cv2.imshow("map", miniMap)
    cv2.imshow("mode",mode_frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break