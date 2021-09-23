# Autovid
A project for automatically creating randomised videos from source clips that are of a fixed length

For proper use, once downloading requirements from the text file, several changes to the moviepy package need to be made.
Naviagate to 'venv/lib/python3.8/site-packages/moviepy/audio/fx/all/__init__.py'. Change it to the following:

------------------------------------------------------------------------------------------------------------------------------
import pkgutil

import moviepy.audio.fx as fx

from moviepy.audio.fx.audio_fadein import audio_fadein\n
from moviepy.audio.fx.audio_fadeout import audio_fadeout\n
from moviepy.audio.fx.audio_left_right import audio_left_right\n
from moviepy.audio.fx.audio_loop import audio_loop\n
from moviepy.audio.fx.audio_normalize import audio_normalize\n
from moviepy.audio.fx.volumex import volumex\n

------------------------------------------------------------------------------------------------------------------------------

Next naviagate to 'venv/lib/python3.8/site-packages/moviepy/video/fx/all/__init__.py'. Change it to the following:

------------------------------------------------------------------------------------------------------------------------------
import pkgutil

import moviepy.video.fx as fx

from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

------------------------------------------------------------------------------------------------------------------------------
This needs to be done to allow the build script to correctly convert the py files to executable binaries.

Once this is done, run 'python -m pip install --upgrade pytube' to ensure the correct version is being used.

To optimize even more, follow this: https://github.com/Zulko/moviepy/issues/1145

In case it's missing, navigate to 'venv/lib/python3.8/site-packages/moviepy/video/compositing/CompositeVideoClip.py-CompositeVideoClip', add 'from PIL import Image', and change the make_frame function:

------------------------------------------------------------------------------------------------------------------------------
def make_frame(t):
    full_w, full_h = self.bg.size
    f = self.bg.get_frame(t).astype('uint8')
    bg_im = Image.fromarray(f)
    for c in self.playing_clips(t):
        img, pos, mask, ismask = c.new_blit_on(t, f)

        x, y = pos
        w, h = c.size

        out_x = x < -w or x == full_w
        out_y = y < -h or y == full_h

        if out_x and out_y:
            continue

        pos = (int(round(min(max(-w, x), full_w))),
               int(round(min(max(-h, y), full_h))))

        paste_im = Image.fromarray(np.uint8(img))

        if mask is not None:
            mask_im = Image.fromarray(255 * mask).convert('L')
            bg_im.paste(paste_im, pos, mask_im)
        else:
            bg_im.paste(paste_im, pos)

    result_frame = np.array(bg_im)

    return result_frame.astype('uint8') if (not ismask) else result_frame
------------------------------------------------------------------------------------------------------------------------------
Next navigate to 'venv/lib/python3.8/site-packages/moviepy/video/VideoClip.py-VideoClip' and add the function 'new_blit_on'

------------------------------------------------------------------------------------------------------------------------------
def new_blit_on(self, t, picture):
    hf, wf = framesize = picture.shape[:2]

    if self.ismask and picture.max() != 0:
        return np.minimum(1, picture + self.blit_on(np.zeros(framesize), t))

    ct = t - self.start  # clip time

    # GET IMAGE AND MASK IF ANY

    img = self.get_frame(ct)
    mask = (None if (self.mask is None) else
            self.mask.get_frame(ct))
    if mask is not None:
        if (img.shape[0] != mask.shape[0]) or (img.shape[1] != mask.shape[1]):
            img = self.fill_array(img, mask.shape)
    hi, wi = img.shape[:2]

    # SET POSITION

    pos = self.pos(ct)

    # preprocess short writings of the position
    if isinstance(pos, str):
        pos = {'center': ['center', 'center'],
               'left': ['left', 'center'],
               'right': ['right', 'center'],
               'top': ['center', 'top'],
               'bottom': ['center', 'bottom']}[pos]
    else:
        pos = list(pos)

    # is the position relative (given in % of the clip's size) ?
    if self.relative_pos:
        for i, dim in enumerate([wf, hf]):
            if not isinstance(pos[i], str):
                pos[i] = dim * pos[i]

    if isinstance(pos[0], str):
        D = {'left': 0, 'center': (wf - wi) / 2, 'right': wf - wi}
        pos[0] = D[pos[0]]

    if isinstance(pos[1], str):
        D = {'top': 0, 'center': (hf - hi) / 2, 'bottom': hf - hi}
        pos[1] = D[pos[1]]

    # pos = map(int, pos)
    return img, pos, mask, self.ismask
------------------------------------------------------------------------------------------------------------------------------

Doing this will optimise the video writing process by about 2 times, so it's worth the headache of digging around in the venv
