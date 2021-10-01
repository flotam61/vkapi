import requests
import json
import yadisk
from tqdm import tqdm

# 76119731

vktoken = input("Введите токен vkapi ")
yatoken = input("Введите токен Яндекс диска, куда хотите загрузить фотографии ")
idvk = input("Введите id страницы в вконтакте ")

url = "https://api.vk.com/method/photos.get"
params = {"owner_id": idvk, "album_id": "profile", "photo_sizes": 1, "extended": 1, "count": 5, "access_token": vktoken, "v": "5.131"}

res = requests.get(url, params=params).json()
count = params["count"]
nameid = params["owner_id"]
yx = 0
listphotos = {}
savejson = []

while yx < count:
    likes = str(res["response"]["items"][yx]["likes"]["count"]) + ".jpg"
    listphotos[likes] = res["response"]["items"][yx]["sizes"][-1]["url"]
    savejson.append({"file_name": likes, "size": res["response"]["items"][yx]["sizes"][-1]["type"]})
    yx += 1

with open('savejson.json', 'w') as outfile:
    json.dump(savejson, outfile)

y = yadisk.YaDisk(token=yatoken)
y.mkdir("/vkapi/id" + nameid)

headers = {
    "Accept": "application/json",
    "Authorization": "OAuth " + yatoken
}

for nameurl in tqdm(listphotos):
    params = {
        'path':"/vkapi/id" + nameid + "/" + str(nameurl),
        'url': listphotos[nameurl]
    }
    url1 = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
    r = requests.post(url=url1, params=params, headers=headers)
    res = r.json()
    print(res)


