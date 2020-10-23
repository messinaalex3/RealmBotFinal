import GrabScreen
import DisplayScreen
import AgentTest
import Utils
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pyautogui
import time
import threading
import sys
import random



pyautogui.FAILSAFE = True
# enemyList = os.listdir("Resources\\")
# enemyList = GrabScreen.enemyListToFileList(enemyList)
# print(enemyList)
# enemyList = GrabScreen.openEnemyTemplates(enemyList)
# #enemyList = GrabScreen.newAlphaConvert(enemyList)
# #enemyList = GrabScreen.convertToAlpha(enemyList)
# enemyList = GrabScreen.convertToGray(enemyList)
# #for testing with edge detection
# #testing edge detection is easy just uncomment this
# #and also the edge function in findEnemies in GrabScreen file
# #enemyList = GrabScreen.convertToEdge(enemyList)
gameWindow = GrabScreen.findWindow("RotMGExalt")
#tempMask = numpy.uint8(tempMask)
# params = cv2.SimpleBlobDetector_Params()
# params.blobColor = 255
# params.minArea = 5
# params.filterByColor = False
# params.filterByArea = True
# params.filterByCircularity = False
# params.filterByConvexity = False
# detector = cv2.SimpleBlobDetector_create(params)
#
# g_nearest_enemy=None
# g_playerPos = [[0,0]]
#
# def hold_char(hold_time,char):
#     pyautogui.keyDown(char)
#     time.sleep(hold_time//1000)
#     pyautogui.keyUp(char)
#
# def motionLR():
#
#     motion_keys = ['a','d']
#
#     while True:
#         #time.sleep(.1)
#         sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
#         #sys.stdout.write("   Player Loc: {}".format(g_playerPos))
#
#         if 'numpy.ndarray' in str(type(g_playerPos)):
#             distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
#             #sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))
#
#             key = ''
#             random.seed(time.time())
#
#             if distance > 30:
#                 if g_nearest_enemy[0] > g_playerPos[0]:
#                     key = 'd'
#                     #print('  tracking press:', key)
#                     hold_char(random.randint(1000, 2000), key)
#                 if g_nearest_enemy[0] <= g_playerPos[0]:
#                     key = 'a'
#                     #print('  tracking press:', key)
#                     hold_char(random.randint(1000, 2000), key)
#
#             elif distance < 10:
#                 if g_nearest_enemy[0] > g_playerPos[0]:
#                     key = 'a'
#                     #print('  retreat press:', key)
#                     hold_char(random.randint(1000, 3000), key)
#                 if g_nearest_enemy[0] <= g_playerPos[0]:
#                     key = 'd'
#                     #print('  retreat press:', key)
#                     hold_char(random.randint(1000, 3000), key)
#
#             else:
#
#                 key = motion_keys[random.randint(0, 1)]
#                 #print(' random press:', key)
#                 hold_char(random.randint(100, 2000), key)
#
#         sys.stdout.flush()
#
# def motionUD():
#
#     motion_keys = ['w','s']
#
#     while True:
#         #time.sleep(.1)
#         #sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
#         #sys.stdout.write("   Player Loc: {}".format(g_playerPos))
#
#         if 'numpy.ndarray' in str(type(g_playerPos)):
#             distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
#             sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))
#
#             key = ''
#             random.seed(time.time())
#
#             if distance > 30:
#                 if g_nearest_enemy[1] > g_playerPos[1]:
#                     key = 's'
#                     #print('  tracking press:', key)
#                     hold_char(random.randint(1000, 2000), key)
#                 if g_nearest_enemy[1] <= g_playerPos[1]:
#                     key = 'w'
#                     #print('  tracking press:', key)
#                     hold_char(random.randint(1000, 2000), key)
#
#
#             elif distance < 10:
#                 if g_nearest_enemy[1] > g_playerPos[1]:
#                     key = 'w'
#                     #print('  retreat press:', key)
#                     hold_char(random.randint(1000, 3000), key)
#                 if g_nearest_enemy[1] <= g_playerPos[1]:
#                     key = 's'
#                     #print('  retreat press:', key)
#                     hold_char(random.randint(1000, 3000), key)
#
#             else:
#
#                 key = motion_keys[random.randint(0, 1)]
#                 #print(' random press:', key)
#                 hold_char(random.randint(100, 2000), key)
#
#         sys.stdout.flush()
#
#
# t1 = threading.Thread(target=motionUD)
# t2 = threading.Thread(target=motionLR)
#
# t1.start()
# t2.start()

while True:

    frame = GrabScreen.captureScreen(gameWindow)

    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)

    mode_frame = frame.copy()[533:550, 613:798]
    game_frame = Utils.cutGameFrame(frame)

    cv2.rectangle(frame, (613, 533), (798, 550), (0, 255, 0), 1)

    cv2.rectangle(game_frame, (15, 477), (25, 487), (0, 255, 0), 1)
    cv2.rectangle(game_frame, (15, 147), (25, 157), (0, 255, 0), 1)
    cv2.rectangle(game_frame, (557, 147), (567, 157), (0, 255, 0), 1)
    cv2.rectangle(game_frame, (557, 477), (567, 487), (0, 255, 0), 1)

    corner_LL =  game_frame[477:487,15:25]
    corner_UL = game_frame[147:157, 15:25]
    corner_UR = game_frame[147:157, 557:567]
    corner_LR = game_frame[477:487, 557:567]

    #print('cv2 Mean: ', cv2.mean(corner_UR), end="\r")

    # for i in range(0,10):                             # Pixel location top left of box
    #     for j in range(0, 10):
    #         game_frame[477+i,15+j] = [255, 255, 255]
    #         game_frame[147 + i, 15 + j] = [255, 255, 255]
    #         game_frame[147 + i, 557 + j] = [255, 255, 255]
    #         game_frame[477 + i, 557 + j] = [255, 255, 255]

    #print('cv2 Mean: ',cv2.mean(cutFrame),end="\r")

    mode_mean = sum(cv2.mean(mode_frame))/3

    mode = ""

    if 56 < mode_mean < 65:
        mode = "Nexus"
    elif mode_mean > 65:
        mode = "Realm"
    elif mode_mean==0:
        mode = "Transition"
    elif mode_mean==54:
        pyautogui.press('space')

    print('Mode: ', mode, end="\r")

    cv2.imshow("Frame",game_frame)
    cv2.imshow('Corner1',corner_UR)
    cv2.imshow("Frame3", frame)
    cv2.imshow("Frame2", mode_frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break


