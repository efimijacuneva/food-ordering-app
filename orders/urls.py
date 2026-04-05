from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.menu, name='menu'),
#     path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
#     path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('place_order/', views.place_order, name='place_order'),
#     path('order_success/', views.order_success, name='order_success'),
    
#     path('order_history/', views.order_history, name='order_history'),
#     path('register/', views.register, name='register'),
#     path('restaurant_dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
#     path('order/<int:order_id>/update_status/', views.update_order_status, name='update_order_status'),

#     path('menu/', views.menu, name='menu'),
#     path('menu/<str:category>/', views.menu_by_category, name='menu_by_category'),

# ]

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/<str:category>/', views.menu_by_category, name='menu_by_category'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('restaurant_dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('order_history/', views.order_history, name='order_history'),
    path('register/', views.register, name='register'),
]