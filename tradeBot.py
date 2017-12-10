from __future__ import print_function
import httplib2
import os
import pprint
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import praw

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'GoogleSheetsTradeSecret.json'
APPLICATION_NAME = 'Trade Bot'

class Trade:

    def __init__(self,fullname,body,date,confirmed=False):

        self.fullname=fullname
        self.body=body
        self.date=datetime.datetime.fromtimestamp(int(date)).strftime('%m/$d/$Y')
        self.confirmed=confirmed

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getLastPostedTradeName(trades):

    return(trades[-1].fullname)

def writeMostRecentCompleted(file,trades):

    with open(file, 'wb') as f:
        f.write(convertUnix2DateTime(trades.comments[-1].timestamp) + ' ' + trades.comments[-1].name)

def readMostRecentCompleted(file):

    with open(file, 'rb') as f:

        for line in f:
            date = line.split(' ')[0]
            name = line.split(' ')[1]

    return [date,name]

def getTrades():

    reddit = praw.Reddit('Trade Bot')

    subreddit = reddit.subreddit("orangeandblueleauge")

    trades = reddit.submission(id='6y39j2') # Trade thread
    trades.comments.replace_more(limit=None,threshold=0)

    return trades.comments

def convertUnix2DateTime(time):
    return datetime.datetime.fromtimestamp(int(time)).strftime('%m/$d/$Y')

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1W7oJecLXON_C-cpCtPNe9sKH5gi55aq3jRQqWqH9jN4'
    rangeName = 'Sheet1!A1:B2'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    numRows = result.get('values') if result.get('values')is not None else 0
    print('{0} rows retrieved.'.format(numRows));

    getTrades()

if __name__ == '__main__':
    main()

