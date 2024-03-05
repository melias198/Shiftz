from django.shortcuts import render
from cars.models import Car

def home(request):
    cars = Car.objects.all()
    return render(request,'index.html',{'cars':cars})