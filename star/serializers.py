#serializers.py
# ������������� ��������� ��������������� ������� ������, ����� ��� querysets � ���������� �������, 
# � �������� ���� ������ Python, ������� ����� ����� ���� ����� ���������� � JSON, XML ��� ������ ���� ��������. 
# ������������� ����� ������������ ��������������, �������� ������������� ���������� ������ ������� � ������� ���� ����� �������� �������� ������.
from rest_framework import serializers
from .models import Category, Catalog, ViewCatalog, Bill, ViewBill, Detailing, ViewDetailing, Reservation, Notification, Configuration, Client, Bonus, Review, News

class CategorySerializer(serializers.ModelSerializer ):
    class Meta:
        model = Category
        #fields = ("id", "title")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        #fields = ("id", "category_id", "title", "details", "price", "photo")
        # �������� ��������, ��� ������� ���� category �� ���������� ��� � ������, � �� category_id, ��� � �������.
        #fields = ("id", "category", "title", "details", "price", "photo")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ViewCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCatalog
        #fields = ("id", "category_id", "category", "title", "details", "price", "photo")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        #fields = ("id", "dateb", "place", "total", "discount", "bonus", "amount")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ViewBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewBill
        #fields = ("id", "dateb", "place", "total", "discount", "bonus", "amount", "detailing")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class DetailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detailing
        #fields = ("id", "bill_id", "catalog_id", "price", "quantity")
        # �������� ��������, ��� ������� ���� category �� ���������� ��� � ������, � �� category_id, ��� � �������.
        #fields = ("id", "bill", "catalog_id", "price", "quantity")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ViewDetailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewDetailing
        #fields = ("id", "bill_id", "dateb", "place", "total", "discount", "bonus", "amount", "catalog_id", "category", "title", "details", "photo", "price", "quantity", "detailing_total")
        # �������� ��������, ��� ������� ���� category �� ���������� ��� � ������, � �� category_id, ��� � �������.
        #fields = ("id", "bill", "dateb", "place", "total", "discount", "bonus", "amount", "catalog", "category", "title", "details", "photo", "price", "quantity", "detailing_total")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        #fields = ("id", "datea", "dater", "client", "quantity", "details", "comments")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        #fields = ("id", "datec", "daten", "client", "details", "datev")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        #fields = ("id", "datec", "discount", "bonus")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        #fields = ("id", "email", "password", "name", "phone", "birthday")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        #fields = ("id", "dateb", "client_id", "accrued")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        #fields = ("id", "dater", "client_id", "rating", "details")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = ("id", "daten", "title", "details", "photo")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"
