from trimmer import *
import gc
import pickle
import multiprocessing


# make video with clips with target duration of 10 minutes
def make_medium():
    # ensure any deletions from the key directories are noted in pickle lists
    check_pickle_integrity(CLIPS_DIR, CLIP_PKL)
    check_pickle_integrity(AUDIO_DIR, AUD_PKL)
    check_pickle_integrity(THUMBNAIL_DIR, THUMB_PKL)

    # load up on new food if empty from checking
    refill_clips()

    # read in clips list
    with open(CLIP_PKL, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(AUD_PKL, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(BCK_PKL, 'rb') as f:
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
        clip = VideoFileClip(clip_package)
        # trim borders off clip
        (left_border, right_border) = get_borders(clip.get_frame(0))
        clip = clip.crop(x1=left_border, x2=clip.size[0]-right_border)
        # add duration to runtime
        vid_dur += clip.duration
        vid_clips.append(clip)
        used_vid_packages.append(clip_package)

    # # make segment for 1 hour version on weekend
    # random.shuffle(vid_clips)
    # # make segment clip for the hour long vid
    # segment_vid = concatenate_videoclips(vid_clips)
    # background_choice = bck_list[0]
    # background_vid = VideoFileClip(background_choice)
    # background_vid = background_vid.set_duration(vid_dur)
    # segment_vid = CompositeVideoClip([background_vid, segment_vid.set_position("center")])
    # segment_vid.audio = None
    # output_path = os.path.join(HOUR_SEGMENTS, "segment_" + str(datetime.datetime.today().weekday()) + ".mp4")
    # segment_vid.write_videofile(output_path, threads=12)
    # del segment_vid
    # gc.collect()

    # make actual video
    random.shuffle(vid_clips)
    output_vid = concatenate_videoclips(vid_clips)

    # get like and sub clip to put in intro
    subscribe_clip = VideoFileClip(LIKE_AND_SUBSCRIBE)
    subscribe_clip.audio = None
    subscribe_clip = subscribe_clip.fx(vfx.mask_color, color=[0, 255, 8], thr=100, s=5)
    subscribe_clip = subscribe_clip.resize(0.3).set_position(('center',0.77), relative=True)

    # get background for today's video
    random.shuffle(bck_list)
    background_choice = bck_list[0]
    background_vid = VideoFileClip(background_choice)
    background_vid = background_vid.set_duration(vid_dur)
    output_vid = CompositeVideoClip([background_vid, output_vid.set_position("center"), subscribe_clip])
    output_vid = output_vid.fadeout(1)

    # constructs audio backing that fits at least the vid length
    while (aud_dur < vid_dur):
        clip_package = aud_list.pop(0)
        # generate music clip
        aud_clip = AudioFileClip(clip_package)
        aud_dur += aud_clip.duration
        aud_clips.append(aud_clip)
        used_aud_packages.append(clip_package)

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
    output_vid.write_videofile(output_path, threads=12)

    # if new food, get rid of used clips and replace with new ones, else just append
    vid_list = update_clips(used_vid_packages, vid_list)

    # if a week has passed, shuffle to keep fresh
    if (datetime.datetime.today().weekday() == 6):
        random.shuffle(vid_list)

    # add audio back to list
    aud_list = update_pickles(used_aud_packages, AUDIO_DIR)

    # save with pickle
    with open(CLIP_PKL, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(AUD_PKL, 'wb') as f:
        pickle.dump(aud_list, f)

    # get title
    if "simply_satisfying" in exec_path:
        title = satisfying_title_generator("medium")
    elif "everything_animal" in exec_path:
        title = animal_title_generator("medium")

    return (title, output_path, make_thumbnail())


# make video with clips with target duration of 10 minutes
def make_long():
    # ensure any deletions from the key directories are noted in pickle lists
    check_pickle_integrity(CLIPS_DIR, CLIP_PKL)
    check_pickle_integrity(AUDIO_DIR, AUD_PKL)
    check_pickle_integrity(THUMBNAIL_DIR, THUMB_PKL)

    # load up on new food if empty from checking
    refill_clips()

    # read in clips list
    with open(CLIP_PKL, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(AUD_PKL, 'rb') as f:
        aud_list = pickle.load(f)

    # read in background list
    with open(BCK_PKL, 'rb') as f:
        bck_list = pickle.load(f)

    used_aud_packages= []
    segments = []

    # go through and collect the 6 videos for making the hour one
    for segment in os.listdir(HOUR_SEGMENTS):
        segments.append(VideoFileClip(os.path.join(HOUR_SEGMENTS, segment)))

    # leave it to fate to pick a good openning clip
    random.shuffle(segments)

    # get first vid and put on sub video
    subscribe_clip = VideoFileClip(LIKE_AND_SUBSCRIBE)
    subscribe_clip.audio = None
    subscribe_clip = subscribe_clip.fx(vfx.mask_color, color=[0, 255, 8], thr=100, s=5)
    subscribe_clip = subscribe_clip.resize(0.3).set_position(('center',0.77), relative=True)

    front_clip = segments.pop(0)
    front_clip = CompositeVideoClip([front_clip, subscribe_clip])
    segments = [front_clip] + segments

    # make video
    output_vid = concatenate_videoclips(segments)
    output_vid = output_vid.fadeout(1)

    # audio things
    aud_dur = 0
    aud_clips = []
    # constructs audio backing that fits at least the vid length
    while (aud_dur < output_vid.duration):
        clip_package = aud_list.pop(0)
        # generate music clip
        aud_clip = AudioFileClip(clip_package)
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
    output_path = os.path.join(OUTPUT_DIR, "new_hour.mp4")
    output_vid.write_videofile(output_path, threads=12)

    # shuffle vid clips for following week and save
    random.shuffle(vid_list)
    with open(CLIP_PKL, 'wb') as f:
        pickle.dump(vid_list, f)

    # shuffle background list and any new ones, ensuring one just used isn't used for next week
    used_background = [bck_list.pop(0)]
    bck_list = update_pickles(used_background, BACKGROUND_DIR)

    with open(BCK_PKL, 'wb') as f:
        pickle.dump(bck_list, f)

    # get title
    if "simply_satisfying" in exec_path:
        title = satisfying_title_generator("long")
    elif "everything_animal" in exec_path:
        title = animal_title_generator("long")

    return (title, output_path, make_thumbnail())


def make_thumbnail():
    # read in thumbnail candidates
    with open(THUMB_PKL, 'rb') as f:
        candidates = pickle.load(f)

    # get which are used to prevent back-to-back thumbnail images
    left_package = candidates.pop(0)
    right_package = candidates.pop(0)
    # get images for thumbnail
    left_img = Image.open(left_package)
    right_img = Image.open(right_package)

    file_path = os.path.join(OUTPUT_DIR, "new_thumbnail.jpg")

    # make white background
    background = Image.new('RGB', (960,540), color = (255, 255, 255))
    # place the pics
    background.paste(left_img, (0,0))
    background.paste(right_img, (483,0))
    background.save(file_path)

    # get any newly added thumbnails into pckl and have most recent added to end
    candidates = update_pickles([left_package, right_package], THUMBNAIL_DIR)

    with open(THUMB_PKL, 'wb') as f:
        pickle.dump(candidates, f)

    return file_path


# make video with clips with target duration of 10 minutes
def make_short():
    # ensure any deletions from the key directories are noted in pickle lists
    check_pickle_integrity(CLIPS_DIR, CLIP_PKL)
    check_pickle_integrity(AUDIO_DIR, AUD_PKL)
    check_pickle_integrity(THUMBNAIL_DIR, THUMB_PKL)

    # load up on new food if empty from checking
    refill_clips()

    # read in clips list
    with open(CLIP_PKL, 'rb') as f:
        vid_list = pickle.load(f)

    # read in audio list
    with open(AUD_PKL, 'rb') as f:
        aud_list = pickle.load(f)

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
        while (vid_dur < 15):
            # get front clip
            clip_package = vid_list.pop(0)
            # generate clip from package
            clip = VideoFileClip(clip_package)
            # add duration to runtime
            vid_dur += clip.duration
            vid_clips.append(clip)
            used_vid_packages.append(clip_package)
        # if over a minute, try again
        if (vid_dur >= 25):
            vid_dur = 0
            vid_clips = []
            vid_list += used_vid_packages
            used_vid_packages = []
        # if duration is not 0, break out since successful clip
        if vid_dur:
            break

    # make video
    output_vid = concatenate_videoclips(vid_clips)

    # constructs audio backing that fits at least the vid length
    while (aud_dur < vid_dur):
        clip_package = aud_list.pop(0)
        # generate music clip
        aud_clip = AudioFileClip(clip_package)
        aud_dur += aud_clip.duration
        aud_clips.append(aud_clip)
        used_aud_packages.append(clip_package)

    # trim to phone size
    (cur_width, _) = output_vid.size
    total_trim = cur_width - 608
    left_trim = total_trim / 2
    right_trim = left_trim + 608

    output_vid = output_vid.crop(x1=left_trim, y1=0, x2=right_trim, y2=1080)
    # get rid of last frame as can cause issues
    output_vid = output_vid.subclip(t_end=(output_vid.duration - 1.0/output_vid.fps))
    output_vid = output_vid.fadeout(0.5)

    # make audio
    output_aud = concatenate_audioclips(aud_clips)
    # trim audio to fit video and re-add fade-out
    output_aud = output_aud.subclip(0,vid_dur)
    # normalize audio
    output_aud = output_aud.audio_normalize()
    # make a bit quieter since is pretty loud by default
    output_aud = output_aud.volumex(0.6)
    output_aud = output_aud.audio_fadeout(3)

    # combine video and audio
    output_vid.audio = output_aud
    output_path = os.path.join(OUTPUT_DIR, "new_short.mp4")
    output_vid.write_videofile(output_path, threads=12)

    # append used clips to list and save
    vid_list = update_clips(used_vid_packages, vid_list)

    # add audio back to list
    aud_list += used_aud_packages

    # save with pickle
    with open(CLIP_PKL, 'wb') as f:
        pickle.dump(vid_list, f)

    with open(AUD_PKL, 'wb') as f:
        pickle.dump(aud_list, f)

    # get title
    if "simply_satisfying" in exec_path:
        title = satisfying_title_generator("short")
    elif "everything_animal" in exec_path:
        title = animal_title_generator("short")

    return (title, output_path)


# makes random names for things since they don't matter
def random_file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# used for video titles that need to be click-baity
def satisfying_title_generator(vid_type):
    prefixes = ["Simply",
                "Strangely",
                "Super",
                "Amazingly",
                "Relaxing",
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
    with open(VID_NUM_PKL, 'rb') as f:
        num_dict = pickle.load(f)

    vid_num = str(num_dict[vid_type] + 1)

    if vid_type == "short":
        return random.choice(prefixes) + " Satisfying Shorts " + random.choice(suffixes) + " | #" + vid_num
    elif vid_type == "medium":
        return random.choice(prefixes) + " Satisfying Videos " + random.choice(suffixes) + " | #" + vid_num
    else:
        return "1 HOUR " + random.choice(prefixes) + " Satisfying Videos " + random.choice(suffixes) + " | #" + vid_num


# used for video titles that need to be click-baity
def animal_title_generator(vid_type):
    exclamation= [
        "SO CUTE! ",
        "CUTE! ",
        "SO FUNNY! ",
        "AWWWW! ",
        "WOW! ",
        "AMAZING! ",
        "SUPER CUTE! ",
        "SUPER FUNNY! ",
        "",
        "ADORABLE! ",
        "SO PRECIOUS! ",
    ]

    prefixes = [
        "Cute ",
        "Funny ",
        "Amazing ",
        "Adorable ",
        "Cutest ",
        "Funniest ",
        "Furriest ",
        "Best ",
        "More ",
        "Paw-some ",
        "Prettiest ",
    ]

    subjects = [
        "Pets ",
        "Animals ",
    ]

    suffixes = [
        "That Will Make You Smile",
        "That Will Make You Laugh",
        "For Helping You Relax",
        "For Every Animal Lover",
        "For Every Pet Lover",
        "That Get Rid Of Stress",
        "To Get Rid Of Stress",
        "That Help You Relax",
        "That Help You Relax At Night",
        "That Help You Smile",
        "That Help You Laugh",
        "That Make You Warm And Fuzzy",
        "That Make You Say Awww",
    ]

    # read in vid numbers
    with open(VID_NUM_PKL, 'rb') as f:
        num_dict = pickle.load(f)

    vid_num = str(num_dict[vid_type] + 1)

    if vid_type == "short":
        return random.choice(exclamation) + random.choice(prefixes) + "Animal Shorts " + random.choice(suffixes) + " | #" + vid_num
    elif vid_type == "medium":
        return random.choice(exclamation) + random.choice(prefixes) + random.choice(subjects) + random.choice(suffixes) + " | #" + vid_num
    else:
        return random.choice(exclamation) + "1 HOUR " + random.choice(prefixes) + random.choice(subjects) + random.choice(suffixes) + " | #" + vid_num


def check_pickle_integrity(directory, pkl_path):
    # get the two lists for comparison
    with open(pkl_path, 'rb') as f:
        pkl_list = pickle.load(f)
    directory_list = os.listdir(directory)
    # build list of existing file_paths
    directory_paths = []
    for fname in directory_list:
        directory_paths.append(os.path.join(directory, fname))
    print("checking " + directory + "...")
    for pkl_item in list(pkl_list):
        if not (pkl_item in directory_paths):
            print(pkl_item + " seems to have been removed...")
            pkl_list.remove(pkl_item)
    # save potentially trimmed list back
    with open(pkl_path, 'wb') as f:
        pickle.dump(pkl_list, f)


def refill_clips():
    # read in clips list
    with open(CLIP_PKL, 'rb') as f:
        vid_list = pickle.load(f)

    food_clips = os.listdir(FOOD_DIR)
    # get number of new clips needed to get back to safe size
    missing_clips = 500 - len(vid_list)
    # while there are still food clips and they need to be used
    while (missing_clips and food_clips):
        clip = food_clips.pop(0)
        new_clip_name = random_file_name_generator() + ".mp4"
        old_clip_path = os.path.join(FOOD_DIR, clip)
        new_clip_path = os.path.join(CLIPS_DIR, new_clip_name)
        # move clip from food to clips
        os.rename(old_clip_path, new_clip_path)
        vid_list.append(new_clip_path)
        # update this to show list got bigger
        missing_clips -= 1
    with open(CLIP_PKL, 'wb') as f:
        pickle.dump(vid_list, f)


def update_clips(used_clips, pickle_clips):
    # get a list of clips in the food dir
    food_clips = os.listdir(FOOD_DIR)
    random.shuffle(food_clips)
    # only exchange clips if there are any new ones to be eaten
    if food_clips:
        for i in range(len(list(used_clips))):
            # try and get new food clip to replace one of the used ones
            try:
                new_clip = food_clips.pop(0)
                new_clip_name = random_file_name_generator() + ".mp4"
                old_clip_path = os.path.join(FOOD_DIR, new_clip)
                new_clip_path = os.path.join(CLIPS_DIR, new_clip_name)
                # get rid of a used clip
                used_clip_path = used_clips.pop(0)
                # delete this old clip
                # os.rename(used_clip_path, os.path.join(EXPIRED_DIR, (random_file_name_generator() + ".mp4")))
                os.remove(used_clip_path)
                # add new clip to this thing
                used_clips.append(new_clip_path)
                # move new clip to the clip directory
                os.rename(old_clip_path, new_clip_path)
            # otherwise not enough food to replace all used clips, so break
            except IndexError:
                break
    return pickle_clips + used_clips


def update_pickles(used_packages, directory):
    new_pickle = []
    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        # only add to new file if not used
        if not (fpath in used_packages):
            new_pickle.append(fpath)
    # add used packages to end so they aren't immediately used
    random.shuffle(new_pickle)
    new_pickle += used_packages
    return new_pickle


def rebuild_pickles(pkl_path, directory):
    new_pkl = []
    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        new_pkl.append(fpath)
    random.shuffle(new_pkl)
    with open(pkl_path, 'wb') as f:
        pickle.dump(new_pkl, f)

# rebuild_pickles(CLIP_PKL, CLIPS_DIR)
# rebuild_pickles(BCK_PKL, BACKGROUND_DIR)
# rebuild_pickles(AUD_PKL, AUDIO_DIR)
# rebuild_pickles(THUMB_PKL, THUMBNAIL_DIR)
