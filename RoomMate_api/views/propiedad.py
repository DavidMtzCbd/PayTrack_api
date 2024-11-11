from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from RoomMate_api.serializers import *
from RoomMate_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
import string
import random
import json


class PropiedadesAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        propiedades = Propiedades.objects.filter(user__is_active = 1).order_by("id")
        propiedades = PropiedadesSerializer(propiedades, many=True).data
        #Aquí convertimos los valores de nuevo a un array
        if not propiedades:
            return Response({},400)
        for propiedad in propiedades:
            propiedad["servicios_json"] = json.loads(propiedad["servicios_json"])

        return Response(propiedades, 200)

class PropiedadesView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        propiedad = get_object_or_404(Propiedades, id = request.GET.get("id"))
        propiedad = PropiedadesSerializer(propiedad, many=False).data
        propiedad["servicios_json"] = json.loads(propiedad["servicios_json"])
        return Response(propiedad, 200)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Obtener los datos de la solicitud POST
         propiedad = Propiedades.objects.create(
                                            direccion= request.data["direccion"],
                                            habitaciones= request.data["habitaciones"],
                                            capacidad= request.data["capacidad"],
                                            precio= request.data["precio"],
                                            servicios_json = json.dumps(request.data["servicios_json"]),
                                            sanitarios= request.data["sanitarios"],
                                            telefono= request.data["telefono"],
                                            estados=request.data["estados"])
         propiedad.save() 
         imagen_urls = []
         if 'imagenes' in request.FILES:
            for img in request.FILES.getlist('imagenes'):
                image_path = f'imagenes_propiedades/{img.name}'
                with open(f'{settings.MEDIA_ROOT}/{image_path}', 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)
                imagen_urls.append(f'{settings.MEDIA_URL}{image_path}')

        # Almacenar las URLs de las imágenes en el campo JSON
         propiedad.imagenes = imagen_urls
         propiedad.save()
         
         
         
         return Response({"propiedad_created_id": propiedad.id }, 201)
     
     
    #Se tiene que modificar la parte de edicion y eliminar
class PropiedadViewEdit(generics.CreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        propiedad = get_object_or_404(Propiedades, id=request.data["id"])
        propiedad.direccion = request.data["direccion"]
        propiedad.habitaciones = request.data["habitaciones"]
        propiedad.capacidad = request.data["capacidad"]
        propiedad.precio = request.data["precio"]
        propiedad.servicios_json = json.dumps(request.data["servicios_json"])
        propiedad.sanitarios = request.data["sanitarios"]
        propiedad.telefono =  request.data["telefono"]
        propiedad.estados =  request.data["estados"]
        propiedad.save()
        temp = propiedad
        temp.direccion = request.data["direccion"]
        temp.capacidad = request.data["capacidad"]
        temp.save()
        propiedades = PropiedadesSerializer(propiedad, many=False).data

        return Response(propiedades,200)
    
    def delete(self, request, *args, **kwargs):
        propiedad = get_object_or_404(Propiedades, id=request.GET.get("id"))
        try:
            propiedad.delete()
            return Response({"details":"Propiedad eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)