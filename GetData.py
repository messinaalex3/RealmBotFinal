import GrabScreen
import Utils
import cv2
import numpy

#remove after video stuff
def getCenterContour(contour):
    M = cv2.moments(contour)
    if M['m00'] > 0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
    else:
        return (-1,-1)

    return (x,y - 15)

def getEnemiesScreen(frame):
    # Cut the frame to only include game windows for enemy tracking
    gameFrame = Utils.cutGameFrame(frame)
    # find enemies based on color and create a mask
    enemyMask = GrabScreen.findColorsInFrame(gameFrame, Utils.enemyColorList)
    #find chunks in mask to get enemy positions
    contours = GrabScreen.findEnemiesFromMask(enemyMask,gameFrame)
    for contour in contours[1]:
        point = getCenterContour(contour)
        cv2.drawMarker(contours[0],point,(0,0,255),cv2.MARKER_TILTED_CROSS,20,2)
    enemiesOnScreen = contours[1]
    cv2.imshow("Enemies", contours[0])
    return enemiesOnScreen

def getEnemiesMap(frame):
    #Get black pixels in map, should convert to percent so less change
    miniMap = GrabScreen.getMapExplored(frame)
    mapMask = GrabScreen.findColorInFrame(miniMap,[0,0,200],[0,0,255])
    mapFound = GrabScreen.findEnemiesFromMask(mapMask,mapMask,"Map")
    enemiesOnMap = mapFound[1]
    cv2.imshow("MapMask",mapMask)
    return enemiesOnMap

def getPlayerData(frame):
    return GrabScreen.findPlayerDataFromColors(frame)

def getMode(frame):
    mode_frame = frame.copy()[533:550, 613:798]
    loot_frame = frame.copy()[589:619, 761:792]
    mode_mean = sum(cv2.mean(mode_frame)) / 3
    loot_rect = sum(cv2.mean(loot_frame)) / 3
    mode = ""
    if 56 < mode_mean < 65:
        mode = "Nexus"
    elif 70 > mode_mean > 65:
        mode = "Realm"
    elif mode_mean == 0:
        mode = "Transition"
    elif mode_mean == 54:
        mode = "Over Portal"
    #   pyautogui.press('space')
    # this is an if instead of if else because of Realm
    if loot_rect == 87:
        mode = "Loot"

    cv2.imshow("ModeFrame",mode_frame)
    cv2.waitKey(1)

    return mode

def getPlayerPos(frame):
    playerPos = [[100,98]]
    # miniMap = GrabScreen.getMapExplored(frame)
    # playerMapMask = GrabScreen.findColorInFrame(miniMap,numpy.array(Utils.whiteMapColor),[255,255,255])
    # playerMapFound = GrabScreen.findEnemiesFromMask(playerMapMask,playerMapMask,doPrint= False)
    # if len(playerMapFound[1]) > 0:
    #     playerPos = playerMapFound[1][0][0]
    return playerPos
