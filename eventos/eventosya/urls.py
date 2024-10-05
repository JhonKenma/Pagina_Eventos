from django.urls import path
from .views import inicio, registro, login_view, listarEventos, logout_view,detalle_evento,panel_vistas # Importa listarEventos directamente
from . import views
urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('eventos/', views.listarEventos, name='listarEventos'),  # Usar la vista importada
    path('eventos/nuevo/', views.crear_evento, name='crear_evento'),
    path('eventos/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/detalle/<int:evento_id>/', detalle_evento, name='detalle_evento'),
    
    path('eventos/registrarse/<int:evento_id>/', views.registrarse_evento, name='registrarse_evento'),
    
    path('eventos/<int:evento_id>/registrados/', views.ver_registrados, name='ver_registrados'),
    
    path('panel-vistas/', panel_vistas, name='panel_vistas'),

]
