#serializers.py
# ������������� ��������� ��������������� ������� ������, ����� ��� querysets � ���������� �������, 
# � �������� ���� ������ Python, ������� ����� ����� ���� ����� ���������� � JSON, XML ��� ������ ���� ��������. 
# ������������� ����� ������������ ��������������, �������� ������������� ���������� ������ ������� � ������� ���� ����� �������� �������� ������.
from rest_framework import serializers
from .models import Category, Catalog, ViewCatalog, Bill, Detailing, News

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

class DetailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detailing
        #fields = ("id", "bill_id", "catalog_id", "price", "quantity")
        # �������� ��������, ��� ������� ���� category �� ���������� ��� � ������, � �� category_id, ��� � �������.
        #fields = ("id", "bill", "catalog_id", "price", "quantity")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = ("id", "daten", "title", "details", "photo")
        #���� � ������������� �� ���������� �������� �� ����� ������ ������, �� � ������ Meta ����� ���������:
        fields = "__all__"
