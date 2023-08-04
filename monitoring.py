from __future__ import print_function
import os.path
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SAMPLE_RANGE_NAME = 'DataBase_auto!L1:Q50'
TN = 'DataBase_auto!B2:100'

def read(file): # читает из json
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

class GoogleSheet:
    SPREADSHEET_ID = '1GGf2GYGYyVDG37FGyE43fCviecS2DNj6PR6L279cE2o'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
    
    def check_sheet(self, range):
        values = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                        range=range,
                                                        majorDimension='COLUMNS').execute()
        return values['values']
    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def deleteRangeValues(self, range):
        body = {
            "ranges": [range]
        }
        result = self.service.spreadsheets().values().batchClear(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        
def main():

    
    user = read('conf.json')['conf'][0]['user']
    tn = int(read('conf.json')['conf'][0]['tab_num'])+1
    bn = read('conf.json')['conf'][0]['bus_num']
    model = read('conf.json')['conf'][0]['bus_model']
    g_number = read('conf.json')['conf'][0]['gov_num']
    with open('tmp.txt', 'r') as tmp:
        chatp = tmp.readline()
        m = tmp.readline()
        x = tmp.readline()
        y = tmp.readline()
    gs = GoogleSheet()
    
    test_values = [
        [user, bn, chatp, m, x, y]
    ]
    test_range = f'DataBase_auto!K{3}:P{3}'
    gs.updateRangeValues(test_range, test_values)
    # print(INDEX, MAX_STR+1)