from trimmer import *
import gc

def clip_source(fname, fpath):
    fname = fname[:-4]
    clip = VideoFileClip(fpath)

    prev_borders = ()
    threshold = 2
    total_dur = -0.2
    subclip_start = 0
    subclip_times = []
    # progress bar things
    seconds_per_bar = round(int(clip.duration)/100, 1)
    cur_percent = 0
    print("|", end="", flush=True)

    for i in range(int(clip.duration/2)*5):
        time = round((i*0.4), 1)
        frame = clip.get_frame(time)
        total_dur = round((total_dur+0.4),1)
        cur_percent += 0.4
        if prev_borders:
            cur_borders = get_borders(frame)
            # if borders are different, then new clip has started
            if (abs(cur_borders[0]-prev_borders[0])>threshold) and (abs(cur_borders[1]-prev_borders[1])>threshold):
                # print("at time " + str(round(total_dur,5)))
                subclip_times.append((subclip_start, (total_dur-0.6)))
                subclip_start = total_dur + 0.1
            # update
            prev_borders = cur_borders
        else:
            prev_borders = get_borders(frame)
        # update process bar if another percent of vid has been parsed
        if (cur_percent >= seconds_per_bar):
            print("=", end="", flush=True)
            cur_percent = 0
        seen_frames = 0

    # append final clip
    subclip_times.append((subclip_start, (clip.duration - 0.1)))
    print("=", end="", flush=True)
    print("|")
    print("writing new clips...")
    for i, (subclip_start, subclip_end) in enumerate(subclip_times):
        # if clip is invalid size, don't make it
        if ((subclip_end - subclip_start) >= 4) and ((subclip_end - subclip_start) <= 60):
            subclip = clip.subclip(subclip_start, subclip_end)
            subclip.audio = None
            subclip = subclip.set_fps(round(subclip.fps))
            output_path = os.path.join(FOOD_DIR, fname + "_" + str(i) + ".mp4")
            subclip.write_videofile(output_path)
        gc.collect()


def clean_chopping_board():
    # go through all new full vids and generate clips
    for fname in os.listdir(CHOPPING_BOARD):
        print("beginning parse of " + fname + "...")
        fpath = os.path.join(CHOPPING_BOARD, fname)
        if len(os.listdir(FOOD_DIR)) < 500:
            clip_source(fname, fpath)
        else:
            print("food directory full, omitting parse...")
        new_fpath = os.path.join(EXPIRED_DIR, fname)
        os.rename(fpath, new_fpath)
