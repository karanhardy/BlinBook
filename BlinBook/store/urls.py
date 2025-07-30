from django.urls import path
from . import views
from .views import order_history, store_home

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name= 'update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-sucess/', views.order_success, name='order_success'),
    path('orders/',order_history, name='order_history'),
    path('', store_home, name='store_home'),
]



