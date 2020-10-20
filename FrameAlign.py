import cv2
import numpy as np
import time

while True:

    # CurrentFrame and NewFrame cut from the following sequence from main
    # frame = GrabScreen.captureScreen(gameWindow)
    # frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
    # gameFrame = Utils.cutGameFrame(frame)

    gameFrame = cv2.imread("Resources\\FrameAlign\\CurrentFrame.jpg")

    # Clipping a portion of the frame for testing (focused on the cone)
    # Had to use copy because the green rectangle OpenCV applied in the main window was being copied over
    # and messing up frame comparison

    comp1 = gameFrame.copy()[280:330, 50:110]

    cv2.rectangle(gameFrame, (50, 280), (110, 330), (0, 255, 0), 0)
    cv2.imshow("CurrentFrame", gameFrame)

    cv2.imshow("comp1", comp1)

    # Cast to np.int16 otherwise arithmetic roles over on uint8
    comp1 = comp1.astype(np.int16)
    gameFrame = gameFrame.astype(np.int16)

    s = 280 # starting point for finding how far frame moved (from original point (50,280))

    # set min to +infinity to initialize
    min_val = float('inf')

    for i in range (0,50):

        # Same procedure as above but moving the rectangle a pixel at a time to check for alignment
        gameFrame2 = cv2.imread("Resources\\FrameAlign\\NewFrame.jpg")

        comp2 = gameFrame2.copy()[(s + i):(s + i + 50), 50:110]

        cv2.rectangle(gameFrame2, (50, s+i), (110, s+i+50), (0, 255, 0), 0)
        cv2.imshow("NewFrame", gameFrame2)

        cv2.imshow("comp2", comp2)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        start_time = time.time()            # Moved this around to check timing of function

        # Cast to np.int16 otherwise arithmetic roles over on uint8
        comp2 = comp2.astype(np.int16)

        # To test total subtraction on whole frame (about .01s on my machine)
        #gameFrame2 = gameFrame2.astype(np.int16)
        #d1 = np.absolute(gameFrame2 - gameFrame)

        # Less than .001s to compare 50x60 subset of pixels
        d1 = np.absolute(comp1 - comp2)
        pixel_diff = np.sum(d1)

        print(time.time() - start_time)

        # For debugging minimum
        if pixel_diff==33618:
            #print(comp1[0])
            #print(comp2[0])
            time.sleep(.1)
            print('ok')

        #print("diff: ",pixel_diff)

        if pixel_diff < min_val:
            min_val = pixel_diff
            #print("Min: ", min_val)

        time.sleep(.2)                  # Slowed down to visualize

    if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break







