# https://developers.google.com/youtube/v3/docs/videos/insert
from maker import *
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import webbrowser
import socket
from googleapiclient.errors import HttpError

def auto_upload():
    # configure metadata
    description = "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #slime #asmr"
    tags = ["satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr", "slime"]

    # if not a sunday, upload regular 10 min vid and 3 shorts, else 1hr and shorts
    if datetime.datetime.today().weekday() != 6:
        print("making medium video...")
        playlist_id = "PLxti3LVGtcTmtdqRYdbgwB84Ty7cpRGq9"
        title, upload_vid, upload_thumbnail = make_medium()
        # title = title_generator("medium")
        # upload_vid = os.path.join(OUTPUT_DIR, "new_vid.mp4")
        # upload_thumbnail = make_thumbnail()
        youtube_upload("medium", title, upload_vid, upload_thumbnail, description, tags, playlist_id, None)
    else:
        print("making long video...")
        playlist_id = "PLxti3LVGtcTnmmxJgRTfRqshZdVRnZdXq"
        title, upload_vid, upload_thumbnail = make_long()
        # title = title_generator("long")
        # upload_vid = os.path.join(OUTPUT_DIR, "new_hour.mp4")
        # upload_thumbnail = make_thumbnail()
        youtube_upload("long", title, upload_vid, upload_thumbnail, description, tags, playlist_id, None)

    # configure metadata for shorts
    description = "#shorts\nWelcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #oddlysatisfying #asmr"
    tags = ["shorts", "satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr"]
    playlist_id = "PLxti3LVGtcTl501sFuIO0JoYHSKa4H6gD"

    # get current time for scheduling uploads
    now = datetime.datetime.now()
    print("making short videos...")

    # generate 5 shorts and upload
    for i in range(5):
        # get time upload will occur (every 2 hours from now)
        time = datetime.datetime(now.year, now.month, now.day, ((now.hour + ((i+1)*2))-1), 0, 0).isoformat() + ".000Z"
        title, upload_vid = make_short()
        # upload the short
        youtube_upload("short", title, upload_vid, None, description, tags, playlist_id, time)
    print("done!")


def youtube_upload(vid_type, title, upload_vid, upload_thumbnail, description, tags, playlist_id, upload_time):
    # needs this so can upload vids of 60 mins
    socket.setdefaulttimeout(999999)

    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube",
              "https://www.googleapis.com/auth/youtube.force-ssl",
              "https://www.googleapis.com/auth/youtubepartner"]
    try:
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
        if upload_time:
            request_body["status"]["privacyStatus"] = "private"
            request_body["status"]["publishAt"] = upload_time
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
    except HttpError as err:
        # if token is expired, delete it and do this again to remake it
        if err.resp.status == 400:
            os.remove(TOKEN)
            youtube_upload(vid_type, title, upload_vid, upload_thumbnail, description, tags, playlist_id, upload_time)
        # otherwise something else went wrong so stop
        else:
            sys.exit(err)


auto_upload()
