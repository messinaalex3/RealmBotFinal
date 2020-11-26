import cv2
import os
import time
import numpy as np
import matplotlib

colorList = []

for subdir, dirs, files in os.walk("../Resources/Bullets"):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".jpg") or filepath.endswith(".png"):
            print(filepath)

        img = cv2.imread(filepath)

        for row in img:
            for pixel in row:
                    inpL = False
                    if list(pixel) != [84, 84, 84]:
                        for p in colorList:
                            if list(pixel) == p[0] and filename == p[1]:
                                p[2] += 1
                                inpL = True

                        if not inpL:
                            colorList.append([list(pixel),filename,1])

        # cv2.imshow("Image",img)
        #
        # cv2.waitKey(1)
        #
        # time.sleep(1)




import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for color in colorList:
    print(color[0],";",color[1],";",color[2])
    xs = color[0][0]
    ys = color[0][1]
    zs = color[0][2]
    ax.scatter(xs=xs, ys=ys, zs=zs,c=[(color[0][2]/255,color[0][1]/255,color[0][0]/255)])


ax.set_xlabel('B')
ax.set_ylabel('G')
ax.set_zlabel('R')

plt.show()