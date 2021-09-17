from conf import *
import datetime
import math
import string
import cv2
import random
import numpy as np
from shutil import copyfile
import time
from moviepy.editor import *
from PIL import Image, ImageOps


def find_border_length(image):
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
                if dist > 5:
                    break
                # keep the array small for good averages
                if len(pixel_colours) > 10:
                    pixel_colours.pop(0)
            else:
                pixel_colours.append(image.getpixel((x,y)))
        # add for safety (better to trim too much than too little)
        x += 10
        if x < (10+int(((image.width-608)/2))):
            cur_border = max(cur_border, x)
        # print("=====================")
    return cur_border


def get_borders(base_frame):
    # get first frame and blur it
    base_frame = Image.fromarray(cv2.blur(base_frame, (15,15)))
    left_border = find_border_length(base_frame)
    base_frame = base_frame.transpose(Image.FLIP_LEFT_RIGHT)
    right_border = find_border_length(base_frame)
    # fix any errors
    if (not left_border) and (not right_border):
        left_border = (10+int(((base_frame.width-608)/2)))
        right_border = left_border
    # helps catch when one border is very off for whatever reason
    if abs(left_border - right_border) >= 100:
        new_border = max(left_border, right_border)
        # set border to be largest of two, so long as it doesn't exceed max trim
        if new_border > (10+int(((base_frame.width-608)/2))):
            new_border = min(left_border, right_border)
            if new_border > (10+int(((base_frame.width-608)/2))):
                new_border = (10+int(((base_frame.width-608)/2)))
        left_border = new_border
        right_border = new_border

    # apparently you can't have an odd-numbered width, so fix that here
    if ((left_border + right_border) % 2) == 1:
        right_border += 1
    return (left_border, right_border)
