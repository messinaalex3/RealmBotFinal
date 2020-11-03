import threading
import time
import GetData
import random
import cv2
import GrabScreen
import Movement
import AgentTest
import Looting
import Nexus

class GameState:
    def __init__(self):
        self.mode = None
        self.lastMode = None
        self.frame = None
        self.modeArray = ["Nexus","Loot","Nexus","Over Portal","Transition","Realm","Over Portal","Realm","Loot","Realm","Transition"]
        self.array_i = 0
        self.screenEnemies = None
        self.mapEnemies = None
        self.playerHealth = 100
        self.gameWindow = GrabScreen.findWindow("RotMGExalt")
        self.playerPos = [[100,98]]
        self.closestEnemy = None
        self.staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
        self.robeImage = cv2.imread("Resources\\WeaponsImages\\T1Robe.png")
        self.potionImage = cv2.imread("Resources\\WeaponsImages\\Potion.png")
        self.mvt = Movement.Movement(self)

    def getMode(self):
        while(True):
            self.mode = GetData.getMode(self.frame)


    def getMainFrame(self):
        while(True):
            tempFrame = GrabScreen.captureScreen(self.gameWindow)
            self.frame = cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)

    def modeListener(self):
        while (True):
            mode = self.mode
            if mode != self.lastMode:
                print("New Mode: ", self.mode)
                if mode =="Nexus":
                    self.nexus()
                elif mode =="Realm":
                    t1 = threading.Thread(target=self.realm)
                    t2 = threading.Thread(target=self.mvt.move,args=('LR',))
                    t3 = threading.Thread(target=self.mvt.move,args=('UD',))
                    t1.start()
                    t2.start()
                    t3.start()
                    t1.join()
                    t2.join()
                    t3.join()
                    self.mvt.modeChange = False
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

            #time.sleep(.1)

    def nexus(self):
        print("Do Nexus Stuff...")
        Nexus.doNexus()
        print("Nexus return")

    def realm(self):
        count = 0
        while(self.mode=="Realm"):
            #print("Running Realm")
            self.screenEnemies = GetData.getEnemiesScreen(self.frame)
            self.mapEnemies = GetData.getEnemiesMap(self.frame)
            self.closestEnemy = AgentTest.findClosestEnemy(self.mapEnemies,self.playerPos)
            AgentTest.Aim(self.screenEnemies,self.gameWindow)
            #im wondering if this should be a thread since we dont want to die if were checking enemies on screen
            AgentTest.monitorHealth(self.playerHealth)
            self.playerPos = GetData.getPlayerPos(self.frame)
        print("realm return")

    def loot(self):
        print("Do Loot Stuff...")
        Looting.doLooting(self.frame,self.staffImage,self.robeImage,self.potionImage,self.gameWindow)
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

    # def moveUD(self):
    #     count = 0
    #     while(self.mode=="Realm"):
    #         Movement.motionUD(self.closestEnemy, self.playerPos[0])
    #         print("Closest Enemy: ",self.closestEnemy)
    #     print("MoveUD Realm return")
    #
    # def moveLR(self):
    #     count = 0
    #     while(self.mode=="Realm"):
    #         Movement.motionLR(self.closestEnemy, self.playerPos[0])
    #     print("MoveLR Realm return")




gs = GameState()
t1 = threading.Thread(target=gs.getMainFrame)
t1.start()
time.sleep(.5)
t2 = threading.Thread(target=gs.getMode)
t2.start()
t3 = threading.Thread(target=gs.modeListener)
t3.start()
t1.join()
t2.join()
t3.join()

print("exit")

















