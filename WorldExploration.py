import cv2
import numpy as np
import random

world = cv2.imread('Worlds\\World1.png',cv2.IMREAD_UNCHANGED)
height, width, depth = world.shape
scale_factor = .4

world = cv2.resize(world,(int(height*scale_factor),int(width*scale_factor)))

img = world

height,width,depth = img.shape
circle_img = np.zeros((height,width), np.uint8)

x = (height // 2) + random.randint(0,50)
y = (width // 2) + random.randint(0,50)

new_circle = cv2.circle(circle_img,(x,y),10,1,thickness=-1)

while x < height and y < width:

    masked_data = cv2.bitwise_and(img, img, mask=new_circle)
    cv2.imshow("World1 Exploration", masked_data)

    if cv2.waitKey(50) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

    x = x + random.randint(-10,10)
    y = y + random.randint(-10, 10)

    new_circle = cv2.circle(circle_img,(x,y),10,1,thickness=-1)

    img = cv2.circle(world.copy(), (x, y), 10,color=(0,0,255), thickness=2)


cv2.waitKey(0)

cv2.imshow('World',world)
cv2.waitKey(0)