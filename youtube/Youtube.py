from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from youtube.models.PrivacyStatuses import PrivacyStatuses
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os


import httplib2
import http.client
import random
import time

load_dotenv()

CLIENT_SECRETS = {
    "installed": {
        "client_id": os.getenv("youtube_client_id"),
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_secret": os.getenv("youtube_client_secret"),
        "redirect_uris": []
    }
}

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

class Youtube:
    def __init__(self):
        flow = InstalledAppFlow.from_client_config(CLIENT_SECRETS, SCOPES)
        credentials = flow.run_console()
        self.client =  build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


    def upload_video(self, file: str, title: str, description: str, keywords: list[str], categoryId: int = 22, privacyStatus: PrivacyStatuses = PrivacyStatuses.public):
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": keywords,
                "categoryId": categoryId
            },
            "status": {
                "privacyStatus": privacyStatus.value
            }
        }

        request = self.client.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
        )

        self.__resumable_upload(request)

    def __resumable_upload(self, request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print('Uploading file...')
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print('Video id "%s" was successfully uploaded.' % response['id'])
                    else:
                        exit('The upload failed with an unexpected response: %s' % response)
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                    e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = 'A retriable error occurred: %s' % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit('No longer attempting to retry.')

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print('Sleeping %f seconds and then retrying...' % sleep_seconds)
                time.sleep(sleep_seconds)
