import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from app.models import Jogo, Mecanica, Tema, Componente

class JogoModelTest(TestCase):
    def setUp(self):
        self.mecanica = Mecanica.objects.create(nome="Deck Building")
        self.tema = Tema.objects.create(nome="Medieval")
        self.componente = Componente.objects.create(nome="Cartas")
        
    def test_criar_jogo(self):
        jogo = Jogo.objects.create(
            nome="Teste Game",
            descricao_curta="Um jogo de teste",
            jogadores_min=2,
            jogadores_max=4,
            tempo_min=30,
            tempo_max=60,
            idade_recomendada=12
        )
        self.assertEqual(jogo.nome, "Teste Game")
        self.assertEqual(jogo.peso, 0.1)
        
    def test_calculo_peso(self):
        jogo = Jogo.objects.create(
            nome="Jogo Complexo",
            descricao_curta="Um jogo complexo",
            jogadores_min=2,
            jogadores_max=4,
            tempo_min=120,
            tempo_max=180,
            idade_recomendada=14
        )
        jogo.mecanicas.add(self.mecanica)
        jogo.componentes.add(self.componente)
        jogo.save()
        
        # Peso base (0.1) + tempo (0.4) + mecânica (0.1) + componente (0.1) = 0.7
        self.assertGreater(jogo.peso, 0.1)

class JogoAPITest(APITestCase):
    def setUp(self):
        self.mecanica = Mecanica.objects.create(nome="Worker Placement")
        
    def test_criar_jogo_via_api(self):
        url = reverse('jogo-list')
        data = {
            'nome': 'Novo Jogo API',
            'descricao_curta': 'Criado via API',
            'jogadores_min': 1,
            'jogadores_max': 4,
            'tempo_min': 45,
            'tempo_max': 90,
            'idade_recomendada': 10,
            'mecanicas_ids': [self.mecanica.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_buscar_jogos(self):
        jogo = Jogo.objects.create(
            nome="Jogo Buscável",
            descricao_curta="Para teste de busca",
            jogadores_min=2,
            jogadores_max=6,
            tempo_min=60,
            tempo_max=120,
            idade_recomendada=12
        )
        
        url = reverse('jogo-buscar')
        response = self.client.get(url, {'q': 'Buscável'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class MecanicaAPITest(APITestCase):
    def test_crud_mecanica(self):
        # Create
        url = reverse('mecanica-list')
        data = {'nome': 'Area Control', 'descricao': 'Controle de território'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Read
        mecanica_id = response.data['id']
        response = self.client.get(f'{url}{mecanica_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update
        data_update = {'nome': 'Area Control Updated'}
        response = self.client.patch(f'{url}{mecanica_id}/', data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete
        response = self.client.delete(f'{url}{mecanica_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)