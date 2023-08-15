#serializers.py
# Сериализаторы позволяют преобразовывать сложные данные, такие как querysets и экземпляры моделей, 
# в нативные типы данных Python, которые затем могут быть легко срендерены в JSON, XML или другие типы контента. 
# Сериализаторы также обеспечивают десериализацию, позволяя преобразовать спарсенные данные обратно в сложные типы после проверки входящих данных.
from rest_framework import serializers
from .models import Category, Catalog, ViewCatalog, Bill, Detailing, News

class CategorySerializer(serializers.ModelSerializer ):
    class Meta:
        model = Category
        #fields = ("id", "title")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        #fields = ("id", "category_id", "title", "details", "price", "photo")
        # Обратите внимание, что внешний ключ category мы обозначаем как в модели, а не category_id, как в таблице.
        #fields = ("id", "category", "title", "details", "price", "photo")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"

class ViewCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCatalog
        #fields = ("id", "category_id", "category", "title", "details", "price", "photo")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        #fields = ("id", "dateb", "place", "total", "discount", "bonus", "amount")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"

class DetailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detailing
        #fields = ("id", "bill_id", "catalog_id", "price", "quantity")
        # Обратите внимание, что внешний ключ category мы обозначаем как в модели, а не category_id, как в таблице.
        #fields = ("id", "bill", "catalog_id", "price", "quantity")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = ("id", "daten", "title", "details", "photo")
        #Если в сериализаторе мы собираемся работать со всеми полями модели, то в классе Meta можно прописать:
        fields = "__all__"
