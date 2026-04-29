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
    #adm do django
    path('admin/', admin.site.urls),

    #pegando as rotas p autenticação JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #puxando o caminho p registrar um novo user
    path('api/register/', RegisterView.as_view(), name='register'),

    #puxando o caminho p pegar os dados do user já logado
    path('api/me/', UsuarioMeView.as_view(), name='me'),

    #rotas automaticsd p os cruds
    path('api/', include(router.urls)),
]