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
    # configure metadata
    description = "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #slime #asmr"
    tags = ["satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr", "slime"]

    # if not a sunday, upload regular 10 min vid and 3 shorts, else 1hr and shorts
    if datetime.datetime.today().weekday() != 6:
        # generate main video of 10 minutes
        title, upload_vid, upload_thumbnail = make_medium()
        # save file to hour_segments folder too
        copyfile(upload_vid, os.path.join(HOUR_SEGMENTS, "segment_" + str(datetime.datetime.today().weekday()) + ".mp4"))
        # configure playlist
        playlist_id = "PLxti3LVGtcTmtdqRYdbgwB84Ty7cpRGq9"
        # upload 10 minute vid
        youtube_upload("medium", title, upload_vid, upload_thumbnail, description, tags, playlist_id, None)
    # sunday so time for a phat hour long upload
    else:
        # generate main video of 60 minutes
        title, upload_vid, upload_thumbnail = make_long()
        # configure playlist
        playlist_id = "PLxti3LVGtcTnmmxJgRTfRqshZdVRnZdXq"
        # upload 10 minute vid
        youtube_upload("long", title, upload_vid, upload_thumbnail, description, tags, playlist_id, None)

    # configure metadata for shorts
    description = "#shorts\nWelcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #oddlysatisfying #asmr"
    tags = ["shorts", "satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr"]
    playlist_id = "PLxti3LVGtcTl501sFuIO0JoYHSKa4H6gD"

    # get current time for scheduling uploads
    now = datetime.datetime.now()

    # generate 5 shorts and upload
    for i in range(5):
        # get time upload will occur (every 3 hours from now)
        time = datetime.datetime(now.year, now.month, now.day, (((now.hour + ((i+1)*2))-1)%24), 0, 0).isoformat() + ".000Z"
        title, upload_vid = make_short()
        # upload the short
        youtube_upload("short", title, upload_vid, None, description, tags, playlist_id, time)


def youtube_upload(vid_type, title, upload_vid, upload_thumbnail, description, tags, playlist_id, time):
    # needs this so can upload vids of 60 mins
    socket.setdefaulttimeout(999999)

    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube",
              "https://www.googleapis.com/auth/youtube.force-ssl",
              "https://www.googleapis.com/auth/youtubepartner"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    request_body = {
        "snippet": {
            "categoryId": 24,
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
        },
        "notifySubscribers": True
    }

    # if being uploaded at a specific time, add this in
    if time:
        request_body["status"]["privacyStatus"] = "private"
        request_body["status"]["publishAt"] = time
    else:
        request_body["status"]["privacyStatus"] = "public"

    media_file = MediaFileUpload(upload_vid)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()

    time.sleep(10)

    # only needed if video is not a short
    if upload_thumbnail:
        service.thumbnails().set(
            videoId=response_upload.get("id"),
            media_body=MediaFileUpload(upload_thumbnail)
        ).execute()

    service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": response_upload.get("id")
                }
            }
        }
    ).execute()

    # read in vid numbers
    with open(VID_NUM_PKL, 'rb') as f:
        vid_nums = pickle.load(f)
    # increment relevant number and save back
    vid_nums[vid_type] += 1
    with open(VID_NUM_PKL, 'wb') as f:
        pickle.dump(vid_nums, f)


auto_upload()

# # for when there are errors...
# socket.setdefaulttimeout(999999)
# title = title_generator("medium")
# upload_vid = os.path.join(OUTPUT_DIR, "new_vid.mp4")
# upload_thumbnail = os.path.join(OUTPUT_DIR, "new_thumbnail.jpg")
# description = "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #slime #asmr"
# tags = ["satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr", "slime"]
# playlist_id = "PLxti3LVGtcTmtdqRYdbgwB84Ty7cpRGq9"
# youtube_upload("medium", title, upload_vid, upload_thumbnail, description, tags, playlist_id, None)
