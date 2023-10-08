from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Категория блюда
class Category(models.Model):
    # Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
    # первым аргументом принимает необязательное читабельное название.
    # Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
    # null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
    # blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
    # Это не то же что и null. null относится к базе данных, blank - к проверке данных.
    # Если поле содержит blank=True, форма позволит передать пустое значение.
    # При blank=False - поле обязательно.
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.title)

# Каталог блюд (меню)
class Catalog(models.Model):
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'catalog'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{} {}".format(self.category, self.title)

# Представление базы данных Каталог блюд (меню)
class ViewCatalog(models.Model):
    category_id = models.IntegerField(_('category_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_catalog'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
        # Таблицу не надо не добавлять не удалять
        managed = False

# Клиент для мобильного приложения 
class Client(models.Model):
    email = models.CharField(_('client_email'), max_length=128)
    password = models.CharField(_('password'), max_length=128)
    name = models.CharField(_('client_name'), max_length=128)
    phone = models.CharField(_('client_phone'), max_length=32)
    birthday = models.DateTimeField(_('birthday'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'client'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]
        # Сортировка по умолчанию
        ordering = ['name']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}, {}".format(self.name, self.phone, self.email)
        
# Счет (заказ)
class Bill(models.Model):
    # Дата заказа
    dateb = models.DateTimeField(_('dateb'), auto_now_add=True)
    # Клиент
    client = models.ForeignKey(Client, related_name='bill_client', on_delete=models.CASCADE)
    # Столик
    place = models.CharField(_('place'), max_length=32)
    # Сумма заказа
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)      
    # Скидка, %
    discount = models.IntegerField(_('discount'), default=0)
    # Оплата бонусами
    bonus = models.DecimalField(_('bonus'), max_digits=9, decimal_places=2, blank=True, null=True)
    # Оплата живыми деньгами
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'bill'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # Сортировка по умолчанию
        ordering = ['dateb']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}: {}".format(self.dateb, self.place, self.amount)

# Представление базы данных заказы
class ViewBill(models.Model):
    dateb = models.DateTimeField(_('dateb'))
    client = models.CharField(_('client'), max_length=256, blank=True, null=True)
    place = models.CharField(_('place'), max_length=32)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)      
    discount = models.IntegerField(_('discount'), default=0)
    bonus = models.DecimalField(_('bonus'), max_digits=9, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    detailing = models.TextField(_('bill_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_bill'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # Сортировка по умолчанию
        ordering = ['dateb']
        # Таблицу не надо не добавлять не удалять
        managed = False

#  Детализация заказа
class Detailing(models.Model):
    bill = models.ForeignKey(Bill, related_name='detailing_bill', on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, related_name='detailing_catalog', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'detailing'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['bill']),
            models.Index(fields=['catalog']),
        ]
        # Сортировка по умолчанию
        ordering = ['bill']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{} {}".format(self.bill, self.catalog)  
    @property
    def total(self):
        # "Возврат суммы."
        return '%f' % (self.price*self.quantity)

# Представление базы данных детализация заказов
class ViewDetailing(models.Model):
    bill_id = models.IntegerField(_('bill_id'))
    dateb = models.DateTimeField(_('dateb'))
    client_id = models.IntegerField(_('client_id'))
    name = models.CharField(_('client_name'), max_length=128, blank=True, null=True)
    email = models.CharField(_('client_email'), max_length=128, blank=True, null=True)
    phone = models.CharField(_('client_phone'), max_length=32, blank=True, null=True)
    place = models.CharField(_('place'), max_length=32)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)      
    discount = models.IntegerField(_('discount'), default=0)
    bonus = models.DecimalField(_('bonus'), max_digits=9, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    catalog_id = models.IntegerField(_('catalog_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    detailing_total = models.DecimalField(_('detailing_total'), max_digits=9, decimal_places=2, blank=True, null=True)  
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_detailing'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
        # Таблицу не надо не добавлять не удалять
        managed = False
        
# Корзина 
class Basket(models.Model):
    basketday = models.DateTimeField(_('basketday'), auto_now_add=True)
    catalog = models.ForeignKey(Catalog, related_name='basket_catalog', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    user = models.ForeignKey(User, related_name='user_basket', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'basket'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['basketday']),
        ]
        # Сортировка по умолчанию
        ordering = ['basketday']
    # Сумма по товару
    def total(self):
        return self.price * self.quantity

# Отзывы клиента 
class Review(models.Model):
    dater = models.DateTimeField(_('dater'), auto_now_add=True)
    client = models.ForeignKey(Client, related_name='review_client', on_delete=models.CASCADE)
    rating = models.IntegerField(_('rating'))
    details = models.TextField(_('review_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'review'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dater']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
