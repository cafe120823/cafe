#serializers.py
# —ериализаторы позвол€ют преобразовывать сложные данные, такие как querysets и экземпл€ры моделей, 
# в нативные типы данных Python, которые затем могут быть легко срендерены в JSON, XML или другие типы контента. 
# —ериализаторы также обеспечивают десериализацию, позвол€€ преобразовать спарсенные данные обратно в сложные типы после проверки вход€щих данных.
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
