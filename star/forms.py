from django import forms
from django.forms import CheckboxInput, ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Category, Catalog, Bill, Detailing, Reservation, Notification, Configuration, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Каталог (меню)
class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('category', 'title', 'details', 'price', 'availability', 'photo')
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 5}),            
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'availability': CheckboxInput(attrs={"size":"100"}),            
        }
        labels = {
            'category': _('category'),
        }
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

#  Счет (заказ)
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('place',)
        widgets = {
            'place': TextInput(attrs={"size":"30"}),
        }
    # Метод-валидатор для поля daten
    def clean_dateb(self):        
        if isinstance(self.cleaned_data['dateb'], datetime) == True:
            data = self.cleaned_data['dateb']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Детализация заказа
class DetailingForm(forms.ModelForm):
    class Meta:
        model = Detailing
        fields = ('catalog', 'quantity')
        widgets = {
            'catalog': forms.Select(attrs={'class': 'chosen'}),
            'quantity': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }
        labels = {
            'catalog': _('catalog'),
        }
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Бронирование
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['comments',]
        widgets = {
            'comments': Textarea(attrs={'cols': 100, 'rows': 5}),               
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Уведомления
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['daten', 'client', 'details']
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'client': forms.Select(attrs={'class': 'chosen'}),
            'details': Textarea(attrs={'cols': 100, 'rows': 5}),               
        }
        labels = {
            'client': _('client'),
        }

# Настройки
class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ('discount', 'bonus',)
        widgets = {
            'discount': NumberInput(attrs={"size":"10", "min": "0", "max": "99", "step": "1"}),     
            'bonus': NumberInput(attrs={"size":"10", "min": "0", "max": "99", "step": "1"}),     
        }
    # Метод-валидатор для поля title
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если начинается не с большой буквы
        if data.istitle() == False:
            raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
