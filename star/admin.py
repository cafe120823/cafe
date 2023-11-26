from django.contrib import admin

from .models import Category, Catalog, Basket, Bill, Detailing, Reservation, Configuration, Client, Bonus, Review, Notification, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Basket)
admin.site.register(Bill)
admin.site.register(Detailing)
admin.site.register(Reservation)
admin.site.register(Client)
admin.site.register(Configuration)
admin.site.register(Bonus)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(News)
