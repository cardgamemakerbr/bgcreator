from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Jogo, Mecanica, Tema, Componente, CondicoesVitoria, CondicoesDerrota, EstruturaJogo, CondicoesEspeciais, Glossario
from .serializers import (JogoSerializer, JogoCreateSerializer, MecanicaSerializer, 
                         TemaSerializer, ComponenteSerializer, CondicoesVitoriaSerializer,
                         CondicoesDerrotaSerializer, EstruturaJogoSerializer, 
                         CondicoesEspeciaisSerializer, GlossarioSerializer)

class MecanicaViewSet(viewsets.ModelViewSet):
    queryset = Mecanica.objects.all()
    serializer_class = MecanicaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome', 'subtitulo', 'descricao_curta']
    filterset_fields = ['mecanicas', 'temas', 'idade_recomendada']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JogoCreateSerializer
        return JogoSerializer
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca personalizada por nome, ID, mecânica ou tema"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Parâmetro q é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        jogos = Jogo.objects.filter(
            Q(nome__icontains=query) |
            Q(id__icontains=query) |
            Q(mecanicas__nome__icontains=query) |
            Q(temas__nome__icontains=query)
        ).distinct()
        
        serializer = self.get_serializer(jogos, many=True)
        return Response(serializer.data)

class CondicoesVitoriaViewSet(viewsets.ModelViewSet):
    queryset = CondicoesVitoria.objects.all()
    serializer_class = CondicoesVitoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jogo']

class CondicoesDerrotaViewSet(viewsets.ModelViewSet):
    queryset = CondicoesDerrota.objects.all()
    serializer_class = CondicoesDerrotaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jogo']

class EstruturaJogoViewSet(viewsets.ModelViewSet):
    queryset = EstruturaJogo.objects.all()
    serializer_class = EstruturaJogoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jogo', 'tipo']

class CondicoesEspeciaisViewSet(viewsets.ModelViewSet):
    queryset = CondicoesEspeciais.objects.all()
    serializer_class = CondicoesEspeciaisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estrutura']

class GlossarioViewSet(viewsets.ModelViewSet):
    queryset = Glossario.objects.all()
    serializer_class = GlossarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['jogo']
    search_fields = ['palavra', 'definicao']