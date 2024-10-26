from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from seguimiento_bus.models import Usuario
from seguimiento_bus.serializers import UsuarioSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def usuario_view(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            obj = Usuario.objects.get(pk=pk)
            serializer = UsuarioSerializer(obj)
            return Response(serializer.data)
        else:
            obj = Usuario.objects.all()
            serializer = UsuarioSerializer(obj, many = True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data = request.data)
        if serializer.is_valid():
            usuario = serializer.save() # guarda al usuario
            token, create= Token.objects.get_or_create(user = usuario)# creacmos el token 
            return Response({'usuario':serializer.data, 'token':token.key},status= status.HTTP_201_CREATED )
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view (['POST'])
@permission_classes([AllowAny]) 
def login_view(request):
    correo = request.data.get('correo')
    password = request.data.get('password')
    # Verifica si el usuario existe antes de autenticar
    try:
        usuario = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    

    usuario = authenticate(request,username=correo, password = password)
    if usuario is not None: 
        # authenticacion exitosa, devuelve el token 
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key})
    else:
        # athenticacion fallida
        return Response({'error':'Credeneciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)
