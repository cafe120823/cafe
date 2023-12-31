from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# ������ ���������� ���������� � ������, � �������� �� ���������.
# ��� �������� ���� � ��������� ����� ������.
# ������ ���� ������ ������������ ���� ������� � ���� ������.
# ������ ������ ��� ����� �������������� �� django.db.models.Model.
# ������� ������ ������������ ���� � ���� ������.
# Django ������������� ������������� ��������� API ��� ������� � ������

# choices (������ ������). �������� (��������, ������ ��� ������) 2-� ���������� ��������,
# ������������ �������� �������� ��� ����.
# ��� �����������, ������ ����� ���������� select ������ ������������ ���������� ����
# � ��������� �������� ���� ���������� ����������.

# ��������� �����
class Category(models.Model):
    # ����������� ��� ���� (�����, label). ������ ����, ����� ForeignKey, ManyToManyField � OneToOneField,
    # ������ ���������� ��������� �������������� ����������� ��������.
    # ���� ��� �� �������, Django �������������� ������� ���, ��������� �������� ����, ������� ������������� �� ������.
    # null - ���� True, Django �������� ������ �������� ��� NULL � ���� ������. �� ��������� - False.
    # blank - ���� True, ���� �� ����������� � ����� ���� ������. �� ��������� - False.
    # ��� �� �� �� ��� � null. null ��������� � ���� ������, blank - � �������� ������.
    # ���� ���� �������� blank=True, ����� �������� �������� ������ ��������.
    # ��� blank=False - ���� �����������.
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'category'
    def __str__(self):
        # ����� ��������� ��� SELECT 
        return "{}".format(self.title)

# ������� ���� (����)
class Catalog(models.Model):
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    availability = models.BooleanField(_('availability'), default=True)
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {}".format(self.category, self.title)

# ������������� ���� ������ ������� ���� (����)
class ViewCatalog(models.Model):
    category_id = models.IntegerField(_('category_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    availability = models.BooleanField(_('availability'), default=True)
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
        # ������� �� ���� �� ��������� �� �������
        managed = False

# ������ ��� ���������� ���������� 
class Client(models.Model):
    email = models.CharField(_('client_email'), max_length=128)
    password = models.CharField(_('password'), max_length=128)
    name = models.CharField(_('client_name'), max_length=128)
    phone = models.CharField(_('client_phone'), max_length=32)
    birthday = models.DateTimeField(_('birthday'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'client'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]
        # ���������� �� ���������
        ordering = ['name']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}, {}, {}".format(self.name, self.phone, self.email)
        
# ���� (�����)
class Bill(models.Model):
    # ���� ������
    dateb = models.DateTimeField(_('bill_date'), auto_now_add=True)
    # ������
    client = models.ForeignKey(Client, related_name='bill_client', on_delete=models.CASCADE)
    # ������
    place = models.CharField(_('place'), max_length=32)
    # ����������� � ������
    comments = models.TextField(_('bill_comments'), blank=True, null=True)    
    # ����� ������
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)      
    # ������, %
    discount = models.IntegerField(_('discount'), default=0)
    # ������ ��������
    bonus = models.DecimalField(_('bonus'), max_digits=9, decimal_places=2, blank=True, null=True)
    # ������ ������ ��������
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'bill'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # ���������� �� ���������
        ordering = ['dateb']
    @property
    def discount_total(self):
        # ������� ����� ������
        return (self.discount*self.total)/100
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}, {}: {}".format(self.dateb, self.place, self.amount)

# ������������� ���� ������ ������
class ViewBill(models.Model):
    dateb = models.DateTimeField(_('bill_date'))
    client_id = models.IntegerField(_('client_id'))
    client = models.CharField(_('client'), max_length=256, blank=True, null=True)
    place = models.CharField(_('place'), max_length=32)
    comments = models.TextField(_('bill_comments'), blank=True, null=True)  
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)      
    discount = models.IntegerField(_('discount'), default=0)
    bonus = models.DecimalField(_('bonus'), max_digits=9, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    detailing = models.TextField(_('bill_details'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_bill'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # ���������� �� ���������
        ordering = ['dateb']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    @property
    def discount_total(self):
        # ������� ����� ������
        return (self.discount*self.total)/100

#  ����������� ������
class Detailing(models.Model):
    bill = models.ForeignKey(Bill, related_name='detailing_bill', on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, related_name='detailing_catalog', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'detailing'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['bill']),
            models.Index(fields=['catalog']),
        ]
        # ���������� �� ���������
        ordering = ['bill']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {}".format(self.bill, self.catalog)  
    @property
    def total(self):
        # "������� �����."
        return '%f' % (self.price*self.quantity)

# ������������� ���� ������ ����������� �������
class ViewDetailing(models.Model):
    bill_id = models.IntegerField(_('bill_id'))
    dateb = models.DateTimeField(_('dateb'))
    client_id = models.IntegerField(_('client_id'))
    name = models.CharField(_('client_name'), max_length=128, blank=True, null=True)
    email = models.CharField(_('client_email'), max_length=128, blank=True, null=True)
    phone = models.CharField(_('client_phone'), max_length=32, blank=True, null=True)
    place = models.CharField(_('place'), max_length=32)
    comments = models.TextField(_('bill_comments'), blank=True, null=True)  
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
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_detailing'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
        # ������� �� ���� �� ��������� �� �������
        managed = False
        
# ������������ ��������
class Reservation(models.Model):
    # ���� ������ �� �����������
    datea = models.DateTimeField(_('reservation_application'), auto_now_add=True)
    # ���� � ����� ������������
    dater = models.DateTimeField(_('reservation_date'))
    # ������
    client = models.ForeignKey(Client, related_name='reservation_client', on_delete=models.CASCADE)
    # ����� �����
    quantity = models.IntegerField(_('quantity_people'), default=0)
    # �������� �� ������������ �� �������
    details = models.TextField(_('reservation_details'))    
    # ����������� � ������������ �� ���������
    comments = models.TextField(_('reservation_comments'), blank=True, null=True)    
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'reservation'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dater']),
        ]
        # ���������� �� ���������
        ordering = ['dater']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}".format(self.dater, self.client)

# ����������� �������
class Notification(models.Model):
    # ���� �������� �����������
    datec = models.DateTimeField(_('notification_create'), auto_now_add=True)
    # ���� � ����� ��������� �����������
    daten = models.DateTimeField(_('notification_date'))
    # ������
    client = models.ForeignKey(Client, related_name='notification_client', on_delete=models.CASCADE)
    # ����� �����������
    details = models.TextField(_('notification_details')) 
    # ���� ��������� �����������
    datev = models.DateTimeField(_('notification_viewed'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'notification'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['daten']),
        ]
        # ���������� �� ���������
        ordering = ['daten']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}, {}".format(self.daten, self.client, self.details)

# ���������
class Configuration(models.Model):
    # ���� ���������
    datec = models.DateTimeField(_('configuration_date'), auto_now_add=True)
    # ������, %
    discount = models.IntegerField(_('configuration_discount'), default=0)
    # ������ ��������
    #bonus = models.DecimalField(_('configuration_bonus'), max_digits=9, decimal_places=2)
    bonus = models.IntegerField(_('configuration_bonus'), default=0)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'configuration'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datec']),
        ]
        # ���������� �� ���������
        ordering = ['-datec']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}\t{}\t{}".format(self.dates, self.discount, self.bonus)

# ������� 
class Basket(models.Model):
    basketday = models.DateTimeField(_('basketday'), auto_now_add=True)
    catalog = models.ForeignKey(Catalog, related_name='basket_catalog', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    #user = models.ForeignKey(User, related_name='user_basket', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='basket_client', on_delete=models.CASCADE)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'basket'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['basketday']),
        ]
        # ���������� �� ���������
        ordering = ['basketday']
    # ����� �� ������
    def total(self):
        return self.price * self.quantity

# ������ �������
class Bonus(models.Model):
    # ���� ���������
    dateb = models.DateTimeField(_('bonus_date'), auto_now_add=True)
    # ������
    client = models.ForeignKey(Client, related_name='bonus_client', on_delete=models.CASCADE)
    # ����������� ������ 
    accrued = models.DecimalField(_('accrued'), max_digits=9, decimal_places=2)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'bonus'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # ���������� �� ���������
        ordering = ['-dateb']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}\t{}\t{}".format(self.dates, self.discount, self.bonus)

# ������ ������� 
class Review(models.Model):
    dater = models.DateTimeField(_('dater'), auto_now_add=True)
    client = models.ForeignKey(Client, related_name='review_client', on_delete=models.CASCADE)
    rating = models.IntegerField(_('rating'))
    details = models.TextField(_('review_details'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'review'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dater']),
        ]
        # ���������� �� ���������
        ordering = ['dater']

# ������� 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'news'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['daten']),
        ]
        # ���������� �� ���������
        ordering = ['daten']
