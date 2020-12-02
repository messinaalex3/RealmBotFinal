import multiprocessing
import random
import sys
import time
import numpy as np
import GrabScreen
import cv2
import GetData
import AgentTest
import Nexus
import pyautogui
import Looting

class GameState:
    def __init__(self, gameWindow,frame,mode,playerPos,closestEnemyPos,retreatDistance,moveTowardDistance):
        self.gameWindow = gameWindow            # LIST, use [0] to access
        self.frame = frame                      # LIST, use [0] to access
        self.mode = mode                        # LIST, use [0] to access
        self.playerPos = playerPos
        self.closestEnemyPos = closestEnemyPos
        self.retreatDistance = retreatDistance
        self.moveTowardDistance = moveTowardDistance
        self.initGS()

    def initGS(self):
        gameWindow = GrabScreen.findWindow("RotMGExalt")   #RotMGExalt #RealmBotFinal
        self.gameWindow[0] = gameWindow
        self.playerPos[0] = [0,0]
        self.closestEnemyPos[0] = [0,0]
        self.retreatDistance[0] = 15
        self.moveTowardDistance[0] = 30

    def getMode(self):
        while True:
            self.mode[0] = GetData.getMode(self.frame[0])
            #print("Mode",self.mode[0])

    def read_state(self):
        for i in range(0, 100000):
            #cv2.imshow("Frame_Read", self.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
        return

    def read_state_2(self):
        for i in range(0, 1000):
            #cv2.imshow("Frame_Read_2", self.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
        return

    def getMainFrame(self):
        while True:
            tempFrame = GrabScreen.captureScreen(self.gameWindow[0])
            self.frame[0] = cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)
            #print("MainFrame:",i)
        return


class Agent:
    def __init__(self, gamestate):
        self.gameState = gamestate

    def printMode(self):
        for i in range(0, 100000):
            #cv2.imshow("Frame_Read_3", self.gameState.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

        print("Agent Mode:", self.gameState.mode[0])

        return

    def runAgent(self):
        GrabScreen.findWindow("RotMGExalt")
        while True:
            while self.gameState.mode[0] == "Nexus":
                print("hello sir, i reside in the nexus.")
                screenEnemies = GetData.getEnemiesScreen(self.gameState.frame[0])
                AgentTest.Aim(screenEnemies,self.gameState.gameWindow[0],self.gameState.frame[0])
                Nexus.doNexus()
            while self.gameState.mode[0] == "Realm":
                print("ahh good day fine sir, you may find me in the realm.")
                screenEnemies = GetData.getEnemiesScreen1(self.gameState.frame[0])
                AgentTest.Aim1(screenEnemies,self.gameState.gameWindow[0],self.gameState.frame[0])
                mapEnemies = GetData.getEnemiesMap(self.gameState.frame[0])
                screenBags = GetData.findLootBags(self.gameState.frame[0])
                self.gameState.playerPos[0] = GetData.getPlayerPos(self.gameState.frame[0])[0]
                #Hey future alex, this is a note from past alex...i know magic right?
                #This is where you left off, check for screen enemies > 1 and use getData.GetSafeMovement to update closestEnemyPos for movement.
                self.gameState.closestEnemyPos[0] = AgentTest.findClosestEnemy(mapEnemies,[self.gameState.playerPos[0]])
                if len(screenEnemies) >= 1:
                    self.gameState.closestEnemyPos[0] = GetData.getSafeMovement(self.gameState.frame[0])
                    self.gameState.retreatDistance[0] = 0
                    self.gameState.moveTowardDistance[0] = 0
                elif len(screenBags) > 0 and len(screenEnemies) == 0 and random.randint(0,10) > 4:
                    self.gameState.closestEnemyPos[0] = screenBags[0]
                    self.gameState.retreatDistance[0] = 0
                    self.gameState.moveTowardDistance[0] = 20
                else:
                    self.gameState.retreatDistance[0] = 15
                    self.gameState.moveTowardDistance[0] = 30
                self.gameState.playerPos[0] = self.gameState.playerPos[0]
            while self.gameState.mode[0] == "Transition":
                print("To be honest...im not sure where i am, im blind")
            while self.gameState.mode[0] == "Loot":
                print("pardon me sir, im counting my cheddar")
                pyautogui.keyUp("w")
                pyautogui.keyUp("s")
                pyautogui.keyUp("a")
                pyautogui.keyUp("d")
                Looting.doLootingNoImage(self.gameState.frame[0],self.gameState.gameWindow[0])

    def AgentLooting(self):
        while True:
            while self.gameState.mode[0] == "Loot":
                print("pardon me sir, im counting my cheddar")
                pyautogui.keyUp("w")
                pyautogui.keyUp("s")
                pyautogui.keyUp("a")
                pyautogui.keyUp("d")
                Looting.doLootingNoImage(self.gameState.frame[0],self.gameState.gameWindow[0])

    def monitorHealth(self):
        while True:
            while self.gameState.mode[0] == "Realm" or self.gameState.mode[0] == "Loot":
                health = GetData.getPlayerData(self.gameState.frame[0])
                outOfPotions = GetData.outOfPotions(self.gameState.frame[0])
                AgentTest.monitorHealth(health,outOfPotions)

    def hold_char(self,hold_time, char):
        pyautogui.keyDown(char)
        time.sleep(hold_time // 1000)
        pyautogui.keyUp(char)

    def motionUD(self):
        while True:

            motion_keys = ['w', 's']
            print(self.gameState.mode[0])
            while self.gameState.mode[0] == "Realm":
                print("LOOK HERE", self.gameState.closestEnemyPos)
                print("inside",self.gameState.mode[0])
                # time.sleep(.1)
                sys.stdout.write("\rNearest Enemy: {}".format(self.gameState.closestEnemyPos[0]))
                sys.stdout.write("   Player Loc: {}".format(self.gameState.playerPos[0][0]))


                distance = abs(self.gameState.closestEnemyPos[0][0] - self.gameState.playerPos[0][0]) + abs(self.gameState.closestEnemyPos[0][1] - self.gameState.playerPos[0][1])
                sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

                key = ''
                random.seed(time.time())

                if distance > self.gameState.moveTowardDistance[0]:
                    if self.gameState.closestEnemyPos[0][1] > self.gameState.playerPos[0][1]:
                        key = 's'
                        print('  tracking press:', key)
                        self.hold_char(random.randint(1000, 1001), key)
                    if self.gameState.closestEnemyPos[0][1] <= self.gameState.playerPos[0][1]:
                        key = 'w'
                        print('  tracking press:', key)
                        self.hold_char(random.randint(1000, 1001), key)


                elif distance < self.gameState.retreatDistance[0]:
                    if self.gameState.closestEnemyPos[0][1] > self.gameState.playerPos[0][1]:
                        key = 'w'
                        print('  retreat press:', key)
                        self.hold_char(random.randint(1000, 1001), key)
                    if self.gameState.closestEnemyPos[0][1] <= self.gameState.playerPos[0][1]:
                        key = 's'
                        print('  retreat press:', key)
                        self.hold_char(random.randint(1000, 1001), key)

                else:

                    key = motion_keys[random.randint(0, 1)]
                    print(' random press:', key)
                    self.hold_char(random.randint(100, 1000), key)

            sys.stdout.flush()

    def motionLR(self):
        while True:
            motion_keys = ['a', 'd']

            while self.gameState.mode[0] == "Realm":
                # time.sleep(.1)
                sys.stdout.write("\rNearest Enemy: {}".format(self.gameState.closestEnemyPos[0]))
                # sys.stdout.write("   Player Loc: {}".format(self.gameState.playerPos[0]))


                distance = abs(self.gameState.closestEnemyPos[0][0] - self.gameState.playerPos[0][0]) + abs(self.gameState.closestEnemyPos[0][1] - self.gameState.playerPos[0][1])
                # sys.stdout.write("\rNearest Enemy Distance: {}".format(distance))

                key = ''
                random.seed(time.time())

                if distance > self.gameState.moveTowardDistance[0]:
                    if self.gameState.closestEnemyPos[0][0] > self.gameState.playerPos[0][0]:
                        key = 'd'
                        # print('  tracking press:', key)
                        self.hold_char(random.randint(1000, 1001), key)
                    if self.gameState.closestEnemyPos[0][0] <= self.gameState.playerPos[0][0]:
                        key = 'a'
                        # print('  tracking press:', key)
                        self.hold_char(random.randint(1000, 1001), key)

                elif distance < self.gameState.retreatDistance[0]:
                    if self.gameState.closestEnemyPos[0][0] > self.gameState.playerPos[0][0]:
                        key = 'a'
                        # print('  retreat press:', key)
                        self.hold_char(random.randint(1000, 1001), key)
                    if self.gameState.closestEnemyPos[0][0] <= self.gameState.playerPos[0][0]:
                        key = 'd'
                        # print('  retreat press:', key)
                        self.hold_char(random.randint(1000, 1001), key)

                else:

                    key = motion_keys[random.randint(0, 1)]
                    # print(' random press:', key)
                    self.hold_char(random.randint(100, 1000), key)

            sys.stdout.flush()


if __name__ == '__main__':
    with multiprocessing.Manager() as mgr:

        window = mgr.list(range(1))
        frame = mgr.list(range(1))
        mode = mgr.list(range(1))
        playerPos = mgr.list(range(1))
        closestEnemyPos = mgr.list(range(1))
        retreatDistance = mgr.list(range(1))
        moveTowardDistance = mgr.list(range(1))
        movementLength = mgr.list(range(1))
        #in case you forgot what you were doing...shh i didnt read your mind
        #you were adding a variable to mvoement length(time) for shorter(and twitchier) movements when enemies are on screen

        gameState = GameState(window,frame,mode,playerPos,closestEnemyPos,retreatDistance,moveTowardDistance)

        agent = Agent(gameState)

        processes = []

        processes.append(multiprocessing.Process(name='append_state', target=gameState.getMainFrame))
        processes.append(multiprocessing.Process(name='get_mode', target=gameState.getMode))
        processes.append(multiprocessing.Process(name='read_state', target=gameState.read_state))
        #processes.append(multiprocessing.Process(name='read_state_3', target=agent.printMode))
        processes.append(multiprocessing.Process(name='run_agent', target=agent.runAgent))
        processes.append(multiprocessing.Process(name='monitor_health', target=agent.monitorHealth))
        # processes.append(multiprocessing.Process(name='agent_looting', target=agent.AgentLooting))
        processes.append(multiprocessing.Process(name='agent_movementUD', target=agent.motionUD))
        processes.append(multiprocessing.Process(name='agent_movementLR', target=agent.motionLR))

        for proc in processes:
            proc.start()

        # time.sleep(3)
        # agent.printMode()

        for proc in processes:
            proc.join()

        print("done")



