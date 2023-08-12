#serializers.py
# ������������� ��������� ��������������� ������� ������, ����� ��� querysets � ���������� �������, 
# � �������� ���� ������ Python, ������� ����� ����� ���� ����� ���������� � JSON, XML ��� ������ ���� ��������. 
# ������������� ����� ������������ ��������������, �������� ������������� ���������� ������ ������� � ������� ���� ����� �������� �������� ������.
from rest_framework import serializers
from .models import Catalog, ViewCatalog

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ("id", "category_id", "title", "details", "price", "photo")

class ViewCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCatalog
        fields = ("id", "category_id", "category", "title", "details", "price", "photo")
