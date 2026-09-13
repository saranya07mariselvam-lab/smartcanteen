from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/<int:food_id>/', views.order_food, name='order_food'),
    path('orders/', views.order_list, name='order_list'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart, name='cart'),

path('increase-cart/<int:food_id>/', views.increase_cart, name='increase_cart'),
path('decrease-cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
path('place-cart-order/', views.place_cart_order, name='place_cart_order'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('register/', views.register_view, name='register'),
]