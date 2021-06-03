#Enable Google Drive
#needs credentials.json if used for the first use or token.json if used for recurrent uses
#import libraries
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
#Import different libraries
import io
from googleapiclient.http import MediaIoBaseDownload
from typing import Tuple
from datetime import date
import ee

def surveyyear_to_range(year: int,satellitename: str) -> Tuple[str, str]:
    if satellitename == "S2":
        if 2012<=year<=2015:
            start_date = '2015-06-24'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    elif satellitename == "nl":
        if year == 2012:
            start_date = '2012-01-01'
            end_date = '2013-01-01'
        elif year == 2013:
            start_date = '2013-01-01'
            end_date = '2014-01-01'
        elif year == 2014:
            start_date = '2014-01-01'
            end_date = '2015-01-01'
        elif year == 2015:
            start_date = '2015-01-01'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    return start_date, end_date

def point_to_box_coords(aoi: ee.Geometry,dimensionradius: int) -> list:
    """gives out 4 coordinates to create a rectangular-shaped image with the width and height of the dimensionradius times 2.

    Args:
        aoi (Geometry): Area of interest, becomes the centroid of the image
        dimensionradius (int): equals half the width of the image

    Returns:
        list: 4 coordinates of lon,lat to create an image
    """
    buffer = aoi.buffer(dimensionradius)
    box = buffer.bounds()
    return box.coordinates().getInfo()

def download_file(file_id, filename):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print('Download done')

def export(i):


    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',['https://www.googleapis.com/auth/drive'])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    # Call the Drive v3 API
    dirpath = '../data'
    os.makedirs(dirpath,exist_ok=True)
    while len([name for name in os.listdir(dirpath)]) != i:
        results = service.files().list(q="mimeType='image/tiff'",spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=None).execute()
        items = results.get('files', [])
        for item in items:
            file_id = item.get('id')
            filename = item.get('name')
            print("Download " + str(filename))
            download_file(item['id'], item['name'])
            service.files().delete(fileId=file_id).execute()
            os.replace(filename,dirpath + "/" + filename)
            print(str(len([name for name in os.listdir(dirpath)]))+ "/" + str(len(df)))