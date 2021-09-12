from maker import *


def setup_dirs():
    # create all directories to hold items in parent dir
    os.mkdir(FOOD_DIR)
    os.mkdir(CHOPPING_BOARD)
    os.mkdir(CLIPS_DIR)
    os.mkdir(AUDIO_DIR)
    os.mkdir(THUMBNAIL_DIR)
    os.mkdir(BACKGROUND_DIR)
    os.mkdir(PKL_DIR)
    os.mkdir(OUTPUT_DIR)
    os.mkdir(HOUR_SEGMENTS)
    os.mkdir(EXPIRED_DIR)


def setup_pickles():
    rebuild_pickles(CLIP_PKL, CLIPS_DIR)
    rebuild_pickles(BCK_PKL, BACKGROUND_DIR)
    rebuild_pickles(AUD_PKL, AUDIO_DIR)
    rebuild_pickles(THUMB_PKL, THUMBNAIL_DIR)

    # init remaining pickles
    tracked_channels_pkl = {}
    vid_num_pkl = {'short': 0, 'medium': 0, 'long': 0}

    # save pickels
    with open(TRACKED_CHANNELS_PKL, 'wb') as f:
        pickle.dump(tracked_channels_pkl, f)
    with open(VID_NUM_PKL, 'wb') as f:
        pickle.dump(vid_num_pkl, f)


def init_autovid():
    # try this since architecture could already be in place
    print("building directories...")
    try:
        setup_dirs()
    except:
        print("directories already built...")
    print("building pickles...")
    setup_pickles()


init_autovid()
