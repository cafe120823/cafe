﻿# Generated by Django 4.2.2 on 2023-08-10 09:20
from pickle import FALSE, TRUE
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.db import migrations
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
# Поделючаем модкль генерации случайных чисел
import random

global dict_category
dict_category = {}
global dict_catalog_price
dict_catalog_price = {}

# Найти или Добавить Категорию
def get_category(apps, val):   
    # Поиск категории
    if val in dict_category.values():
        for k, v in dict_category.items():
            if v == val:
                return k    
    else:
        Category = apps.get_model("star", "Category")
        category = Category()
        category.title = val
        category.save()
        dict_category[category.id] = category.title
        return category.id

# Добавить блюдо из меню
def insert_catalog(apps, param_catalog):   
    Catalog = apps.get_model("star", "Catalog")
    catalog = Catalog()
    catalog.category_id = param_catalog[0]
    catalog.title = param_catalog[1]
    catalog.details = param_catalog[2]
    catalog.price = param_catalog[3]
    catalog.availability = param_catalog[4]
    catalog.photo = param_catalog[5]
    catalog.save()
    dict_catalog_price[catalog.id] = catalog.price    
    return

# Добавить настройки: скидки, бонусы
def insert_configuration(apps, param):
    Configuration = apps.get_model("star", "Configuration")
    configuration = Configuration()
    configuration.datec = param[0]
    configuration.discount = param[1]
    configuration.bonus = param[2]
    configuration.save()
    configuration.datec = param[0]
    configuration.save()
    return 

# Добавить клиента мобильного приложения
def insert_client(apps, param_client):   
    Client = apps.get_model("star", "Client")
    client = Client()
    client.email = param_client[0]
    client.password = param_client[1]
    client.name = param_client[2]
    client.phone = param_client[3]
    client.birthday = param_client[4]
    client.save()
    return

# Добавить отзывы от клиента мобильного приложения
def insert_review(apps, param_review):   
    Review = apps.get_model("star", "Review")
    review = Review()
    review.dater = param_review[0]
    review.client_id = param_review[1]
    review.rating = param_review[2]
    review.details = param_review[3]
    review.save()
    review.dater = param_review[0]
    review.save()
    return

# Добавить чек (заказ)
def insert_bill(apps, param_bill):   
    Bill = apps.get_model("star", "Bill")
    bill = Bill()
    bill.dateb = param_bill[0]
    bill.client_id = param_bill[1]
    bill.place = param_bill[2]
    bill.comments = param_bill[3]
    bill.total = param_bill[4]
    bill.discount = param_bill[5]
    bill.bonus = param_bill[6]
    bill.amount = param_bill[7]
    bill.save()
    bill.dateb = param_bill[0]
    bill.save()
    return

# Добавить бронирование
def insert_reservation(apps, param_reservation):   
    Reservation = apps.get_model("star", "Reservation")
    reservation = Reservation()
    reservation.datea = param_reservation[0]
    reservation.dater = param_reservation[1]
    reservation.client_id = param_reservation[2]
    reservation.quantity = param_reservation[3]
    reservation.details = param_reservation[4]
    reservation.comments = param_reservation[5]
    reservation.save()
    reservation.datea = param_reservation[0]
    reservation.save()
    return

## Добавить детализацию чека (заказа)
#def insert_detailing(apps, param_detailing):   
#    # Добавить товар
#    Detailing = apps.get_model("star", "Detailing")
#    detailing = Detailing()
#    detailing.bill_id = param_detailing[0]
#    detailing.catalog_id = param_detailing[1]
#    detailing.price = param_detailing[2]
#    detailing.quantity = param_detailing[3]
#    detailing.save()
#    return

# Добавить детализацию чека (заказа)
# _catalog - список id каталога
# _quantity - соответствующе ему количество
def insert_detailing(apps, bill_id, _catalog, _quantity):   
    Detailing = apps.get_model("star", "Detailing")
    i=0
    total=0
    while i < len(_catalog):
        detailing = Detailing() 
        detailing.bill_id = bill_id
        detailing.catalog_id = _catalog[i]
        detailing.price = dict_catalog_price.get(_catalog[i])
        detailing.quantity =  _quantity[i]
        total = total + (detailing.price*detailing.quantity) 
        detailing.save()
        i += 1
    # Подсчитать сумму
    Bill = apps.get_model("star", "Bill")    
    bill = Bill.objects.get(id=bill_id) 
    bill.total = total
    bill.save()
    return

# Добавить Уведомления
def insert_notification(apps, param):
    Notification = apps.get_model("star", "Notification")
    notification = Notification()
    notification.datec = param[0]
    notification.daten = param[1]
    notification.client_id = param[2]
    notification.details = param[3]
    notification.save()
    notification.datec = param[0]
    notification.save()
    return 

# Добавить Новости
def insert_news(apps, param):
    News = apps.get_model("star", "News")
    news = News()
    news.daten = param[0]
    news.title = param[1]
    news.details = param[2]
    news.photo = param[3]
    news.save()
    return 

# Начальные данные
def new_data(apps, schema_editor):
    # Суперпользователь id=1
    user = User.objects.create_superuser(username='root',
    email='cafe120823@mail.ru',
    first_name='Суперпользователь', 
    last_name='',
    password='SsNn5678+-@')
    print("Суперпользователь создан")
    
    # Группа менеджеров
    managers = Group.objects.get_or_create(name = 'Managers')
    managers = Group.objects.get(name='Managers')
    print("Группа менеджеров создана")
    
    # Пользователь с ролью менеджера id=2
    user = User.objects.create_user(username='manager', password='Ss0066+-', email='manager@mail.ru', first_name='Менеджер',)
    managers.user_set.add(user)
    print("Менеджер добавлен в группу менеджеров")

    # Пользователи для мобильного приложения пароль 123456 в SHA256 равен 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
    parameters = ["user1@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Жерихов Дмитрий", "+7-905-123-4567", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user2@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Тесля Валерий", "+7-905-452-3252", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user3@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Пьяных Анна", "+7-905-326-7854", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user4@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Шишик Александр", "+7-905-951-3657", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user5@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Сенько Андрей", "+7-905-952-3256", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user6@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Пикалова Алёна", "+7-905-712-9635", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user7@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Федченко Олеся", "+7-905-256-3210", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user8@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Мороз Дарья", "+7-905-128-6824", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user9@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Баталина Анна", "+7-905-934-6423", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    parameters = ["user10@mail.ru", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", "Боцман Юлия", "+7-905-934-9521", datetime.now() - timedelta(days=random.randint(8000, 22000))]
    insert_client(apps, parameters)
    print("Добавлены пользователи для мобильного приложения ")

    # Добавить настройки: скидки, бонусы
    parameters = [datetime.now() - timedelta(days=30), 5, 3 ]
    insert_configuration(apps, parameters)
    parameters = [datetime.now() - timedelta(days=15), 5, 5 ]
    insert_configuration(apps, parameters)
    parameters = [datetime.now() - timedelta(days=5), 3, 5 ]
    insert_configuration(apps, parameters)

    # Новости
    parameters = [datetime.now() - timedelta(days=35), "Заголовок новости", """Текст новости""", "images/news1.jpeg" ]
    insert_news(apps, parameters)
    print("Добавлены новости")

    #1 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Салаты"),  "Домашний салат", """Классика домашнего салата из помидоров, огурцов,лука, заправлен майонезом или растительным маслом""", 240, 1, "images/catalog01.jpg"]
    insert_catalog(apps, parameters)    
    #2 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Салаты"),  "Оливье классический", """Салат оливье — король салатов, без которого ни один новый год не может быть полноценным. Представляем вашему вниманию наш классический вариант всеми любимого оливье""", 300, 1, "images/catalog02.jpg"]
    insert_catalog(apps, parameters)    
    #3 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Салаты"),  "Салат \"Гнездо глухаря\"", """В основу салата входит: куриный рулет, листья салата, заправлен майонезом, посыпается картофелем пай, поверх ложат перепелинные яйца""", 360, 1, "images/catalog03.jpg"]
    insert_catalog(apps, parameters)    
    #4 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Салаты"),  "Салат \"Греческий\"", """Классический греческий салат в состав входит: сыр Фета, огурцы, помидоры, болгарский перец, лист салата, маслины, оливки заправлен на оливковом масле с добавлением бальзамического уксуса""", 362, 1, "images/catalog04.jpg"]
    insert_catalog(apps, parameters)    
    #5 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Салаты"),  "Салат \"Деревенский\"", """Кубиками нарезн филе курицы, добавлена консервированная фасоль, кукуруза, корнишоны, сухари, заправляются на майонезе""", 420, 1, "images/catalog05.jpg"]
    insert_catalog(apps, parameters)    
    #6 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Первые блюда"),  "Пельмени с бульоном", """Фирменные пельмени из отборной говядины приготовленные на пару с фирменным бульоном""", 320, 1, "images/catalog06.jpg"]
    insert_catalog(apps, parameters)    
    #7 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Первые блюда"),  "Солянка", """Ароматный суп с мясными деликатесами""", 340, 1, "images/catalog07.jpg"]
    insert_catalog(apps, parameters)    
    #8 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Первые блюда"),  "Уха по царски", """Бульон на рыбных костях, семга, судак, овощи""", 370, 1, "images/catalog08.jpg"]
    insert_catalog(apps, parameters)    
    #9 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Первые блюда"),  "Лапша по-домашнему", """Лапша по-домашнему (на курином бульоне)""", 260, 1, "images/catalog09.jpg"]
    insert_catalog(apps, parameters)    
    #10 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Первые блюда"),  "Твиндян тиге", """Традиционный корейский суп на основе соевой пасты с мясом говядины луком, помидорами, перцем, кабачками, тубу и яйцом""", 400, 1, "images/catalog10.jpg"]
    insert_catalog(apps, parameters)    
    #11 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Вторые блюда"),  "Бефстроганов с пюре", """Говядина вырезка, грибы шампиньоны, сливки, сметана, горчица""", 740, 1, "images/catalog11.jpg"]
    insert_catalog(apps, parameters)    
    #12 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Вторые блюда"),  "Мясо с грибами в сливочном соусе", """Телятина, шампиньоны, сливочный соус""", 600, 1, "images/catalog12.jpg"]
    insert_catalog(apps, parameters)    
    #13 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Вторые блюда"),  "Картофель по-домашнему с мясом", """Домашнее блюдо жаренный картофель с мясом""", 600, 1, "images/catalog13.jpg"]
    insert_catalog(apps, parameters)    
    #14 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Вторые блюда"),  "Мясо по-гречески", """Говяжья отбивная под сыром, грибы шампиньоны, яйцо, картофель фри""", 600, 1, "images/catalog14.jpg"]
    insert_catalog(apps, parameters)    
    #15 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Вторые блюда"),  "Мясо по-французски", """Говяжья отбивная, запеченная с помидорами и сыром, картофель фри""", 600, 1, "images/catalog15.jpg"]
    insert_catalog(apps, parameters)    
    #16 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Закуски"),  "Мясное ассорти", """Говядина х/к, казы, бастурма, рулет из индейки, ципленок х/к""", 1000, 1, "images/catalog16.jpg"]
    insert_catalog(apps, parameters)    
    #17 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Закуски"),  "Овощи по-кавказски", """Нарезка из свежих овощей (помидоры, огурцы, болгарский перец), сыр брынза и свежая зелень""", 450, 1, "images/catalog17.jpg"]
    insert_catalog(apps, parameters)    
    #18 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Закуски"),  "Рыбное ассорти", """Нарезка семги, балык и скумбрии""", 1060, 1, "images/catalog18.jpg"]
    insert_catalog(apps, parameters)    
    #19 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Закуски"),  "Сельдь по-русски", """Нарезка селедки, вареная картошка, маринованные огурци и лук""", 350, 1, "images/catalog19.jpg"]
    insert_catalog(apps, parameters)    
    #20 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Закуски"),  "Сатэ", """Обжаренные баклажаны в кляре с начиной из помидора и тар-тара""", 320, 1, "images/catalog20.jpg"]
    insert_catalog(apps, parameters)    
    #21 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Напитки"),  "Минеральная вода \"ASU\" 1л", """Минеральная вода""", 170, 1, "images/catalog21.jpg"]
    insert_catalog(apps, parameters)    
    #22 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Напитки"),  "Морс Смородины 1л", """Морс Смородины""", 340, 1, "images/catalog22.jpg"]
    insert_catalog(apps, parameters)    
    #23 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Напитки"),  "Лимонад Киви лайм 1л", """Лимонад Киви лайм""", 500, 1, "images/catalog23.jpg"]
    insert_catalog(apps, parameters)    
    #24 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Напитки"),  "Лимонад Клубника лайм 1л", """Лимонад Клубника лайм""", 500, 1, "images/catalog24.jpg"]
    insert_catalog(apps, parameters)    
    #25 Каталог parameters - товар, (категория, название, описание, цена, фото)
    parameters = [get_category(apps, "Напитки"),  "Сок в ассортименте 0,95л", """Сок в ассортименте 0,95л""", 300, 1, "images/catalog25.jpg"]
    insert_catalog(apps, parameters)    
    print("Добавлен каталог")

    #1 Заказы    bill.dateb, bill.client_id, bill.place, bill.comments, bill.total, bill.discount, bill.bonus, bill.amount
    parameters = [datetime.now() - timedelta(days=30), 1, "№1", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    #insert_detailing(apps, 1, [random.randint(1, 5), random.randint(6, 10), random.randint(11, 15), random.randint(21, 25)], [random.randint(1, 2), random.randint(1, 2), 2, random.randint(1, 2)])
    insert_detailing(apps, 1, [1, 6, 11, 21], [1, 2, 2, 1])
    #2 Заказы
    parameters = [datetime.now() - timedelta(days=30), 2, "№2", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 2, [2, 7, 12, 22], [1, 2, 2, 1])
    #3 Заказы
    parameters = [datetime.now() - timedelta(days=30), 3, "№3", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 3, [3, 8, 13, 23], [1, 2, 2, 1])
    #4 Заказы
    parameters = [datetime.now() - timedelta(days=30), 4, "№4", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 4, [4, 9, 14, 24], [1, 2, 2, 1])    
    #5 Заказы
    parameters = [datetime.now() - timedelta(days=30), 5, "№5", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 5, [5, 10, 15, 25], [1, 2, 2, 1])    
    #6 Заказы
    parameters = [datetime.now() - timedelta(days=29), 6, "№1", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 6, [3, 8, 14, 24], [1, 2, 2, 1])    
    #7 Заказы
    parameters = [datetime.now() - timedelta(days=29), 7, "№2", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 7, [2, 7, 11, 21], [1, 1, 1, 1])    
    #8 Заказы
    parameters = [datetime.now() - timedelta(days=29), 8, "№3", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 8, [2, 7, 13, 22], [1, 2, 2, 1])    
    #9 Заказы
    parameters = [datetime.now() - timedelta(days=29), 9, "№4", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 9, [2, 7, 11, 21], [1, 1, 2, 1])    
    #10 Заказы
    parameters = [datetime.now() - timedelta(days=29), 10, "№5", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 10, [3, 8, 14, 21], [1, 1, 1, 1])   

    #11 Заказы   
    parameters = [datetime.now() - timedelta(days=28), 1, "№1", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 11, [2, 8, 10, 21], [1, 2, 2, 1])
    #12 Заказы
    parameters = [datetime.now() - timedelta(days=28), 2, "№2", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 12, [3, 9, 14, 23], [1, 2, 2, 1])
    #13 Заказы
    parameters = [datetime.now() - timedelta(days=28), 3, "№3", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 13, [1, 6, 12, 21], [1, 2, 2, 1])
    #14 Заказы
    parameters = [datetime.now() - timedelta(days=27), 4, "№4", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 14, [5, 7, 12, 20], [1, 2, 2, 1])    
    #15 Заказы
    parameters = [datetime.now() - timedelta(days=27), 5, "№5", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 15, [4, 12, 14, 24], [1, 2, 2, 1])    
    #16 Заказы
    parameters = [datetime.now() - timedelta(days=27), 1, "№1", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 16, [5, 9, 11, 21], [1, 2, 2, 1])    
    #17 Заказы
    parameters = [datetime.now() - timedelta(days=26), 2, "№2", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 17, [3, 6, 14, 23], [1, 1, 1, 1])    
    #18 Заказы
    parameters = [datetime.now() - timedelta(days=26), 3, "№3", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 18, [2, 7, 13, 22], [1, 2, 2, 1])    
    #19 Заказы
    parameters = [datetime.now() - timedelta(days=26), 1, "№4", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 19, [4, 8, 14, 24], [1, 1, 2, 1])    
    #20 Заказы
    parameters = [datetime.now() - timedelta(days=25), 2, "№5", "", 0, 0, 0, 0 ]
    insert_bill(apps, parameters)
    insert_detailing(apps, 20, [2, 8, 11, 25], [1, 1, 1, 1])        

    print("Добавлены заказы")

    #1 Бронирование
    parameters = [datetime.now() - timedelta(days=30), datetime.now() - timedelta(days=28), 1, 4, "Столик на четверых", "" ]
    insert_reservation(apps, parameters)
    parameters = [datetime.now() - timedelta(days=29), datetime.now() - timedelta(days=27), 2, 2, "Столик на двоих", "" ]
    insert_reservation(apps, parameters)
    parameters = [datetime.now() - timedelta(days=28), datetime.now() - timedelta(days=26), 3, 4, "Столик на четверых", "" ]
    insert_reservation(apps, parameters)
    parameters = [datetime.now() - timedelta(days=27), datetime.now() - timedelta(days=25), 4, 2, "Столик на двоих", "" ]
    insert_reservation(apps, parameters)
    parameters = [datetime.now() - timedelta(days=26), datetime.now() - timedelta(days=24), 5, 2, "VIP-кабина", "" ]
    insert_reservation(apps, parameters)
    
    print("Добавлены бронирование")

    #1 Отзывы
    parameters = [datetime.now() - timedelta(days=30), 1, 5,  "Всё прошло на высшем уровне! Спасибо большое за то, что вы есть!"]
    insert_review(apps, parameters)
    #2 Отзывы
    parameters = [datetime.now() - timedelta(days=29), 2, 5,  "Отличное место. Прекрасное расположение, легко добраться. Очень отзывчивые администраторы, все объяснили, подсказали с напитками, с посадкой в общем находка, а не администраторы."]
    insert_review(apps, parameters)
    #3 Отзывы
    parameters = [datetime.now() - timedelta(days=28), 3, 5,  "Кафе очень хорошее. Обслуживание на высоте. Кухня очень вкусная."]
    insert_review(apps, parameters)
    #4 Отзывы
    parameters = [datetime.now() - timedelta(days=27), 4, 5,  "Нам понравилось все от момента, как нас встретили при выборе заведения, составлении меню до сервировки, обслуживания во время банкета."]
    insert_review(apps, parameters)
    #5 Отзывы
    parameters = [datetime.now() - timedelta(days=26), 5, 5,  "Спасибо за классный вечер! Долго выбирали зал и ни разу не пожалели что выбрали ваше заведение."]
    insert_review(apps, parameters)
    #6 Отзывы
    parameters = [datetime.now() - timedelta(days=25), 6, 5,  "Благодарю заведение за прекрасный вечер! Все было очень красиво и вкусно. Официанты очень внимательные."]
    insert_review(apps, parameters)
    #7 Отзывы
    parameters = [datetime.now() - timedelta(days=24), 7, 5,  "Банкетный зал уютный и светлый! Весьма вкусная кухня! Чистота, организованность, порядочность!"]
    insert_review(apps, parameters)
    #8 Отзывы
    parameters = [datetime.now() - timedelta(days=23), 8, 5,  "Отличное место! Чисто, уютно, вкусно! Замечательный сервис и персонал."]
    insert_review(apps, parameters)
    #9 Отзывы
    parameters = [datetime.now() - timedelta(days=22), 9, 5,  "Хотим выразить благодарность всей команде этого замечательного заведения. Спасибо за помощь в выборе меню и отличный сервис. Доверились рекомендациям своих знакомых и ни чуть не пожалели. Кухня очень вкусная, зал уютный."]
    insert_review(apps, parameters)
    #10 Отзывы
    parameters = [datetime.now() - timedelta(days=21), 10, 5,  " Проводили день рождение и все прошло на высшем уровне , прям как хотели, даже лучше !! Все продумано и очень вкусно!!! "]
    insert_review(apps, parameters)

    print("Добавлены отзывы")

    #1 Уведомления
    parameters = [datetime.now() - timedelta(days=30), datetime.now() - timedelta(days=28), 1, "Текст уведомления для 1" ]
    insert_notification(apps, parameters)
    parameters = [datetime.now() - timedelta(days=27), datetime.now() - timedelta(days=26), 2, "Текст уведомления для 2" ]
    insert_notification(apps, parameters)
    parameters = [datetime.now() - timedelta(days=25), datetime.now() - timedelta(days=24), 3, "Текст уведомления для 3" ]
    insert_notification(apps, parameters)

    print("Добавлены уведомления")

class Migration(migrations.Migration):

    dependencies = [
        ('star', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(new_data),
        # Представления для SQLite и PostgreSQL
        migrations.RunSQL("""CREATE VIEW view_catalog AS
            SELECT catalog.id, catalog.category_id, category.title AS category, catalog.title, catalog.details, catalog.price, catalog.availability, catalog.photo
            FROM catalog LEFT JOIN category ON catalog.category_id = category.id
            WHERE catalog.availability=True """),
        migrations.RunSQL("""CREATE VIEW view_detailing AS
            SELECT detailing.id, detailing.bill_id, bill.dateb, bill.client_id, client.name, client.email, client.phone, bill.place, bill.comments, bill.total, bill.discount, bill.bonus, bill.amount, detailing.catalog_id, view_catalog.category, 
            view_catalog.title, view_catalog.details,  view_catalog.photo, detailing.price, detailing.quantity, detailing.price*detailing.quantity AS detailing_total
            FROM detailing LEFT JOIN bill ON detailing.bill_id=bill.id
            LEFT JOIN client ON bill.client_id=client.id
            LEFT JOIN view_catalog ON detailing.catalog_id=view_catalog.id"""),

#        # Представление для SQLite
#        migrations.RunSQL("""CREATE VIEW view_bill AS
#SELECT id, dateb, client_id, (SELECT (name || ': ' || phone || ', ' || email) FROM view_detailing WHERE bill.id=view_detailing.bill_id GROUP BY (name || ': ' || phone || ', ' || email) ) AS client,
#place, comments, total, discount, bonus, amount, (SELECT GROUP_CONCAT(category || ': ' || title || ' - ' || quantity || '*' || price || '=' || detailing_total, ';') 
#FROM view_detailing WHERE bill.id=view_detailing.bill_id) AS detailing
#FROM bill"""),

        # Представление для PostgreSQL
        migrations.RunSQL("""CREATE VIEW view_bill AS
SELECT id, dateb, client_id, (SELECT (name || ': ' || phone || ', ' || email) FROM view_detailing WHERE bill.id=view_detailing.bill_id GROUP BY (name || ': ' || phone || ', ' || email) ) AS client, 
place, comments, total, discount, bonus, amount, (SELECT STRING_AGG(category || ': ' || title || ' - ' || quantity || '*' || price || '=' || detailing_total, ';') 
FROM view_detailing WHERE bill.id=view_detailing.bill_id) AS detailing
FROM bill"""),

        ## Тригер SQLite
        #migrations.RunSQL("""CREATE TRIGGER bill_total_insert_detailing AFTER INSERT
        #    ON detailing
        #    BEGIN
        #    UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=NEW.bill_id) WHERE id = NEW.bill_id;
        #    END;"""),
        #migrations.RunSQL("""CREATE TRIGGER bill_total_update_detailing AFTER UPDATE
        #    ON detailing
        #    BEGIN
        #    UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=NEW.bill_id) WHERE id = NEW.bill_id;
        #    END;"""),
        #migrations.RunSQL("""CREATE TRIGGER bill_total_delete_detailing AFTER DELETE
        #    ON detailing
        #    BEGIN
        #    UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=OLD.bill_id) WHERE id = OLD.bill_id;
        #    END;"""),

        # Тригер PostgreSQL
        migrations.RunSQL("""CREATE OR REPLACE FUNCTION insert_detailing()
              RETURNS trigger AS
            $$
            BEGIN
	            UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=NEW.bill_id) WHERE id = NEW.bill_id;  
            RETURN NEW;
            END;
            $$
            LANGUAGE 'plpgsql';
            CREATE TRIGGER bill_total_insert_detailing
              AFTER INSERT
              ON "detailing"
              FOR EACH ROW
              EXECUTE PROCEDURE insert_detailing();"""),
        migrations.RunSQL("""CREATE OR REPLACE FUNCTION update_detailing()
              RETURNS trigger AS
            $$
            BEGIN
	            UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=NEW.bill_id) WHERE id = NEW.bill_id;  
            RETURN NEW;
            END;
            $$
            LANGUAGE 'plpgsql';
            CREATE TRIGGER bill_total_update_detailing
              AFTER UPDATE
              ON "detailing"
              FOR EACH ROW
              EXECUTE PROCEDURE update_detailing();"""),
        migrations.RunSQL("""CREATE OR REPLACE FUNCTION delete_detailing()
              RETURNS trigger AS
            $$
            BEGIN
	            UPDATE bill SET total = (SELECT SUM(price*quantity) FROM detailing WHERE bill_id=OLD.bill_id) WHERE id = OLD.bill_id;  
            RETURN NEW;
            END;
            $$
            LANGUAGE 'plpgsql';
            CREATE TRIGGER bill_total_delete_detailing
              AFTER DELETE
              ON "detailing"
              FOR EACH ROW
              EXECUTE PROCEDURE delete_detailing();"""),
    ]
