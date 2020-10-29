import GrabScreen
import cv2
import pyautogui
import time


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
while (True):
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap, [200, 0, 0], [255, 0, 0])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map",doPrint=False)

    # playerMapMask = GrabScreen.findColorInFrame(miniMap,numpy.array(Utils.whiteMapColor),[255,255,255])
    # playerMapFound = GrabScreen.findEnemiesFromMask(playerMapMask,playerMapMask,doPrint= False)
    # if len(playerMapFound[1]) > 0:
    #     playerPos = playerMapFound[1][0][0]
    #     #print("Player pos: ",playerPos[0],end="\r")

    # Player [100 98]       # player position moves slightly with movement like [102 100] if up or something

    max_pos = -float('inf')

    for points in mapFound[1]:
        if points[0][0][1] > 60:
            if points[0][0][0] > max_pos:
                max_pos = points[0][0][0]

    print("Distance to center: ", 112-max_pos,end="\r")     # 112 is 94 (pos left) + 130 (pos right) / 2 from testing

    center_diff = 112-max_pos

    print(center_diff)

    if  center_diff > 3 and not pressedA:
        pyautogui.keyDown('a')
        pressedA = True
        print("Press A")
    elif center_diff < 4 and  pressedA:
        pyautogui.keyUp('a')
        pressedA = False
        print("Release A")
    elif center_diff < -3 and not pressedD:
        pyautogui.keyDown('d')
        print("Press D")
        pressedD = True
    elif center_diff > -4 and pressedD:
        pyautogui.keyUp('d')
        pressedD = False
        print("Release D")

    if -3 <= center_diff <= 3 and not pressedW:
        pyautogui.keyDown('w')
        pressedW = True
        print("Press W")

        time.sleep(3)

        pyautogui.keyUp('w')

    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap, [18, 0, 125], [28, 18, 145])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map", doPrint=False)


    cv2.imshow("map",mapMask)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
