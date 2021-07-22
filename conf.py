import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")
AUDIO_DIR = os.path.join(BASE_DIR, "../audio")

SAT_CLIPS_DIR = os.path.join(BASE_DIR, "../satisfying/clips")
SAT_BACKGROUND_DIR = os.path.join(BASE_DIR, "../satisfying/backgrounds")
SAT_THUMBNAIL_DIR = os.path.join(BASE_DIR, "../satisfying/thumbnails")
SAT_FOOD_DIR = os.path.join(BASE_DIR, "../satisfying/food")

# SAT_CLIPS_DIR = os.path.join(BASE_DIR, "../satisfying/clips")
# SAT_BACKGROUND_DIR = os.path.join(BASE_DIR, "../satisfying/backgrounds")
# SAT_THUMBNAIL_DIR = os.path.join(BASE_DIR, "../satisfying/thumbnails")
# SAT_FOOD_DIR = os.path.join(BASE_DIR, "../satisfying/food")

OUTPUT_DIR = os.path.join(BASE_DIR, "../results")

SAT_CLIP_PKL = os.path.join(PARENT_DIR, "satisfying/sat_clips.pkl")
SAT_AUD_PKL = os.path.join(PARENT_DIR, "satisfying/sat_audio.pkl")
SAT_BCK_PKL = os.path.join(PARENT_DIR, "satisfying/sat_backgrounds.pkl")
SAT_THUMB_PKL = os.path.join(PARENT_DIR, "satisfying/sat_thumbnails.pkl")

CLIENT_SECRET_FILE = os.path.join(PARENT_DIR, "client_secret.json")
