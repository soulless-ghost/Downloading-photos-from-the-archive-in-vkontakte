import os
import requests
from bs4 import BeautifulSoup
import re
import uuid

print('Если скаченный архив из Вконтакте в формате zip, разархивируйте его на рабочий стол, в ином случае программа не заработает!!!')
choice = input('Чтобы остановить работу приложения нажмите сочетание Ctrl+C\nНачать работу? \n"1"—Да\n"2"—Выход\n')
if choice == "1":
        # Определение домошней дирректории
        homepath = os.getenv('USERPROFILE') 
        # print(homepath)

        number = input("Ведите название-номер папки человека у которого хотите скачать фото: \n")

        for adress, dirs, files in os.walk(os.path.join(homepath, f'Desktop\Archive\messages/{number}')):
            
            for file in files:
                # Получаем полным путь к файлу html
                site_adress = os.path.join(adress, file)
                
                #Чтение файла html
                hml_file = open(site_adress, 'r')
                file_reading = hml_file.read()
                hml_file.close()
                # print(file_reading)

                # Получаем htlm код с которым можем работать
                soup = BeautifulSoup(file_reading, 'lxml')
                # Находим в коде странице только блоки div и получаем содержащийся текст на странице
                block = soup.find('div').text
                # print(block)

                #Создание шаблона для поиска и поиск ссылки на фото
                pattern = r'[a-z:]+//[a-z-./0-9A-Z]+\b.jpg'
                result = re.findall(pattern, block)
                if result == []:
                    print('Фотографий на сайте не найдено!')
                # print(result)

                # Достаем ссылку из списка
                for url_site in result:
                    link = url_site

                    # Создаем папку и ловим ошибку если папка уже создана
                    try: 
                        os.mkdir(homepath + "/Desktop/vk_img/")
                    except FileExistsError:
                        print("Папка существует")

                    # Отправляем запрос на сервер
                    p = requests.get(link)
                    # Генерируем рандомное имя для фотографии
                    photo_name = uuid.uuid4()
                    print(photo_name)
                    # Открываем созданную папку в бинарном режиме
                    out = open(homepath + f"/Desktop/vk_img/{photo_name}" + ".jpg", "wb")
                    # .content записывает фотографию
                    out.write(p.content)
                    out.close()

else:
    print("Выход из программы!")