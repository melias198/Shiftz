from django import forms
from .models import Car
from categories.models import Brand


brands = Brand.objects.all()
cars = Car.objects.all()

BRAND = ((i.slug,i) for i in brands)
CARS = ((i.slug,i) for i in cars)

BRAND_WITH_PLACEHOLDER = [("", "Select Brand")] + list(BRAND)
CARS_WITH_PLACEHOLDER = [("", "Select Car")] + list(CARS)

class CarFilterForm(forms.Form):
    brand = forms.ChoiceField(choices=BRAND_WITH_PLACEHOLDER,required=False,label="Brand Filter")
    model = forms.ChoiceField(choices=CARS_WITH_PLACEHOLDER,required=False,label="Model Filter")