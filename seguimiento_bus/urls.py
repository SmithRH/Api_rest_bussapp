from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.routers import DefaultRouter
from seguimiento_bus import views

urlpatterns = [
    path('usuarios/', views.usuario_view, name= 'usuarios'),
    path('usuarios/<int:pk>/', views.usuario_view, name= 'usuarios-detail'),
    path('login/',views.login_view, name='login' ),
]

