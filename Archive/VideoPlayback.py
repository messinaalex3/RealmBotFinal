import GrabScreen
import DisplayScreen
import cv2
from matplotlib import pyplot as plt
import numpy
import threading
import time
import win32gui


# # path
# path = "Resources/Pirate.png"
#
# # Reading an image in default mode
# image = cv2.imread(path)
#
# # Window name in which image is displayed
# window_name = 'image'
#
# # Using cv2.imshow() method
# # Displaying the image
# cv2.imshow(window_name, image)
#
# # waits for user to press any key
# # (this is necessary to avoid Python kernel form crashing)
# cv2.waitKey(0)
#
# # closing all open windows
# cv2.destroyAllWindows()
#
# pirate = cv2.imread("Resources/Pirate.png")
# pirateLeft = cv2.imread("Resources/PirateLeft.png")
# pirate = cv2.cvtColor(pirate, cv2.COLOR_BGR2GRAY)
# w, h = pirate.shape[::-1]
# print(GrabScreen.enemyList)
# print(GrabScreen.enemyListToFileList(GrabScreen.enemyList))
# temp = cv2.imread(GrabScreen.enemyListToFileList(GrabScreen.enemyList)[0])

def winEnumHandler(hwnd, ctx):
  if win32gui.IsWindowVisible(hwnd):
    print(hex(hwnd), win32gui.GetWindowText(hwnd))


def playVideo(cap):
  while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

      # Display the resulting frame
      cv2.imshow('Frame', frame)
      #win32gui.EnumWindows(winEnumHandler, None)

      # Press Q on keyboard to  exit
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Break the loop
    else:
      break

  # When everything done, release the video capture object
  cap.release()

  # Closes all the frames
  cv2.destroyAllWindows()

def drawEnemies(cap):

  time.sleep(1)

  while True:
    # Capture frame-by-frame
    try:
      gameWindow = GrabScreen.findWindow("Frame")
      frame = GrabScreen.captureScreen(gameWindow)
      cv2.imshow("hi", GrabScreen.findEnemies(frame, enemyList))


      if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    except:
      break

  # When everything done, release the video capture object
  cap.release()

  # Closes all the frames
  cv2.destroyAllWindows()


enemyList = ['Bandit Enemy','Bandit Leader','Pirate','Piratess','Poison Scorpion','Purple Gelatinous Cube',\
'Red Gelatinous Cube', 'Scorpion Queen', 'Snake','Green Gelatinous Cube']
enemyList = GrabScreen.enemyListToFileList(enemyList)
enemyList = GrabScreen.openEnemyTemplates(enemyList)
enemyList = GrabScreen.convertToGray(enemyList)
#enemyList = GrabScreen.convertToEdge(enemyList)
#gameWindow = GrabScreen.findWindow("Realm of the Mad God")

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture("Video/Capture_3.mp4")

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
if cap.isOpened():
  processThread = threading.Thread(target=playVideo, args=(cap,))  # <- note extra ','
  processThread.start()

  processThread = threading.Thread(target=drawEnemies, args=(cap,))  # <- note extra ','
  processThread.start()

# while True:
#
#
#     #cv2.imshow("hi",pi)
#     #cv2.imshow("yo",enemyList[5])
#     frame = GrabScreen.captureScreen(gameWindow)
#     cv2.imshow("hi",GrabScreen.findEnemies(frame,enemyList))
#     if cv2.waitKey(25) & 0xFF == ord("q"):
#             cv2.destroyAllWindows()
#             break


