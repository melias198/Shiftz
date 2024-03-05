from django.contrib import admin
from .models import Brand

# Register your models here.
class AdminBrand(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}
    list_display = ['id','brand_name','slug']
admin.site.register(Brand,AdminBrand)