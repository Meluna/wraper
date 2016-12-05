from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from Libwrapp.models import HDD, Brand, Interface, Volume, Speed

# массив брендов для панели выбора бренда
brand_array = Brand.objects.all()
# массив брендов для панели выбора бренда
interface_array = Interface.objects.all()
# массив объемов для панели выбора объема ЖД
volume_array = Volume.objects.all()
# массив скоростей для панели выбора скорости ЖД
speed_array = Speed.objects.all()
# максимальная цена товара для панели выбора цены
for price in HDD.objects.raw('''SELECT id, MAX(price) From Libwrapp_hdd;'''):
    max_price = price.price

def main(request):
    # --- формируем строку условия(цена) на языке sql для запроса к БД ---
    chosen_price_min = "0"
    chosen_price_max = "47499"
    try:
        chosen_price_min = request.POST['price_min']
    except MultiValueDictKeyError:
        pass
    try:
        chosen_price_max = request.POST['price_max']
    except MultiValueDictKeyError:
        pass
    price_predict = "Libwrapp_hdd.price BETWEEN " + chosen_price_min + " AND " + chosen_price_max

    # --- формируем строку условия(бренд) на языке sql для запроса к БД ---
    chosen_brand =""
    try:
        chosen_brand = request.POST['brand_checkbox']
    except MultiValueDictKeyError:
        pass
    if(chosen_brand != ""):
        brand_predict = " AND Libwrapp_brand.name = '" + chosen_brand + "'"
    else:
        brand_predict = ""

    # --- формируем строку условия(интерфейс ЖД на языке sql для запроса к БД ---
    chosen_interface =""
    try:
        chosen_interface = request.POST['interface_checkbox']
    except MultiValueDictKeyError:
        pass
    if (chosen_interface != ""):
        interface_predict = " AND Libwrapp_interface.name = '" + chosen_interface + "'"
    else:
        interface_predict = ""

    # --- формируем строку условия(цвет на языке sql для будущего запроса к БД ---
    chosen_volume =""
    try:
        chosen_volume = request.POST['volume_checkbox']
    except MultiValueDictKeyError:
        pass
    if (chosen_volume != ""):
        volume_predict = " AND Libwrapp_volume.name = '" + chosen_volume + "'"
    else:
        volume_predict = ""

    # --- формируем строку условия(скрость ЖД на языке sql для запроса к БД ---
    chosen_speed =""
    try:
        chosen_speed = request.POST['speed_checkbox']
    except MultiValueDictKeyError:
        pass
    if (chosen_speed != ""):
        speed_predict = " AND Libwrapp_speed.name = '" + chosen_speed + "'"
    else:
        speed_predict = ""

    # итоговый предикат выборки товаров из БД для оператора WHERE
    where_predict = price_predict + \
                    brand_predict + \
                    interface_predict + \
                    volume_predict + \
                    speed_predict

    # массив выбранных товаров
    chosen_hdd_array = []
    # запрос выборки товаров из БД, по ранее сформированному условию
    for hdd in HDD.objects.raw('''SELECT Libwrapp_hdd.id,
    Libwrapp_hdd.name AS name,
    Libwrapp_hdd.image AS image,
    Libwrapp_brand.name AS b,
    Libwrapp_hdd.description AS description,
    Libwrapp_interface.name AS int,
    Libwrapp_volume.name AS v,
    Libwrapp_speed.name AS s,
    Libwrapp_hdd.page AS page,
    Libwrapp_hdd.price AS price
    FROM Libwrapp_hdd
    JOIN Libwrapp_brand ON Libwrapp_hdd.brand_id = Libwrapp_brand.id
    JOIN Libwrapp_interface ON Libwrapp_hdd.interface_id = Libwrapp_interface.id
    JOIN Libwrapp_volume ON Libwrapp_hdd.volume_id = Libwrapp_volume.id
    JOIN Libwrapp_speed ON Libwrapp_hdd.speed_id = Libwrapp_speed.id
    WHERE ''' + where_predict +
    ''' ORDER BY price'''):
        chosen_hdd_array.append([hdd.image,
                                 hdd.name,
                                 hdd.b,
                                 hdd.price,
                                 hdd.page,
                                 hdd.int,
                                 hdd.description,
                                 hdd.v,
                                 hdd.s])

    return render(request, 'Libwrapp/main.html', {'hdd_array': chosen_hdd_array,
                                                  'interface_array': interface_array,
                                                  'volume_array': volume_array,
                                                  'speed_array': speed_array,
                                                  'brand_array': brand_array,
                                                  'max_price': max_price})