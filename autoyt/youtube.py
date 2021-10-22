import os   
import datetime   
import json
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

#todo - create and verify youtube account (description in vid above) (DONE)
#jacob.autoyt@gmail.com
#todo - fill out necessary audit form (description in vid above)
#https://support.google.com/youtube/contact/yt_api_form?hl=en

def build_authenticated_service(client_secret_file, api_service_name, api_version, scopes):
    # get credentials - will add in auto-refresh using pickle
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
    credentials = flow.run_local_server()

    service = build(api_service_name, api_version, credentials=credentials)
    print('Created successfully')
    return service
    #check if still valid - if not refresh - how?


def upload_video(service, file, request_body):
    mediaFile = MediaFileUpload(file)
    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()
    print(response_upload.get('id'))
    print(response_upload.get('channelId'))
    print(response_upload.get('channelTitle'))
    print(response_upload.get('kind'))

    return response_upload.get('id')
    # should contain video uploading and monitoring of response

def amend_thumbnail(service, thumbnail, video_id):
    # amend thumbnail of video
    service.thumbnails().set(videoId=video_id,
    media_body=MediaFileUpload(thumbnail)
    ).execute()
    print('Thumbnail amended!')
    #get response and try again?


# add exceptions blah  blah blah


if __name__ == "__main__":
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    service = build_authenticated_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)





    request_body = {
        'snippet': {

            'categoryI': 19,
            'title': 'Test_title',
            'description': 'Test description',
            'tags': ['test_tag', 'reddit', 'askreddit']
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False,
        'onBehalfOfContentOwnerChannel': "AutoReddit"
        
    }



    #response_id = upload_video(service, 'test_movie.mp4', request_body)