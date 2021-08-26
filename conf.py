import os
import sys


PARENT_DIR = "/mnt/h/Personal/projects/autovid"
BASE_DIR = os.path.join(PARENT_DIR, "autovid")
FOOD_DIR = os.path.join(PARENT_DIR, "food")
CHOPPING_BOARD = os.path.join(PARENT_DIR, "chopping_board")

CLIPS_DIR = os.path.join(PARENT_DIR, "clips")
AUDIO_DIR = os.path.join(PARENT_DIR, "audio")
THUMBNAIL_DIR = os.path.join(PARENT_DIR, "thumbnails")
BACKGROUND_DIR = os.path.join(PARENT_DIR, "backgrounds")

CLIP_PKL = os.path.join(PARENT_DIR, "pickles/clips.pkl")
AUD_PKL = os.path.join(PARENT_DIR, "pickles/audio.pkl")
THUMB_PKL = os.path.join(PARENT_DIR, "pickles/thumbnails.pkl")
BCK_PKL = os.path.join(PARENT_DIR, "pickles/backgrounds.pkl")

OUTPUT_DIR = os.path.join(PARENT_DIR, "results")
HOUR_SEGMENTS = os.path.join(OUTPUT_DIR, "hour_segments")
CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
VID_NUM_PKL = os.path.join(OUTPUT_DIR, "vid_nums.pkl")

EXPIRED_DIR = os.path.join(PARENT_DIR, "expired")
TOKEN = os.path.join(BASE_DIR, "token_youtube_v3.pickle")
