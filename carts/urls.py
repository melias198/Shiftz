from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('<int:car_id>/',views.add_to_cart,name='add_cart'),
    path('remove/<int:car_id>/',views.remove_cart,name='remove_cart'),
    path('delete/<int:car_id>/',views.delete_cart,name='delete_cart'),
]
