from urllib import request
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



def converter_status(valor):
    """Converte boolean ou string para formato da API (A/I)"""
    if valor in [True, 'True', 'true', 1, '1', 'T', 't', 'Ativo', 'ativo', 'A', 'a']:
        return 'A'
    return 'I'


#criando popular sensores
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_locais(request):
    arquivo = request.FILES.get('file')
    print("Lindomar", request.FILES.get('file'))
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        if 'local' not in df.columns:
            return Response({"detail": "Coluna 'local' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        for _, row in df.iterrows():
            obj, created = Locais.objects.get_or_create(local=row["local"])
            if created:
                inseridos += 1
        
        return Response({"detail": f"Importação concluída! {inseridos} locais inseridos."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


#criando popular responsaveis
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_responsaveis(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        if 'responsavel' not in df.columns:
            return Response({"detail": "Coluna 'responsavel' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        for _, row in df.iterrows():
            obj, created = Responsaveis.objects.get_or_create(responsavel=row["responsavel"])
            if created:
                inseridos += 1
        
        return Response({"detail": f"Importação concluída! {inseridos} responsáveis inseridos."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


#criando popular ambientes
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_ambientes(request):
    print(request.FILES)
    print(request.content_type) 
    print(request.FILES.keys())
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(arquivo)
        colunas_esperadas = ["local", "descricao", "responsavel"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response({"detail": f"Coluna '{coluna}' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        erros = []
        
        for idx, row in df.iterrows():
            local_id = int(row["local"])
            responsavel_id = int(row["responsavel"])
            descricao = row["descricao"]  
            
            if not Locais.objects.filter(id=local_id).exists():
                erros.append(f"Linha {idx+2}: Local ID {local_id} não existe")
                continue
                
            if not Responsaveis.objects.filter(id=responsavel_id).exists():
                erros.append(f"Linha {idx+2}: Responsável ID {responsavel_id} não existe")
                continue
            
            Ambiente.objects.create(
                local_id=local_id,
                descricao=descricao,
                responsavel_id=responsavel_id
            )
            inseridos += 1
        
        mensagem = f"Importação concluída! {inseridos} ambientes inseridos."
        if erros:
            mensagem += f" Erros: {'; '.join(erros[:5])}"
        
        return Response({"detail": mensagem}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


#criando popular microcontroladores
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def popular_microcontroladores(request):
    arquivo = request.FILES.get('file')
    if not arquivo:
        return Response({"error": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
    
    print(request.FILES)
    try:
        df = pd.read_excel(arquivo)
        print(df.columns)
        colunas_esperadas = ["modelo", "mac_address", "latitude", "longitude", "status", "ambiente"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                return Response({"detail": f"Coluna '{coluna}' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        for _, row in df.iterrows():
            ambiente_id = int(row["ambiente"])
            if not Ambiente.objects.filter(id=ambiente_id).exists():
                return Response({"detail": f"Ambiente ID {ambiente_id} não existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            status_value = converter_status(row["status"])
            
            obj, created = Microcontroladores.objects.get_or_create(
                mac_adress=row["mac_address"],
                defaults={
                    'modelo': row["modelo"],
                    'latitude': row["latitude"],
                    'longitude': row["longitude"],
                    'status': status_value,
                    'ambiente_id': ambiente_id
                }
            )
            if created:
                inseridos += 1
        
        return Response({"detail": f"Importação concluída! {inseridos} microcontroladores inseridos."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


#criando popular sensores
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
                return Response({"detail": f"Coluna '{coluna}' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        for _, row in df.iterrows():
            mic_id = int(row["mic"])
            if not Microcontroladores.objects.filter(id=mic_id).exists():
                return Response({"detail": f"Microcontrolador ID {mic_id} não existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            sensor_nome = row["sensor"].lower()
            status_value = converter_status(row["status"])
            
            Sensor.objects.create(
                sensor=sensor_nome,
                unidade_medida=row["unidade_med"],
                microcontrolador_id=mic_id,
                status=status_value
            )
            inseridos += 1
        
        return Response({"detail": f"Importação concluída! {inseridos} sensores inseridos."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


#criando popular historicos
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
                return Response({"detail": f"Coluna '{coluna}' obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        inseridos = 0
        for _, row in df.iterrows():
            sensor_id = int(row["sensor"])
            if not Sensor.objects.filter(id=sensor_id).exists():
                return Response({"detail": f"Sensor ID {sensor_id} não existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            Historico.objects.create(
                sensor_id=sensor_id,
                valor=row["valor"],
                time_stamp=row["timestamp"] 
            )
            inseridos += 1
        
        return Response({"detail": f"Importação concluída! {inseridos} históricos inseridos."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)