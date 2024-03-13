from django.urls import path
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('success/', views.success_view, name='success_view'),
    path('payment/faild/',views.faild_view,name='faild'),
    path('order_track/<int:id>/', views.user_order_track, name="order_track"),
]
