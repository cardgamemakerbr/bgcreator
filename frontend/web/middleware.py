from django.conf import settings
from django.core.exceptions import DisallowedHost
import json
from pathlib import Path

class DynamicHostsMiddleware:
    """Middleware para gerenciar hosts confiáveis dinamicamente"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.data_file = 'data/bgcreator_data.json'
    
    def __call__(self, request):
        # Carregar hosts confiáveis do arquivo de dados
        hosts_confiaveis = self.carregar_hosts_confiaveis()
        
        # Atualizar CSRF_TRUSTED_ORIGINS dinamicamente
        if hosts_confiaveis:
            # Adicionar protocolos aos hosts
            trusted_origins = []
            for host in hosts_confiaveis:
                if not host.startswith(('http://', 'https://')):
                    trusted_origins.append(f'http://{host}')
                    trusted_origins.append(f'https://{host}')
                else:
                    trusted_origins.append(host)
            
            # Atualizar configuração do Django
            settings.CSRF_TRUSTED_ORIGINS = trusted_origins
        
        response = self.get_response(request)
        return response
    
    def carregar_hosts_confiaveis(self):
        """Carrega lista de hosts confiáveis do arquivo de dados"""
        try:
            if Path(self.data_file).exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                return dados.get('hosts_confiaveis', ['localhost:8000'])
        except Exception as e:
            print(f"Erro ao carregar hosts confiáveis: {e}")
        
        return ['localhost:8000']  # Fallback padrão