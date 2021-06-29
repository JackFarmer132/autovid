from conf import *
from clip_times import *

import math
import random
import string

from moviepy.editor import *
from PIL import Image

# runs the ripper using the given clip times to generate all clips from input
def rip_looper():
    # for each source video
    type = ""
    for source in clip_times:
        # get list of timings for clipping
        for ct in clip_times[source]:
            if ((ct == "VIDEO") or (ct == "AUDIO")):
                type = ct
                continue
            source_name = source
            start_time = ct[0]
            end_time = ct[1]
            ripper(source_name, start_time, end_time, type)

def ripper(source_name, clip_start, clip_end, type):
    # path of the selected mp4 video
    source_path = os.path.join(SOURCE_DIR, source_name)
    clip = VideoFileClip(source_path)
    subclip = clip.subclip(clip_start, clip_end)

    # if vid, save as mp4 and remove audio
    if (type == "VIDEO"):
        # generate name of output file
        fname = file_name_generator() + ".mp4"
        clip_path = os.path.join(CLIPS_DIR, fname)
        subclip = subclip.set_audio(None)
        subclip.write_videofile(clip_path)
    # otherwise clipping audio so mp3 and keep audio
    else:
        # generate name of output file
        fname = file_name_generator() + ".mp3"
        clip_path = os.path.join(AUDIO_DIR, fname)
        subclip_audio = subclip.audio
        subclip_audio = subclip_audio.audio_fadeout(7)
        subclip_audio.write_audiofile(clip_path)

# makes random names for clips since they don't matter
def file_name_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

ripper("sample1.mp4", 0, 20, "AUDIO")
