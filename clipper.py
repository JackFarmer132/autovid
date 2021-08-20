from conf import *

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
from skimage.metrics import structural_similarity



base_clip = VideoFileClip(os.path.join(TEMP_CLIPS, "ten.mp4"))
# trim away some background to increase differences
clip = base_clip.crop(x1=300, x2=base_clip.size[0]-300)
prev_frame = np.empty(0)
frames = []
blur = 10
threshold = 0.65
frame_no = 0

subclip_start = 0
subclip_times = []

for f in clip.iter_frames():
    frame_no += 1
    total_dur = frame_no/clip.fps
    if prev_frame.any():
        # convert to grey to allow analysis
        cur_frame = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        # blur a bit to help with noticing similar frames
        cur_frame = cv2.blur(cur_frame, (blur,blur))
        (score, _) = structural_similarity(cur_frame, prev_frame, full=True)
        # print("at time " + str(round(frame_no/clip.fps,5)) + ", score is " + str(score))
        if score <= threshold:
            print("at time " + str(round(total_dur,5)) + ", score is " + str(score))
            subclip_times.append((subclip_start, (total_dur-0.1)))
            subclip_start = total_dur + 0.1
        prev_frame = cur_frame
    else:
        prev_frame = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        prev_frame = cv2.blur(prev_frame, (blur,blur))
# append final clip
subclip_times.append((subclip_start, (clip.duration - 0.1)))

print(subclip_times)

for i, (subclip_start, subclip_end) in enumerate(subclip_times):
    # if clip is over 4 seconds, then use it
    if (subclip_end - subclip_start) >= 4:
        subclip = base_clip.subclip(subclip_start, subclip_end)
        output_path = os.path.join(TEMP_CLIPS, "frames/clip_" + str(i) + ".mp4")
        subclip.write_videofile(output_path)


# frames = []
# for f in clip.iter_frames():
#     frames.append(f)
#     print(f.shape)
#
# print(frames[0].shape)
# print("===========================")
# frame_one = Image.fromarray(frames[0]).convert('RGBA')
# frame_end = Image.fromarray(frames[-1]).convert('RGBA')
#
# frame_end.putalpha(127)
#
# frame_one.save(os.path.join(TEMP_CLIPS, "frames/one.png"))
# frame_end.save(os.path.join(TEMP_CLIPS, "frames/end.png"))
#
# frame_one.paste(frame_end, (0, 0), frame_end)
# frame_one.save(os.path.join(TEMP_CLIPS, "frames/merge.png"))
#
# frame_one = np.array(frame_one)[...,:-1]
# print(frame_one.shape)
