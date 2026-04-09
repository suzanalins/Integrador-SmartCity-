from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
import pandas as pd
from rest_framework.decorators import api_view, action, permission_classes
from .models import Sensor, Microcontroladores, Historico, Locais, Responsaveis, Ambiente
from .serializers import SensorSerializer, MicrocontroladoresSerializer, HistoricoSerializer, LocaisSerializer, ResponsaveisSerializer, AmbienteSerializer, UsuariosSerializer


class UsuariosViewSet(ModelViewSet):
  



