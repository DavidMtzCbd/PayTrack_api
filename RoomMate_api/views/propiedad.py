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
import base64



class PropiedadesAll(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        propiedades = Propiedades.objects.filter(cliente__user__is_active=True).order_by("id")
        propiedades = PropiedadesSerializer(propiedades, many=True).data

        for propiedad in propiedades:
            # Convertir las imágenes de la propiedad a base64
            if propiedad.get("imagenes"):
                propiedad["imagenes"] = []
                for img_path in propiedad["imagenes"]:
                    with open(f'{settings.MEDIA_ROOT}/{img_path}', 'rb') as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        propiedad["imagenes"].append(f"data:image/jpeg;base64,{encoded_string}")

        return Response(propiedades, status=status.HTTP_200_OK)

class PropiedadesView(generics.CreateAPIView):
    # Obtener los datos de la solicitud POST
    def post(self, request, *args, **kwargs):
        propiedad = Propiedades.objects.create(
            direccion=request.data["direccion"],
            habitaciones=request.data["habitaciones"],
            capacidad=request.data["capacidad"],
            precio=request.data["precio"],
            servicios_json=json.dumps(request.data["servicios_json"]),
            sanitarios=request.data["sanitarios"],
            telefono=request.data["telefono"],
            estados=request.data["estados"]
        )
        propiedad.save()

        imagenes_base64 = []
        if 'imagenes' in request.FILES:
            for img in request.FILES.getlist('imagenes'):
                # Abrir la imagen y convertirla a base64
                with open(f'{settings.MEDIA_ROOT}/imagenes_propiedades/{img.name}', 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)
                
                with open(f'{settings.MEDIA_ROOT}/imagenes_propiedades/{img.name}', 'rb') as image_file:
                    # Leer la imagen y convertir a base64
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    imagenes_base64.append(f"data:image/jpeg;base64,{encoded_string}")

        # Almacenar las imágenes codificadas en base64
        propiedad.imagenes = imagenes_base64
        propiedad.save()

        return Response({"propiedad_created_id": propiedad.id}, status=status.HTTP_201_CREATED)
     
     
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