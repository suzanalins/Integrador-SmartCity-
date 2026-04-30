from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import *


#aqui ta definindo as rotas da api
router = DefaultRouter()
router.register(r'locais', LocaisViewSet)
router.register(r'responsaveis', ResponsaveisViewSet)
router.register(r'ambientes', AmbienteViewSet)
router.register(r'microcontroladores', MicrocontroladoresViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'historicos', HistoricoViewSet)

urlpatterns = [
    #pegando as rotas p autenticação JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#aqui vc coloca o username e a password e ele te da 2 tipos de token, op refresh e o acess
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), #pra o refresh funcionar vc precisa passar o token de refresh no json

    #puxando o caminho p registrar um novo user
    path('register/', RegisterView.as_view(), name='register'),

    #puxando o caminho p pegar os dados do user já logado
    path('me/', UsuarioMeView.as_view(), name='me'),
    path('', include(router.urls)),
]

