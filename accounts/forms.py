from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from orders.models import Order
from categories.models import Brand
from cars.models import Car

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        

class BrandForm(forms.ModelForm):
    class Meta:
        model =Brand
        fields = '__all__'
        
    
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'