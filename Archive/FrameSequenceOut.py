import cv2
import time
import numpy as np
import GrabScreen
import Utils

gameWindow = GrabScreen.findWindow("RotMGExalt")

time.sleep(1)

count = 1
count2 = 1

while(True):

    frame = GrabScreen.captureScreen(gameWindow)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    frame = Utils.cutGameFrame(frame)

    filename = "Resources\\TestImages\\FrameSeq\\Frame_" + str(count) + ".png"

    cv2.imwrite(filename,frame)

    cv2.imshow("Frame",frame)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

    count += 1
    count2 += 1

    if count == 21:
        count = 1

    if count2 == 300:
        break

    time.sleep(.1)