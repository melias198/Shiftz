from django.contrib import admin
from .models import Car

# Register your models here.
class AdminCar(admin.ModelAdmin):
    prepopulated_fields = {'slug':('car_name',)}
    list_display = ['id','car_name','slug','vin','price','stock','brand','is_available','created_date','modified_date']
admin.site.register(Car,AdminCar)