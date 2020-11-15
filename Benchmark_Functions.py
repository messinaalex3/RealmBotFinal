import time
import GrabScreen
import cv2
import Utils
import GetData
import AgentTest
import Bullets
import threading

class MTBenchmark:
    def __init__(self,trials,mode):
        self.trials = trials
        self.count = 0
        self.str_width = 50
        self.loopMode = mode
        
        self.playerPos = [[100,98]]
        self.frame = None
        self.gameFrame = None
        self.gameWindow = None
        self.screenEnemies = []
        
        self.GrabScreenfindWindow = 0
        self.GrabScreencaptureScreen = 0
        self.ConvertCutFrameColor = 0
        self.UtilscutGameFrame = 0
        self.GetDatagetMode = 0
        self.GetDatagetEnemiesScreen1 = 0
        self.AgentTestAim1 = 0
        self.GetDatagetEnemiesMap = 0
        self.AgentTestfindClosestEnemy = 0
        self.GetDatagetPlayerData = 0
        self.AgentTestmonitorHealth = 0
        self.BulletgetEightWayZones = 0
        self.LoopTime = 0

        self.runtrials()

    def everythingElse(self):
    
        # Get Mode
        start = time.time()
        mode = GetData.getMode(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getMode(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetMode += delta

        # Get Screen Enemies
        start = time.time()
        self.screenEnemies = GetData.getEnemiesScreen1(self.gameFrame)
        delta = time.time()-start
        #print("{0}. GetData.getEnemiesScreen1(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetEnemiesScreen1 += delta

        # Aim
        if self.loopMode == "serialized" or self.loopMode == "bulletLoopThread":
            start = time.time()
            AgentTest.Aim1(self.screenEnemies, self.gameWindow,self.gameFrame)
            delta = time.time()-start
            #print("{0}. AgentTest.Aim1(screenEnemies, gameWindow, frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.AgentTestAim1 += delta

        # Get Map Enemies
        start = time.time()
        mapEnemies = GetData.getEnemiesMap(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getEnemiesMap(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetEnemiesMap += delta


        # Closest Map Enemy
        start = time.time()
        closestEnemy = AgentTest.findClosestEnemy(mapEnemies,self.playerPos)
        delta = time.time()-start
        #print("{0}. AgentTest.findClosestEnemy(mapEnemies,playerPos):".format(self.count).ljust(self.str_width,' '),delta)
        self.AgentTestfindClosestEnemy += delta


        # Get Health
        start = time.time()
        health = GetData.getPlayerData(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getPlayerData(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetPlayerData += delta


        # Monitor Health
        start = time.time()
        if mode == "Realm":
            AgentTest.monitorHealth(health)
        delta = time.time()-start
        #print("{0}. AgentTest.monitorHealth(health):".format(self.count).ljust(self.str_width,' '),delta)
        self.AgentTestmonitorHealth += delta

    def bulletFunction(self):
        # Get Bullets
        start = time.time()
        safestMove = Bullets.getEightWayZones(self.gameFrame)
        delta = time.time()-start
        #print("{0}. Bullet.getEightWayZones(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.BulletgetEightWayZones += delta

    def bulletSep(self):
        while(self.count < self.trials):
            # Get Bullets
            start = time.time()
            safestMove = Bullets.getEightWayZones(self.gameFrame)
            time.sleep(.000000001)
            delta = time.time()-start
            #print("{0}. Bullet.getEightWayZones(frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.BulletgetEightWayZones += delta


    def AimSep(self):
        while(self.count < self.trials):
            start = time.time()
            AgentTest.Aim1(self.screenEnemies, self.gameWindow,self.gameFrame)
            time.sleep(.000000001)
            delta = time.time()-start
            #print("{0}. AgentTest.Aim1(screenEnemies, gameWindow, frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.AgentTestAim1 += delta

    def printResults(self):
        functions = []

        functions.append(("GrabScreen.findWindow(RotMGExalt)", self.GrabScreenfindWindow))
        functions.append(("GrabScreen.captureScreen(gameWindow)", self.GrabScreencaptureScreen))
        functions.append(("cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)", self.ConvertCutFrameColor))
        functions.append(("Utils.cutGameFrame(frame)", self.UtilscutGameFrame))
        functions.append(("GetData.getMode(frame)", self.GetDatagetMode))
        functions.append(("GetData.getEnemiesScreen1(frame)", self.GetDatagetEnemiesScreen1))
        functions.append(("AgentTest.Aim1(screenEnemies, gameWindow, frame)", self.AgentTestAim1))
        functions.append(("GetData.getEnemiesMap(frame)", self.GetDatagetEnemiesMap))
        functions.append(("AgentTest.findClosestEnemy(mapEnemies,playerPos)", self.AgentTestfindClosestEnemy))
        functions.append(("(Health) GetData.getPlayerData(frame)", self.GetDatagetPlayerData))
        functions.append(("AgentTest.monitorHealth(health)", self.AgentTestmonitorHealth))
        functions.append(("Bullet.getEightWayZones(frame)", self.BulletgetEightWayZones))

        print("\n\nTrials: ", f'{int(self.trials):,}')
        print("\n----------Averages----------\n")

        functions.sort(key=lambda x: x[1], reverse=True)

        total_avg_time = 0

        for function in functions:
            print((function[0] + ":").ljust(self.str_width, ' '), "{:.10f}".format(function[1] / self.trials))
            total_avg_time += function[1] / self.trials

        print("\nTotal Avg Time:".ljust(self.str_width + 1, ' '), "{:.10f}".format(total_avg_time))
        print("Loop Time:".ljust(self.str_width, ' '), "{:.10f}".format(self.LoopTime / self.trials))

    def mainLoop(self):
        while (self.count < self.trials):

            print("Trial Loop#:", self.count)

            start_loop = time.time()

            # GrabScreen.findWindow
            start = time.time()
            self.gameWindow = GrabScreen.findWindow("RotMGExalt")
            delta = time.time() - start
            #print("{0}. GrabScreen.findWindow(RotMGExalt):".format(self.count).ljust(self.str_width, ' '), delta)
            self.GrabScreenfindWindow += delta

            # GrabScreen.captureScreen
            start = time.time()
            tempFrame = GrabScreen.captureScreen(self.gameWindow)
            delta = time.time() - start
            #print("{0}. GrabScreen.captureScreen(gameWindow):".format(self.count).ljust(self.str_width, ' '), delta)
            self.GrabScreencaptureScreen += delta

            # Convert cutframe color
            start = time.time()
            self.frame = cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)
            delta = time.time() - start
            #print("{0}. cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB):".format(self.count).ljust(self.str_width, ' '),delta)
            self.ConvertCutFrameColor += delta

            # Utils.cutGameFrame
            start = time.time()
            self.gameFrame = Utils.cutGameFrame(self.frame)
            delta = time.time() - start
            #print("{0}. Utils.cutGameFrame(frame):".format(self.count).ljust(self.str_width, ' '), delta)
            self.UtilscutGameFrame += delta

            if self.loopMode == "serialized":
                #-------- Serial --------#

                self.everythingElse()
                self.bulletFunction()

            elif self.loopMode == "bulletLoopThread":
                # -------- Multi-Threaded --------#

                t1 = threading.Thread(target=self.bulletFunction)
                t2 = threading.Thread(target=self.everythingElse)

                t1.start()
                t2.start()

                t1.join()
                t2.join()

            elif self.loopMode == "bulletAimThreads":
                #-------- Separate Bullet and Aim Threads --------#
                self.everythingElse()

            #print('')

            delta_loop = time.time() - start_loop

            self.LoopTime += delta_loop

            self.count += 1

    def runtrials(self):

        if self.loopMode == "serialized" or self.loopMode == "bulletLoopThread":
            # Bullet in main loop or serial
            self.mainLoop()
        elif self.loopMode == "bulletAimThreads":
            # Separate Bullet and Aim
            t1 = threading.Thread(target=self.mainLoop)
            t2 = threading.Thread(target=self.bulletSep)
            t3 = threading.Thread(target=self.AimSep)

            t1.start()
            time.sleep(.1)
            t2.start()
            t3.start()

            t1.join()
            t2.join()
            t3.join()

        self.printResults()


if __name__ == "__main__":

    call_mode = "bulletAimThreads"         # "bulletLoopThread" or "bulletAimThreads" or "serialized"
    bm = MTBenchmark(200.0, call_mode)

