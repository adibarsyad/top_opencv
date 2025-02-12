import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


game_img = cv.imread('screenshot.png', cv.IMREAD_UNCHANGED)
spot_img = cv.imread('fishing_spot.png', cv.IMREAD_UNCHANGED)


result = cv.matchTemplate(game_img, spot_img, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

threshold = 0.9
# The np.where() return value will look like this:
# (array([482, 483, 483, 483, 484], dtype=int32), array([514, 513, 514, 515, 514], dtype=int32))
locations = np.where(result >= threshold)
# We can zip those up into a list of (x, y) position tuples
locations = list(zip(*locations[::-1]))
print(locations)

if locations:
    print('Found fishing spot.')

    spot_w = spot_img.shape[1]
    spot_h = spot_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + spot_w, top_left[1] + spot_h)
        # Draw the box
        cv.rectangle(game_img, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', game_img)
    cv.waitKey()
    #cv.imwrite('result.jpg', haystack_img)

else:
    print('Fishing spot not found.')