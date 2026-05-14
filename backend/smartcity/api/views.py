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
        try:
            return self.request.user.perfil
        except:
            from rest_framework.exceptions import NotFound
            raise NotFound("Perfil de usuário não encontrado.")


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




#criando população dos locais com base no exel passado
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_locais(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["local"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    


#criando população dos responsaveis com base no exel passado
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_responsaveis(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["responsavel"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    

#criando população dos ambientes com base no exel passado
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  
def popular_ambientes(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    

    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["local","ambiente", "responsavel"]
        for coluna in colunas_esperadas: #se no exel nao existir uma das colunas esperadas ele diz que é obrigatoria
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
   
            for _, row in df.iterrows():
                local_id = int(row["local"])
                responsavel_id = int(row["responsavel"])
                ambiente_nome = row["ambiente"]

            if not Locais.objects.filter(id=local_id).exists():
                return Response(
                    {"detail":f"Local ID: {local_id} não existe..."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            if not Responsaveis.objects.filter(id=responsavel_id).exists():
                return Response(
                    {"detail":f"Responsavel ID: {responsavel_id} não existe..."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            Ambiente.objects.create(
                local_id=row["local"],  
                ambiente_nome= row["ambiente"],
                responsavel_id=row["responsavel"]
            )

            return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

#criando população dos microcontroladores com base no exel passado  
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  
def popular_microcontroladores(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["modelo", "mac_address", "latitude", "longitude", "status", "ambiente"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            for _, row in df.iterrows():
                ambiente_id = int(row["ambiente"])
                if not Ambiente.objects.filter(id=ambiente_id).exists():
                    return Response(
                        {"detail":f"Ambiente ID: {ambiente_id} não existe..."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                Microcontroladores.objects.create(
                    modelo=row["modelo"],
                    mac_adress=row["mac_address"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    status=row["status"],
                    ambiente_id=row["ambiente"]
                )

        return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    

#criando população dos sensores com base no exel passado
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_sensores(request):  
    arquivo = request.FILES.get('file') 
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["sensor", "unidade_med", "mic", "status"]

        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            for _, row in df.iterrows():
                mic_id = int(row["mic"])
                if not Microcontroladores.objects.filter(id=mic_id).exists():
                    return Response(
                        {"detail":f"Microcontrolador ID: {mic_id} não existe..."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                Sensor.objects.create(
                    sensor=row["sensor"],
                    unidade_medida=row["unidade_med"],
                    microcontrolador_id=row["mic"],
                    status=row["status"]
                )
        return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    

#criando população dos historicos com base no exel passado
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_historicos(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["sensor", "valor", "timestamp"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response(
                    {"detail":f"Coluna {coluna} obrigatória."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            for _, row in df.iterrows():
                sensor_id = int(row["sensor"])
                if not Sensor.objects.filter(id=sensor_id).exists():
                    return Response(
                        {"detail":f"Sensor ID: {sensor_id} não existe..."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                Historico.objects.create(
                    sensor_id=row["sensor"],
                    valor=row["valor"],
                    data_hora=row["timestamp"]
                )
        return Response(
            {"detail":"Importação concluida com sucesso..."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"detail":f"Erro ao importar o arquivo {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
