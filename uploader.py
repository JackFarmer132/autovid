# https://developers.google.com/youtube/v3/docs/videos/insert
from maker import *
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import webbrowser
import socket
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

def auto_upload():
    # configure metadata
    if "simply_satisfying" in exec_path:
        vid_description = "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #oddlysatisfying #slime #asmr"
        vid_tags = ["satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr", "slime"]
        medium_playlist = "PLxti3LVGtcTmtdqRYdbgwB84Ty7cpRGq9"
        long_playlist = "PLxti3LVGtcTnmmxJgRTfRqshZdVRnZdXq"
        long_upload_day = 6
        short_description = "#shorts\nWelcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nFrom Slime Videos to Soap Cutting, the most satisfying videos can be found here! \nPlease like and subscribe and please let us know what you thought of the video!\n\n#satisfying #oddlysatisfying #asmr"
        short_tags = ["shorts", "satisfying", "relaxing", "simplysatisfying", "oddlysatisfying", "asmr"]
        short_playlist = "PLxti3LVGtcTl501sFuIO0JoYHSKa4H6gD"
    elif "everything_animal" in exec_path:
        vid_description = "Welcome to Everything Animal! \n\nWe post the cutest and funniest animal videos that we can find! \nWhether it's cats, dogs or other amazing animals, the cutest clips can be found right here! \n Please like and subscribe and let us know what you though of the video! \n\n#animals #pets #cute #funny"
        vid_tags = ["cute", "relaxing", "funny", "animals", "asmr", "pets"]
        medium_playlist = "PL21fniLIdL1sk0QHt2xZMZ_BYWow2gN_M"
        long_playlist = "PL21fniLIdL1v6O2mLD2088-pSAz6PrJl_"
        long_upload_day = 5
        short_description = "#shorts\nWelcome to Everything Animal! \n\nWe post the cutest and funniest animal videos that we can find! \nWhether it's cats, dogs or other amazing animals, the cutest clips can be found right here! \n Please like and subscribe and let us know what you though of the video! \n\n#animals #pets #cute #funny"
        short_tags = ["shorts", "cute", "relaxing", "funny", "animals", "asmr", "pets"]
        short_playlist = "PL21fniLIdL1tX0pmBEkurzawFeOoqfrcu"

    if (datetime.datetime.today().weekday() != long_upload_day):
        print("making medium video...")
        # title, upload_vid, upload_thumbnail = make_medium()
        if "simply_satisfying" in exec_path:
            title = satisfying_title_generator("medium")
        elif "everything_animal" in exec_path:
            title = animal_title_generator("medium")
        upload_vid = os.path.join(OUTPUT_DIR, "new_vid.mp4")
        upload_thumbnail = make_thumbnail()
        youtube_upload("medium", title, upload_vid, upload_thumbnail, vid_description, vid_tags, medium_playlist, None)
    else:
        print("making long video...")
        title, upload_vid, upload_thumbnail = make_long()
        # if "simply_satisfying" in exec_path:
        #     title = satisfying_title_generator("long")
        # elif "everything_animal" in exec_path:
        #     title = animal_title_generator("long")
        # upload_vid = os.path.join(OUTPUT_DIR, "new_hour.mp4")
        # upload_thumbnail = make_thumbnail()
        youtube_upload("long", title, upload_vid, upload_thumbnail, vid_description, vid_tags, long_playlist, None)

    # get current time for scheduling uploads
    now = datetime.datetime.now()
    print("making short videos...")

    # generate 5 shorts and upload
    for i in range(5):
        # get time upload will occur (every 2 hours from now)
        time = datetime.datetime(now.year, now.month, now.day, ((now.hour + ((i+1)*2))-1), 0, 0).isoformat() + ".000Z"
        title, upload_vid = make_short()
        # upload the short
        youtube_upload("short", title, upload_vid, None, short_description, short_tags, short_playlist, time)
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
    except RefreshError as err:
        print("token expired, please re-instantiate...")
        os.remove(TOKEN)
        youtube_upload(vid_type, title, upload_vid, upload_thumbnail, description, tags, playlist_id, upload_time)


auto_upload()
