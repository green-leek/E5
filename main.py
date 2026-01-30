import requests
import json
import time
import random 
import subprocess

# Register the azure app first and make sure the app has the following permissions:
# files: Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user: User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail: Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# After registration, you must click on behalf of xxx to grant administrator consent, otherwise outlook api cannot be called






calls = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/beta/me/outlook/masterCategories',
    'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]


def get_access_token(endpoint):
    access_token = subprocess.check_output(
        ["az", "account", "get-access-token", "--query", "accessToken", "--resource-type", "ms-graph", "-o", "tsv"]
    ).strip().decode('utf-8')
    response = requests.post(endpoint, headers={"Authorization": f"Bearer {access_token}"})
    return response.json()

def main():
    random.shuffle(calls)
    endpoints = calls[random.randint(0,10)::]
    num = 0
    for endpoint in endpoints:
        try:
            access_token = get_access_token(endpoint)
            session = requests.Session()
            session.headers.update({
                'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json'
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
