import cv2
import time
import numpy as np
import GrabScreen
import Utils
import pyautogui

# # T0
# ourBulletColors = [
# [181, 181, 181],
# [255, 255, 255]
# ]


# T1
ourBulletColors = [
[0, 0, 255],
[0, 212, 255]
]


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

gameWindow = GrabScreen.findWindow("RotMGExalt")

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

def getEightWayZones(enemy_contours):
    ec2 = []
    bulletCenters = []
    directions = [[0,"wa"],[1,"a"],[2,"sa"],[3,"w"],[4,"s"],[5,"wd"],[6,"d"],[7,"sd"]]
    dirOpposite = ["sd",    "d",    "wd",      "s",     "w",    "sa",    "a",    "wa"]
    dirZones = [0] * 8
    for e_contour in enemy_contours:
        area = cv2.contourArea(e_contour)
        enemyCenter = getCenterContour(e_contour)
        found = False
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
                print("leftsiiiideee")
                if y_dist >= -150 and y_dist <= -50:
                    ec2.append((e_contour, 1))
                elif y_dist >= -50 and y_dist <= 50:
                    ec2.append((e_contour,2))
                elif y_dist >= 50 and y_dist <= 150:
                    ec2.append((e_contour, 3))
            #Center Col
            elif x_dist >= -50 and x_dist <= 50:
                if y_dist >= -150 and y_dist <= -50:
                    ec2.append((e_contour,4))
                elif y_dist >= 50 and y_dist <= 150:
                    ec2.append((e_contour,5))
            #Right Col
            elif x_dist >= 50 and x_dist <= 150:
                if y_dist >= -150 and y_dist <= -50:
                    ec2.append((e_contour, 6))
                elif y_dist >= -50 and y_dist <= 50:
                    ec2.append((e_contour,7))
                elif y_dist >= 50 and y_dist <= 150:
                    ec2.append((e_contour, 8))


            bulletCenters.append(enemyCenter)

    enemy_contours = ec2
    for c,zone in enemy_contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if zone == 1:
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
        elif zone == 2:
            cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)
        elif zone == 3:
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        else:
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        dirZones[zone - 1] += 1



    safeMovement = dirZones.index(min(dirZones))
    worseMovement = dirZones.index(max(dirZones))
    time.sleep(.01)
    print(dirOpposite[worseMovement])







while(True):

    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    frame = Utils.cutGameFrame(frame)

    start_time = time.time()

    # Get Contours for our bullets and all bullets
    enemy_contours = BulletContours(frame,bulletColors)
    our_contours = BulletContours(frame,ourBulletColors)

    agent_center_x = frame.shape[0]//2
    agent_center_y = (frame.shape[1]//2)-15


    # Remove bullets that match ours based on area and center of contour
    # Have to append to second list because you can't remove a ndarray object from a list. Why? I don't know
    # ec2 = []
    # bulletCenters = []
    #
    # for e_contour in enemy_contours:
    #     area = cv2.contourArea(e_contour)
    #     enemyCenter = getCenterContour(e_contour)
    #     found = False
    #     if 220 < area:
    #         for contour in our_contours:
    #             ourCenter = getCenterContour(contour)
    #             if enemyCenter == ourCenter:
    #                 found = True
    #                 break
    #
    #     if not found and area > 50:
    #         x_dist_1 = enemyCenter[0] - agent_center_x
    #         y_dist_1 = enemyCenter[1] - agent_center_y
    #
    #         x_dist = abs(x_dist_1)
    #         y_dist = abs(y_dist_1)
    #
    #         if -80 <= y_dist_1 <= 0 and x_dist <= 30:       # To ignore red writing when we are hit by a bullet
    #             #print(y_dist_1)
    #             pass
    #         elif x_dist <= 30 and y_dist <= 30:
    #             pass
    #         elif x_dist <= 100 and y_dist <= 100:
    #             ec2.append((e_contour,1))
    #         elif x_dist <= 150 and y_dist <= 150:
    #             ec2.append((e_contour,2))
    #         else:
    #             ec2.append((e_contour, 3))
    #
    #         bulletCenters.append(enemyCenter)
    #
    # enemy_contours = ec2
    #
    # # Get bounding boxes of contours and draw them
    # for c,zone in enemy_contours:
    #     rect = cv2.minAreaRect(c)
    #     box = cv2.boxPoints(rect)
    #     box = np.int0(box)
    #     if zone == 1:
    #         cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
    #     elif zone == 2:
    #         cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)
    #     elif zone == 3:
    #         cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)


    getEightWayZones(enemy_contours)
    # To test amount of time required to process... .08sec for 81 colors, .03sec for 36 on my machine
    print(time.time() - start_time)

    cv2.rectangle(frame, (agent_center_x-100, agent_center_y-100), (agent_center_x+100, agent_center_y+100), (0, 255, 0), 1)
    cv2.rectangle(frame, (agent_center_x-150, agent_center_y-150), (agent_center_x+150, agent_center_y+150), (0, 255, 0), 1)

    #adding 8-way directional zones
    #top row
    cv2.rectangle(frame,(agent_center_x-150,agent_center_y - 150),(agent_center_x - 50,agent_center_y - 50),(0,0,255),1)
    cv2.rectangle(frame,(agent_center_x - 50, agent_center_y - 150),(agent_center_x + 50, agent_center_y - 50),(0, 0, 255), 1)
    cv2.rectangle(frame, (agent_center_x + 50, agent_center_y - 150), (agent_center_x + 150, agent_center_y - 50),(0, 0, 255), 1)

    #middle row
    cv2.rectangle(frame, (agent_center_x - 150, agent_center_y - 50), (agent_center_x -50, agent_center_y + 50),(0, 0, 255), 1)
    cv2.rectangle(frame, (agent_center_x + 50, agent_center_y - 50), (agent_center_x + 150, agent_center_y + 50),(0, 0, 255), 1)

    #bottom row
    cv2.rectangle(frame, (agent_center_x - 150, agent_center_y + 50), (agent_center_x - 50, agent_center_y + 150),(0, 0, 255), 1)
    cv2.rectangle(frame, (agent_center_x - 50, agent_center_y + 50), (agent_center_x + 50, agent_center_y + 150),(0, 0, 255), 1)
    cv2.rectangle(frame, (agent_center_x + 50, agent_center_y + 50), (agent_center_x + 150, agent_center_y + 150),(0, 0, 255), 1)
    #cv2.drawMarker(frame,(agent_center_x,agent_center_y),(255,255,255),cv2.MARKER_TILTED_CROSS,20,2)

    # Show frame
    cv2.imshow("Bullet Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break



