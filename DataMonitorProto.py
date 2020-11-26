import numpy as np
import cv2
import time
import random


class DataMonitor:
    def __init__(self):
        self.blank_image = 255 * np.ones((200,400,3), np.uint8)
        self.font = cv2.QT_FONT_NORMAL
        self.org = (10, 20)
        self.fontScale = .6
        self.color = (0, 0, 0)
        self.thickness = 1

    def showDirZones(self,dirZones,title):

        str_width = 10

        text = 'Zones'
        text2 = str(dirZones[0]).rjust(str_width, ' ') + str(dirZones[3]).rjust(str_width, ' ') + str(dirZones[5]).rjust(str_width, ' ')
        text3 = str(dirZones[1]).rjust(str_width, ' ') + ''.rjust(str_width, ' ') + str(dirZones[6]).rjust(str_width,' ')
        text4 = str(dirZones[2]).rjust(str_width, ' ') + str(dirZones[4]).rjust(str_width, ' ') + str(dirZones[7]).rjust(str_width,' ')


        image = cv2.putText(self.blank_image.copy(), text, (10, 20), self.font, self.fontScale,self.color, self.thickness, cv2.LINE_AA, False)
        image = cv2.putText(image, text2, (10, 50), self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA, False)
        image = cv2.putText(image, text3, (10, 80), self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA, False)
        image = cv2.putText(image, text4, (10, 110), self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA, False)

        cv2.imshow("DataMonitor:"+title,image)

        cv2.waitKey(1)

        return



# while(True):
#
#     text = 'Value:   ' + str(random.randint(0,100))
#     text2 = 'Value2: (' + str(random.randint(0, 100)) + ', ' + str(random.randint(0, 100)) + ')'
#
#     image = cv2.putText(blank_image.copy(), text, (10, 20), font, fontScale,color, thickness, cv2.LINE_AA, False)
#     image = cv2.putText(image, text2, (10, 50), font, fontScale, color, thickness, cv2.LINE_AA, False)
#
#     cv2.imshow("Data Monitor",image)
#
#     time.sleep(.2)
#
#     if cv2.waitKey(25) & 0xFF == ord("q"):
#         cv2.destroyAllWindows()
#         break