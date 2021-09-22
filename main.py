import requests
import pprint
import json
import yadisk
from tqdm import tqdm


with open("token.txt", "r") as file_object:
    token = file_object.read().strip()

with open("yadisktoken.txt", "r") as myfile_object:
    yatoken = myfile_object.read().strip()

url = "https://api.vk.com/method/photos.get"
params = {"owner_id": "76119731", "album_id": "profile", "photo_sizes": 1, "extended": 1, "access_token": token, "v": "5.131"}

res = requests.get(url, params=params).json()
count = res["response"]["count"]
nameid = params["owner_id"]
yx = 0
listphotos = {}

while yx < count:
    likes = res["response"]["items"][yx]["likes"]["count"]
    listphotos[likes] = res["response"]["items"][yx]["sizes"][-1]["url"]
    yx += 1

with open('listphotos.json', 'w') as outfile:
    json.dump(listphotos, outfile)

y = yadisk.YaDisk(token=yatoken)
y.mkdir("/vkapi/id" + nameid)

headers = {
    "Accept": "application/json",
    "Authorization": "OAuth " + yatoken
}

for nameurl in tqdm(listphotos):
    params = {
        'path':"/vkapi/id" + nameid + "/" + str(nameurl) + ".jpg",
        'url': listphotos[nameurl]
    }
    url1 = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
    r = requests.post(url=url1, params=params, headers=headers)
    res = r.json()
    print(res)


