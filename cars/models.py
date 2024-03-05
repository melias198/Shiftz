from django.db import models
from categories.models import Brand
# Create your models here.

class Car(models.Model):
    car_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    vin = models.CharField(max_length=17,unique=True)
    description = models.TextField(max_length=255,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/cars')
    stock = models.IntegerField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.car_name
    