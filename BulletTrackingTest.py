import cv2
import time
import numpy as np
import GrabScreen
import Utils

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

while(True):

    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    frame = Utils.cutGameFrame(frame)

    # scale_percent = 50  # percent of original size
    # width = int(frame.shape[1] * scale_percent / 100)
    # height = int(frame.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # # resize image
    # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_NEAREST)


    start_time = time.time()

    # Get Contours for our bullets and all bullets
    enemy_contours = BulletContours(frame,bulletColors)
    our_contours = BulletContours(frame,ourBulletColors)


    # Remove bullets that match ours based on area and center of contour
    # Have to append to second list because you can't remove a ndarray object from a list. Why? I don't know
    ec2 = []

    for e_contour in enemy_contours:
        area = cv2.contourArea(e_contour)
        found = False
        if 220 < area:
            for contour in our_contours:
                enemyCenter = getCenterContour(e_contour)
                ourCenter = getCenterContour(contour)
                if enemyCenter == ourCenter:
                    found = True
                    break

        if not found and area > 50:
            ec2.append(e_contour)

    enemy_contours = ec2

    # Get bounding boxes of contours and draw them
    for c in enemy_contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

    # To test amount of time required to process... .08sec for 81 colors, .03sec for 36 on my machine
    print(time.time() - start_time)

    # Show frame
    cv2.imshow("Bullet Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break



