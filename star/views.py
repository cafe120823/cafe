from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Category, Catalog, ViewCatalog, Basket, Bill, Detailing, News
# Подключение cериализаторов
from .serializers import CategorySerializer, CatalogSerializer, ViewCatalogSerializer, BillSerializer, DetailingSerializer, NewsSerializer
from rest_framework import viewsets
# Подключение форм
from .forms import CategoryForm, CatalogForm, BillForm, DetailingForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        #catalog = ViewCatalog.objects.all().order_by('?')[0:4]
        #reviews = ViewSale.objects.exclude(rating=None).order_by('?')[0:4]
        news1 = News.objects.all().order_by('-daten')[0:1]
        news24 = News.objects.all().order_by('-daten')[1:4]
        #return render(request, "index.html", {"catalog": catalog, "reviews": reviews, "news1": news1, "news24": news24})    
        return render(request, "index.html", {"news1": news1, "news24": news24})    
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

## Отчеты
#@login_required
#@group_required("Managers")
#def report_index(request):
#    try:
#        catalog = ViewCatalog.objects.all().order_by('title')
#        sale = ViewSale.objects.all().order_by('saleday')
#        delivery = Delivery.objects.all().order_by('deliveryday')
#        review = ViewSale.objects.exclude(rating=None).order_by('category', 'title', 'saleday')
#        return render(request, "report/index.html", {"catalog": catalog, "sale": sale, "delivery": delivery, "review": review })    
#    except Exception as exception:
#        print(exception)
#        return HttpResponse(exception)    

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# ModelViewSet - это специальное представление, которое предоставляет Django Rest Framework. Он обрабатывает GET и POST без дополнительной работы.
# Класс ModelViewSet наследуется от GenericAPIView и реализует различные действия, совмещая функционал различных классов миксинов.
# Класс ModelViewSet предоставляет следующие действия .list(), .retrieve(), .create(), .update(), .partial_update(), и .destroy(). 
class categoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # http://127.0.0.1:8000/api/category/

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request):
    try:
        #catalog = Catalog.objects.all().order_by('title')
        #invoice = Invoice.objects.get(id=invoice_id)
        catalog = Catalog.objects.all().order_by('title')
        return render(request, "catalog/index.html", {"catalog": catalog, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    
    
# Список для просмотра и отправки в корзину
#@login_required
def catalog_list(request):
    try:
        # Категории и подкатегория товара (для поиска)
        category = Category.objects.all().order_by('title')
        # Подчситать количество товара в корзине доступны записи только текущего пользователя
        # Текущий пользователь
        _user_id = request.user.id
        # Только доступный товар
        catalog = ViewCatalog.objects.all()    
        # Доступны записи только текущего пользователя
        basket = Basket.objects.filter(user_id=_user_id).order_by('basketday')
        # Количество товара в корзине и общая стоимость товарв в корзине для пользователя _user_id
        basket_count, basket_total = basket_count_total(_user_id)   

        #print(basket_count)        
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по категории товара
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    catalog = catalog.filter(category=selected_item_category).all()
                # Поиск по названию товара
                catalog_search = request.POST.get("catalog_search")
                #print(catalog_search)                
                if catalog_search != '':
                    catalog = catalog.filter(title__contains = catalog_search).all()
                # Сортировка
                sort = request.POST.get('radio_sort')
                #print(sort)
                direction = request.POST.get('checkbox_sort_desc')
                #print(direction)
                if sort=='title':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-title')
                    else:
                        catalog = catalog.order_by('title')
                elif sort=='price':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-price')
                    else:
                        catalog = catalog.order_by('price')
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "selected_item_category": selected_item_category, "catalog_search": catalog_search , "sort": sort, "direction": direction })
            elif 'resetBtn' in request.POST:          
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category,  })
            else:
                # Выделить id товара
                catalog_id = request.POST.dict().get("catalog_id")
                print("catalog_id ", catalog_id)
                price = request.POST.dict().get("price")
                #print("price ", price)
                user = request.POST.dict().get("user")
                #print("user ", user)
                # Отправить товар в корзину
                basket = Basket()
                basket.catalog_id = catalog_id
                basket.price = float(int(price.replace(",00","")))
                #basket.price = price
                basket.user_id = user
                basket.save()
                message = _('Item added to basket')
                basket_count = Basket.objects.filter(user_id=_user_id).count()
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "mess": message, "basket_count": basket_count })         
        else:
            return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "basket_count": basket_count,})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            if 'photo' in request.FILES:                
                catalog.photo = request.FILES['photo']
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index',))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def catalog_edit(request, id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            if 'photo' in request.FILES:
                catalog.photo = request.FILES['photo']
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', ))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform, })            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price, 'photo': catalog.photo, })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform, })
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index', ))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = ViewCatalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None).order_by('-saleday')
        return render(request, "catalog/details.html", {"catalog": catalog, })
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

# ModelViewSet - это специальное представление, которое предоставляет Django Rest Framework. Он обрабатывает GET и POST без дополнительной работы.
# Класс ModelViewSet наследуется от GenericAPIView и реализует различные действия, совмещая функционал различных классов миксинов.
# Класс ModelViewSet предоставляет следующие действия .list(), .retrieve(), .create(), .update(), .partial_update(), и .destroy(). 
class catalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    # http://127.0.0.1:8000/api/catalog/

class viewCatalogViewSet(viewsets.ModelViewSet):
    queryset = ViewCatalog.objects.all()
    serializer_class = ViewCatalogSerializer
    # http://127.0.0.1:8000/api/viewcatalog/

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def bill_index(request):
    try:
        bill = Bill.objects.all().order_by('dateb')
        return render(request, "bill/index.html", {"bill": bill,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def bill_create(request):
    try:
        if request.method == "POST":
            bill = Bill()
            bill.place = request.POST.get("place")
            billform = BillForm(request.POST)
            if billform.is_valid():
                bill.save()
                return HttpResponseRedirect(reverse('bill_index'))
            else:
                return render(request, "bill/create.html", {"form": billform})
        else:        
            billform = BillForm()
            return render(request, "bill/create.html", {"form": billform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def bill_edit(request, id):
    try:
        bill = Bill.objects.get(id=id)
        if request.method == "POST":
            bill.place = request.POST.get("place")
            billform = BillForm(request.POST)
            if billform.is_valid():
                bill.save()
                return HttpResponseRedirect(reverse('bill_index'))
            else:
                return render(request, "bill/edit.html", {"form": billform})
        else:
            # Загрузка начальных данных
            billform = BillForm(initial={'place': bill.place, })
            return render(request, "bill/edit.html", {"form": billform})
    except Bill.DoesNotExist:
        return HttpResponseNotFound("<h2>Bill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def bill_delete(request, id):
    try:
        bill = Bill.objects.get(id=id)
        bill.delete()
        return HttpResponseRedirect(reverse('bill_index'))
    except Bill.DoesNotExist:
        return HttpResponseNotFound("<h2>Bill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def bill_read(request, id):
    try:
        bill = Bill.objects.get(id=id) 
        return render(request, "bill/read.html", {"bill": bill})
    except Bill.DoesNotExist:
        return HttpResponseNotFound("<h2>Bill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# ModelViewSet - это специальное представление, которое предоставляет Django Rest Framework. Он обрабатывает GET и POST без дополнительной работы.
# Класс ModelViewSet наследуется от GenericAPIView и реализует различные действия, совмещая функционал различных классов миксинов.
# Класс ModelViewSet предоставляет следующие действия .list(), .retrieve(), .create(), .update(), .partial_update(), и .destroy(). 
class billViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    # http://127.0.0.1:8000/api/bill/

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def detailing_index(request, bill_id):
    try:
        #detailing = Detailing.objects.all().order_by('title')
        invoice = Invoice.objects.get(id=bill_id)
        detailing = Detailing.objects.filter(bill_id=bill_id).order_by('title')
        return render(request, "detailing/index.html", {"detailing": detailing, "invoice": invoice, "bill_id": bill_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def detailing_create(request, bill_id):
    try:
        if request.method == "POST":
            detailing = Detailing()
            detailing.bill_id = bill_id
            detailing.category = Category.objects.filter(id=request.POST.get("category")).first()
            detailing.title = request.POST.get("title")
            detailing.details = request.POST.get("details")        
            detailing.price = request.POST.get("price")
            detailing.quantity = request.POST.get("quantity")
            if 'photo' in request.FILES:                
                detailing.photo = request.FILES['photo']
            detailingform = DetailingForm(request.POST)
            if detailingform.is_valid():
                detailing.save()
                return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
            else:
                return render(request, "detailing/create.html", {"form": detailingform})
        else:        
            detailingform = DetailingForm()
            return render(request, "detailing/create.html", {"form": detailingform, "bill_id": bill_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def detailing_edit(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id) 
        if request.method == "POST":
            detailing.category = Category.objects.filter(id=request.POST.get("category")).first()
            detailing.title = request.POST.get("title")
            detailing.details = request.POST.get("details")        
            detailing.price = request.POST.get("price")
            detailing.quantity = request.POST.get("quantity")
            if 'photo' in request.FILES:
                detailing.photo = request.FILES['photo']
            detailingform = DetailingForm(request.POST)
            if detailingform.is_valid():
                detailing.save()
                return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
            else:
                return render(request, "detailing/edit.html", {"form": detailingform, "bill_id": bill_id})            
        else:
            # Загрузка начальных данных
            detailingform = DetailingForm(initial={'category': detailing.category, 'subcategory': detailing.subcategory, 'title': detailing.title, 'details': detailing.details, 'price': detailing.price, 'quantity': detailing.quantity, 'photo': detailing.photo, })
            #print('->',detailing.photo )
            return render(request, "detailing/edit.html", {"form": detailingform, "bill_id": bill_id})
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def detailing_delete(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id)
        detailing.delete()
        return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def detailing_read(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id) 
        return render(request, "detailing/read.html", {"detailing": detailing, "bill_id": bill_id})
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# ModelViewSet - это специальное представление, которое предоставляет Django Rest Framework. Он обрабатывает GET и POST без дополнительной работы.
# Класс ModelViewSet наследуется от GenericAPIView и реализует различные действия, совмещая функционал различных классов миксинов.
# Класс ModelViewSet предоставляет следующие действия .list(), .retrieve(), .create(), .update(), .partial_update(), и .destroy(). 
class detailingViewSet(viewsets.ModelViewSet):
    queryset = Detailing.objects.all()
    serializer_class = DetailingSerializer
    # http://127.0.0.1:8000/api/detailing/

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def detailing_index(request, bill_id):
    try:
        #detailing = Detailing.objects.all().order_by('title')
        bill = Bill.objects.get(id=bill_id)
        detailing = Detailing.objects.filter(bill_id=bill_id)
        return render(request, "detailing/index.html", {"detailing": detailing, "bill": bill, "bill_id": bill_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def detailing_create(request, bill_id):
    try:
        if request.method == "POST":
            detailing = Detailing()
            detailing.bill_id = bill_id
            detailing.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            detailing.quantity = request.POST.get("quantity")
            detailingform = DetailingForm(request.POST)
            if detailingform.is_valid():
                detailing.save()
                return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
            else:
                return render(request, "detailing/create.html", {"form": detailingform})
        else:        
            detailingform = DetailingForm()
            return render(request, "detailing/create.html", {"form": detailingform, "bill_id": bill_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def detailing_edit(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id) 
        if request.method == "POST":
            detailing.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            detailing.quantity = request.POST.get("quantity")
            detailingform = DetailingForm(request.POST)
            if detailingform.is_valid():
                detailing.save()
                return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
            else:
                return render(request, "detailing/edit.html", {"form": detailingform, "bill_id": bill_id})            
        else:
            # Загрузка начальных данных
            detailingform = DetailingForm(initial={'catalog': detailing.catalog, 'quantity': detailing.quantity, })
            #print('->',detailing.photo )
            return render(request, "detailing/edit.html", {"form": detailingform, "bill_id": bill_id})
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def detailing_delete(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id)
        detailing.delete()
        return HttpResponseRedirect(reverse('detailing_index', args=(bill_id,)))
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def detailing_read(request, id, bill_id):
    try:
        detailing = Detailing.objects.get(id=id) 
        return render(request, "detailing/read.html", {"detailing": detailing, "bill_id": bill_id})
    except Detailing.DoesNotExist:
        return HttpResponseNotFound("<h2>Detailing not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Количество товара в корзине и общая стоимость товарв в корзине для пользователя _user_id
def basket_count_total(_id):
    try:
        # Количество товара в корзине и общая стоимость товарв в корзине для пользователя _user_id
        count = 0        
        total = 0
        # Текущий пользователь _user_id
        # Доступны записи только текущего пользователя
        basket = Basket.objects.filter(user_id=_id)
        # Подсчитать стоимость товара в корзине
        if basket.count() > 0:
            count = basket.count()
            for b in basket:
                total = total + b.price*b.quantity
        print(count)        
        print(total)        
        return count, total
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Корзина
@login_required
def basket(request):
    try:
        # Текущий пользователь
        _user_id = request.user.id
        # Доступны записи только текущего пользователя
        basket = Basket.objects.filter(user_id=_user_id).order_by('basketday')
        # Количество товара в корзине и общая стоимость товарв в корзине для пользователя _user_id
        basket_count, basket_total = basket_count_total(_user_id)   
        #print(total)        
        place = request.POST.get('place')
        # Если это подтверждение какого-либо действия
        if request.method == "POST":        
            # Увеличение или уменьшение количества товара в корзине
            if ('btn_plus' in request.POST) or ('btn_minus' in request.POST):
                # Выделить id записи в корзине и количество товара       
                basket_id = request.POST.dict().get("basket_id")
                quantity = request.POST.dict().get("quantity")
                # Найти запись в корзине
                basket = Basket.objects.get(id=basket_id)
                # Изменить запись в корзине
                if 'btn_plus' in request.POST:
                    basket.quantity = basket.quantity + 1
                if 'btn_minus' in request.POST:
                    if basket.quantity > 1:
                        basket.quantity = basket.quantity - 1
                # Сохранить
                basket.save()
                # Доступны записи только текущего пользователя
                basket = Basket.objects.filter(user_id=_user_id).order_by('basketday')
                # Подсчитать количество и стоимость товара в корзине
                basket_count, basket_total = basket_count_total(_user_id)        
                return render(request, "catalog/basket.html", {"basket": basket,  "basket_count": basket_count, "basket_total": basket_total,})
            # Приобретение, если нажата кнопка Buy
            if 'buy' in request.POST:
                # Добавить счет (заказ)
                bill = Bill()
                bill.place = request.POST.get('place')
                bill.save()
                bill_id= Bill.objects.order_by('-id')[:1].values_list('id')[0][0]
                #print("Сохранен заказ id " + str(bill_id))
                # Перебрать всю корзину отправить ее в детализацию заказ!
                for b in basket:
                    # Добавить в продажи
                    detailing = Detailing()
                    detailing.bill_id = int(bill_id)
                    detailing.catalog_id = b.catalog_id
                    detailing.price = b.price
                    detailing.quantity = b.quantity
                    detailing.save()
                    #print("Сохранено")
                # Очистить корзину
                basket.delete()
                #print("Корзина очищена")
                # Перейти к совершенным покупкам
                return HttpResponseRedirect(reverse("bill_index"))
        else:
            return render(request, "catalog/basket.html", {"basket": basket, "basket_count": basket_count, "basket_total": basket_total, "place": place})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление из корзины
@login_required
def basket_delete(request, id):
    try:
        basket = Basket.objects.get(id=id)                
        basket.delete()
        # Текущий пользователь
        _user_id = request.user.id
        # Доступны записи только текущего пользователя
        basket = Basket.objects.filter(user_id=_user_id).order_by('basketday')
        # Подсчитать стоимость товара в корзине
        basket_total = 0
        for b in basket:
            basket_total = basket_total + b.price*b.quantity    
        return render(request, "catalog/basket.html", {"basket": basket, "basket_total": basket_total})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Basket not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
## Список приобретения + Оставление отзыва
#@login_required
#def buy(request):
#    try:
#        # Текущий пользователь
#        # Текущий пользователь
#        _user_id = request.user.id
#        # Доступны записи только текущего пользователя
#        basket = Basket.objects.filter(user_id=_user_id).order_by('basketday')
#        # Количество товара в корзине и общая стоимость товарв в корзине для пользователя _user_id
#        basket_count, basket_total = basket_count_total(_user_id)  
#        # Доступны записи только текущего пользователя
#        sale = ViewSale.objects.filter(user_id=_user_id).order_by('-saleday')  
#        return render(request, "catalog/buy.html", {"sale": sale, "basket_count": basket_count, "basket_total": basket_total})        
#    except Exception as exception:
#        print(exception)
#        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        #news = News.objects.all().order_by('surname', 'name', 'patronymic')
        #return render(request, "news/index.html", {"news": news})
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/list.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']        
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:        
            #newsform = NewsForm(request.FILES, initial={'daten': datetime.now().strftime('%Y-%m-%d'),})
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# ModelViewSet - это специальное представление, которое предоставляет Django Rest Framework. Он обрабатывает GET и POST без дополнительной работы.
# Класс ModelViewSet наследуется от GenericAPIView и реализует различные действия, совмещая функционал различных классов миксинов.
# Класс ModelViewSet предоставляет следующие действия .list(), .retrieve(), .create(), .update(), .partial_update(), и .destroy(). 
class newsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # http://127.0.0.1:8000/api/news/

###################################################################################################    

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

