import requests
import json
from tqdm import tqdm

# 76119731
# 306030189

def vkphoto(idvk, vktoken):
    print("Функция загружает на яДиск необходимое кол-во фото с аватарок vk данного ID")
    print("И сохраняет список файлов в формате <Имя : размер> в файл <savejson.json>")
    countphotos = int(input("Сколько фотографий загрузить? "))

    url = "https://api.vk.com/method/photos.get"
    params = {"owner_id": idvk, "album_id": "profile", "photo_sizes": 1, "extended": 1, "count": countphotos,
              "access_token": vktoken, "v": "5.131"}
    resvk = requests.get(url, params=params).json()

    if countphotos > resvk["response"]["count"]:
        print("Столько фото нет, максимум:", resvk["response"]["count"])
        return vkphoto(idvk, vktoken)
    else:
        listphotos = {}
        savejson = []

        c = 0
        v = 0
        y = 0

        for item in resvk["response"]["items"]:
            for u in item["sizes"]:
                if u["height"] >= c:
                    v += 1
                    c = u["height"]
            if str(item["likes"]["count"]) + ".jpg" in listphotos.keys():
                likes = str(item["likes"]["count"]) + str(item["date"]) + ".jpg"
                listphotos[likes] = item["sizes"][v]
                savejson.append({"file_name": likes, "size": item["sizes"][v]["type"]})
                y += 1
                c = 0
                v = 0
            else:
                likes = str(item["likes"]["count"]) + ".jpg"
                listphotos[likes] = item["sizes"][v]
                savejson.append({"file_name": likes, "size": item["sizes"][-1]["type"]})
                y += 1
                c = 0
                v = 0

    with open('savejson.json', 'w') as outfile:
        json.dump(savejson, outfile)
    return listphotos

def upload_yadisk(listphotos):
    print()
    print("Загружаем фото на яДиск")
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + yatoken
    }
    url_create_folder = "https://cloud-api.yandex.net/v1/disk/resources/"
    params_create_folder = {
        'path': "id" + idvk
    }
    res_folder = requests.put(url=url_create_folder, params=params_create_folder, headers=headers)
    if res_folder.status_code == 201:
        print("Все хорошо, фотографии загружаются")
    else:
        print("Произошла ошибка", res_folder.status_code)
    for name_url in tqdm(listphotos):
        params = {
            'path': "id" + idvk + "/" + str(name_url),
            'url': listphotos[name_url]['url']
        }
        url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
        r = requests.post(url=url_upload, params=params, headers=headers)
        if r.status_code == 202:
            print("Фото загрузилось успешно")
        else:
            print("Произошла ошибка", r.status_code)


if __name__ == '__main__':
    print("Программа сохраняет фотографии с разных API на яДиск. Выберите API")
    choise = input("Возможные варианты: vk, instagram, ok. (Пока возможно только вк) ")
    yatoken = input("Введите Token яДиска, куда загрузить фотографии ")
    if choise == "vk" or choise == "VK":
        idvk = input("Введите ID пользователя vk ")
        vktoken = input("Введите token VK ")
        print()
        listphotos = vkphoto(idvk, vktoken)
        upload_yadisk(listphotos)
    else:
        print("Неверно! Напишите <vk>, остальные функции появятся в сл. версии программы.")