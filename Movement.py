import pyautogui
import time
import sys
import random
import threading


class Movement:
    def __init__(self, gamestate):
        self.gameState = gamestate
        self.modeChange = False

    def modeListener(self):
        lastMode = self.gameState.mode
        while (True):
            mode = self.gameState.mode
            if mode != lastMode:
                self.modeChange = True
                return
            time.sleep(.1)

    def doAction(self, duration, key):

        start = int(round(time.time() * 1000))
        pyautogui.keyDown(key)

        while ((int(round(time.time() * 1000)) - start) < duration) and not self.modeChange:
            time.sleep(.1)

        pyautogui.keyUp(key)

        return

    def move(self,mode=None):

        t1 = threading.Thread(target=self.modeListener)
        t1.start()

        motion_keys = None

        if mode=='LR':
            motion_keys = ['a','d']
        elif mode=='UD':
            motion_keys = ['w','s']

        while(not self.modeChange):

            g_nearest_enemy = self.gameState.closestEnemy
            g_playerPos = [100,98]

            if 'numpy.ndarray' in str(type(g_nearest_enemy)):
                distance = abs(g_nearest_enemy[0] - g_playerPos[0]) + abs(g_nearest_enemy[1] - g_playerPos[1])

                random.seed(time.time())

                if distance > 30:
                    if g_nearest_enemy[0] > g_playerPos[0]:
                        key = motion_keys[1]    # d,s
                        print('  tracking press:', key)
                        self.doAction(random.randint(1000, 2000), key)
                    if g_nearest_enemy[0] <= g_playerPos[0]:
                        key = motion_keys[0]   # a,w
                        print('  tracking press:', key)
                        self.doAction(random.randint(1000, 2000), key)

                elif distance < 10:
                    if g_nearest_enemy[0] > g_playerPos[0]:
                        key = motion_keys[0]   # a,w
                        print('  retreat press:', key)
                        self.doAction(random.randint(1000, 3000), key)
                    if g_nearest_enemy[0] <= g_playerPos[0]:
                        key = motion_keys[1]    # d,s
                        print('  retreat press:', key)
                        self.doAction(random.randint(1000, 3000), key)
                else:

                    key = motion_keys[random.randint(0, 1)]
                    print(' random press:', key)
                    self.doAction(random.randint(100, 2000), key)

        return


# def hold_char(hold_time,char):
#     pyautogui.keyDown(char)
#     time.sleep(hold_time//1000)
#     pyautogui.keyUp(char)
#
# def motionLR(g_nearest_enemy,g_playerPos):
#     motion_keys = ['a','d']
#     #sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
#     #sys.stdout.write("   Player Loc: {}".format(g_playerPos))
#
#     if 'numpy.ndarray' in str(type(g_nearest_enemy)):
#         distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
#         #sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))
#
#         key = ''
#         random.seed(time.time())
#
#         if distance > 30:
#             if g_nearest_enemy[0] > g_playerPos[0]:
#                 key = 'd'
#                 print('  tracking press:', key)
#                 hold_char(random.randint(1000, 2000), key)
#             if g_nearest_enemy[0] <= g_playerPos[0]:
#                 key = 'a'
#                 print('  tracking press:', key)
#                 hold_char(random.randint(1000, 2000), key)
#
#         elif distance < 10:
#             if g_nearest_enemy[0] > g_playerPos[0]:
#                 key = 'a'
#                 print('  retreat press:', key)
#                 hold_char(random.randint(1000, 3000), key)
#             if g_nearest_enemy[0] <= g_playerPos[0]:
#                 key = 'd'
#                 print('  retreat press:', key)
#                 hold_char(random.randint(1000, 3000), key)
#
#         else:
#
#             key = motion_keys[random.randint(0, 1)]
#             print(' random press:', key)
#             hold_char(random.randint(100, 2000), key)
#
#     sys.stdout.flush()
#
# def motionUD(g_nearest_enemy,g_playerPos):
#
#     motion_keys = ['w','s']
#
#
#
#     if 'numpy.ndarray' in str(type(g_nearest_enemy)):
#         distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
#         #sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))
#
#         key = ''
#         random.seed(time.time())
#
#         if distance > 30:
#             if g_nearest_enemy[1] > g_playerPos[1]:
#                 key = 's'
#                 print('  tracking press:', key)
#                 hold_char(random.randint(1000, 2000), key)
#             if g_nearest_enemy[1] <= g_playerPos[1]:
#                 key = 'w'
#                 #print('  tracking press:', key)
#                 hold_char(random.randint(1000, 2000), key)
#
#
#         elif distance < 10:
#             if g_nearest_enemy[1] > g_playerPos[1]:
#                 key = 'w'
#                 print('  retreat press:', key)
#                 hold_char(random.randint(1000, 3000), key)
#             if g_nearest_enemy[1] <= g_playerPos[1]:
#                 key = 's'
#                 print('  retreat press:', key)
#                 hold_char(random.randint(1000, 3000), key)
#
#         else:
#
#             key = motion_keys[random.randint(0, 1)]
#             print(' random press:', key)
#             hold_char(random.randint(100, 2000), key)
#
#     #sys.stdout.flush()
