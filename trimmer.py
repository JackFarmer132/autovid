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
from PIL import Image, ImageOps

def findBorderLength(image):
    cur_border = 0
    # find the border for the left of the clip
    for y in range(0, int(image.height), 10):
        # hold previously seen pixel values to determine anomolies
        pixel_colours = []
        # go into image from left until assumed border ends
        for x in range(int(image.width/2)):
            if pixel_colours:
                # average over past 10 pixels
                (r1,g1,b1) = [sum(c) / len(c) for c in zip(*pixel_colours)]
                pixel_colours.append(image.getpixel((x,y)))
                # pixel values for new pixel
                (r2,g2,b2) = pixel_colours[-1]
                # distance between average and current
                dist = math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)
                # print(str(pixel_colours[-1]) + ", " + str(dist))
                # if above theshold for difference, border is over
                if dist > 10:
                    break
                # keep the array small for good averages
                if len(pixel_colours) > 10:
                    pixel_colours.pop(0)
            else:
                pixel_colours.append(image.getpixel((x,y)))
        # add for safety (better to trim too much than too little)
        x += 10
        cur_border = max(cur_border, x)

    # if this is the case then it's likely an error occured and default border should be used
    if cur_border >= 656:
        cur_border = 0
    return cur_border


def getBorders(video):
    # get first frame and blur it
    base_frame = Image.fromarray(cv2.blur(video.get_frame(0), (15,15)))
    left_border = findBorderLength(base_frame)
    base_frame = base_frame.transpose(Image.FLIP_LEFT_RIGHT)
    right_border = findBorderLength(base_frame)

    # fix any errors
    if (not left_border) and (not right_border):
        left_border = 500
        right_border = 500
    elif not left_border:
        left_border = right_border
    elif not right_border:
        right_border = left_border

    # apparently you can't have an odd-numbered width, so fix that here
    if ((left_border + right_border) % 2) == 1:
        right_border += 1

    return (left_border, right_border)


for fname in os.listdir(TEMP_CLIPS):
    clip = VideoFileClip(os.path.join(TEMP_CLIPS, fname))
    # get border lengths
    (left_border, right_border) = getBorders(clip)
    print("left border (correct one) is " + str(left_border))
    print("right border is " + str(right_border))
    # base_frame = base_frame.crop((max_border, 0, base_frame.width-max_border, base_frame.height))
    # base_frame.save(os.path.join(TEMP_CLIPS, "0-trimmed.png"))
    trimmed_clip = clip.crop(x1=left_border, x2=clip.size[0]-right_border)
    trimmed_clip.write_videofile(os.path.join(TEMP_CLIPS, "zzzzzzzz/" + fname[:-4] + "-trimmed.mp4"))
