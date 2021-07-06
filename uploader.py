import datetime

from conf import *
from maker import *

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

upload_date_time = datetime.datetime(2021, 7, 6, 15, 0, 0).isoformat() + ".000Z"

title, upload_vid, upload_thumbnail = make_vid()

request_body = {
    "snippet": {
        "title": title,
        "description": "hello world desc",
        "tags": ["Travel"]
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
