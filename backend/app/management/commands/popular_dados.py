from django.core.management.base import BaseCommand
from app.models import Mecanica, Tema, Componente

class Command(BaseCommand):
    help = 'Popula dados iniciais com descrições'

    def handle(self, *args, **options):
        # Mecânicas com descrições
        mecanicas_data = [
            ('Alocação de Trabalhadores (Worker Placement)', 'Posicionar peões em locais do tabuleiro para bloquear a ação para outros e ganhar recursos.'),
            ('Construção de Baralho (Deck Building)', 'Jogadores compram cartas para melhorar seu próprio baralho durante a partida.'),
            ('Controle de Área (Area Control)', 'Ganhar bônus ou pontos por ter a maioria de unidades em um território específico.'),
            ('Colecionar Conjuntos (Set Collection)', 'Acumular itens do mesmo tipo para multiplicar a pontuação final.'),
            ('Draft de Cartas', 'Escolher uma carta de uma mão e passar o restante para o próximo jogador.'),
            ('Rolagem de Dados', 'Uso de dados para determinar o sucesso ou a força de uma ação.'),
            ('Gestão de Mão', 'Otimizar o uso das cartas que você possui para maximizar jogadas.'),
            ('Movimentação em Grid', 'Mover peças em um tabuleiro dividido em quadrados ou espaços definidos.'),
            ('Leilão / Licitação', 'Disputar um item ou recurso através de lances de moeda ou pontos.'),
            ('Colocação de Peças (Tile Placement)', 'Construir o mapa ou cenário encaixando peças como um quebra-cabeça.')
        ]
        
        # Temas com descrições
        temas_data = [
            ('Horror Lovecraftiano', 'Mistérios cósmicos e terror psicológico antigo.'),
            ('Investigação Criminal', 'Solução de crimes e busca por evidências.'),
            ('Gastronomia / Culinária', 'Gestão de cozinha e preparo de pratos.'),
            ('Comércio Marítimo', 'Troca de mercadorias entre portos históricos.'),
            ('Industrialização', 'O boom das fábricas e ferrovias do século XIX.'),
        ]

        # Componentes com descrições
        componentes_data = [
            ('Meeple de Madeira', 'Boneco humanoide que representa trabalhadores.'),
            ('Dados D6', 'O clássico dado de 6 faces para sorteios.'),
            ('Dados Poliédricos', 'Dados de 4, 8, 10, 12 ou 20 faces.'),
            ('Cartas Standard', 'Cartas de tamanho padrão de baralho.'),
            ('Cartas Mini', 'Versões reduzidas para economizar espaço na mesa.'),
        ]

        # Criar mecânicas
        for nome, descricao in mecanicas_data:
            Mecanica.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
        self.stdout.write(f'✅ {len(mecanicas_data)} mecânicas criadas')

        # Criar temas
        for nome, descricao in temas_data:
            Tema.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
        self.stdout.write(f'✅ {len(temas_data)} temas criados')

        # Criar componentes
        for nome, descricao in componentes_data:
            Componente.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
        self.stdout.write(f'✅ {len(componentes_data)} componentes criados')

        self.stdout.write(self.style.SUCCESS('🎉 Dados com descrições populados!'))