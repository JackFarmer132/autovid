import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")
AUDIO_DIR = os.path.join(BASE_DIR, "../audio")

SAT_FOOD_DIR = os.path.join(BASE_DIR, "../satisfying/food")
SAT_CLIPS_DIR = os.path.join(BASE_DIR, "../satisfying/clips")
SAT_BACKGROUND_DIR = os.path.join(BASE_DIR, "../satisfying/backgrounds")
SAT_THUMBNAIL_DIR = os.path.join(BASE_DIR, "../satisfying/thumbnails")

SAT_CLIP_PKL = os.path.join(PARENT_DIR, "satisfying/sat_clips.pkl")
SAT_AUD_PKL = os.path.join(PARENT_DIR, "satisfying/sat_audio.pkl")
SAT_BCK_PKL = os.path.join(PARENT_DIR, "satisfying/sat_backgrounds.pkl")
SAT_THUMB_PKL = os.path.join(PARENT_DIR, "satisfying/sat_thumbnails.pkl")

OUTPUT_DIR = os.path.join(BASE_DIR, "../results")
HOUR_SEGMENTS = os.path.join(OUTPUT_DIR, "hour_segments")
CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
SAT_VID_NUM_PKL = os.path.join(OUTPUT_DIR, "vid_nums.pkl")

# ANI_FOOD_DIR = os.path.join(BASE_DIR, "../animal/food")
# ANI_CLIPS_DIR = os.path.join(BASE_DIR, "../animal/clips")
# ANI_BACKGROUND_DIR = os.path.join(BASE_DIR, "../animal/backgrounds")
# ANI_THUMBNAIL_DIR = os.path.join(BASE_DIR, "../animal/thumbnails")
#
# ANI_CLIP_PKL = os.path.join(PARENT_DIR, "animal/ani_clips.pkl")
# ANI_AUD_PKL = os.path.join(PARENT_DIR, "animal/ani_audio.pkl")
# ANI_BCK_PKL = os.path.join(PARENT_DIR, "animal/ani_backgrounds.pkl")
# ANI_THUMB_PKL = os.path.join(PARENT_DIR, "animal/ani_thumbnails.pkl")
