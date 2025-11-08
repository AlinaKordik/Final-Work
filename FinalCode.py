import json
import time
from tqdm import tqdm
import requests


words = input('Enter your word for random cat: ')
token = input('Enter your token to upload files to your Yandex Disk: ')
response = requests.get(f'https://cataas.com/cat/says/{words}')


with open(f'Cats/{words}.jpg', 'wb') as f:
    f.write(response.content)

with open(f'Cats/{words}.json', 'w') as f:
    data = response.headers
    keep = ["Content-Length"]
    keep_dict = {key: data[key] for key in keep}
    json.dump(keep_dict, f)


"""Creating yandex disk file for saving images"""


class YAPI:
    base_url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.header = {'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        params = {'path': folder_name}

        response = requests.put(f'{self.base_url}/v1/disk/resources',
                                headers=self.header,
                                params=params)
        return response.status_code

    def upload_files(self, local_path, yandex_disk, local_json, yandex_json):
        params = {'path': yandex_disk}
        response = requests.get(f'{self.base_url}/v1/disk/resources/upload', params=params, headers=self.header)
        # print(response.status_code) --Checking response
        upload_link = response.json()['href']

        with open(local_path, 'rb') as f:
            requests.put(upload_link, files={'file': f})

        params = {'path': yandex_json}

        response = requests.get(f'{self.base_url}/v1/disk/resources/upload', params=params, headers=self.header)
        # print(response.status_code) --Checking response
        upload_link = response.json()['href']

        with open(local_json, 'r') as f:
            requests.put(upload_link, files={'file': f})

"""Progress bar by tqdm"""

links = ['https://cloud-api.yandex.net/v1/disk/resources', 'https://cloud-api.yandex.net/v1/disk/resources/upload']
for link in tqdm(links):
    time.sleep(2)


"""For users"""

account = YAPI(token)
account.create_folder("PD-FPY-136")
account.upload_files(f'Cats/{words}.jpg', f'PD-FPY-136/{words}.jpg', f'Cats/{words}.json', f'PD-FPY-136/{words}.json' )


