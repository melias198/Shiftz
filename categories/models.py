from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=200,blank=True)
    brand_img = models.ImageField(upload_to='photos/brands',blank=True)
    
    def __str__(self):
        return self.brand_name