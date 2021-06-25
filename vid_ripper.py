from conf import *
import math
from moviepy.editor import VideoFileClip as vfc
from PIL import Image

#path of the selected mp4 video
source_path = os.path.join(SOURCE_DIR, "sample1.mp4")

clip = vfc(source_path)

duration = math.floor(clip.duration)

for i, frame in enumerate(clip.iter_frames()):
    new_img = Image.fromarray(frame)
    output_path = os.path.join(OUTPUT_DIR, f"{i}.jpg")
    new_img.save(output_path)

#destination for clips
# dest_path = CLIPS_DIR
# os.makedirs(dest_path, exist_ok=True)
#
# clip = VideoFileClip(source_path)
#
# print(clip.reader.fps)
# print(clip.reader.nframes)
#
# #turning frames into images
# duration = clip.reader.duration
# duration = int(duration) + 1
#
# for i in range(0, 10):
#     print(f"frame at {i} seconds")
#     frame = clip.get_frame(int(i))
#     new_img = Image.fromarray(frame)
#     new_img_filepath = os.path.join(dest_path, f"img{i}.jpg")
#     new_img.save(new_img_filepath)
