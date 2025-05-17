"""point_experts_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from PayTrack_api.views import bootstrap
from PayTrack_api.views import users
from PayTrack_api.views import auth
from PayTrack_api.views import pagos

urlpatterns = [
    #Version
        path('bootstrap/version', bootstrap.VersionView.as_view()),
    #Crear Cliente/Usuario
        path('usuarios/', users.ClienteView.as_view()),
    #Editar Cliente/Usuario
        path('usuarios-edit/',users.ClienteViewEdit.as_view()),
    #Login
        path('token/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),
    #Create Pagos
        path('pagos/', pagos.PagosView.as_view()),
    #List Pagos
        path('lista-pagos/', pagos.PagosAll.as_view()),
    #Editar Pagos
        path('pagos-edit/', pagos.PagosViewEdit.as_view()),
    
]
