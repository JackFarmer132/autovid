from conf import *
import math
from moviepy.editor import *
from PIL import Image
from moviepy.video.fx.all import crop

try:
    # parameters: enter the source file name, beginning of clip and end of clip
    source_name = str(sys.argv[1]) + ".mp4"
    clip_start = int(sys.argv[2])
    clip_end = int(sys.argv[3])

    #path of the selected mp4 video
    source_path = os.path.join(SOURCE_DIR, source_name)
    clip_path = os.path.join(CLIPS_DIR, "clip.mp4")

    clip = VideoFileClip(source_path)
    subclip = clip.subclip(clip_start, clip_end)
    subclip.write_videofile(clip_path)
except:
    print("you probs forgot to add the params for clipping")
