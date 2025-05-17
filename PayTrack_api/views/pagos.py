from django.shortcuts import render, get_object_or_404
from django.db.models import *
from django.conf import settings
from django.http import JsonResponse
from PayTrack_api.serializers import *
from PayTrack_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
import json
 
 
class PagosAll(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        pagos = Pagos.objects.all().order_by("id")
        pagos = PagosSerializer(pagos, many=True).data
 
        return Response(pagos, status=status.HTTP_200_OK)
 
 
class PagosView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pagos = Pagos.objects.create(
            monto=request.data["monto"],
            fecha=request.data["fecha"],
            tipo=request.data["tipo"],
        )
        pagos.save()

 
        return Response({"pago_created_id": pagos.id}, status=status.HTTP_201_CREATED)
 
 
class PagosViewEdit(generics.CreateAPIView):
    def put(self, request, *args, **kwargs):
        pagos = get_object_or_404(Pagos, id=request.data["id"])
        pagos.monto = request.data["monto"]
        pagos.fecha = request.data["fecha"]
        pagos.tipo = request.data["tipo"]
   
        pagos.save()
 
        pagos = PagosSerializer(pagos, many=False).data
        return Response(pagos, status=status.HTTP_200_OK)
 
    def delete(self, request, *args, **kwargs):
        pagos = get_object_or_404(Pagos, id=request.GET.get("id"))
        try:
            pagos.delete()
            return Response({"details": "Pago eliminado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error al eliminar el pago"}, status=status.HTTP_400_BAD_REQUEST)
 
 
