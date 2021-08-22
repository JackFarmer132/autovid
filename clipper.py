from conf import *
from trimmer import *

import datetime
import math
import string
import pickle
import cv2
import random
import numpy as np
from shutil import copyfile
import time
import gc

from moviepy.editor import *
from PIL import Image, ImageOps


def clipSource(fname, fpath):
    fname = fname[:-4]
    clip = VideoFileClip(fpath)
    clip = clip.set_fps(25)

    prev_borders = ()
    threshold = 2
    total_dur = 0
    subclip_start = 0
    subclip_times = []
    # progress bar things
    seconds_per_bar = round(int(clip.duration)/100, 1)
    cur_percent = 0
    print("|", end="", flush=True)

    # for i in range(10*(int(clip.duration/2))):
    #     frame = clip.get_frame((i*0.2))
    #     total_dur = round((total_dur+0.2),1)
    #     cur_percent += 0.2
    #     if prev_borders:
    #         cur_borders = getBorders(frame)
    #         # if borders are different, then new clip has started
    #         if (abs(cur_borders[0]-prev_borders[0])>threshold) and (abs(cur_borders[1]-prev_borders[1])>threshold):
    #             # print("at time " + str(round(total_dur,5)))
    #             subclip_times.append((subclip_start, (total_dur-0.4)))
    #             subclip_start = total_dur + 0.3
    #         # update
    #         prev_borders = cur_borders
    #     else:
    #         prev_borders = getBorders(frame)
    #     # update process bar if another percent of vid has been parsed
    #     if (cur_percent >= seconds_per_bar):
    #         print("=", end="", flush=True)
    #         cur_percent = 0

    seen_frames = 0
    # sees how many frames needed until 0.2 seconds has passed
    frames_until_target = (clip.fps/5)
    for frame in clip.iter_frames():
        seen_frames += 1
        # if 0.2 seconds has passed
        if seen_frames == frames_until_target:
            total_dur = round((total_dur+0.2),1)
            cur_percent += 0.2
            if prev_borders:
                cur_borders = getBorders(frame)
                # if borders are different, then new clip has started
                if (abs(cur_borders[0]-prev_borders[0])>threshold) and (abs(cur_borders[1]-prev_borders[1])>threshold):
                    # print("at time " + str(round(total_dur,5)))
                    subclip_times.append((subclip_start, (total_dur-0.4)))
                    subclip_start = total_dur + 0.3
                # update
                prev_borders = cur_borders
            else:
                prev_borders = getBorders(frame)
            # update process bar if another percent of vid has been parsed
            if (cur_percent >= seconds_per_bar):
                print("=", end="", flush=True)
                cur_percent = 0
            seen_frames = 0
        # otherwise keep skipping frames


    # append final clip
    subclip_times.append((subclip_start, (clip.duration - 0.1)))
    print("|")

    print("writing new clips...")
    for i, (subclip_start, subclip_end) in enumerate(subclip_times):
        # if clip is invalid size, don't make it
        if ((subclip_end - subclip_start) >= 4) and ((subclip_end - subclip_start) <= 60):
            subclip = clip.subclip(subclip_start, subclip_end)
            subclip.audio = None
            output_path = os.path.join(TEMP_CLIPS, fname + "_" + str(i) + ".mp4")
            subclip.write_videofile(output_path)
        gc.collect()



def cleanChoppingBoard():
    # go through all new full vids and generate clips
    for fname in os.listdir(CHOPPING_BOARD):
        print("beginning parse of " + fname + "...")
        fpath = os.path.join(CHOPPING_BOARD, fname)
        clipSource(fname, fpath)
        # os.remove(fpath)


cleanChoppingBoard()
