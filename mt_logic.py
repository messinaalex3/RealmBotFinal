import threading
import time
import random

class Movement:
    def __init__(self, gamestate):
        self.gameState = gamestate

    def moveUD(self):
        count = 0
        while(self.gameState.mode=="Realm"):
            print("MoveUD realm stuff: ",count)
            count += 1
            time.sleep(.1)
        print("MoveUD Realm return")

    def moveLR(self):
        count = 0
        while(self.gameState.mode=="Realm"):
            print("MoveLR realm stuff: ",count)
            count += 1
            time.sleep(.1)
        print("MoveLR Realm return")


class GameState:
    def __init__(self):
        self.mode = None
        self.lastMode = None
        self.frame = None
        self.modeArray = ["Nexus","Loot","Nexus","Over Portal","Transition","Realm","Over Portal","Realm","Loot","Realm","Transition"]
        self.array_i = 0
        self.mvt = Movement(self)

    def getMode(self):
        while(True):
            self.mode = self.modeArray[self.array_i]
            time.sleep(1)
            if self.array_i == len(self.modeArray)-1:
                self.array_i = 0
            else:
                self.array_i += 1

    def getMainFrame(self):
        while(True):
            self.frame = time.time()
            time.sleep(1)

    def modeListener(self):
        while (True):
            mode = self.mode
            if mode != self.lastMode:
                print("New Mode: ", self.mode)
                if mode =="Nexus":
                    self.nexus()
                elif mode =="Realm":
                    t1 = threading.Thread(target=self.realm)
                    t2 = threading.Thread(target=self.mvt.moveLR)
                    t3 = threading.Thread(target=self.mvt.moveUD)
                    t1.start()
                    t2.start()
                    t3.start()
                    t1.join()
                    t2.join()
                    t3.join()
                    print("Joined Threads")
                elif mode =="Loot":
                    self.loot()
                elif mode =="Over Portal":
                    if self.lastMode == "Nexus":
                        self.portal()
                    else:
                        print("Last Mode not Nexus, don't enter portal!")
                elif mode == "Transition":
                    self.transition()

            self.lastMode = mode

            time.sleep(.1)

    def nexus(self):
        print("Do Nexus Stuff...")
        time.sleep(.1)
        print("Nexus return")

    def realm(self):
        count = 0
        while(self.mode=="Realm"):
            print("Do realm stuff: ",count)
            count += 1
            time.sleep(.1)
        print("realm return")

    def loot(self):
        print("Do Loot Stuff...")
        time.sleep(.1)
        print("Loot return")

    def portal(self):
        print("Do Portal Stuff...")
        time.sleep(.1)
        print("Portal return")

    def transition(self):
        count = 0
        while(self.mode=="Transition"):
            print("Do transition stuff: ",count)
            count += 1
            time.sleep(.1)
        print("Transition return")







gs = GameState()
t1 = threading.Thread(target=gs.getMainFrame)
t1.start()
t2 = threading.Thread(target=gs.getMode)
t2.start()
t3 = threading.Thread(target=gs.modeListener)
t3.start()



















