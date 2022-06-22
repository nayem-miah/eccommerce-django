from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.Products.as_view(), name='products' ),
    path('product-id/<str:unique_id>/', views.Products_detail.as_view(), name='detail' ),
    path('cart/', views.Cart_view.as_view(), name='cart' ),
    path('add-to-cart/<str:unique_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<str:unique_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('delete-cart/<str:unique_id>/', views.delete_cart, name="delete_cart"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('payment/', views.Payment_view.as_view(), name="payment"),

]
