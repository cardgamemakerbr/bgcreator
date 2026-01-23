from django.contrib import admin
from .models import Jogo, Mecanica, Tema, Componente

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'peso', 'jogadores_min', 'jogadores_max', 'created_at']
    list_filter = ['peso', 'idade_recomendada', 'created_at']
    search_fields = ['nome', 'subtitulo']

@admin.register(Mecanica)
class MecanicaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']