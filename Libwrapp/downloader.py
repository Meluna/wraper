from django.shortcuts import render, redirect
#импорт регулярных выражений
import re
# импорт модуля обработки ссылок (получение страниц с таковым адресом с удаленного сервера)
import urllib.request
# импорт парсера
from bs4 import BeautifulSoup
# импорт моделей приложения
from Libwrapp.models import HDD, Brand, Interface, Volume, Speed

def load(request):
    # очистака таблиц HDD, Brand, Volume, Speed
    HDD.objects.all().delete()
    Brand.objects.all().delete()
    Volume.objects.all().delete()
    Speed.objects.all().delete()

    # запрос страницы с сервера dns-shop.ru
    resp = urllib.request.urlopen(
         'http://www.dns-shop.ru/catalog/17a8914916404e77/zhestkie-diski-35/?mode=list')
    # чтение страницы
    readed_page = resp.read()

    # парсинг страницы возвращеной сервером
    soup_obj1 = BeautifulSoup(readed_page, "html.parser")

    # Поиск всех брендов на странице
    brand_list = soup_obj1.find('div', id = re.compile('^checkbox-list-brand-\w+$')).findAll('input', type="checkbox")
    # цикл добавления списка брендов в БД
    for i in range(0, len(brand_list)):
        obj_brand = Brand(name = brand_list[i]('span')[0].string) # текущий элемент списка
        obj_brand.save() # сохранение в БД

    # Поиск объемов ЖД на странице
    volume_list = soup_obj1.find('div', id = re.compile('^checkbox-list-n1-\w+$')).findAll('input', type="checkbox")

    for i in range(0, len(volume_list)):
        obj_volume = Volume(name = volume_list[i]('span')[0].string)
        obj_volume.save()

    # Поиск скоростей ЖД на странице
    speed_list = soup_obj1.find('div', id = re.compile('^checkbox-list-134-\w+$')).findAll('input', type="checkbox")

    for i in range(1, len(speed_list)):
        obj_speed = Speed(name = speed_list[i]('span')[0].string)
        obj_speed.save()

    # Считывание списка интерфейсов из БД
    interface_array = (Interface.objects.all())
    # Считывание списка объемов из БД
    volume_array = (Volume.objects.all())
    # Считывание списка скоростей из БД
    speed_array = (Speed.objects.all())

    # Цикл заполения строк таблицы HDD(ЖД), основной таблицы хранящей сущность жесткий диск
    for brand in brand_list:
        # запрос страницы с результатами для конкретного бренда ЖД
        product_resp = urllib.request.urlopen(
            'http://www.dns-shop.ru/catalog/17a8914916404e77/zhestkie-diski-35/?mode=list'
            + '&brand=' + str(brand['value']))
        # чтение страницы
        readed_page2 = product_resp.read()
        # парсинг страницы
        soup_obj2 = BeautifulSoup(readed_page2, "html.parser")
        # сохранение списка изоюражений товаров на странице
        image_list = soup_obj2.body.findAll(attrs={"class": "popover-content img-popover"})
        # сохранение списка наименований товаров на странице
        name_list = soup_obj2.body.findAll(attrs={"class": "item-name"})
        # сохранение списка цен товаров на странице
        prices_list = soup_obj2.body.findAll(attrs={"class": "price_g"})
        # сохранение списка цен товаров на странице
        prod_links_list = soup_obj2.body.findAll(attrs={"class": "item-name"})
        # сохранение списка опциональных сведений товаров на странице
        options = soup_obj2.body.findAll(attrs={"class": "item-desc"})
        # определение значения внешнего ключа Бренда
        prod_id = (Brand.objects.get(name = str(brand('span')[0].string))).id
        # цикл установки значений полей объектов таблицы HDD
        for i in range(0, len(name_list)):
            # страница товара
            prod_page = ("http://www.dns-shop.ru" + prod_links_list[i]('a')[0]['href'])
            # запрос страницы товара
            resp = urllib.request.urlopen(prod_page)
            # чтение страницы товара
            html_desc = resp.read()
            # парсинг страницы товара сервером
            soup2 = BeautifulSoup(html_desc, "html.parser")
            # получение значения блока описания на странице товара
            description = soup2.body.find(attrs={"class": "price_item_description"})('p')[0].string

            # условия определения значения внешних ключей(FK) таблицы HDD
            for interface in interface_array[::-1]:
                if interface.name in (options[i]('a')[0].string):
                    interface_id = interface.id
            for volume in volume_array:
                if volume.name in (name_list[i]('a')[0].string):
                    volume_id = volume.id
            for speed in speed_array:
                if speed.name in (options[i]('a')[0].string):
                    speed_id = speed.id
            # сохранение текущего товара в таблицу, базы данных, HDD
            obj2_prod = HDD(image = image_list[i]('img')[0]['data-image-desktop'], # ссылка на изображение товара
                            name = name_list[i]('a')[0].string, # наименование товара
                            brand_id = prod_id, # производитель товара
                            interface_id = interface_id, # внешний ключ на таблицу Interfaces
                            volume_id = volume_id, # внешний ключ на таблицу Volume
                            speed_id = speed_id, # внешний ключ на таблицу Speed
                            description = description, # описание товара
                            price = int((prices_list[i]('span')[0].string).replace(" ", "")), # цена товара
                            page = prod_page) # ссылка на страницу товара
            obj2_prod.save() # сохранение в БД
    return redirect("/") # возвращение на главную страницу веб-приложения