import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")
FOOD_DIR = os.path.join(BASE_DIR, "../food")

CLIPS_DIR = os.path.join(BASE_DIR, "../clips")
AUDIO_DIR = os.path.join(BASE_DIR, "../audio")
THUMBNAIL_DIR = os.path.join(BASE_DIR, "../thumbnails")
BACKGROUND_DIR = os.path.join(BASE_DIR, "../backgrounds")

CLIP_PKL = os.path.join(PARENT_DIR, "pickles/clips.pkl")
AUD_PKL = os.path.join(PARENT_DIR, "pickles/audio.pkl")
THUMB_PKL = os.path.join(PARENT_DIR, "pickles/thumbnails.pkl")
BCK_PKL = os.path.join(PARENT_DIR, "pickles/backgrounds.pkl")

OUTPUT_DIR = os.path.join(BASE_DIR, "../results")
HOUR_SEGMENTS = os.path.join(OUTPUT_DIR, "hour_segments")
CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
VID_NUM_PKL = os.path.join(OUTPUT_DIR, "vid_nums.pkl")

TEMP_CLIPS = os.path.join(BASE_DIR, "../temp_clips")
