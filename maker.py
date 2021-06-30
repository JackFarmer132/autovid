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
    directories = [CLIPS_DIR, AUDIO_DIR, BACKGROUND_DIR]
    pickle_paths = [SAT_CLIP_PKL, SAT_AUD_PKL, SAT_BCK_PKL]

    for i in range(3):
        newlist = []
        directory = directories[i]
        pkl_path = pickle_paths[i]

        # for each clip in the folder
        for fname in os.listdir(directory):
            path = os.path.join(directory, fname)
            # filename, filepath
            entry = (fname, path)
            newlist.append(entry)
        # shuffle, baby!
        random.shuffle(newlist)
        # save with pickle
        with open(pkl_path, 'wb') as f:
            pickle.dump(newlist, f)


# make video with clips with target duration of 10 minutes
def make_vid():
    # read in clips list
    with open(SAT_CLIP_PKL, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(SAT_AUD_PKL, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(SAT_BCK_PKL, 'rb') as f:
        bck_list = pickle.load(f)

    # reading from head, construct video until duration is 10 minutes
    vid_clips = []
    aud_clips = []
    used_vid_packages = []
    used_aud_packages= []
    # holds current duration in seconds
    vid_dur = 0
    aud_dur = 0

    # constructs video of at least 10 minutes
    while (vid_dur < 600):
        # get front clip
        clip_package = vid_list.pop(0)
        # generate clip from package
        clip = VideoFileClip(clip_package[1])
        # add duration to runtime
        vid_dur += clip.duration
        vid_clips.append(clip)
        used_vid_packages.append(clip_package)

    # make video
    output_vid = concatenate_videoclips(vid_clips, method="compose")

    # constructs audio backing that fits at least the vid length
    while (aud_dur < vid_dur):
        clip_package = aud_list.pop(0)
        # generate music clip
        aud_clip = AudioFileClip(clip_package[1])
        aud_dur += aud_clip.duration
        aud_clips.append(aud_clip)
        used_aud_packages.append(clip_package)


    # get background
    random.shuffle(bck_list)
    background_choice = bck_list[0]
    background_vid = VideoFileClip(background_choice[1])
    background_vid = background_vid.set_duration(vid_dur)
    background_vid = background_vid.resize(newsize=output_vid.size)
    left_side = background_vid.set_position((-1400, 0))
    right_side = background_vid.set_position((1400, 0))

    # overlay videos and add fadeout
    output_vid = CompositeVideoClip([output_vid, left_side, right_side])
    output_vid = output_vid.fadeout(1)

    # make audio
    output_aud = concatenate_audioclips(aud_clips)
    # trim audio to fit video and re-add fade-out
    output_aud = output_aud.subclip(0,vid_dur)
    output_aud = output_aud.audio_fadeout(7)

    # combine video and audio
    output_vid.audio = output_aud
    output_name = "sat_" + file_name_generator() + ".mp4"
    output_path = os.path.join(OUTPUT_DIR, output_name)
    output_vid.write_videofile(output_path)

    # update list and restore as pickle
    random.shuffle(vid_list)
    vid_list += used_vid_packages

    # add audio back to list and shuffle
    aud_list += used_aud_packages
    random.shuffle(aud_list)

    # save with pickle
    with open(SAT_CLIP_PKL, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(SAT_AUD_PKL, 'wb') as f:
        pickle.dump(aud_list, f)


# makes random names for clips since they don't matter
def file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# struct_maker()
make_vid()
