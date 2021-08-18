from conf import *
from clip_times import *

import datetime
import math
import string
import pickle
import cv2
import random
import numpy as np
from shutil import copyfile

from moviepy.editor import *
from PIL import Image, ImageChops

for i in range(10):
    clip = VideoFileClip(os.path.join(TEMP_CLIPS, str(i) + ".mp4"))
    base_frame = Image.fromarray(clip.get_frame(0))

    # holds frames for border analysis
    frames = []

    # sample one frame per second
    for j in range(int(clip.duration)):
        # save grey-scale frame to array
        frames.append(cv2.cvtColor(clip.get_frame(j),cv2.COLOR_BGR2GRAY))

    # perform 'and' to make all changing frames black and unchanging white
    result = cv2.bitwise_and(frames[0], frames[1])
    for frame in frames[2:]:
        result = cv2.bitwise_and(result, frame)

    # invert image so target area is white and borders black
    result = cv2.bitwise_not(result)
    result = cv2.blur(result, (5, 5))
    # convert to Image
    image = Image.fromarray(result)

    image.save(os.path.join(TEMP_CLIPS, str(i) + "-grey.png"))

    # get 10 random y-axis coords to get trim amount
    y_coords = random.sample(range(image.height-1), 10)
    # best guess for length of border to be trimmed
    best_guess = 0
    # go through x-axis until white pixels found
    for y in y_coords:
        x = 0
        border_length = 0
        print(x)
        print(y)
        while (image.getpixel((x,y)) < 250) and (x<image.width):
            border_length += 1
            x += 1
        best_guess = max(best_guess, border_length)
        print(border_length)

    # add some extra padding to estimate for safety
    best_guess += 5

    # trim clip and write back
    trimmed_clip = clip.crop(x1=best_guess, x2=image.width-best_guess)
    trimmed_clip.write_videofile(os.path.join(TEMP_CLIPS, str(i) + "-trimmed.mp4"))
