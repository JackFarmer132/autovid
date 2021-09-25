import os
import sys


exec_path = os.getcwd()
if "simply_satisfying" in exec_path:
    PARENT_DIR = "/mnt/h/Personal/projects/simply_satisfying"
elif "everything_animal" in exec_path:
    PARENT_DIR = "/mnt/h/Personal/projects/everything_animal"
BASE_DIR = os.path.join(PARENT_DIR, "autovid")
FOOD_DIR = os.path.join(PARENT_DIR, "food")
CHOPPING_BOARD = os.path.join(PARENT_DIR, "chopping_board")

CLIPS_DIR = os.path.join(PARENT_DIR, "clips")
AUDIO_DIR = os.path.join(PARENT_DIR, "audio")
THUMBNAIL_DIR = os.path.join(PARENT_DIR, "thumbnails")
BACKGROUND_DIR = os.path.join(PARENT_DIR, "backgrounds")
PKL_DIR = os.path.join(PARENT_DIR, "pickles")
UTILS_DIR = os.path.join(PARENT_DIR, "utils")

CLIP_PKL = os.path.join(PKL_DIR, "clips.pkl")
AUD_PKL = os.path.join(PKL_DIR, "audio.pkl")
THUMB_PKL = os.path.join(PKL_DIR, "thumbnails.pkl")
BCK_PKL = os.path.join(PKL_DIR, "backgrounds.pkl")
TRACKED_CHANNELS_PKL = os.path.join(PKL_DIR, "tracked_channels.pkl")

OUTPUT_DIR = os.path.join(PARENT_DIR, "results")
HOUR_SEGMENTS = os.path.join(OUTPUT_DIR, "hour_segments")
CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
VID_NUM_PKL = os.path.join(OUTPUT_DIR, "vid_nums.pkl")

LIKE_AND_SUBSCRIBE = os.path.join(UTILS_DIR, "like_and_subscribe.mp4")
BLACK_BACKGROUND = os.path.join(UTILS_DIR, "black_background.mp4")

EXPIRED_DIR = os.path.join(PARENT_DIR, "expired")
TOKEN = os.path.join(PARENT_DIR, "token_youtube_v3.pickle")
