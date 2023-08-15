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
        
# ���� (�����)
class Bill(models.Model):
    dateb = models.DateTimeField(_('dateb'), auto_now_add=True)
    # ������
    place = models.CharField(_('place'), max_length=32)
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
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}, {}: {}".format(self.dateb, self.place, self.amount)

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

    
# ������� 
class Basket(models.Model):
    basketday = models.DateTimeField(_('basketday'), auto_now_add=True)
    catalog = models.ForeignKey(Catalog, related_name='basket_catalog', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'), default=1)
    user = models.ForeignKey(User, related_name='user_basket', on_delete=models.CASCADE)
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
