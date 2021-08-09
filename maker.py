from conf import *
from clip_times import *

import datetime
import math
import random
import string
import pickle
from shutil import copyfile

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
def make_medium(food_dir, clips_dir, audio_dir, background_dir, thumbnail_dir,
             clip_pkl, audio_pkl, bck_pkl, thumb_pkl):
    # eat anything new
    consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          background_dir, clip_pkl, audio_pkl, thumb_pkl,
                          bck_pkl)

    # read in clips list
    with open(clip_pkl, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(audio_pkl, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(bck_pkl, 'rb') as f:
        bck_list = pickle.load(f)

    # reading from head, construct video until duration is target
    vid_clips = []
    aud_clips = []
    used_vid_packages = []
    used_aud_packages= []
    # holds current duration in seconds
    vid_dur = 0
    aud_dur = 0

    # constructs video of at least given length
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
    output_vid = CompositeVideoClip([output_vid, left_side, right_side])

    output_vid = output_vid.fadeout(1)

    # make audio
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
    output_path = os.path.join(OUTPUT_DIR, "new_vid.mp4")
    output_vid.write_videofile(output_path)

    # save file to hour_segments folder too
    copyfile(output_path, os.path.join(HOUR_SEGMENTS, "segment_" + str(datetime.datetime.today().weekday()) + ".mp4"))

    # update list and restore as pickle
    random.shuffle(vid_list)
    vid_list += used_vid_packages

    # add audio back to list
    aud_list += used_aud_packages

    # save with pickle
    with open(clip_pkl, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(audio_pkl, 'wb') as f:
        pickle.dump(aud_list, f)

    return (title_generator("medium"), output_path, make_thumbnail(thumb_pkl))


# make video with clips with target duration of 10 minutes
def make_long(food_dir, clips_dir, audio_dir, background_dir, thumbnail_dir,
             clip_pkl, audio_pkl, bck_pkl, thumb_pkl):
    # eat anything new
    consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          background_dir, clip_pkl, audio_pkl, thumb_pkl,
                          bck_pkl)

    # read in clips list
    with open(clip_pkl, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(audio_pkl, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(bck_pkl, 'rb') as f:
        bck_list = pickle.load(f)

    # audio things
    aud_dur = 0
    aud_clips = []

    # create hour-long video from the 6 segments
    segments = []
    for i in range(6):
        segment = VideoFileClip(os.path.join(HOUR_SEGMENTS, "segment_" + str(i) + ".mp4"))
        segments.append(segment)

    # shuffle vids so not as obvious
    random.shuffle(segments)

    # add fade in to all but the first segment
    for i in range(1,6):
        segments[i] = segments[i].fadein(1)

    # make video
    output_vid = concatenate_videoclips(segments, method="compose")

    # add background
    random.shuffle(bck_list)
    background_choice = bck_list[0]
    background_vid = VideoFileClip(background_choice[1])
    background_vid = background_vid.set_duration(output_vid.duration)
    background_vid = background_vid.resize(newsize=output_vid.size)
    left_side = background_vid.set_position((-1400, 0))
    right_side = background_vid.set_position((1400, 0))
    output_vid = CompositeVideoClip([output_vid, left_side, right_side])

    output_vid = output_vid.fadeout(1)

    # constructs audio backing that fits at least the vid length
    while (aud_dur < output_vid.duration):
        clip_package = aud_list.pop(0)
        # generate music clip
        aud_clip = AudioFileClip(clip_package[1])
        aud_dur += aud_clip.duration
        aud_clips.append(aud_clip)
        # add package to end of list again since needs to repeat some songs
        aud_list.append(clip_package)

    # make audio
    output_aud = concatenate_audioclips(aud_clips)
    # trim audio to fit video and re-add fade-out
    output_aud = output_aud.subclip(0,output_vid.duration)
    # normalize audio
    output_aud = output_aud.audio_normalize()
    # make a bit quieter since is pretty loud by default
    output_aud = output_aud.volumex(0.6)
    output_aud = output_aud.audio_fadeout(7)

    # combine video and audio
    output_vid.audio = output_aud
    output_path = os.path.join(OUTPUT_DIR, "new_vid.mp4")
    output_vid.write_videofile(output_path)

    return (title_generator("long"), output_path, make_thumbnail(thumb_pkl))


def make_thumbnail(thumb_pkl):
    # read in thumbnail candidates
    with open(thumb_pkl, 'rb') as f:
        candidates = pickle.load(f)

    # get which are used to prevent back-to-back thumbnail images
    left_package = candidates.pop(0)
    right_package = candidates.pop(0)
    # get images for thumbnail
    left_img = Image.open(left_package[1])
    right_img = Image.open(right_package[1])

    file_path = os.path.join(OUTPUT_DIR, "new_thumbnail.jpg")

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


# make video with clips with target duration of 10 minutes
def make_short(food_dir, clips_dir, audio_dir, background_dir, thumbnail_dir,
             clip_pkl, audio_pkl, bck_pkl, thumb_pkl):
    # eat anything new
    consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          background_dir, clip_pkl, audio_pkl, thumb_pkl,
                          bck_pkl)
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

    # constructs shorts until over 15 seconds but under 60
    while True:
        # make video over 30 seconds
        while (vid_dur < 30):
            # get front clip
            clip_package = vid_list.pop(0)
            # generate clip from package
            clip = VideoFileClip(clip_package[1])
            # add duration to runtime
            vid_dur += clip.duration
            vid_clips.append(clip)
            used_vid_packages.append(clip_package)
        # if over a minute, try again
        if (vid_dur >= 60):
            vid_dur = 0
            vid_clips = []
        # if duration is not 0, break out since successful clip
        if vid_dur:
            break

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

    # trim to phone size
    output_vid = output_vid.crop(x1=656, y1=0, x2=1264, y2=1080)
    output_vid = output_vid.fadeout(1)

    # make audio
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
    output_path = os.path.join(OUTPUT_DIR, "new_short.mp4")
    output_vid.write_videofile(output_path)

    # update list and restore as pickle
    random.shuffle(vid_list)
    vid_list += used_vid_packages

    # add audio back to list
    aud_list += used_aud_packages

    # save with pickle
    with open(clip_pkl, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(audio_pkl, 'wb') as f:
        pickle.dump(aud_list, f)

    return (title_generator("short"), output_path)


# makes random names for things since they don't matter
def random_file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# used for video titles that need to be click-baity
def title_generator(vid_type):
    prefixes = ["Simply",
                "Strangely",
                "Super",
                "Amazingly",
                "Relaxing",
                "Interesting",
                "Incredibly",
                "Extra",
                "Crazy",
                "Oddly",
                "Most",
                "Best",
                "More",
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
        "To Put Your Mind At Ease",
        "For Relaxing At Night",
        "For Taking A Break",
        "For Going To Sleep",
    ]

    # read in vid numbers
    with open(SAT_VID_NUM_PKL, 'rb') as f:
        num_dict = pickle.load(f)

    vid_num = str(num_dict[vid_type] + 1)

    if vid_type == "short":
        return random.choice(prefixes) + " Satisfying Shorts " + random.choice(suffixes) + " | #" + vid_num
    elif vid_type == "medium":
        return random.choice(prefixes) + " Satisfying Videos " + random.choice(suffixes) + " | #" + vid_num
    else:
        return "1 Hour " + random.choice(prefixes) + " Satisfying Videos " + random.choice(suffixes) + " | #" + vid_num


# goes through the food bin and sorts new clips/audio/thumbnails into correct places
def consume_new_resources(food_dir, clips_dir, audio_dir, thumbnail_dir,
                          background_dir, clip_pkl, audio_pkl, thumb_pkl,
                          bck_pkl):
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

    directories.append(background_dir)
    pickle_paths.append(bck_pkl)

    struct_maker(directories, pickle_paths)
