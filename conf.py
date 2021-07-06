import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")
SOURCE_DIR = os.path.join(BASE_DIR, "../sources")
CLIPS_DIR = os.path.join(BASE_DIR, "../clips")
AUDIO_DIR = os.path.join(BASE_DIR, "../audio")
BACKGROUND_DIR = os.path.join(BASE_DIR, "../backgrounds")
THUMBNAIL_DIR = os.path.join(BASE_DIR, "../thumbnails")
FOOD_DIR = os.path.join(BASE_DIR, "../food")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results")

SAT_CLIP_PKL = os.path.join(PARENT_DIR, "sat_clips.pkl")
SAT_AUD_PKL = os.path.join(PARENT_DIR, "sat_audio.pkl")
SAT_BCK_PKL = os.path.join(PARENT_DIR, "sat_backgrounds.pkl")
SAT_THUMB_PKL = os.path.join(PARENT_DIR, "sat_thumbnails.pkl")

CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
