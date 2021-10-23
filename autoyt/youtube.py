'''
Author: Jacob Howard-Parker

Functions to upload youtube videos using the official Youtube data API.

Note: Requires verified youtube channel and project in GCP. 
Note: Public uploads require your app to be audited by YouTube 
        (This includes uploading as private then changing to public)
        https://support.google.com/youtube/contact/yt_api_form?hl=en
        
'''


import os   
import datetime   
import json
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request



def build_authenticated_service(client_secret_file, api_service_name, 
                                api_version, scopes):
    # get credentials - will add in auto-refresh using pickle
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
    credentials = flow.run_local_server()

    service = build(api_service_name, api_version, credentials=credentials)
    print('Created successfully')
    return service



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
    # Needs error handling



def amend_thumbnail(service, thumbnail, video_id):
    # amend thumbnail of video
    service.thumbnails().set(videoId=video_id,
    media_body=MediaFileUpload(thumbnail)
    ).execute()
    print('Thumbnail amended!')
    # needs error handling