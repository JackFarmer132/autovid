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

from moviepy.editor import *
from PIL import Image, ImageOps


clip = VideoFileClip(os.path.join(TEMP_CLIPS, "ten.mp4"))

prev_borders = ()
threshold = 2
total_dur = 0
subclip_start = 0
subclip_times = []

for i in range(10*(int(clip.duration)+1)):
    frame = clip.get_frame((i*0.1))
    total_dur += 0.1
    if prev_borders:
        cur_borders = getBorders(frame)
        # if borders are different, then new clip has started
        if (abs(cur_borders[0]-prev_borders[0])>threshold) and (abs(cur_borders[1]-prev_borders[1])>threshold):
            print("at time " + str(round(total_dur,5)))
            subclip_times.append((subclip_start, (total_dur-0.2)))
            subclip_start = total_dur + 0.1
        # update
        prev_borders = cur_borders
    else:
        prev_borders = getBorders(frame)
# append final clip
subclip_times.append((subclip_start, (clip.duration - 0.1)))

for i, (subclip_start, subclip_end) in enumerate(subclip_times):
    # if clip is invalid size, don't make it
    if ((subclip_end - subclip_start) >= 5) and ((subclip_end - subclip_start) <= 35):
        subclip = clip.subclip(subclip_start, subclip_end)
        subclip.audio = None
        output_path = os.path.join(TEMP_CLIPS, "frames/clip_" + str(i) + ".mp4")
        subclip.write_videofile(output_path)
