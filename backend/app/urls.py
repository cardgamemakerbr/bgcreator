from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import (JogoViewSet, MecanicaViewSet, TemaViewSet, ComponenteViewSet,
                   CondicoesVitoriaViewSet, CondicoesDerrotaViewSet, EstruturaJogoViewSet,
                   CondicoesEspeciaisViewSet, GlossarioViewSet)

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'BGCreator API',
        'endpoints': {
            'jogos': '/api/jogos/',
            'mecanicas': '/api/mecanicas/',
            'temas': '/api/temas/',
            'componentes': '/api/componentes/',
        }
    })

router = DefaultRouter()
router.register(r'jogos', JogoViewSet)
router.register(r'mecanicas', MecanicaViewSet)
router.register(r'temas', TemaViewSet)
router.register(r'componentes', ComponenteViewSet)
router.register(r'condicoes-vitoria', CondicoesVitoriaViewSet)
router.register(r'condicoes-derrota', CondicoesDerrotaViewSet)
router.register(r'estruturas', EstruturaJogoViewSet)
router.register(r'condicoes-especiais', CondicoesEspeciaisViewSet)
router.register(r'glossario', GlossarioViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/', include(router.urls)),
]