import cv2
import time
import numpy as np
import Utils

ourBulletColors = {
    'T0': [[181,181,181],[255,255,255]],
    'T1': [[0, 0, 255],[0, 212, 255]],
    'T2': [[181, 181, 181],[255, 255, 255]],
    'T3': [[64, 166, 0],[114, 240, 36]],
    'T4': [[0, 212, 255],[179, 236, 246]],
    'T5': [[66, 66, 255],[177, 177, 255]],
    'T6': [[177, 13, 113],[255, 136, 208]],
    'T7': [[0, 0, 255],[0, 212, 255]],
    'T8': [[255, 111, 90],[248, 175, 162]],
    'T9': [[181, 181, 181],[255, 255, 255]],
    'T10': [[177, 13, 113],[255, 136, 208]],
    'T11': [[134, 171, 43],[238, 255, 196]],
    'T12': [[0, 0, 255],[0, 212, 255]]
}

bulletColors = [
[134, 171, 43],
[238, 255, 196],
[230, 230, 230],
[255, 255, 255],
[66, 66, 66],
[16, 16, 16],
[143, 143, 143],
[112, 112, 112],
[44, 45, 45],
[181, 181, 181],
[211, 211, 211],
[227, 99, 64],
[255, 155, 128],
[255, 111, 90],
[248, 175, 162],
[168, 73, 59],
[255, 112, 90],
[248, 176, 162],
[24, 57, 80],
[38, 90, 126],
[166, 156, 0],
[239, 227, 37],
[166, 39, 0],
[239, 84, 37],
[53, 53, 53],
[30, 30, 30],
[102, 102, 102],
[127, 127, 127],
[117, 117, 117],
[71, 71, 71],
[0, 0, 255],
[0, 212, 255],
[98, 249, 255],
[193, 252, 255],
[12, 238, 255],
[38, 218, 255],
[97, 247, 255],
[25, 201, 255],
[175, 175, 175],
[206, 206, 206],
[232, 232, 232],
[247, 247, 247],
[254, 254, 254],
[34, 100, 164],
[39, 206, 163],
[26, 137, 68],
[157, 157, 157],
[64, 166, 0],
[114, 240, 36],
[41, 148, 0],
[65, 229, 0],
[189, 255, 183],
[160, 160, 160],
[243, 243, 243],
[255, 100, 89],
[255, 148, 130],
[255, 183, 184],
[255, 144, 142],
[255, 174, 173],
[0, 142, 255],
[153, 210, 255],
[255, 66, 223],
[255, 217, 249],
[135, 34, 116],
[255, 65, 220],
[255, 217, 248],
[29, 29, 222],
[56, 63, 238],
[0, 0, 181],
[53, 38, 190],
[0, 0, 124],
[36, 28, 240],
[66, 66, 255],
[177, 177, 255],
[177, 13, 113],
[255, 136, 208],
[237, 202, 202],
[255, 217, 179],
[255, 237, 219],
[255, 247, 247],
[179, 236, 246]
]

Zones = [[87,86],[87,98],[87,110],[100,86],[100,110],[112,86],[112,98],[112,110]]



directions = [[0,"wa"],[1,"a"],[2,"sa"],[3,"w"],[4,"s"],[5,"wd"],[6,"d"],[7,"sd"]]

#gameWindow = GrabScreen.findWindow("RotMGExalt")

def BulletContours(frame,colors):
    # Create blank image for concatenating masks
    x, y, c = frame.shape
    result = np.zeros((x, y), dtype="uint8")

    # Add mask for each color
    for color in colors:
        mask = cv2.inRange(frame, (color[0], color[1], color[2]), (color[0], color[1], color[2]))
        result = cv2.add(result, mask)

    # Dilate makes all the mask areas thicker so they group better
    kernel = np.ones((2, 2), np.uint8)
    result = cv2.dilate(result, kernel, iterations=1)

    # Get contours of masks
    contours, hierarchy = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    return contours

def getCenterContour(contour):
    M = cv2.moments(contour)
    if M['m00'] > 0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
    else:
        return (-1,-1)

    return (x,y)

def sortBySecondElement(item):
    return item[1]

def getEightWayZones(frame):
    enemy_contours = BulletContours(frame,bulletColors)
    our_contours = BulletContours(frame,ourBulletColors['T3'])

    bag_contours = BulletContours(frame,[Utils.brownBag])
    bagCenters = []
    for bag in bag_contours:
        bagCenters.append(getCenterContour(bag))

    agent_center_x = frame.shape[0]//2
    agent_center_y = (frame.shape[1]//2)-15

    #ec2 = []
    bulletCenters = []
    # directions = [[0,"wa"],[1,"a"],[2,"sa"],[3,"w"],[4,"s"],[5,"wd"],[6,"d"],[7,"sd"]]
    dirOpposite = [7,    6,    5,      4,     3,    2,    1,    0]
    dirZones = [0] * 8
    for e_contour in enemy_contours:
        area = cv2.contourArea(e_contour)
        enemyCenter = getCenterContour(e_contour)
        found = False

        for bag in bagCenters:
            if abs(bag[0] - enemyCenter[0]) == 7 and abs(bag[1] - enemyCenter[1]) == 4:
                found = True

        if 220 < area:
            for contour in our_contours:
                ourCenter = getCenterContour(contour)
                if enemyCenter == ourCenter:
                    found = True
                    break

        if not found and area > 50:
            x_dist_1 = enemyCenter[0] - agent_center_x
            y_dist_1 = enemyCenter[1] - agent_center_y

            x_dist = x_dist_1
            y_dist = y_dist_1

            if -80 <= y_dist_1 <= 0 and x_dist <= 30:  # To ignore red writing when we are hit by a bullet
                # print(y_dist_1)
                pass
            # elif x_dist <= 30 and y_dist <= 30:
            #     pass
            #Left Col
            if x_dist >= -150 and x_dist <= -50:
                #print("leftsiiiideee")
                if y_dist >= -150 and y_dist <= -50:
                    #ec2.append((e_contour, 1))
                    dirZones[0] += 1
                    # dirZones[1] += .5
                    # # dirZones[2] += 1
                    # dirZones[3] += .5
                    # # dirZones[5] += 1
                elif y_dist >= -50 and y_dist <= 50:
                    #ec2.append((e_contour,2))
                    dirZones[1] += 1
                    # dirZones[0] += 1
                    # dirZones[2] += 1
                elif y_dist >= 50 and y_dist <= 150:
                    #ec2.append((e_contour, 3))
                    dirZones[2] += 1
                    # # dirZones[0] += 1
                    # dirZones[1] += .5
                    # dirZones[4] += .5
                    # # dirZones[7] += 1
            #Center Col
            elif x_dist >= -50 and x_dist <= 50:
                if y_dist >= -150 and y_dist <= -50:
                    #ec2.append((e_contour,4))
                    dirZones[3] += 1
                    # dirZones[0] += 1
                    # dirZones[5] += 1
                elif y_dist >= 50 and y_dist <= 150:
                    #ec2.append((e_contour,5))
                    dirZones[4] += 1
                    # dirZones[2] += 1
                    # dirZones[7] += 1
            #Right Col
            elif x_dist >= 50 and x_dist <= 150:
                if y_dist >= -150 and y_dist <= -50:
                    #ec2.append((e_contour, 6))
                    dirZones[5] += 1
                    # # dirZones[0] += 1
                    # dirZones[3] += .5
                    # dirZones[6] += .5
                    # # dirZones[7] += 1
                elif y_dist >= -50 and y_dist <= 50:
                    #ec2.append((e_contour,7))
                    dirZones[6] += 1
                    # dirZones[5] += .5
                    # dirZones[7] += .5
                elif y_dist >= 50 and y_dist <= 150:
                    #ec2.append((e_contour, 8))
                    dirZones[7] += 1
                    # dirZones[6] += .5
                    # # dirZones[5] += 1
                    # dirZones[4] += .5
                    # # dirZones[2] += 1


            #bulletCenters.append(enemyCenter)

    # enemy_contours = ec2
    # for c,zone in enemy_contours:
    #     # rect = cv2.minAreaRect(c)
    #     # box = cv2.boxPoints(rect)
    #     # box = np.int0(box)
    #     # if zone == 1:
    #     #     cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
    #     # elif zone == 2:
    #     #     cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)
    #     # elif zone == 3:
    #     #     cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
    #     # else:
    #     #     cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
    #     dirZones[zone - 1] += 1

    #print(dirZones)

    safeMovement = dirZones.index(min(dirZones))
    worseMovement = dirZones.index(max(dirZones))

    # return dirOpposite[worseMovement]

    # #adding 8-way directional zones
    # #top row
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
    # cv2.imshow("Bullet Tracking", frame)
    #
    # cv2.waitKey(1)

    return safeMovement

def getBulletCenters(frame):
    enemy_contours = BulletContours(frame, bulletColors)
    our_contours = BulletContours(frame, ourBulletColors['T8'])

    bag_contours = BulletContours(frame,[Utils.brownBag])
    bagCenters = []
    for bag in bag_contours:
        bagCenters.append(getCenterContour(bag))

    agent_center_x = frame.shape[0] // 2
    agent_center_y = (frame.shape[1] // 2) - 15

    bulletCenters = []

    for e_contour in enemy_contours:
        area = cv2.contourArea(e_contour)
        enemyCenter = getCenterContour(e_contour)
        found = False

        for bag in bagCenters:
            if abs(bag[0] - enemyCenter[0]) == 7 and abs(bag[1] - enemyCenter[1]) == 4:
                found = True

        if 150 < area:
            for contour in our_contours:
                ourCenter = getCenterContour(contour)
                if enemyCenter == ourCenter:
                    found = True
                    break

        if not found and area > 50:
            x_dist = enemyCenter[0] - agent_center_x
            y_dist = enemyCenter[1] - agent_center_y

            if -80 <= y_dist <= 0 and x_dist <= 30:  # To ignore red writing when we are hit by a bullet
                pass
            else:
                bulletCenters.append(enemyCenter)

    return bulletCenters