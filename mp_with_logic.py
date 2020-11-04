import multiprocessing
import random
import time
import numpy as np
import GrabScreen
import cv2
import GetData
import AgentTest
import Nexus

class GameState:
    def __init__(self, gameWindow,frame,mode):
        self.gameWindow = gameWindow            # LIST, use [0] to access
        self.frame = frame                      # LIST, use [0] to access
        self.mode = mode                        # LIST, use [0] to access
        self.initGS()

    def initGS(self):
        gameWindow = GrabScreen.findWindow("RotMGExalt")   #RotMGExalt #RealmBotFinal
        self.gameWindow[0] = gameWindow

    def getMode(self):
        while True:
            self.mode[0] = GetData.getMode(self.frame[0])
            #print("Mode",self.mode[0])

    def read_state(self):
        for i in range(0, 100000):
            cv2.imshow("Frame_Read", self.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
        return

    def read_state_2(self):
        for i in range(0, 1000):
            cv2.imshow("Frame_Read_2", self.frame[0])
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
            cv2.imshow("Frame_Read_3", self.gameState.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

        print("Agent Mode:", self.gameState.mode[0])

        return

    def runAgent(self):
        while True:
            while self.gameState.mode[0] == "Nexus":
                print("hello sir, i reside in the nexus.")
                screenEnemies = GetData.getEnemiesScreen(self.gameState.frame[0])
                AgentTest.Aim(screenEnemies,self.gameState.gameWindow[0],self.gameState.frame[0])
                #Nexus.doNexus()
            while self.gameState.mode[0] == "Realm":
                print("ahh good day fine sir, you may find me in the realm.")
                screenEnemies = GetData.getEnemiesScreen(self.gameState.frame[0])
                AgentTest.Aim(screenEnemies,self.gameState.gameWindow[0],self.gameState.frame[0])
                mapEnemies = GetData.getEnemiesMap(self.gameState.frame[0])
                playerPos = GetData.getPlayerPos(self.gameState.frame[0])
                closestEnemy = AgentTest.findClosestEnemy(mapEnemies,playerPos)
                # self.screenEnemies = GetData.getEnemiesScreen(self.frame)
                # self.mapEnemies = GetData.getEnemiesMap(self.frame)
                # self.closestEnemy = AgentTest.findClosestEnemy(self.mapEnemies, self.playerPos)
                # AgentTest.Aim(self.screenEnemies, self.gameWindow)
                # # im wondering if this should be a thread since we dont want to die if were checking enemies on screen
                # AgentTest.monitorHealth(self.playerHealth)
                # self.playerPos = GetData.getPlayerPos(self.frame)
            while self.gameState.mode[0] == "Transition":
                print("To be honest...im not sure where i am, im blind")
            while self.gameState.mode[0] == "Loot":
                print("pardon me sir, im counting my cheddar")


if __name__ == '__main__':
    with multiprocessing.Manager() as mgr:

        window = mgr.list(range(1))
        frame = mgr.list(range(1))
        mode = mgr.list(range(1))

        gameState = GameState(window,frame,mode)

        agent = Agent(gameState)

        processes = []

        processes.append(multiprocessing.Process(name='append_state', target=gameState.getMainFrame))
        processes.append(multiprocessing.Process(name='get_mode', target=gameState.getMode))
        processes.append(multiprocessing.Process(name='read_state', target=gameState.read_state))
        #processes.append(multiprocessing.Process(name='read_state_3', target=agent.printMode))
        processes.append(multiprocessing.Process(name='run_agent', target=agent.runAgent))

        for proc in processes:
            proc.start()

        # time.sleep(3)
        # agent.printMode()

        for proc in processes:
            proc.join()

        print("done")



