# https://developers.google.com/youtube/v3/docs/videos/insert

import datetime
import webbrowser
import keyboard
import time
import socket
import sys

from conf import *
from maker import *

from Google import Create_Service
from googleapiclient.http import MediaFileUpload


def auto_upload():
    # needs this so can upload vids of 10 mins
    socket.setdefaulttimeout(30000)

    vid_type = "ani"

    if vid_type == sat:
        food_dir = SAT_FOOD_DIR
        clips_dir = SAT_CLIPS_DIR
        audio_dir = AUDIO_DIR
        background_dir = SAT_BACKGROUND_DIR
        thumbnail_dir = SAT_THUMBNAIL_DIR

        clip_pkl = SAT_CLIP_PKL
        audio_pkl = SAT_AUD_PKL
        bck_pkl = SAT_BCK_PKL
        thumb_pkl = SAT_THUMB_PKL
    elif vid_type == "ani":
        print("easter egg")
    else:
        print("invalid form of video requested, please try again")
        sys.exit()


    title, upload_vid, upload_thumbnail = make_vid(food_dir, clips_dir, audio_dir,
                                                   background_dir, thumbnail_dir,
                                                   vid_type, clip_pkl, audio_pkl,
                                                   bck_pkl, thumb_pkl)

    print(title)
    print(upload_vid)
    print(upload_thumbnail)

    # API_NAME = "youtube"
    # API_VERSION = "v3"
    # SCOPES = ["https://www.googleapis.com/auth/youtube",
    #           "https://www.googleapis.com/auth/youtube.force-ssl",
    #           "https://www.googleapis.com/auth/youtubepartner"]
    #
    # service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    #
    # playlist_id = "PLxti3LVGtcTmeO6u8BVAb61vw2yYGhDF9"
    #
    # request_body = {
    #     "snippet": {
    #         "categoryId": 24,
    #         "title": title,
    #         "description": "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nPlease leave a like and let us know what you thought of the video!",
    #         "tags": ["Satisfaction", "Relaxing", "Stress-Reducing"]
    #     },
    #     "status": {
    #         "privacyStatus": "public",
    #         "selfDeclareMadeForKids": True,
    #     },
    #     "notifySubscribers": True
    # }
    #
    # media_file = MediaFileUpload(upload_vid)
    #
    # response_upload = service.videos().insert(
    #     part='snippet,status',
    #     body=request_body,
    #     media_body=media_file
    # ).execute()
    #
    # service.thumbnails().set(
    #     videoId=response_upload.get("id"),
    #     media_body=MediaFileUpload(upload_thumbnail)
    # ).execute()
    #
    # service.playlistItems().insert(
    #     part="snippet",
    #     body={
    #         "snippet": {
    #             "playlistId": playlist_id,
    #             "resourceId": {
    #                 "kind": "youtube#video",
    #                 "videoId": response_upload.get("id")
    #             }
    #         }
    #     }
    # ).execute()

    # if all has gone well, then update the vid number so next one is correct
    # get the number video this is
    f = open(os.path.join(OUTPUT_DIR, (vid_type + "_cheating.txt")), "r")
    vid_num = str(int(f.read()) + 1)
    f = open(os.path.join(OUTPUT_DIR, (vid_type + "_cheating.txt")), "w")
    f.write(vid_num)

auto_upload()
