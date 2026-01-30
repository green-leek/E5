import requests
import json
import time
import random 
import os

# Register the azure app first and make sure the app has the following permissions:
# files: Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user: User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail: Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# After registration, you must click on behalf of xxx to grant administrator consent, otherwise outlook api cannot be called






calls = [
    'https://graph.microsoft.com/v1.0/users/{}/drive/root'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/users/{}/drive'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/users/{}/messages'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/users/{}/mailFolders/inbox/messageRules'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/users/{}/drive/root/children'.format(os.getenv("USER_ID")),
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/users/{}/mailFolders'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/users/{}/outlook/masterCategories'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/users/{}/?$select=displayName,skills'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/users/{}/mailFolders/Inbox/messages/delta'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/beta/users/{}/outlook/masterCategories'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/beta/users/{}/messages?$select=internetMessageHeaders&$top=1'.format(os.getenv("USER_ID")),
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]


def get_access_token(endpoint):
    access_token = os.getenv("AZURE_ACCESS_TOKEN")
    return access_token
def main():
    random.shuffle(calls)
    endpoints = calls[random.randint(0,10)::]
    num = 0
    for endpoint in endpoints:
        try:
            access_token = get_access_token(endpoint)
            session = requests.Session()
            session.headers.update({
                'Authorization': f"Bearer {access_token}"
            })
            response = session.get(endpoint)
            if response.status_code == 200:
                num += 1
                print(f'{num}th Call successful')
            else:
                print(f'Error: {response.status_code}, Message: {response.text}')
        except requests.exceptions.RequestException as e:
            print(e)
            pass
    localtime = time.asctime(time.localtime(time.time()))
    print('The end of this run is :', localtime)
    print('Number of calls is :', str(len(endpoints)))

for _ in range(3):
    main()
