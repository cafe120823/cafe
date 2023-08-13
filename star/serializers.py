#serializers.py
# ������������� ��������� ��������������� ������� ������, ����� ��� querysets � ���������� �������, 
# � �������� ���� ������ Python, ������� ����� ����� ���� ����� ���������� � JSON, XML ��� ������ ���� ��������. 
# ������������� ����� ������������ ��������������, �������� ������������� ���������� ������ ������� � ������� ���� ����� �������� �������� ������.
from rest_framework import serializers
from .models import Category, Catalog, ViewCatalog, Bill, Detailing, News

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ("id", "category_id", "title", "details", "price", "photo")

class ViewCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCatalog
        fields = ("id", "category_id", "category", "title", "details", "price", "photo")

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ("id", "dateb", "place", "total", "discount", "bonus", "amount")

class DetailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detailing
        fields = ("id", "bill_id", "catalog_id", "price", "quantity")

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("id", "daten", "title", "details", "photo")
