import requests
import json
from tqdm import tqdm

# 76119731

def menu():
    print("Программа сохраняет фотографии с разных API на яДиск. Выберите API")
    global choise
    choise = input("Возможные варианты: vk, instagram, ok. (Пока возможно только вк) ")
    global yatoken
    yatoken = input("Введите Token яДиска, куда загрузить фотографии ")
    if choise == "vk" or choise == "VK":
        print()
        vkphoto()
    else:
        print("Неверно! Напишите <vk>, остальные функции появятся в сл. версии программы.")
        return menu()

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

    y = 0
    global listphotos
    listphotos = {}
    savejson = []

    while y < countphotos:
        likes = str(resvk["response"]["items"][y]["likes"]["count"]) + ".jpg"
        listphotos[likes] = resvk["response"]["items"][y]["sizes"][-1]["url"]
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
            'path': "/vkapi/id" + idvk
        }
        res_folder = requests.put(url=url_create_folder, params=params_create_folder, headers=headers)
        for name_url in tqdm(listphotos):
            params = {
                'path': "/vkapi/id" + idvk + "/" + str(name_url),
                'url': listphotos[name_url]
            }
            url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            r = requests.post(url=url_upload, params=params, headers=headers)
            res_upload = r.json()
            print(res_upload)

menu()