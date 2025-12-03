from django.contrib import admin
from django.urls import path, include
from paciente import views
from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name='base'),
    # SISTEMA
    path('agendarCi/', views.agendarCi, name='agendarCi'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path("documentacion/", views.documentacion, name="documentacion"),
path("documentacion/ver/<int:paciente_id>/", views.ver_documento, name="ver_documento"), # Usamos paciente_id
path("documentacion/eliminar/<int:documento_id>/", views.eliminar_documento, name="eliminar_documento"), # Usamos documento_id
    path('registroInsu/', views.registroInsu, name='registroInsu'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #CITAS
    #path('agendarCi/guardar/', views.agendarCi_guardar, name='agendarCi_guardar'),

    path('agendarCi/', views.agendarCi, name='agendarCi'),
    path('agendarCi/guardar/', views.agendarCi_guardar, name='agendarCi_guardar'),
    path('agendarCi/editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('agendarCi/eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),


    # INSUMOS
    path('crear_insumo/', views.crear_insumo, name='crear_insumo'),
    path('registroInsu/editar/<int:pk>/', views.editar_insumo, name='editar_insumo'),
    path('registroInsu/eliminar/<int:pk>/', views.eliminar_insumo, name='eliminar_insumo'),
    # Rutas para el reseteo de contraseña
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), 
         name="reset_password"),

    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
         name="password_reset_complete"),

    path('api/', include('api_rest.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  
]
