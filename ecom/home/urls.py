from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name='home' ),
    path('delivery/', views.delivery, name='delivery'),
    path('contact/', views.contact, name='contact'),
]
