import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
# Define your app's authorization scopes.
# When modifying these scopes, delete the file token.json, if it exists.
SCOPES = ['https://www.googleapis.com/auth/chat']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
# print(creds.)

def main():
    '''
    Authenticates with Chat API via user credentials,
    then creates a text message in a Chat space.
    '''



    # Build a service endpoint for Chat API.
    chat = build('chat', 'v1', credentials=creds)

    # Use the service endpoint to call Chat API.
    result = chat.spaces().list(

          # An optional filter that returns named spaces or unnamed group chats,
          # but not direct messages (DMs).
          filter='spaceType = "SPACE" OR spaceType = "GROUP_CHAT"'

      ).execute()
    # Prints details about the created membership.
    print(result)

if __name__ == '__main__':
    main()