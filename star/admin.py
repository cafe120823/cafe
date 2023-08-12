from django.contrib import admin

from .models import Category, Catalog, Basket, Bill, Detailing, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Basket)
admin.site.register(Bill)
admin.site.register(Detailing)
admin.site.register(News)
