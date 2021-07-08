import datetime
import webbrowser

from conf import *
from maker import *

from Google import Create_Service
from googleapiclient.http import MediaFileUpload


def auto_upload():
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = datetime.datetime(2021, 7, 6, 15, 0, 0).isoformat() + ".000Z"

    title, upload_vid, upload_thumbnail = make_vid()

    request_body = {
        "snippet": {
            "title": title,
            "description": "Welcome to Simply Satisfying! \n\nHere we post the most satisfying content we can find! \nPlease leave a like and let us know what you thought of the video!",
            "tags": ["Entertainment"]
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": upload_date_time,
            "selfDeclareMadeForKids": False,
        },
        "notifySubscribers": False
    }

    media_file = MediaFileUpload(upload_vid)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()

    service.thumbnails().set(
        videoId=response_upload.get("id"),
        media_body=MediaFileUpload(upload_thumbnail)
    ).execute()


def manual_upload():
    make_vid()
    webbrowser.open('https://studio.youtube.com/channel/UCK5aZ60crdCqVsOttPPlkJQ/videos/upload?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D', new=2)

manual_upload()
