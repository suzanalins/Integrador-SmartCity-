from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    #criando a tabela auth_user
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    #criando tabela api_usuarios
    nome = serializers.CharField()
    telefone = serializers.CharField()
    tipo_usuario = serializers.ChoiceField(choices=Usuarios.TIPO_CHOICES)


    def create(self, validated_data):
        #criando o usuario na tabela api_usuarios

        nome = validated_data['nome', '']# o validated_data armazena os dados que foram passados na requisição (JSON, formulário) e passaram com sucesso por todas as regras de validação
        email = validated_data['email',]
        telefone = validated_data['telefone', '']
        tipo_usuario = validated_data['tipo_usuario', '']


        #Criando na tabela auth_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        if tipo_usuario == 'user': #se o tipo do usuario for user ele nao tem acesso a parte admin
            user.is_staff = False
        
        elif tipo_usuario == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
        
        else: 
            raise serializers.ValidationError("Tipo de usuário inválido. Escolha 'admin' ou 'user'.")
        
        user.is_active = True
        user.is_superuser = False
        user.save()#salva o tipo_usuario

        Usuarios.objects.create(
            user = user,
            nome = nome if nome else user.username,
            email = email,
            telefone = telefone,
            tipo_usuario = tipo_usuario
        ) #adciona as informações criadas no auth_user para a tabela Usuarios
        return user


class UsuarioMeSerializer(serializers.ModelSerializer): #aqui esta perguntando o que o usuario é e o que ele tem acesso
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'is_staff', 'is_superuser', 'is_active', 'nome', 'telefone', 'tipo_usuario'] #aqui é oq ele precisa mostrar para o usuario


class LocaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = '__all__'

class ResponsaveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsaveis
        fields = '__all__'


class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'


class MicrocontroladoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microcontroladores
        fields = '__all__'