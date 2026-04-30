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
    nome = serializers.CharField(write_only=True)
    telefone = serializers.CharField(write_only=True)
    tipo_usuario = serializers.ChoiceField(choices=Usuarios.TIPO_CHOICES, write_only= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nome', 'telefone', 'tipo_usuario']


    #validando se o username já existe, se existir ele não deixa criar o usuario
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username já existe.")
        return value
    

    def validate_email(self, value):  
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email já existe.")
            return value


    def create(self, validated_data):
        #criando o usuario na tabela api_usuarios
        nome = validated_data.get('nome', '')# o validated_data armazena os dados que foram passados na requisição (JSON, formulário) e passaram com sucesso por todas as regras de validação
        email = validated_data.get('email', '')
        telefone = validated_data.get('telefone', '')
        tipo_usuario = validated_data.get('tipo_usuario', '')


        #Criando na tabela auth_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        #ate aqui ok

        if tipo_usuario == 'user': #se o tipo do usuario for user ele nao tem acesso a parte admin
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
        
        elif tipo_usuario == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
        
        else: 
            user.delete() #se o tipo do usuario for diferente de user ou admin ele deleta o usuario criado na tabela auth_user e nao cria o usuario na tabela api_usuarios
            raise serializers.ValidationError("Tipo de usuário inválido. Escolha 'admin' ou 'user'.")
        
    
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