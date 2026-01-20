from django.core.management.base import BaseCommand
from app.models import Mecanica, Tema, Componente

class Command(BaseCommand):
    help = 'Popula dados iniciais com descrições'

    def handle(self, *args, **options):
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

        # Criar temas
        for nome, descricao in temas_data:
            Tema.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
        self.stdout.write(f'✅ {len(temas_data)} temas criados')

        # Criar componentes
        for nome, descricao in componentes_data:
            Componente.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
        self.stdout.write(f'✅ {len(componentes_data)} componentes criados')

        self.stdout.write(self.style.SUCCESS('🎉 Dados com descrições populados!'))