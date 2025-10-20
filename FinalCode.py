import json
import requests

words = input('Enter your word for random cat: ')
response = requests.get(f'https://cataas.com/cat/says/{words}')


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

    def upload_files(self, path_to_file, path_to_disk):

        params = {
            'path': f'PD-FPY-136/{words}.jpg'
        }
        response = requests.get(f'{self.base_url}/v1/disk/resources/upload', params=params, headers=self.header)
        print(response.status_code)
        upload_link = response.json()['href']

        with open(f'Cats/{words}.jpg', 'rb') as f:
            requests.put(upload_link, files={'file': f})

        params = {
            'path': f'PD-FPY-136/{words}.json'
        }

        response = requests.get(f'{self.base_url}/v1/disk/resources/upload', params=params, headers=self.header)
        print(response.status_code)
        upload_link = response.json()['href']

        with open(f'Cats/{words}.json', 'r') as f:
            requests.put(upload_link, files={'file': f})

"""Uploading file to yandex disk. After each successful operation shows code 200 
    as files been uploaded to your account"""

with open (f'Cats/{words}.jpg', 'wb') as f:
    f.write(response.content)

with open (f'Cats/{words}.json' , 'w') as f:
    data = response.headers
    keep = ["Content-Length"]
    keep_dict = {key: data[key] for key in keep}
    json.dump(keep_dict, f)



"""Place your token for using this program"""

account = YAPI(token)
account.create_folder("PD-FPY-136")
account.upload_files(f'{words}.jpg', f"PD-FPY-136/{words}.jpg")
