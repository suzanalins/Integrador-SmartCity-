from django.db import models
from django.contrib.auth.models import User



class Usuarios(models.Model):
    TIPO_CHOICES = [
        ('admin', 'Administrador'), 
        ('user', 'Usuário Comum'),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nome= models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome


class Locais(models.Model):
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.local


class Responsaveis(models.Model):
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return self.responsavel

class Status(models.TextChoices):
    ACTIVE = 'A', 'Ativo'
    INACTIVE = 'I', 'Inativo'


class Ambiente(models.Model):
   local = models.ForeignKey (Locais, on_delete=models.CASCADE, related_name='ambientes')
   descricao = models.TextField()
   responsavel = models.ForeignKey (Responsaveis, on_delete=models.CASCADE, related_name='ambientes')

   def __str__(self):
        return self.local.local


class Sensor(models.Model):
    SENSOR_CHOICES =[
        ('temperatura', 'Temperatura'), 
        ('umidade', 'Umidade'), 
        ('luminosidade', 'Luminosidade'), 
        ('contador', 'Contador'),
    ]

    UNIDADEMED_CHOICES = [
        ('°C', 'Graus Celsius'),
        ('%', 'Porcentagem'),
        ('lux', 'Lux'),
        ('uni', 'Unidades'),
    ]

    sensor =models.CharField(max_length=100, choices=SENSOR_CHOICES)
    unidade_medida = models.CharField(max_length=20, choices=UNIDADEMED_CHOICES)
    microcontrolador = models.ForeignKey('Microcontroladores', on_delete=models.CASCADE, related_name='sensores')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return self.sensor


class Historico(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='historicos')
    valor = models.FloatField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class Microcontroladores(models.Model):
    modelo = models.CharField(max_length=100)
    mac_adress = models.CharField(max_length=17, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.ACTIVE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, related_name='microcontroladores')

    def __str__(self):
        return self.modelo