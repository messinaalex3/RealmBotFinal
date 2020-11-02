import threading
import time
import GetData
import random
import cv2
import GrabScreen
import Movement
import AgentTest
import Looting

class GameState:
    mode = None
    lastMode = None
    frame = None
    modeArray = ["Nexus","Loot","Nexus","Over Portal","Transition","Realm","Over Portal","Realm","Loot","Realm","Transition"]
    array_i = 0
    screenEnemies = None
    mapEnemies = None
    playerHealth = 100
    gameWindow = GrabScreen.findWindow("RotMGExalt")
    playerPos = [[100,98]]
    closestEnemy = None
    staffImage = cv2.imread("Resources\\WeaponsImages\\SerpentineStaff.png")
    robeImage = cv2.imread("Resources\\WeaponsImages\\T1Robe.png")
    potionImage = cv2.imread("Resources\\WeaponsImages\\Potion.png")

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
                    t2 = threading.Thread(target=self.moveLR)
                    t3 = threading.Thread(target=self.moveUD)
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

            #time.sleep(.1)

    def nexus(self):
        print("Do Nexus Stuff...")
        time.sleep(.1)
        print("Nexus return")

    def realm(self):
        count = 0
        while(self.mode=="Realm"):
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

    def moveUD(self):
        count = 0
        while(self.mode=="Realm"):
            Movement.motionUD(self.closestEnemy, self.playerPos[0])
        print("MoveUD Realm return")

    def moveLR(self):
        count = 0
        while(self.mode=="Realm"):
            Movement.motionLR(self.closestEnemy, self.playerPos[0])
        print("MoveLR Realm return")






gs = GameState()
t1 = threading.Thread(target=gs.getMainFrame)
t1.start()
time.sleep(.5)
t2 = threading.Thread(target=gs.getMode)
t2.start()
t3 = threading.Thread(target=gs.modeListener)
t3.start()



















