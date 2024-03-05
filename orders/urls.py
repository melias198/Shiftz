from django.urls import path
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('success/', views.success_view, name='success_view'),
]
