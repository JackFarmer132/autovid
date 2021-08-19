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
                if dist > 5:
                    break
                # keep the array small for good averages
                if len(pixel_colours) > 10:
                    pixel_colours.pop(0)
            else:
                pixel_colours.append(image.getpixel((x,y)))
        # add for safety (better to trim too much than too little)
        x += 10
        if x < 656:
            cur_border = max(cur_border, x)
    return cur_border


def getBorders(video):
    # get first frame and blur it
    base_frame = Image.fromarray(cv2.blur(video.get_frame(0), (15,15)))
    base_frame.save(os.path.join(TEMP_CLIPS, "zzzzzzzz/base.jpg"))
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

    return video.crop(x1=left_border, x2=clip.size[0]-right_border)


# read in clips list
with open(CLIP_PKL, 'rb') as f:
    vid_list = pickle.load(f)
# read in audio list
with open(AUD_PKL, 'rb') as f:
    aud_list = pickle.load(f)

# reading from head, construct video until duration is target
vid_clips = []
aud_clips = []
# holds current duration in seconds
vid_dur = 0
aud_dur = 0

# constructs video of at least given length
while (vid_dur < 600):
    clip = VideoFileClip(vid_list.pop(0)[1])
    trimmed_clip = getBorders(clip)
    # add duration to runtime
    vid_dur += trimmed_clip.duration
    vid_clips.append(trimmed_clip)

# make video
output_vid = concatenate_videoclips(vid_clips, method="compose")

# constructs audio backing that fits at least the vid length
while (aud_dur < vid_dur):
    aud_clip = AudioFileClip(aud_list.pop(0)[1])
    aud_dur += aud_clip.duration
    aud_clips.append(aud_clip)

output_vid = output_vid.fadeout(1)

# combine video and audio
output_vid.audio = None
output_path = os.path.join(TEMP_CLIPS, "new_vid.mp4")
output_vid.write_videofile(output_path)

background_vid = VideoFileClip(os.path.join(TEMP_CLIPS, "background.mp4"))
background_vid = background_vid.set_duration(output_vid.duration)
output_vid = CompositeVideoClip([background_vid, output_vid.set_position("center")])
output_aud = concatenate_audioclips(aud_clips)
# trim audio to fit video and re-add fade-out
output_aud = output_aud.subclip(0,vid_dur)
# normalize audio
output_aud = output_aud.audio_normalize()
# make a bit quieter since is pretty loud by default
output_aud = output_aud.volumex(0.6)
output_aud = output_aud.audio_fadeout(7)
# combine video and audio
output_vid.audio = output_aud
output_path = os.path.join(TEMP_CLIPS, "new_vid_backed.mp4")
output_vid.write_videofile(output_path)
