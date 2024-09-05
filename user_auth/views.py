from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import User_Auth

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    fullname = request.data.get('fullname')
    weight = request.data.get('weight')
    
    if User_Auth.objects.filter(email=email).exists():
        return Response({'message': 'Email já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User_Auth.objects.create(
        email=email,
        password=password,
        fullname=fullname,
        weight=weight,
    )
    
    return Response({'message': 'Usuário registrado com sucesso!'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User_Auth.objects.get(email=email)
    except User_Auth.DoesNotExist:
        return Response({'message': 'Usuário ou Senha incorretos'}, status=status.HTTP_404_NOT_FOUND)
    
    if check_password(password, user.password):
        return Response({'message': 'Login realizado com sucesso!', 'id': user.id}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Usuário ou Senha incorretos'}, status=status.HTTP_400_BAD_REQUEST)
