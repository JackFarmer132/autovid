from conf import *
from clip_times import *

import math
import random
import string
import pickle

from moviepy.editor import *
from PIL import Image

# use this if you need to remake the list if clips folder is updated
def struct_maker():
    newlist = []
    # for each clip in the folder
    for fname in os.listdir(CLIPS_DIR):
        path = os.path.join(CLIPS_DIR, fname)
        clip = VideoFileClip(path)
        # filename, filepath, duration
        entry = (fname, path, clip.duration)
        newlist.append(entry)

    # save with pickle
    pickle_path = os.path.join(PARENT_DIR, "sat_list.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(newlist, f)

# make video with clips with target duration of 10 minutes
def make_vid():
    # read in list
    pickle_path = os.path.join(PARENT_DIR, "sat_list.pkl")
    with open(pickle_path, 'rb') as f:
        clip_list = pickle.load(f)

    # reading from head, construct video until duration is 10 minutes
    vid_clips = []
    used_packages = []
    # holds current duration in seconds
    cur_dur = 0

    while (cur_dur < 600):
        # get front clip
        clip_package = clip_list.pop(0)
        # add duration to runtime
        cur_dur += clip_package[2]
        # generate clip from package
        clip = VideoFileClip(clip_package[1])
        vid_clips.append(clip)
        used_packages.append(clip_package)

    # make video
    output = concatenate_videoclips(vid_clips, method="compose")
    output_name = file_name_generator() + ".mp4"
    output_path = os.path.join(OUTPUT_DIR, output_name)
    output.write_videofile(output_path)

    # update list and restore as pickle
    random.shuffle(clip_list)

    clip_list += used_packages

    # save with pickle
    with open(pickle_path, 'wb') as f:
        pickle.dump(clip_list, f)

# makes random names for clips since they don't matter
def file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# struct_maker()
make_vid()
