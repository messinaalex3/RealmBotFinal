import pyautogui
import time
import sys
import random


def hold_char(hold_time,char):
    pyautogui.keyDown(char)
    time.sleep(hold_time//1000)
    pyautogui.keyUp(char)

def motionLR(g_nearest_enemy,g_playerPos):

    motion_keys = ['a','d']

    while True:
        sys.stdout.write("\rNearest Enemy: {}".format(g_nearest_enemy))
        #sys.stdout.write("   Player Loc: {}".format(g_playerPos))

        if 'numpy.ndarray' in str(type(g_playerPos)):
            distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
            #sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

            key = ''
            random.seed(time.time())

            if distance > 30:
                if g_nearest_enemy[0] > g_playerPos[0]:
                    key = 'd'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)
                if g_nearest_enemy[0] <= g_playerPos[0]:
                    key = 'a'
                    #print('  tracking press:', key)
                    hold_char(random.randint(1000, 2000), key)

            elif distance < 10:
                if g_nearest_enemy[0] > g_playerPos[0]:
                    key = 'a'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)
                if g_nearest_enemy[0] <= g_playerPos[0]:
                    key = 'd'
                    #print('  retreat press:', key)
                    hold_char(random.randint(1000, 3000), key)

            else:

                key = motion_keys[random.randint(0, 1)]
                #print(' random press:', key)
                hold_char(random.randint(100, 2000), key)

        sys.stdout.flush()

def motionUD(g_nearest_enemy,g_playerPos):

    motion_keys = ['w','s']



    if 'numpy.ndarray' in str(type(g_playerPos)):
        distance = abs(g_nearest_enemy[0]-g_playerPos[0]) + abs(g_nearest_enemy[1]-g_playerPos[1])
        sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

        key = ''
        random.seed(time.time())

        if distance > 30:
            if g_nearest_enemy[1] > g_playerPos[1]:
                key = 's'
                #print('  tracking press:', key)
                hold_char(random.randint(1000, 2000), key)
            if g_nearest_enemy[1] <= g_playerPos[1]:
                key = 'w'
                #print('  tracking press:', key)
                hold_char(random.randint(1000, 2000), key)


        elif distance < 10:
            if g_nearest_enemy[1] > g_playerPos[1]:
                key = 'w'
                #print('  retreat press:', key)
                hold_char(random.randint(1000, 3000), key)
            if g_nearest_enemy[1] <= g_playerPos[1]:
                key = 's'
                #print('  retreat press:', key)
                hold_char(random.randint(1000, 3000), key)

        else:

            key = motion_keys[random.randint(0, 1)]
            #print(' random press:', key)
            hold_char(random.randint(100, 2000), key)

    sys.stdout.flush()
