import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")

AUDIO_DIR = os.path.join(BASE_DIR, "../audio")
FOOD_DIR = os.path.join(BASE_DIR, "../food")
CLIPS_DIR = os.path.join(BASE_DIR, "../clips")
BACKGROUND_DIR = os.path.join(BASE_DIR, "../backgrounds")
THUMBNAIL_DIR = os.path.join(BASE_DIR, "../thumbnails")

CLIP_PKL = os.path.join(PARENT_DIR, "pickles/clips.pkl")
AUD_PKL = os.path.join(PARENT_DIR, "pickles/audio.pkl")
BCK_PKL = os.path.join(PARENT_DIR, "pickles/backgrounds.pkl")
THUMB_PKL = os.path.join(PARENT_DIR, "pickles/thumbnails.pkl")

OUTPUT_DIR = os.path.join(BASE_DIR, "../results")
HOUR_SEGMENTS = os.path.join(OUTPUT_DIR, "hour_segments")
CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
VID_NUM_PKL = os.path.join(OUTPUT_DIR, "vid_nums.pkl")

# ANI_FOOD_DIR = os.path.join(BASE_DIR, "../animal/food")
# ANI_CLIPS_DIR = os.path.join(BASE_DIR, "../animal/clips")
# ANI_BACKGROUND_DIR = os.path.join(BASE_DIR, "../animal/backgrounds")
# ANI_THUMBNAIL_DIR = os.path.join(BASE_DIR, "../animal/thumbnails")
#
# ANI_CLIP_PKL = os.path.join(PARENT_DIR, "animal/ani_clips.pkl")
# ANI_AUD_PKL = os.path.join(PARENT_DIR, "animal/ani_audio.pkl")
# ANI_BCK_PKL = os.path.join(PARENT_DIR, "animal/ani_backgrounds.pkl")
# ANI_THUMB_PKL = os.path.join(PARENT_DIR, "animal/ani_thumbnails.pkl")
