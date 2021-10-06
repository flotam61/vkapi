import requests
import json
from tqdm import tqdm

# 76119731
# 457239031
# 125131457

def vkphoto():
    print("Функция загружает на яДиск необходимое кол-во фото с аватарок vk данного ID")
    print("И сохраняет список файлов в формате <Имя : размер> в файл <savejson.json>")
    vktoken = input("Введите token VK ")
    global idvk
    idvk = input("Введите ID пользователя vk ")
    countphotos = int(input("Сколько фотографий загрузить? "))

    url = "https://api.vk.com/method/photos.get"
    params = {"owner_id": idvk, "album_id": "profile", "photo_sizes": 1, "extended": 1, "count": countphotos,
              "access_token": vktoken, "v": "5.131"}
    resvk = requests.get(url, params=params).json()

    if countphotos > resvk["response"]["count"]:
        print("Столько фото нет, максимум:", resvk["response"]["count"])
        return vkphoto()
    else:
        global listphotos
        listphotos = {}
        savejson = []

        c = 0
        v = 0
        for y in resvk["response"]["items"][0]["sizes"]:
            v += 1
            if y["height"] > c:
                c = y["height"]

        y = 0
        for item in resvk["response"]["items"]:
            if str(resvk["response"]["items"][y]["likes"]["count"]) + ".jpg" in listphotos.keys():
                likes = str(resvk["response"]["items"][y]["likes"]["count"]) + str(
                    resvk["response"]["items"][y]["date"]) + ".jpg"
                listphotos[likes] = resvk["response"]["items"][y]["sizes"][v - 1]["url"]
                savejson.append({"file_name": likes, "size": resvk["response"]["items"][y]["sizes"][-1]["type"]})
                y += 1
            else:
                likes = str(resvk["response"]["items"][y]["likes"]["count"]) + ".jpg"
                listphotos[likes] = resvk["response"]["items"][y]["sizes"][v - 1]["url"]
                savejson.append({"file_name": likes, "size": resvk["response"]["items"][y]["sizes"][-1]["type"]})
                y += 1

    with open('savejson.json', 'w') as outfile:
        json.dump(savejson, outfile)
    upload_yadisk()

def upload_yadisk():
    print()
    print("Загружаем фото на яДиск")
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + yatoken
    }
    url_create_folder = "https://cloud-api.yandex.net/v1/disk/resources/"
    if choise == "vk" or choise == "VK":
        params_create_folder = {
            'path': "id" + idvk
        }
        res_folder = requests.put(url=url_create_folder, params=params_create_folder, headers=headers)
        for name_url in tqdm(listphotos):
            params = {
                'path': "id" + idvk + "/" + str(name_url),
                'url': listphotos[name_url]
            }
            url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            r = requests.post(url=url_upload, params=params, headers=headers)
            res_upload = r.json()

if __name__ == '__main__':
    print("Программа сохраняет фотографии с разных API на яДиск. Выберите API")
    choise = input("Возможные варианты: vk, instagram, ok. (Пока возможно только вк) ")
    yatoken = input("Введите Token яДиска, куда загрузить фотографии ")
    if choise == "vk" or choise == "VK":
        print()
        vkphoto()
    else:
        print("Неверно! Напишите <vk>, остальные функции появятся в сл. версии программы.")