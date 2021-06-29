import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
PARENT_DIR = os.path.join(BASE_DIR, "../")
SOURCE_DIR = os.path.join(BASE_DIR, "../sources")
CLIPS_DIR = os.path.join(BASE_DIR, "../clips")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results")

SAT_CLIP_PKL = os.path.join(PARENT_DIR, "sat_clips.pkl")
