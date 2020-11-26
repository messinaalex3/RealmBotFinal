import GrabScreen
import cv2
import Bullets
import Utils
import numpy as np

treeMMColors = [
    [29, 74, 24],
    [56, 138, 158],
    [0, 98, 117],
    [24, 49, 79],
    [117, 135, 123],
    [40, 102, 33],
    [13, 13, 13],
    [111, 111, 201],
    [40, 105, 15]
]

# Don't Use
# treeFrameColors1 = [
#     # Tree 1
#     [22, 56, 18],
#     [29, 74, 24] ,
#     [40, 102, 33],
#
#     # Tree 2
#     [0, 98, 117],
#     [0, 117, 140],
#
#     # Tree 3
#     [10,10,10],
#
#     # Tree 4
#     [16,78,9],
#     [29,74,24],
#     [40,102,33],
#
#     # Tree 5
#     [24,49,79],
#     [111,111,201],
#     [176,176,247],
#
#     # Tree 6
#     [13,36,59],
#     [30,61,99],
#     [0,10,27],
#
#     # Cactus 1
#     [21,80,0],
#     [7,73,0],
#     [40,105,15],
#
#     # Boulder 1
#     [56,138,158],
#     [35,86,99]
#
# ]

treeFrameColors = [
    [18,130,0],
    [13,77,0],
    [0,41,0],
    [16,80,0],
    [40,105,15],
    [28,38,39],
    [29,74,24],
    [6,40,2],
    [22,56,18],
    [0,2,27],
    [4,28,52],
    [0,16,46],
    [40,102,33],
    [81,81,81],  # Wall
    [99,99,99],  # Wall
    [5,5,5],
    [0,98,117],
    [16,40,71],
    [69,69,69],
    [19,40,65],
    [25,53,86],
    [56,138,158],
    [27,77,91],
    [77,60,41],     # Wall
    [130,102,68],   # Wall
    [128,126,128],
    [64,64,64],
    [145,166,152],  # Wall
    [139,74,43]     # Dark Water
]

def pt_miniMapToGameFrame(point,frame_shape,map_shape):
    x = int((point[0]/(map_shape[0]))*frame_shape[0])
    y = int((point[1]/(map_shape[1])) * frame_shape[1])
    return (x,y)

def pt_gameFrameToMiniMap(point,frame_shape,map_shape):
    x = int((point[0]/frame_shape[0])*(map_shape[0]))
    y = int((point[1]/frame_shape[1]) * (map_shape[1]))
    return (x,y)

# Project Minimap Contours onto Frame (Doesn't work well - contours combine into one and get lost when near)
# while True:
#
#     gameWindow = GrabScreen.findWindow("RotMGExalt")
#
#     frame = GrabScreen.captureScreen(gameWindow)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     gameFrame = Utils.cutGameFrame(frame)
#
#
#     # Minimap
#
#     # miniMap = GrabScreen.getMapExplored(frame)
#     # miniMapGameWindow = miniMap[76:123,75:122]
#     #
#     # for color in treeMMColors:
#     #     mapMask = GrabScreen.findColorInFrame(miniMapGameWindow, [color[0]-10,color[1]-10,color[2]-10], [color[0]+10,color[1]+10,color[2]+10])
#     #     mapFound = GrabScreen.findEnemiesFromMask(mapMask, mapMask, "Map", doPrint=False)
#     #     points = []
#     #
#     #     for contour in mapFound[1]:
#     #         map_pt = Bullets.getCenterContour(contour)
#     #         cv2.drawMarker(miniMapGameWindow, map_pt, (0, 0, 255), cv2.MARKER_TILTED_CROSS, 10, 1)
#     #         cv2.drawMarker(gameFrame, pt_miniMapToGameFrame(map_pt,gameFrame.shape,miniMapGameWindow.shape), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 10, 1)
#     #
#     # cv2.rectangle(miniMap,(75,75),(125,125),(0, 255, 0),1)
#
#
#     # Frame
#
#     x, y, c = gameFrame.shape
#     result = np.zeros((x, y), dtype="uint8")
#
#     for color in treeFrameColors:
#         mask = cv2.inRange(gameFrame, (color[0]-5, color[1]-5, color[2]-5), (color[0]+5, color[1]+5, color[2]+5))
#         result = cv2.add(result, mask)
#
#
#
#
#     # cv2.imshow("MiniMap", miniMap)
#     # cv2.imshow("Trees", miniMapGameWindow)
#     cv2.imshow("Frame", result)
#
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break


# Enlarge MiniMap Mask to impose on gameframe (loses track when character near obstacle)
# while True:
#
#     gameWindow = GrabScreen.findWindow("RotMGExalt")
#
#     frame = GrabScreen.captureScreen(gameWindow)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     gameFrame = Utils.cutGameFrame(frame)
#
#     miniMap = GrabScreen.getMapExplored(frame)
#     miniMapGameWindow = miniMap[76:123,75:122]
#
#
#     x, y, c = miniMapGameWindow.shape
#     result = np.zeros((x, y), dtype="uint8")
#
#     for color in treeMMColors:
#         mapMask = GrabScreen.findColorInFrame(miniMapGameWindow, [color[0]-10,color[1]-10,color[2]-10], [color[0]+10,color[1]+10,color[2]+10])
#         result = cv2.add(result, mapMask)
#
#     result = cv2.resize(result, (gameFrame.shape[1],frame.shape[0]), interpolation=cv2.INTER_NEAREST)
#
#
#     # cv2.imshow("MiniMap", miniMap)
#     # cv2.imshow("Trees", miniMapGameWindow)
#     cv2.imshow("Result", result)
#     #cv2.imshow("Frame", frame)
#
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break



# # Outline Mask
# while True:
#
#     gameWindow = GrabScreen.findWindow("RotMGExalt")
#
#     frame = GrabScreen.captureScreen(gameWindow)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     gameFrame = Utils.cutGameFrame(frame)
#
#     outlineMask = GrabScreen.findColorInFrame(gameFrame, (0,0,0),(70,70,70))
#
#     cv2.imshow("Outlines", outlineMask)
#
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break


# Obstacle Mask

def getObstacleMask(frame,threshold):

    x, y, c = frame.shape
    result = np.zeros((x, y), dtype="uint8")
    thresh = threshold

    for color in treeFrameColors:
        mapMask = GrabScreen.findColorInFrame(frame, [color[0]-thresh,color[1]-thresh,color[2]-thresh], [color[0]+thresh,color[1]+thresh,color[2]+thresh])
        result = cv2.add(result, mapMask)

    return result


# while True:
#
#     gameWindow = GrabScreen.findWindow("RotMGExalt")
#
#     frame = GrabScreen.captureScreen(gameWindow)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#     gameFrame = Utils.cutGameFrame(frame)
#
#     x, y, c = gameFrame.shape
#     result = np.zeros((x, y), dtype="uint8")
#
#     for color in treeFrameColors:
#         mapMask = GrabScreen.findColorInFrame(gameFrame, [color[0]-10,color[1]-10,color[2]-10], [color[0]+10,color[1]+10,color[2]+10])
#         result = cv2.add(result, mapMask)
#
#     cv2.imshow("Obstacle Mask", result)
#
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break








