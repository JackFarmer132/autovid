from conf import *
from clip_times import *

import math
import random
import string
import pickle

from moviepy.editor import *
from PIL import Image

# use this if you need to remake the list if clips folder is updated
def struct_maker(directories, pickle_paths):

    for i in range(len(directories)):
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
def make_vid(food_dir, clips_dir, audio_dir, background_dir, thumbnail_dir,
             vid_type, clip_pkl, audio_pkl, bck_pkl, thumb_pkl):
    # eat anything new
    consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          clip_pkl, audio_pkl, thumb_pkl)

    # read in clips list
    with open(clip_pkl, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(audio_pkl, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(bck_pkl, 'rb') as f:
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
    while (vid_dur < 1):
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
    # normalize audio
    output_aud = output_aud.audio_normalize()
    # make a bit quieter since is pretty loud by default
    output_aud = output_aud.volumex(0.8)
    output_aud = output_aud.audio_fadeout(7)

    # combine video and audio
    output_vid.audio = output_aud
    output_path = os.path.join(OUTPUT_DIR, "sat_new_vid.mp4")
    output_vid.write_videofile(output_path)

    # update list and restore as pickle
    random.shuffle(vid_list)
    vid_list += used_vid_packages

    # add audio back to list and shuffle
    random.shuffle(aud_list)
    aud_list += used_aud_packages

    # save with pickle
    with open(clip_pkl, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(audio_pkl, 'wb') as f:
        pickle.dump(aud_list, f)

    return (title_generator(vid_type), output_path, make_thumbnail(thumb_pkl, vid_type))


def make_thumbnail(thumb_pkl, vid_type):
    # read in thumbnail candidates
    with open(thumb_pkl, 'rb') as f:
        candidates = pickle.load(f)

    # get which are used to prevent back-to-back thumbnail images
    left_package = candidates.pop(0)
    right_package = candidates.pop(0)
    # get images for thumbnail
    left_img = Image.open(left_package[1])
    right_img = Image.open(right_package[1])

    file_path = os.path.join(OUTPUT_DIR, (vid_type + "_new_thumbnail.jpg"))

    # make white background
    background = Image.new('RGB', (960,540), color = (255, 255, 255))
    # place the pics
    background.paste(left_img, (0,0))
    background.paste(right_img, (483,0))
    background.save(file_path)

    # shuffle list and store again
    random.shuffle(candidates)
    candidates.append(left_package)
    candidates.append(right_package)

    with open(thumb_pkl, 'wb') as f:
        pickle.dump(candidates, f)

    return file_path


# makes random names for things since they don't matter
def random_file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# used for video titles that need to be click-baity
def title_generator(vid_type):
    if vid_type == "sat":
        prefixes = ["Simply",
                    "Strangely",
                    "Super",
                    "Amazingly",
                    "Relaxing",
                    "Interesting",
                    "Incredibly",
                    "Extra",
                    "Crazy",
        ]
        suffixes = [
            "That Will Help You Relax",
            "That Will Help You Sleep",
            "That Will Calm Your Nerves",
            "That Will Help With Anxiety",
            "That Make You Fall Asleep",
            "That Will Relax and Calm You Before Sleep",
            "That Get Rid Of Stress",
            "That Will Make You Calm",
            "To Calm Your Nerves",
            "To Help You Sleep",
            "To Make You Tired",
            "To Relax In Bed",
            "To Watch To Relax",
            "To Fall Asleep To",
            "To Watch Before Bed",
            "For Relaxing At Night",
            "For Taking A Break",
            "For Going To Sleep",
        ]

        # get the number video this is
        f = open(os.path.join(OUTPUT_DIR, (vid_type + "_cheating.txt")), "r")
        vid_num = str(int(f.read()) + 1)

        return random.choice(prefixes) + " Satisfying Videos " + random.choice(suffixes) + " | #" + vid_num
    return "SOMETHIG WENT WRONG lmao"


# goes through the food bin and sorts new clips/audio/thumbnails into correct places
def consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          clip_pkl, audio_pkl, thumb_pkl):
    new_clip = False
    new_audio = False
    new_thumbnail = False
    directories = []
    pickle_paths = []
    # for each file in the food directory
    for fname in os.listdir(food_dir):
        # get path
        fname_path = os.path.join(food_dir, fname)
        # if file is video, is a new clip
        if (".mp4" in fname):
            new_clip = True
            new_fname = random_file_name_generator() + ".mp4"
            new_home = os.path.join(clips_dir, new_fname)
        # if audio
        elif (".mp3" in fname):
            new_audio = True
            new_fname = random_file_name_generator() + ".mp3"
            new_home = os.path.join(audio_dir, new_fname)
        # if thumbnail
        elif (".jpg" in fname):
            new_thumbnail = True
            new_fname = random_file_name_generator() + ".jpg"
            new_home = os.path.join(thumbnail_dir, new_fname)
        # otherwise is unrecognised and leavve it be
        else:
            continue
        # move the target file with new name and location
        os.rename(fname_path, new_home)
    # update pickle lists if new things were added
    if new_clip:
        directories.append(clips_dir)
        pickle_paths.append(clip_pkl)
    if new_audio:
        directories.append(audio_dir)
        pickle_paths.append(audio_pkl)
    if new_thumbnail:
        directories.append(thumbnail_dir)
        pickle_paths.append(thumb_pkl)

    struct_maker(directories, pickle_paths)
