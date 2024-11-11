from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return "Perfil del cliente"+self.first_name
    
class Propiedades(models.Model):
    id = models.BigAutoField(primary_key=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    habitaciones = models.CharField(max_length=255, null=True, blank=True)
    capacidad = models.CharField(max_length=255, null=True, blank=True)
    precio = models.CharField(max_length=255, null=True, blank=True)
    servicios_json = models.TextField(null=True, blank=True)
    sanitarios = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    estados = models.CharField(max_length=255, null=True, blank=True)
    imagenes = models.JSONField(default=list)
    
    def __str__(self):
        return f"Propiedad: {self.direccion}, capacidad: {self.capacidad}"