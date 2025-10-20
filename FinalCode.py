import requests



"""Creating yandex disk file for saving images"""

class YAPI():
    base_url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.header = {'Authorization': f'OAuth {token}'}  # You should place your current token

    def create_folder(self, folder_name):
        params = {'path': folder_name}

        response = requests.put('self.base_url/v1/disk/resources',
                                headers=self.header,
                                params=params)
        return response.status_code

    def upload_file(self, path_to_file, path_to_disk):
        pass


"""Making input fot client to generate file and file size"""

words = input('Enter your word for random cat: ')
response = requests.get(f'https://cataas.com/cat/says/{words}')
image_size = response.headers['Content-Length']
image_size_kb = int(image_size) * 0.001
formatted_size = ('{:.3f}'.format(image_size_kb))


def write_files():
    with open(f'Cats_text/{words}.jpg', 'wb') as f:
        f.write(response.content)

    with open(f'Cats_text/{words}.json', 'w') as f:
        f.write(f'Size of the image with word {words} is {formatted_size} bytes')


"""Uploading file to yandex disk. After each successful operation shows code 200 
    as files been uploaded to your account"""


class Uploading(YAPI):
    def __init__(self, token):
        super().__init__(token)
        params = {
            'path': f'PD-FPY-136/{words}.jpg'
        }
        response = requests.get('self.base_url/v1/disk/resources', params=params, headers=self.header)
        print(response.status_code)
        upload_link = response.json()['href']

        with open(f'Cats_text/{words}.jpg', 'rb') as f:
            requests.put(upload_link, files={'file': f})

        upload_file_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'PD-FPY-136/{words}.json'
        }

        response = requests.get(upload_file_url, params=params, headers=self.header)
        print(response.status_code)
        upload_link = response.json()['href']

        with open(f'Cats_text/{words}.json', 'r') as f:
            requests.put(upload_link, files={'file': f})


"""Place your token for using this program"""

account = YAPI(token)  # place your token here to generate files in your account
account.create_folder('PD-FPY-136')  # do not change this path!
account.upload_file(f'{words}.jpg', f'PD-FPY-136/{words}.jpg')  # do not change these paths!
