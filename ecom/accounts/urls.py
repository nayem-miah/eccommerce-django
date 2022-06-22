from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('forget/', views.forget, name='forget'),
    path('terms/', views.terms, name='terms'),
    
]
