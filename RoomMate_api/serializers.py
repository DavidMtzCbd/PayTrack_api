from rest_framework import serializers
from rest_framework.authtoken.models import Token
from RoomMate_api.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class ClienteSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Cliente
        fields = "__all__"

class PropiedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propiedades
        fields = '__all__'