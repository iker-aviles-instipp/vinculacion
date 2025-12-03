from django.urls import path, include
from rest_framework import routers
from api_rest import api_views 

# Crea un router y registra las ViewSets
router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'profiles', api_views.ProfileViewSet)
router.register(r'pacientes', api_views.PacientesViewSet) 
router.register(r'citas', api_views.CitaViewSet)         
router.register(r'insumos', api_views.InsumoViewSet)     
router.register(r'documentos', api_views.DocumentoViewSet) 


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]