import django_filters
from .models import Sensor, Microcontroladores, Historico, Locais, Responsaveis, Ambiente, Usuarios

class UsuariosFilter(django_filters.FilterSet):
    class Meta:
        model = Usuarios
        fields = {
            'nome': ['icontains'], #vai filtrar por nome ou parte do nome igual a string dada
            'email': ['exact'], #tem que ser exatamente igual a string dada
            'telefone': ['exact'],
            'tipo_usuario': ['exact']
        }

class LocaisFilter(django_filters.FilterSet):
    class Meta:
        model = Locais
        fields = {
            'local': ['icontains']
        }

class ResponsaveisFilter(django_filters.FilterSet):
    class Meta:
        model = Responsaveis
        fields = {
            'responsavel': ['icontains']
        }

class AmbienteFilter(django_filters.FilterSet):
    class Meta:
        model = Ambiente
        fields = {
            'local': ['exact'],
            'descricao': ['icontains'],
            'responsavel': ['exact']
        }

class SensorFilter(django_filters.FilterSet):
    class Meta:
        model = Sensor
        fields = {
            'sensor': ['exact'],
            'unidade_medida': ['exact'],
            'microcontrolador': ['exact'],
            'status': ['exact']
        }

class MicrocontroladoresFilter(django_filters.FilterSet):
    class Meta:
        model = Microcontroladores
        fields = {
            'modelo': ['icontains'],
            'mac_adress': ['exact'],
            'latitude': ['exact'],
            'longitude': ['exact'],
            'status': ['exact'],
            'ambiente': ['exact']
        }

class HistoricoFilter(django_filters.FilterSet):
    class Meta:
        model = Historico
        fields = {
            'sensor': ['exact'],
            'valor': ['exact'],
            'time_stamp': ['exact']
        }