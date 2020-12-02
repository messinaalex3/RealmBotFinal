import cv2
import numpy
import pyautogui

import GrabScreen
import GetData
import Utils
import Looting
import AgentTest
import GetData
import Bullets
import Zones2


pyautogui.FAILSAFE = True
gameWindow = GrabScreen.findWindow("RotMGExalt")
frame = cv2.imread("Resources\\TestImages\\TestFrame.png")
frame = GrabScreen.captureScreen(gameWindow)
    #Convert window to 3-channel RGB without Alpha
frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
#Looting.doLooting(frame,gameWindow)
potion = cv2.imread("Resources\\WeaponsImages\\Loot Bag.png")
potion = cv2.cvtColor(potion,cv2.COLOR_BGRA2GRAY)
potion = GrabScreen.frameToEdge(potion)
#Using Gregs method for color mean to check if were on a bag
#If we are run our looting method
#if we stop movement and call this on finding the right mean we should also set a timer to only stop movement
#once every second so we dont stop twice on the same bag
playerPos = [310,350]
brownBag = [148,189,229]
pinkBag = [237,00,237]

def getCenterContour(contour):
    M = cv2.moments(contour)
    if M['m00'] > 0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
    else:
        return (-1,-1)

    return (x,y)

agent_center_x = 297
agent_center_y = 280
# Zones = [[147,130],[147,280],[147,430],[297,130],[297,430],[447,130],[447,280],[447,430]]
Zones = [[87,86],[87,98],[87,110],[100,86],[100,110],[112,86],[112,98],[112,110]]

# Zones.append([147,130])
# Zones.append([147, 280])
# Zones.append([147, 430])
# Zones.append([297,130])
# Zones.append([297,430])
# Zones.append([447,130])
# Zones.append([447,280])
# Zones.append([447, 430])

while True:
    indexList = [0,1,2,3,4,5,6,7]
    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    minimap = GrabScreen.getMapExplored(frame)
    frame = Utils.cutGameFrame(frame)
    # minimap_center_x = minimap.shape[0]//2
    # minimap_center_y = (minimap.shape[1]//2)-15
    zoneStats = Zones2.getZoneStats(frame)
    print(zoneStats)
    lowestWeight = 10000
    lowestIndex = 0
    for i in range(0,8):
        zone = zoneStats[i]
        if not zone[0] == True:
            zoneWeight = zone[1] + zone[2]
            if zoneWeight < lowestWeight:
                lowestWeight = zoneWeight
                lowestIndex = i
    print(lowestIndex)


    # safeMovement = Bullets.directions[Bullets.getEightWayZones(frame)]
    # print(safeMovement)
    #
    #
    # cv2.rectangle(frame,(agent_center_x-150,agent_center_y - 150),(agent_center_x - 50,agent_center_y - 50),(0,0,255),1)
    # cv2.rectangle(frame,(agent_center_x - 50, agent_center_y - 150),(agent_center_x + 50, agent_center_y - 50),(0, 0, 255), 1)
    # cv2.rectangle(frame, (agent_center_x + 50, agent_center_y - 150), (agent_center_x + 150, agent_center_y - 50),(0, 0, 255), 1)
    #
    # #middle row
    # cv2.rectangle(frame, (agent_center_x - 150, agent_center_y - 50), (agent_center_x -50, agent_center_y + 50),(0, 0, 255), 1)
    # cv2.rectangle(frame, (agent_center_x + 50, agent_center_y - 50), (agent_center_x + 150, agent_center_y + 50),(0, 0, 255), 1)
    #
    # #bottom row
    # cv2.rectangle(frame, (agent_center_x - 150, agent_center_y + 50), (agent_center_x - 50, agent_center_y + 150),(0, 0, 255), 1)
    # cv2.rectangle(frame, (agent_center_x - 50, agent_center_y + 50), (agent_center_x + 50, agent_center_y + 150),(0, 0, 255), 1)
    # cv2.rectangle(frame, (agent_center_x + 50, agent_center_y + 50), (agent_center_x + 150, agent_center_y + 150),(0, 0, 255), 1)
    #
    #
    #
    #
    # cv2.rectangle(frame,(agent_center_x + 150,agent_center_y + 150),(agent_center_x + 151, agent_center_y + 151),(0,0,255),2)
    # cv2.imshow("Frame",frame)
    #
    # mapPoints = []
    # for location in Zones:
    #     cv2.circle(minimap, (location[0], location[1]), 2, (255, 0, 255), 2)
    #     # center = location
    #     # diff = ((298 - center[0]),(280 - center[1]))
    #     # mapConversionDiff = (diff[0]/12,diff[1]/12)
    #     # mapDrawPoint = (round(100 - mapConversionDiff[0]),round(98 - mapConversionDiff[1]))
    #     # mapPoints.append(mapDrawPoint)
    #     # cv2.circle(minimap,(mapDrawPoint[0],mapDrawPoint[1]),2,(255,0,255),2)
    #     # print(mapDrawPoint)
    #
    # cv2.imshow("minimap",minimap)

    # [610,545]
    # cv2.rectangle(frame,(663,505),(675,523),(0,0,255),2)
    # mode_frame = frame.copy()[505:523, 663:675]
    #
    # mode_mean = sum(cv2.mean(mode_frame)) / 3
    # cv2.imshow("potions",mode_frame)
    # print(mode_mean)


    # cutFrame = Utils.cutGameFrame(frame)
    # # cv2.rectangle(frame, (319, 310), (330, 321), (255, 0, 0), 2)
    # minimap = GrabScreen.getMapExplored(frame)
    # cv2.rectangle(minimap,(75,73),(125,123),(0,0,255),2)
    # mask = GrabScreen.findColorsInFrame(cutFrame,[brownBag,pinkBag])
    # contours = GrabScreen.findEnemiesFromMask(mask,cutFrame)
    #
    # enemiesScreen = GetData.getEnemiesScreen1(frame)
    # enemiesMap = GetData.getEnemiesMap(frame)
    # closestEnemyMap = AgentTest.findClosestEnemy(enemiesMap,GetData.getPlayerPos(frame))
    # for contour in contours[1]:
    #     center = getCenterContour(contour)
    #     betterCenter = (center[0]/10,center[1]/10)
    #     diff = ((307 - center[0]),(313 - center[1]))
    #     mapConversionDiff = (diff[0]/12,diff[1]/12)
    #     print(mapConversionDiff)
    #     mapDrawPoint = (round(100 - mapConversionDiff[0]),round(98 - mapConversionDiff[1]))
    #     print(mapDrawPoint)
    #     # cv2.rectangle(minimap,center,(center[0] + 1,center[1] + 1),(0,0,255),2)
    #     cv2.rectangle(minimap, (mapDrawPoint[0],mapDrawPoint[1]), (mapDrawPoint[0] + 1, mapDrawPoint[1] + 1), (0, 0, 255), 2)
    #
    #
    # print("screen",enemiesScreen)
    # print("map",closestEnemyMap)
    # cv2.imshow("test",contours[0])
    # cv2.imshow("minimap",minimap)

    #
    # GetData.getEnemiesMap(frame)
    # GetData.getEnemiesScreen(frame)


    # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    # edgeFrame = GrabScreen.frameToEdge(cutFrame)
    # mode = GetData.getMode(frame)
    # print(mode)
    # cv2.rectangle(frame,(310,310),(350,311),(0,255,255),2)
    #
    # cv2.imshow("hiiiiii",potion)
    # lootLoc = [0,0]
    # result = cv2.matchTemplate(edgeFrame, potion, cv2.TM_CCOEFF_NORMED)
    # location = numpy.where(result >= .4)
    # w, h = potion.shape[::-1]
    # for pt in zip(*location[::-1]):
    #     cv2.rectangle(edgeFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
    #     print(pt)
    #     lootLoc[0] = pt[0]
    #     lootLoc[1] = pt[1]
    # cv2.imshow("hiiii",frame)
    #
    # movementDir = [0,0]
    # movementDir[0] = playerPos[0] - lootLoc[0]
    # movementDir[1] = playerPos[1] - lootLoc[1]
    # print(movementDir)
   #  miniMap = GrabScreen.getMapExplored(frame)
   #  mapMask = GrabScreen.findColorsInFrame(miniMap,Utils.avoidOnMap)
   # #mapMask = GrabScreen.findColorInFrame(miniMap,Utils.treeMapColor,Utils.treeMapColor)
   #  mapFound = GrabScreen.findEnemiesFromMask(mapMask,mapMask,"Map")
   #  enemiesOnMap = mapFound[1]
   #  cv2.imshow("hi there!",mapMask)
   #  print(enemiesOnMap)
   #  AgentTest.checkIfOnBag(frame,gameWindow)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break


def cutWindowItemPickup(frame):
    tempFrame = frame.copy()
    temp = tempFrame[525:630,610:805]
    #This is where we need to drag to for weapons
    return temp

def cutWindowPlayerItems(frame):
    tempFrame = frame.copy()
    temp = tempFrame[325:390,610:805]
    return temp


def matchTieredItem(frame,item,offset,window,tierList,defaultPos):
    tempFrame = frame.copy()
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # rgbEnemy = cv2.cvtColor(item, cv2.COLOR_RGBA2GRAY)
    edgeFrame = GrabScreen.frameToEdge(tempFrame)
    edgeEnemy = GrabScreen.frameToEdge(item)
    result = cv2.matchTemplate(edgeFrame, edgeEnemy, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= .7)
    w, h = edgeEnemy.shape[::-1]
    windowOffset = [window[0] + offset[0],window[1] + offset[1]]
    tiersFound = []
    if not defaultPos == [0,0]:
        tiersFound.append([-1,[defaultPos[0] + window[0],defaultPos[1] + window[1]]])
    for pt in zip(*location[::-1]):
        cv2.rectangle(tempFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        weaponFrame = tempFrame.copy()
        weaponFrame = weaponFrame[pt[1]:(pt[1] + h), pt[0]:(pt[0] + w)]
        for color in tierList:
            weaponColor = numpy.array(color[0])
            found = cv2.inRange(weaponFrame, weaponColor, weaponColor)
            if numpy.any(found):
                # print("We have found a tier ", color[1])
                tiersFound.append([color[1],[pt[0] + w/2 + windowOffset[0],pt[1] + h/2 + windowOffset[1]]])
    cv2.imshow("hellooo",tempFrame)
    return tiersFound

def sorter(input):
    return input[0]

def loot(frame,image,tierList,defaultPos,window):
    itemPickupWindow = cutWindowItemPickup(frame)
    playerItemWindow = cutWindowPlayerItems(frame)
    foundItems = matchTieredItem(itemPickupWindow, image, Utils.lootPos, window,tierList,[0,0])
    playerItems = matchTieredItem(playerItemWindow, image, Utils.playerItemsPos, window,tierList,defaultPos)


    wepPosX = Utils.playerWeaponPos[0]
    wepPosY = Utils.playerWeaponPos[1]
    wepPosX += gameWindow[0]
    wepPosY += gameWindow[1]

    if not len(foundItems) == 0:
        if not len(playerItems) == 0:
            foundItems.sort(reverse=True, key=sorter)
            playerItems.sort(reverse=True,key=sorter)
            maxTierItem = foundItems[0]
            if maxTierItem[0] > playerItems[0][0]:
                pyautogui.moveTo(maxTierItem[1])
                pyautogui.dragTo(playerItems[0][1][0], playerItems[0][1][1], .35, pyautogui.easeInQuad)
    print("Player item tier =", playerItems)
    print("Loot item tier = ", foundItems)
    #Get window
# frame = GrabScreen.captureScreen(gameWindow)
#     #Convert window to 3-channel RGB without Alpha
# frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)

def doLooting(frame,window):
    tempFrame = frame.copy()
    cv2.imshow("uhm",tempFrame)
    pyautogui.sleep(5)
    staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
    robeImage = cv2.imread("Resources\\WeaponsImages\\T1Robe.png")
    loot(frame,staffImage,Utils.weaponColorToTierList,Utils.playerWeaponPos,window)
    loot(frame,robeImage,Utils.robeColorToTierList,Utils.playerArmorPos,window)



#staffImage = GrabScreen.frameToEdge(staffImage)
# while (True):
#     cv2.rectangle(frame,(610,325),(805,390),(0,255,255),2)
#     cv2.rectangle(frame, (735, 345), (736, 346), (0, 255, 255), 2)
#     #temp = tempFrame[325:390,610:805]
#     cv2.imshow("hithere",frame)
#
#     # frame = GrabScreen.captureScreen(gameWindow)
#     # # Convert window to 3-channel RGB without Alpha
#     # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     # lootFrame = cutWindowItemPickup(frame)
#     # playerFrame = cutWindowPlayerItems(frame)
#     # #playerFrame = GrabScreen.frameToEdge(playerFrame)
#     #
#      #cv2.imshow("Loot",lootFrame)
#     # cv2.imshow("PlayerLoot",playerFrame)
#     # cv2.imshow("Staff",staffImage)
#     # playerItems = matchTieredItem(playerFrame,staffImage,Utils.playerItemsPos,gameWindow)
#     # foundItems = matchTieredItem(lootFrame,staffImage,Utils.lootPos,gameWindow)
#     # print("player",playerItems)
#     # print("loot",foundItems)
#
#     if cv2.waitKey(25) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break


