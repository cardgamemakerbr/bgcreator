from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('', views.home, name='home'),
    path('debug/', views.debug, name='debug'),
    path('jogos/', views.jogos_lista, name='jogos_lista'),
    path('jogos/novo/', views.jogo_novo, name='jogo_novo'),
    path('jogos/<int:jogo_id>/', views.jogo_detalhes, name='jogo_detalhes'),
    path('jogos/copiar/<int:jogo_id>/', views.jogo_copiar, name='jogo_copiar'),
    path('jogos/editar/<int:jogo_id>/', views.jogo_editar, name='jogo_editar'),
    path('jogos/revisao/<int:jogo_id>/', views.jogo_revisao, name='jogo_revisao'),
    path('jogos/revisao-leitura/<int:jogo_id>/', views.jogo_revisao_leitura, name='jogo_revisao_leitura'),
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
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/novo/', views.usuario_novo, name='usuario_novo'),
    path('usuarios/editar/<int:user_id>/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/excluir/<int:user_id>/', views.usuario_excluir, name='usuario_excluir'),
    path('usuarios/bloquear/<int:user_id>/', views.usuario_bloquear, name='usuario_bloquear'),
    path('usuarios/configurar-complexidade/', views.configurar_complexidade_senha, name='configurar_complexidade_senha'),
    path('backup/', views.backup_sistema, name='backup_sistema'),
    path('backup/download/<str:filename>/', views.backup_download, name='backup_download'),
    path('backup/delete/<str:filename>/', views.backup_delete, name='backup_delete'),
    path('ajax/cadastrar-mecanica/', views.cadastrar_mecanica_rapido, name='cadastrar_mecanica_rapido'),
    path('ajax/cadastrar-tema/', views.cadastrar_tema_rapido, name='cadastrar_tema_rapido'),
    path('ajax/cadastrar-componente/', views.cadastrar_componente_rapido, name='cadastrar_componente_rapido'),
    path('api/<path:path>', views.api_proxy, name='api_proxy'),
]