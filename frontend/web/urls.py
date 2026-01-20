from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('debug/', views.debug, name='debug'),
    path('jogos/', views.jogos_lista, name='jogos_lista'),
    path('jogos/novo/', views.jogo_novo, name='jogo_novo'),
    path('jogos/<int:jogo_id>/', views.jogo_detalhes, name='jogo_detalhes'),
    path('jogos/editar/<int:jogo_id>/', views.jogo_editar, name='jogo_editar'),
    path('jogos/excluir/<int:jogo_id>/', views.jogo_excluir, name='jogo_excluir'),
    path('mecanicas/', views.mecanicas_lista, name='mecanicas_lista'),
    path('mecanicas/novo/', views.mecanica_novo, name='mecanica_novo'),
    path('componentes/', views.componentes_lista, name='componentes_lista'),
    path('componentes/novo/', views.componente_novo, name='componente_novo'),
    path('temas/', views.temas_lista, name='temas_lista'),
    path('temas/novo/', views.tema_novo, name='tema_novo'),
    path('api/<path:path>', views.api_proxy, name='api_proxy'),
]