import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('Sky Pirates Online - A New Era')
# initialize the Vision class
vision_fishingspot = Vision('fishing_spot.png')


loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # display the processed image
    points = vision_fishingspot.find(screenshot, 0.5, 'rectangles')
    #points = vision_fishingspot.find(screenshot, 0.4, 'points')

    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #result = len(points)
    
    #print('number of fishing spot : ',result)
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')