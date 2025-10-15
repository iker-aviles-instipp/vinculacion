from django.contrib import admin
from django.urls import path, include
from paciente import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name='base'),
    # SISTEMA
    path('agendarCi/', views.agendarCi, name='agendarCi'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('registroInsu/', views.registroInsu, name='registroInsu'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #CITAS
    path('agendarCi/guardar/', views.agendarCi_guardar, name='agendarCi_guardar'),
    

    # INSUMOS
    path('crear_insumo/', views.crear_insumo, name='crear_insumo'),
    path('registroInsu/editar/<int:pk>/', views.editar_insumo, name='editar_insumo'),
    path('registroInsu/eliminar/<int:pk>/', views.eliminar_insumo, name='eliminar_insumo'),
  
]
