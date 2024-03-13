from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.sign_up,name='register'),
    path('login/',views.sign_in,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.sign_out,name='logout'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('order_history/',views.order_history,name='history'),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('order_complete/',views.order_complete,name='completed'),
    path('track/',views.track_order,name='track'),
    path('transactions_history/',views.transaction_history,name='transaction_history'),
    path('transaction_details/<int:id>',views.transaction_details,name='transaction_details'),
    path('admin_orders/',views.orders_admin,name='admin_orders'),
    path('admin_order_details/<int:id>',views.admin_order_details,name='admin_order_details'),
    path('order_updates/<int:id>',views.admin_update,name='update'),
    path('status_updates/<int:id>',views.update_status,name='update_status'),
    path('brands/',views.brand_view,name='brand_view'),
    path('brand_upload/',views.brand_upload,name='brand_upload'),
    path('brand_update/<int:id>',views.brand_update,name='brand_update'),
    path('brand_delete/<int:id>',views.delete_brand,name='brand_delete'),
    path('cars_view/',views.car_view,name='car_view'),
    path('car_upload/',views.car_upload,name='car_upload'),
    path('car_update/<int:id>',views.car_update,name='car_update'),
    path('car_delete/<int:id>',views.delete_car,name='car_delete'),
]
