import cv2
import numpy as np

def drawContours(contours,image,color):
    ret_img = image.copy()
    for c in contours:
        # From OpenCV
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(ret_img, (x, y), (x + w, y + h), color, 2)

    return ret_img

def resize_image(image,percent):
    # From OpenCV
    scale_percent = percent  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized

####################################################

# Birds Example

birds = cv2.imread("..\\Real_World_App\\Birds_sky.png")

mask = cv2.inRange(birds,(0,0,0),(100,100,100))
kernel = np.ones((4, 4), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

birds_2 = drawContours(contours,birds,(0, 255, 0))

cv2.imshow("birds",cv2.hconcat([resize_image(birds,60),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),60),resize_image(birds_2,60)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Road Signs

road_sign = cv2.imread("..\\Real_World_App\\Road_Signs.jpg")

mask = cv2.inRange(road_sign,(100,120,0),(140,170,5))

kernel = np.ones((4, 4), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

road_sign_2 = drawContours(contours,road_sign,(0,0,255))

cv2.imshow("road_signs",cv2.hconcat([resize_image(road_sign,60),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),60),resize_image(road_sign_2,60)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Ships

ships = cv2.imread("..\\Real_World_App\\Ships_Ocean.jpg")

ship_blur = cv2.blur(ships,(7,7))

mask = cv2.inRange(ship_blur,(0,0,0),(190,130,110))
mask = cv2.bitwise_not(mask)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

ships_2 = ships.copy()

for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    area = cv2.contourArea(c)
    if area > 300:
        cv2.drawContours(ships_2, [box], 0, (0, 0, 255), 4)

cv2.imshow("Ships",cv2.hconcat([resize_image(ships,30),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),30),resize_image(ships_2,30)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Bodies of Water

water = cv2.imread("..\\Real_World_App\\Bodies of Water.JPG")

water_blur = cv2.blur(water,(15,15))

mask = cv2.inRange(water_blur,(0,0,0),(40,40,30))
kernel = np.ones((4, 4), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

water_2 = water.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 50:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(water_2, (x, y), (x + w, y + h), (0,255,0), 2)

cv2.imshow("bodies_of_water",cv2.hconcat([resize_image(water,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50),resize_image(water_2,50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Football

football = cv2.imread("..\\Real_World_App\\Football.JPG")

mask = cv2.inRange(football,(0,40,140),(45,100,240))
kernel = np.ones((18, 18), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

football_2 = football.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 500:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(football_2, (x, y), (x + w, y + h), (0,255,0), 2)

cv2.imshow("Football",cv2.hconcat([resize_image(football,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50),resize_image(football_2,50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Oranges

oranges = cv2.imread("..\\Real_World_App\\Oranges.JPG")

mask = cv2.inRange(oranges,(1,30,90),(6,75,230))
kernel = np.ones((6, 6), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

mask += cv2.inRange(oranges,(55,220,250),(65,230,255))
kernel = np.ones((6, 6), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

oranges_2 = oranges.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 500:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(oranges_2, (x, y), (x + w, y + h), (0,255,0), 2)

cv2.imshow("Oranges",cv2.hconcat([resize_image(oranges,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50),resize_image(oranges_2,50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Soccer

soccer = cv2.imread("..\\Real_World_App\\Soccer_Players.jpg")

mask = cv2.inRange(soccer,(30,0,200),(65,30,255))
kernel = np.ones((18, 18), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

soccer_2 = soccer.copy()

for c in contours:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(soccer_2, (x, y), (x + w, y + h), (0,255,0), 2)

cv2.imshow("Soccer",cv2.hconcat([resize_image(soccer,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50),resize_image(soccer_2,50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Soccer 2

soccer = cv2.imread("..\\Real_World_App\\Soccer_2.jpeg")

soccer_blur = cv2.blur(soccer,(3,3))

mask = cv2.inRange(soccer_blur,(210,210,210),(255,255,255))
kernel = np.ones((10, 10), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

soccer_2 = soccer.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 500:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(soccer_2, (x, y), (x + w, y + h), (0,255,0), 2)

cv2.imshow("Soccer 2",cv2.hconcat([resize_image(soccer,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50),resize_image(soccer_2,50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Road Lines

road_lines = cv2.imread("..\\Real_World_App\\Road_Lines.JPG")

mask = cv2.inRange(road_lines,(185,180,180),(255,255,255))
# kernel = np.ones((6, 6), np.uint8)
# mask = cv2.dilate(mask, kernel, iterations=1)

mask += cv2.inRange(road_lines,(90,140,160),(140,165,230))
kernel = np.ones((6, 6), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

road_lines_2 = road_lines.copy()

cv2.imshow("Road Lines",cv2.hconcat([resize_image(road_lines,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################

# Road Lines 2

road_lines = cv2.imread("..\\Real_World_App\\Road_Lines_2.JPG")

mask = cv2.inRange(road_lines,(160,160,160),(255,255,255))
# kernel = np.ones((6, 6), np.uint8)
# mask = cv2.dilate(mask, kernel, iterations=1)

mask += cv2.inRange(road_lines,(60,70,135),(85,140,200))
kernel = np.ones((6, 6), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=1)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

road_lines_2 = road_lines.copy()

cv2.imshow("Road Lines 2",cv2.hconcat([resize_image(road_lines,50),resize_image(cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB),50)]))

cv2.waitKey(0)

cv2.destroyAllWindows()

####################################################