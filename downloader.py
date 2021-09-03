from clipper import *
from pytube import Playlist, YouTube
import pickle


def download_from_targets():
    # load in information on channels currently being monitored
    with open(TRACKED_CHANNELS_PKL, 'rb') as f:
        tracked_channels = pickle.load(f)

    # query all channels for potential new videos
    for channel in tracked_channels:
        print("searching for recent upload from " + channel + "...")
        (channel_url, last_downloaded) = tracked_channels[channel]
        # create playlist object for all uploads from channel
        playlist = Playlist(channel_url)
        # get url of most recent upload
        recent_upload_url = playlist.video_urls[0]

        # if url is same as saved, no new videos so don't download again
        if not (recent_upload_url == last_downloaded):
            recent_upload = YouTube(recent_upload_url)
            print("downloading " + recent_upload.title)
            # if video is too long, ignore it
            if recent_upload.length > 4000:
                print("clip was too long, i'm not eating that smh...")
                continue
            try:
                recent_upload.streams.filter(res="1080p", mime_type="video/mp4").first().download(CHOPPING_BOARD)
            except:
                print("download failed, moving on...")
                continue
            # save this in tracked_channels to prevent redownloading
            tracked_channels[channel][1] = recent_upload_url
        else:
            print("nothing new...")

    # save new tracked channels with updated recent downloads
    with open(TRACKED_CHANNELS_PKL, 'wb') as f:
        pickle.dump(tracked_channels, f)


def auto_download():
    print("beginning downloads...")
    download_from_targets()
    print()
    clean_chopping_board()


auto_download()
