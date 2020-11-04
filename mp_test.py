import multiprocessing
import random
import time
import numpy as np
import GrabScreen
import cv2
import GetData

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
        for i in range(0, 1000):
            self.mode[0] = GetData.getMode(self.frame[0])
            #print("Mode",self.mode[0])

    def read_state(self):
        for i in range(0, 1000):
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
        for i in range(0, 500):
            tempFrame = GrabScreen.captureScreen(self.gameWindow[0])
            self.frame[0] = cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)
            #print("MainFrame:",i)
        return


class Agent:
    def __init__(self, gamestate):
        self.gameState = gamestate

    def printMode(self):
        for i in range(0, 1000):
            cv2.imshow("Frame_Read_3", self.gameState.frame[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

        print("Agent Mode:", self.gameState.mode[0])

        return


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
        processes.append(multiprocessing.Process(name='read_state_3', target=agent.printMode))

        for proc in processes:
            proc.start()

        # time.sleep(3)
        # agent.printMode()

        for proc in processes:
            proc.join()

        print("done")



