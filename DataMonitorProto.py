import numpy as np
import cv2
import time
import random

blank_image = 255 * np.ones((200,400,3), np.uint8)

font = cv2.QT_FONT_NORMAL
org = (10, 20)
fontScale = .6
color = (0, 0, 0)
thickness = 1

while(True):

    text = 'Value:   ' + str(random.randint(0,100))
    text2 = 'Value2: (' + str(random.randint(0, 100)) + ', ' + str(random.randint(0, 100)) + ')'

    image = cv2.putText(blank_image.copy(), text, (10, 20), font, fontScale,color, thickness, cv2.LINE_AA, False)
    image = cv2.putText(image, text2, (10, 50), font, fontScale, color, thickness, cv2.LINE_AA, False)

    cv2.imshow("Data Monitor",image)

    time.sleep(.2)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break