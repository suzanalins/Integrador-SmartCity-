from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework import viewsets
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .filters import *
from .serializers import *
import pandas as pd
from rest_framework.decorators import api_view, action, permission_classes
from .models import Sensor, Microcontroladores, Historico, Locais, Responsaveis, Ambiente
from .serializers import SensorSerializer, MicrocontroladoresSerializer, HistoricoSerializer, LocaisSerializer, ResponsaveisSerializer, AmbienteSerializer, UsuariosSerializer



class RegisterView(generics.CreateAPIView): #registrar novo usuário
    serializer_class = RegisterSerializer #puxando o serializer 
    permission_classes = [permissions.AllowAny] #qualquer pesso acessa mesmo sem autenticacao



class UsuarioMeView(generics.RetrieveAPIView):
    serializer_class = UsuarioMeSerializer
    permission_classes = [permissions.IsAuthenticated]#precisa de autenticação para acessar

    def get_object(self):
        return self.request.user.perfil


class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [permissions.IsAuthenticated]



class ResponsaveisViewSet(viewsets.ModelViewSet):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes = [permissions.IsAuthenticated]



class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer
    permission_classes = [permissions.IsAuthenticated]



class MicrocontroladoresViewSet(viewsets.ModelViewSet):
    queryset = Microcontroladores.objects.all()
    serializer_class = MicrocontroladoresSerializer
    permission_classes = [permissions.IsAuthenticated]


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]


class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]