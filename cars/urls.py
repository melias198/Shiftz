from django.urls import path
from . import views

urlpatterns = [
    path('store/',views.cars,name='store'),
    path('brand/<slug:brand_slug>/',views.cars,name='cars_by_brand'),
    path('car/<slug:car_slug>/',views.cars,name='car_by_model'),
    path('search/',views.search_view,name='search_by_cars'),
    path('filter/',views.filter_view,name='filter_by_cars'),
    path('<slug:brand_slug>/<slug:car_slug>/',views.car_details,name='car_details'),
   
]
