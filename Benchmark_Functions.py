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
        self.closestEnemy = None
        self.gameMode = None

        self.GrabScreenfindWindow = [0,0]
        self.GrabScreencaptureScreen = [0,0]
        self.ConvertCutFrameColor = [0,0]
        self.UtilscutGameFrame = [0,0]
        self.GetDatagetMode = [0,0]
        self.GetDatagetEnemiesScreen1 = [0,0]
        self.AgentTestAim1 = [0,0]
        self.GetDatagetEnemiesMap = [0,0]
        self.AgentTestfindClosestEnemy = [0,0]
        self.GetDatagetPlayerData = [0,0]
        self.AgentTestmonitorHealth = [0,0]
        self.BulletgetEightWayZones = [0,0]
        self.LoopTime = [0,0]
        self.MTBenchmarkmotionLR = [0,0]
        self.MTBenchmarkmotionUD = [0,0]

        self.runtrials()

    def everythingElse(self):
    
        # Get Mode
        start = time.time()
        self.gameMode = GetData.getMode(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getMode(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetMode[0] += delta
        self.GetDatagetMode[1] += 1

        # Get Screen Enemies
        start = time.time()
        self.screenEnemies = GetData.getEnemiesScreen1(self.gameFrame)
        delta = time.time()-start
        #print("{0}. GetData.getEnemiesScreen1(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetEnemiesScreen1[0] += delta
        self.GetDatagetEnemiesScreen1[1] += 1

        # Aim
        if self.loopMode == "serialized" or self.loopMode == "bulletLoopThread":
            start = time.time()
            AgentTest.Aim1(self.screenEnemies, self.gameWindow,self.gameFrame)
            delta = time.time()-start
            #print("{0}. AgentTest.Aim1(screenEnemies, gameWindow, frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.AgentTestAim1[0] += delta
            self.AgentTestAim1[1] += 1

        # Get Map Enemies
        start = time.time()
        mapEnemies = GetData.getEnemiesMap(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getEnemiesMap(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetEnemiesMap[0] += delta
        self.GetDatagetEnemiesMap[1] += 1


        # Closest Map Enemy
        start = time.time()
        self.closestEnemy = AgentTest.findClosestEnemy(mapEnemies,self.playerPos)
        delta = time.time()-start
        #print("{0}. AgentTest.findClosestEnemy(mapEnemies,playerPos):".format(self.count).ljust(self.str_width,' '),delta)
        self.AgentTestfindClosestEnemy[0] += delta
        self.AgentTestfindClosestEnemy[1] += 1


        # Get Health
        start = time.time()
        health = GetData.getPlayerData(self.frame)
        delta = time.time()-start
        #print("{0}. GetData.getPlayerData(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.GetDatagetPlayerData[0] += delta
        self.GetDatagetPlayerData[1] += 1


        # Monitor Health
        start = time.time()
        if self.gameMode == "Realm":
            AgentTest.monitorHealth(health)
        delta = time.time()-start
        #print("{0}. AgentTest.monitorHealth(health):".format(self.count).ljust(self.str_width,' '),delta)
        self.AgentTestmonitorHealth[0] += delta
        self.AgentTestmonitorHealth[1] += 1

    def bulletFunction(self):
        # Get Bullets
        start = time.time()
        safestMove = Bullets.getEightWayZones(self.gameFrame)
        delta = time.time()-start
        #print("{0}. Bullet.getEightWayZones(frame):".format(self.count).ljust(self.str_width,' '),delta)
        self.BulletgetEightWayZones[0] += delta
        self.BulletgetEightWayZones[1] += 1

    def bulletSep(self):
        while(self.count < self.trials):
            # Get Bullets
            start = time.time()
            safestMove = Bullets.getEightWayZones(self.gameFrame)
            time.sleep(.000000001)
            delta = time.time()-start
            #print("{0}. Bullet.getEightWayZones(frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.BulletgetEightWayZones[0] += delta
            self.BulletgetEightWayZones[1] += 1


    def AimSep(self):
        while(self.count < self.trials):
            start = time.time()
            AgentTest.Aim1(self.screenEnemies, self.gameWindow,self.gameFrame)
            time.sleep(.000000001)
            delta = time.time()-start
            #print("{0}. AgentTest.Aim1(screenEnemies, gameWindow, frame):".format(self.count).ljust(self.str_width,' '),delta)
            self.AgentTestAim1[0] += delta
            self.AgentTestAim1[1] += 1

    def motionUD(self):
        while (self.count < self.trials):
            start = time.time()
            if self.gameMode == "Realm":
                nearest = self.closestEnemy
            time.sleep(.01)
            delta = time.time() - start
            #print("{0}. MTBenchmark.motionUD():".format(self.count).ljust(self.str_width,' '),delta)
            self.MTBenchmarkmotionUD[0] += delta
            self.MTBenchmarkmotionUD[1] += 1

    def motionLR(self):
        while (self.count < self.trials):
            start = time.time()
            if self.gameMode == "Realm":
                nearest = self.closestEnemy
            time.sleep(.01)
            delta = time.time() - start
            #print("{0}. MTBenchmark.motionLR():".format(self.count).ljust(self.str_width,' '),delta)
            self.MTBenchmarkmotionLR[0] += delta
            self.MTBenchmarkmotionLR[1] += 1

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
        functions.append(("MTBenchmark.motionUD()", self.MTBenchmarkmotionUD))
        functions.append(("MTBenchmark.motionLR()", self.MTBenchmarkmotionLR))

        print("\n\nTrials: ", f'{int(self.trials):,}')
        print("\n----------Averages----------\n")

        functions.sort(key=lambda x: (x[1][0]/x[1][1]), reverse=True)

        total_avg_time = 0

        for function in functions:
            print((function[0] + ":").ljust(self.str_width, ' '), "{:.10f}".format(function[1][0] / function[1][1]))
            total_avg_time += function[1][0] / function[1][1]

        print("\nTotal Avg Time:".ljust(self.str_width + 1, ' '), "{:.10f}".format(total_avg_time))
        print("Loop Time:".ljust(self.str_width, ' '), "{:.10f}".format(self.LoopTime[0] / self.LoopTime[1]))

    def mainLoop(self):
        while (self.count < self.trials):

            print("Trial Loop#:", self.count)

            start_loop = time.time()

            # GrabScreen.findWindow
            start = time.time()
            self.gameWindow = GrabScreen.findWindow("RotMGExalt")
            delta = time.time() - start
            #print("{0}. GrabScreen.findWindow(RotMGExalt):".format(self.count).ljust(self.str_width, ' '), delta)
            self.GrabScreenfindWindow[0] += delta
            self.GrabScreenfindWindow[1] += 1

            # GrabScreen.captureScreen
            start = time.time()
            tempFrame = GrabScreen.captureScreen(self.gameWindow)
            delta = time.time() - start
            #print("{0}. GrabScreen.captureScreen(gameWindow):".format(self.count).ljust(self.str_width, ' '), delta)
            self.GrabScreencaptureScreen[0] += delta
            self.GrabScreencaptureScreen[1] += 1

            # Convert cutframe color
            start = time.time()
            self.frame = cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB)
            delta = time.time() - start
            #print("{0}. cv2.cvtColor(tempFrame, cv2.COLOR_RGBA2RGB):".format(self.count).ljust(self.str_width, ' '),delta)
            self.ConvertCutFrameColor[0] += delta
            self.ConvertCutFrameColor[1] += 1

            # Utils.cutGameFrame
            start = time.time()
            self.gameFrame = Utils.cutGameFrame(self.frame)
            delta = time.time() - start
            #print("{0}. Utils.cutGameFrame(frame):".format(self.count).ljust(self.str_width, ' '), delta)
            self.UtilscutGameFrame[0] += delta
            self.UtilscutGameFrame[1] += 1

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

            self.LoopTime[0] += delta_loop
            self.LoopTime[1] += 1

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
            t4 = threading.Thread(target=self.motionLR)
            t5 = threading.Thread(target=self.motionUD)

            t1.start()
            time.sleep(.1)
            t2.start()
            t3.start()
            t4.start()
            t5.start()

            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()

        self.printResults()


if __name__ == "__main__":

    call_mode = "bulletAimThreads"         # "bulletLoopThread" or "bulletAimThreads" or "serialized"
    bm = MTBenchmark(1500.0, call_mode)

