from django.urls import path
from . import views

urlpatterns = [
    path('store/',views.cars,name='store'),
    path('<slug:brand_slug>/<slug:car_slug>/',views.car_details,name='car_details'),
   
]
