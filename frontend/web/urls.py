from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('debug/', views.debug, name='debug'),
    path('jogos/', views.jogos_lista, name='jogos_lista'),
    path('jogos/novo/', views.jogo_novo, name='jogo_novo'),
    path('jogos/<int:jogo_id>/', views.jogo_detalhes, name='jogo_detalhes'),
    path('jogos/editar/<int:jogo_id>/', views.jogo_editar, name='jogo_editar'),
    path('jogos/imprimir/<int:jogo_id>/', views.jogo_imprimir, name='jogo_imprimir'),
    path('jogos/excluir/<int:jogo_id>/', views.jogo_excluir, name='jogo_excluir'),
    path('mecanicas/', views.mecanicas_lista, name='mecanicas_lista'),
    path('mecanicas/novo/', views.mecanica_novo, name='mecanica_novo'),
    path('mecanicas/editar/<int:item_id>/', views.mecanica_editar, name='mecanica_editar'),
    path('componentes/', views.componentes_lista, name='componentes_lista'),
    path('componentes/novo/', views.componente_novo, name='componente_novo'),
    path('componentes/editar/<int:item_id>/', views.componente_editar, name='componente_editar'),
    path('temas/', views.temas_lista, name='temas_lista'),
    path('temas/novo/', views.tema_novo, name='tema_novo'),
    path('temas/editar/<int:item_id>/', views.tema_editar, name='tema_editar'),
    path('mecanicas/excluir/<int:item_id>/', views.mecanica_excluir, name='mecanica_excluir'),
    path('componentes/excluir/<int:item_id>/', views.componente_excluir, name='componente_excluir'),
    path('temas/excluir/<int:item_id>/', views.tema_excluir, name='tema_excluir'),
    path('api/<path:path>', views.api_proxy, name='api_proxy'),
]