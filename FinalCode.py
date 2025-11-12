import json
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

    def upload_files(self, local_path, yandex_disk):
        params = {'path': yandex_disk}
        response = requests.get(f'{self.base_url}/v1/disk/resources/upload', params=params, headers=self.header)
        upload_link = response.json()['href']
        with open(local_path, 'rb') as f:
            requests.put(upload_link, files={'file': f})

"""For users"""

account = YAPI(token)
account.create_folder("PD-FPY-136")

files_to_upload = [
    {'local': f'Cats/{words}.jpg', 'remote': f'PD-FPY-136/{words}.jpg'},
    {'local': f'Cats/{words}.json', 'remote': f'PD-FPY-136/{words}.json'}
]

"""Progress bar by tqdm"""

print("Загрузка файлов на Яндекс.Диск...")
for file in tqdm(files_to_upload):
    account.upload_files(local_path = file['local'], yandex_disk = file['remote'])


