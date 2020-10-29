import GrabScreen
import cv2
import pyautogui
import time

pyautogui.FAILSAFE = True
gameWindow = GrabScreen.findWindow("RotMGExalt")
time.sleep(1)


while True:

    frame = GrabScreen.captureScreen(gameWindow)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    mode_frame = frame.copy()[533:550, 613:798]
    loot_frame = frame.copy()[589:619, 761:792]

    cv2.rectangle(frame, (613, 533), (798, 550), (0, 255, 0), 1)

    cv2.rectangle(frame, (761, 589), (792, 619), (0, 255, 0), 1)

    mode_mean = sum(cv2.mean(mode_frame)) / 3
    loot_rect = sum(cv2.mean(loot_frame)) / 3

    mode = ""

    if 56 < mode_mean < 65:
        mode = "Nexus"
    elif 70 > mode_mean > 65:
        mode = "Realm"
    elif mode_mean == 0:
        mode = "Transition"
    elif mode_mean == 54:
        mode = "Over Portal"
    #   pyautogui.press('space')
    elif loot_rect == 87:
        mode = "Loot"

    print('Mode: ', mode, end="\r")


    cv2.imshow("Frame", frame)
    cv2.imshow("Mode", mode_frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
