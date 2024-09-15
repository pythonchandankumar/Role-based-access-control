"""
URL configuration for role_base_access_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('create/',BlogCreateview.as_view(),name='create'),
    path('list/',BlogGetview.as_view(),name='list'),
    path('update/<int:pk>/',BlogUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',BlogDelete.as_view(),name='delete'),
]
