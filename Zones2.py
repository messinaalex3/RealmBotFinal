import GrabScreen
import cv2
import Bullets
import Utils
import numpy as np
import GetData
import Trees
import DataMonitorProto as DM


def getObstacles(mask,threshold):
    x = (mask.shape[1]) // 2
    y = (mask.shape[0]) // 2

    top = mask[y - 60:y - 20, x - 20:x + 20]
    bottom = mask[y + 20:y + 60, x - 20:x + 20]
    left = mask[y - 20:y + 20, x - 60:x - 20]
    right = mask[y - 20:y + 20, x + 20:x + 60]

    top_left = mask[y - 60:y - 20,x - 60:x - 20]
    top_right = mask[y - 60:y - 20,x + 20:x + 60]
    bottom_left = mask[y + 20:y + 60,x - 60:x - 20]
    bottom_right = mask[y + 20:y + 60,x + 20:x + 60]

    # print("Top mean:",cv2.mean(top)[0],end='\r')

    # cv2.imshow("top mask", top)
    # cv2.imshow("bottom mask", bottom)
    # cv2.imshow("left mask", left)
    # cv2.imshow("right mask", right)

    # cv2.imshow("top_left mask", top_left)
    # cv2.imshow("top_right mask", top_right)
    # cv2.imshow("bottom_left mask", bottom_left)
    # cv2.imshow("bottom_right mask", bottom_right)

    dirArray = [
        cv2.mean(top_left)[0] > threshold,
        cv2.mean(left)[0] > threshold,
        cv2.mean(bottom_left)[0] > threshold,
        cv2.mean(top)[0] > threshold,
        cv2.mean(bottom)[0] > threshold,
        cv2.mean(top_right)[0] > threshold,
        cv2.mean(right)[0] > threshold,
        cv2.mean(bottom_right)[0] > threshold
    ]

    # print(dirArray,end="\r")

    return dirArray

    #cv2.waitKey(1)

def drawObstacles(frame,obstacles):

    x = frame.shape[0] // 2
    y = frame.shape[1] // 2

    if obstacles[0]:
        cv2.drawMarker(frame, (x-40,y-40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[1]:
        cv2.drawMarker(frame, (x-40,y), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[2]:
        cv2.drawMarker(frame, (x-40,y+40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[3]:
        cv2.drawMarker(frame, (x,y-40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[4]:
        cv2.drawMarker(frame, (x,y+40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[5]:
        cv2.drawMarker(frame, (x+40,y-40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[6]:
        cv2.drawMarker(frame, (x+40,y), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)
    if obstacles[7]:
        cv2.drawMarker(frame, (x+40,y+40), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 25, 2)

    # cv2.waitKey(1)


def drawZones(frame,size):

    x = frame.shape[1] // 2
    y = frame.shape[0] // 2
    
    half = size//2
    threeHalf = int(1.5 *size)
    
    #top row
    cv2.rectangle(frame,(x-threeHalf,y - threeHalf),(x - half,y - half),(0,0,255),1)
    cv2.rectangle(frame,(x - half, y - threeHalf),(x + half, y - half),(0, 0, 255), 1)
    cv2.rectangle(frame, (x + half, y - threeHalf), (x + threeHalf, y - half),(0, 0, 255), 1)

    #middle row
    cv2.rectangle(frame, (x - threeHalf, y - half), (x -half, y + half),(0, 0, 255), 1)
    cv2.rectangle(frame, (x + half, y - half), (x + threeHalf, y + half),(0, 0, 255), 1)

    #bottom row
    cv2.rectangle(frame, (x - threeHalf, y + half), (x - half, y + threeHalf),(0, 0, 255), 1)
    cv2.rectangle(frame, (x - half, y + half), (x + half, y + threeHalf),(0, 0, 255), 1)
    cv2.rectangle(frame, (x + half, y + half), (x + threeHalf, y + threeHalf),(0, 0, 255), 1)

    # cv2.waitKey(1)

def getZoneCounts(frameShape,points,size):
    
    x = frameShape[0] // 2
    y = frameShape[1] // 2
    
    half = size//2
    threeHalf = int(1.5 *size)
    
    dirZones = [0] * 8

    for point in points:
        x_dist = point[0] - x
        y_dist = point[1] - y
    
        # Left Col
        if x_dist >= -threeHalf and x_dist <= -half:
            if y_dist >= -threeHalf and y_dist <= -half:
                dirZones[0] += 1
                dirZones[1] += .5
                dirZones[3] += .5
                dirZones[2] += .25
                dirZones[5] += .25
            elif y_dist >= -half and y_dist <= half:
                dirZones[1] += 1
                dirZones[0] += .5
                dirZones[2] += .5
            elif y_dist >= half and y_dist <= threeHalf:
                dirZones[2] += 1
                dirZones[1] += .5
                dirZones[4] += .5
                dirZones[0] += .25
                dirZones[7] += .25
        # Center Col
        elif x_dist >= -half and x_dist <= half:
            if y_dist >= -threeHalf and y_dist <= -half:
                dirZones[3] += 1
                dirZones[0] += .5
                dirZones[5] += .5
            elif y_dist >= half and y_dist <= threeHalf:
                dirZones[4] += 1
                dirZones[2] += .5
                dirZones[7] += .5
        # Right Col
        elif x_dist >= half and x_dist <= threeHalf:
            if y_dist >= -threeHalf and y_dist <= -half:
                dirZones[5] += 1
                dirZones[3] += .5
                dirZones[6] += .5
                dirZones[0] += .25
                dirZones[7] += .25
            elif y_dist >= -half and y_dist <= half:
                dirZones[6] += 1
                dirZones[5] += .5
                dirZones[7] += .5
            elif y_dist >= half and y_dist <= threeHalf:
                dirZones[7] += 1
                dirZones[6] += .5
                dirZones[4] += .5
                dirZones[5] += .25
                dirZones[2] += .25


    return dirZones


def getZoneStats(gameFrame):

    centerPoint = [297,280]

    size = 180
    edgeBuffer = 10

    half = size//2
    threeHalf = int(1.5 *size)

    zoneFrame = gameFrame[(centerPoint[1] - threeHalf - edgeBuffer):(centerPoint[1] + threeHalf + edgeBuffer),
                            (centerPoint[0] - threeHalf - edgeBuffer):(centerPoint[0] + threeHalf + edgeBuffer)]

    obsFrame = gameFrame[(centerPoint[1] - 60):(centerPoint[1] + 60),
                            (centerPoint[0] - 60):(centerPoint[0] + 60)]

    bulletCenters = Bullets.getBulletCenters(zoneFrame)
    enemyCenters = GetData.getEnemiesScreen1(zoneFrame)
    obsMask = Trees.getObstacleMask(obsFrame,10)           # 10 - Color range +/- 10 BGR values

    obstacle_array = getObstacles(obsMask,50)               # 50 - Mean for mask value. 0 black, 255 white
    bulletZoneCount = getZoneCounts(zoneFrame.shape,bulletCenters,size)
    enemyZoneCount = getZoneCounts(zoneFrame.shape,enemyCenters,size)

    zoneStats = []

    for i in range(0,8):
        zoneStats.append((obstacle_array[i],bulletZoneCount[i],enemyZoneCount[i]))


    return zoneStats




# Zones 2 Test Loop
#
# datamon = DM.DataMonitor()
#
# while True:
#
#     gameWindow = GrabScreen.findWindow("RotMGExalt")
#
#     frame = GrabScreen.captureScreen(gameWindow)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     gameFrame = Utils.cutGameFrame(frame)
#
#     #print(getZoneStats(gameFrame),end='\r')
#
#     centerPoint = [297,280] #[400,400]
#
#     size = 180
#     edgeBuffer = 10
#
#     half = size//2
#     threeHalf = int(1.5 *size)
#
#     zoneFrame = gameFrame[(centerPoint[1] - threeHalf - edgeBuffer):(centerPoint[1] + threeHalf + edgeBuffer),
#                             (centerPoint[0] - threeHalf - edgeBuffer):(centerPoint[0] + threeHalf + edgeBuffer)]
#
#     obsFrame = gameFrame[(centerPoint[1] - 60):(centerPoint[1] + 60),
#                             (centerPoint[0] - 60):(centerPoint[0] + 60)]
#
#     bulletCenters = Bullets.getBulletCenters(zoneFrame)
#     enemyCenters = GetData.getEnemiesScreen1(zoneFrame)
#     obsMask = Trees.getObstacleMask(obsFrame,10)
#     obstacle_array = getObstacles(obsMask,50)
#     datamon.showDirZones(obstacle_array,"Obstacles")
#     drawObstacles(zoneFrame,obstacle_array)
#     drawZones(zoneFrame,size)
#
#     bulletZoneCount = getZoneCounts(zoneFrame.shape,bulletCenters,size)
#     datamon.showDirZones(bulletZoneCount,"Bullet Counts")
#
#     enemyZoneCount = getZoneCounts(zoneFrame.shape,enemyCenters,size)
#     datamon.showDirZones(enemyZoneCount,"Enemy Counts")
#
#     for bullet in bulletCenters:
#         cv2.drawMarker(zoneFrame, bullet, (255, 0, 0), cv2.MARKER_TILTED_CROSS, 15, 2)
#
#     for enemy in enemyCenters:
#         cv2.drawMarker(zoneFrame, enemy, (0, 255, 0), cv2.MARKER_TILTED_CROSS, 15, 2)
#
#     cv2.imshow("Zone Frame", zoneFrame)
#     cv2.imshow("Obstacles", obsMask)
#
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break

