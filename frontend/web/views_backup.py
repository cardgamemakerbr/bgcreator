from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.conf import settings

# Lista temporária para armazenar jogos criados
jogos_criados = []

def get_api_data(endpoint, page=1, per_page=1000):
    """Busca dados da API real do backend com fallback local"""
    try:
        response = requests.get(f'{settings.API_BASE_URL}{endpoint}/?page={page}&per_page={per_page}')
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao conectar com API: {e}")
    
    # Fallback para dados locais
    mecanicas_completas = [
        'Alocação de Trabalhadores (Worker Placement)', 'Construção de Baralho (Deck Building)',
        'Controle de Área (Area Control)', 'Colecionar Conjuntos (Set Collection)',
        'Draft de Cartas', 'Rolagem de Dados', 'Gestão de Mão', 'Movimentação em Grid',
        'Leilão / Licitação', 'Colocação de Peças (Tile Placement)', 'Cooperativo',
        'Traidor Oculto', 'Dedução Social', 'Memória', 'Sorte na Medida (Push Your Luck)',
        'Negociação', 'Movimento Ponto-a-Ponto', 'Sistema de Pontos de Ação',
        'Reconhecimento de Padrões', 'Storytelling', 'Campanha / Legado', 'Destreza',
        'Eliminação de Jogadores', 'Simulação', 'Escolha Simultânea de Ações',
        'Pegar e Entregar (Pick-up and Deliver)', 'Tabuleiro Modular', 'Alocação de Dados',
        'Construção de Motor (Engine Building)', 'Apostas', 'Programação de Movimento',
        'Influência em Área', 'Movimento Oculto', 'Gerenciamento de Recursos',
        'Árvore Tecnológica', 'Atuação / Mímica', 'Desenhar (Paper-and-Pencil)',
        'Rolar e Escrever (Roll and Write)', 'Virar e Escrever (Flip and Write)',
        'Conexões de Rotas', 'Controle de Unidades', 'Resolução de Conflitos por Cartas',
        'Ciclo de Dia/Noite', 'Ordem de Turno Variável', 'Poderes Variáveis de Jogadores',
        'Votação', 'Componente de Tempo Real', 'Captura de Peças', 'Linha do Tempo',
        'Quebra-cabeça', 'Empilhamento', 'Mercado Dinâmico', 'Contratos',
        'Eventos Aleatórios', 'Movimento por Grade Hexagonal', 'Manobra de Combate',
        'Reforço de Unidades', 'Escondidinho (Hidden Information)', 'Blefe', 'Corridas',
        'Labirinto', 'Resolução de Enigmas', 'Troca de Cartas', 'Drafting de Dados',
        'Bag Building (Construção de Saquinho)', 'Tableau Building', 'Movimento em Trilhas',
        'Rodondel', 'Sistema de Herança', 'RPG Lite', 'Alocação de Trabalhadores com Dados',
        'Combate Baseado em Cartas', 'Controle de Fluxo', 'Escalonamento', 'Investimento',
        'Maioria de Área', 'Movimento por Cordas/Régua', 'Multiplicadores de Pontos',
        'Oráculo/Previsão', 'Padrões Geométricos', 'Peças Empilháveis',
        'Posicionamento Tático', 'Produção Automática', 'Recrutamento',
        'Recuperação de Ações', 'Remoção de Peças', 'Reputação / Karma',
        'Rodadas de Pontuação Intermediária', 'Seleção de Ações em Grade',
        'Sistema de Fome/Sobrevivência', 'Solo (Modo Carreira)', 'Tabuleiro Giratório',
        'Territórios Conquistáveis', 'Testes de Habilidade', 'Trapaça Permitida (Regra Específica)',
        'Trocas Assimétricas', 'Uso de Aplicativo Integrado', 'Uso de Áudio',
        'Vantagem do Primeiro Jogador', 'Zona de Controle'
    ]
    
    temas_completos = [
        ('Horror Lovecraftiano', 'Mistérios cósmicos e terror psicológico antigo.'),
        ('Investigação Criminal', 'Solução de crimes e busca por evidências.'),
        ('Gastronomia / Culinária', 'Gestão de cozinha e preparo de pratos.'),
        ('Comércio Marítimo', 'Troca de mercadorias entre portos históricos.'),
        ('Industrialização', 'O boom das fábricas e ferrovias do século XIX.'),
        ('Viagem no Tempo', 'Saltos entre eras para alterar a história.'),
        ('Super-Heróis', 'Combate ao crime com poderes extraordinários.'),
        ('Cyber-Espionagem', 'Invasão de sistemas e roubo de dados sigilosos.'),
        ('Mitologia Nórdica', 'Vikings, deuses de Asgard e o fim do mundo.'),
        ('Safari / Animais', 'Observação e preservação da vida selvagem africana.')
    ]
    
    componentes_completos = [
        ('Meeple de Madeira', 'Boneco humanoide que representa trabalhadores.'),
        ('Dados D6', 'O clássico dado de 6 faces para sorteios.'),
        ('Dados Poliédricos', 'Dados de 4, 8, 10, 12 ou 20 faces.'),
        ('Cartas Standard', 'Cartas de tamanho padrão de baralho.'),
        ('Cartas Mini', 'Versões reduzidas para economizar espaço na mesa.'),
        ('Tabuleiro Principal', 'A base onde o jogo central acontece.'),
        ('Tabuleiros Individuais', 'Área de controle particular de cada jogador.'),
        ('Moedas de Metal', 'Dinheiro físico durável e temático.'),
        ('Moedas de Papel/Cartão', 'Dinheiro econômico em cartão rígido.'),
        ('Cubos de Madeira', 'Representação genérica de recursos variados.')
    ]
    
    if endpoint == 'mecanicas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(mecanicas_completas)]
    elif endpoint == 'temas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(temas_completos)]
    elif endpoint == 'componentes':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(componentes_completos)]
    else:
        dados = []
    
    # Paginação
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'results': dados[start:end],
        'count': len(dados),
        'total_pages': (len(dados) + per_page - 1) // per_page,
        'current_page': page,
        'per_page': per_page
    }

def debug(request):
    mecanicas = get_api_data('mecanicas')
    temas = get_api_data('temas')
    componentes = get_api_data('componentes')
    
    return render(request, 'debug.html', {
        'mecanicas': mecanicas,
        'temas': temas,
        'componentes': componentes,
    })

def home(request):
    global jogos_criados
    
    # Contar jogos reais (exemplos + criados)
    jogos_exemplo = 2  # Catan e Ticket to Ride
    total_jogos = jogos_exemplo + len(jogos_criados)
    
    # Obter dados reais da API do backend
    try:
        mecanicas_response = requests.get(f'{settings.API_BASE_URL}mecanicas/?per_page=1000')
        temas_response = requests.get(f'{settings.API_BASE_URL}temas/?per_page=1000')
        componentes_response = requests.get(f'{settings.API_BASE_URL}componentes/?per_page=1000')
        jogos_response = requests.get(f'{settings.API_BASE_URL}jogos/?per_page=1000')
        
        total_mecanicas = mecanicas_response.json().get('count', 0) if mecanicas_response.status_code == 200 else 0
        total_temas = temas_response.json().get('count', 0) if temas_response.status_code == 200 else 0
        total_componentes = componentes_response.json().get('count', 0) if componentes_response.status_code == 200 else 0
        
        if jogos_response.status_code == 200:
            jogos_backend = jogos_response.json().get('count', 0)
            total_jogos = jogos_backend + len(jogos_criados)
        
    except Exception as e:
        print(f"Erro ao conectar com API: {e}")
        # Fallback para dados locais
        mecanicas_data = get_api_data('mecanicas', page=1, per_page=1000)
        temas_data = get_api_data('temas', page=1, per_page=1000)
        componentes_data = get_api_data('componentes', page=1, per_page=1000)
        
        total_mecanicas = mecanicas_data['count']
        total_temas = temas_data['count']
        total_componentes = componentes_data['count']
    
    return render(request, 'home.html', {
        'total_jogos': total_jogos,
        'total_mecanicas': total_mecanicas,
        'total_componentes': total_componentes,
        'total_temas': total_temas,
    })

def jogos_lista(request):
    global jogos_criados
    
    print(f"Jogos criados na lista: {len(jogos_criados)}")  # Debug
    print(f"Jogos: {jogos_criados}")  # Debug
    
    # Combinar jogos criados com dados de exemplo
    jogos_exemplo = [
        {
            'id': 1,
            'nome': 'Catan',
            'subtitulo': 'Colonizadores de Catan',
            'descricao_curta': 'Jogo de estratégia sobre colonização',
            'jogadores_min': 3,
            'jogadores_max': 4,
            'tempo_min': 60,
            'tempo_max': 90,
            'idade_recomendada': 10,
            'peso': 2.3
        },
        {
            'id': 2,
            'nome': 'Ticket to Ride',
            'subtitulo': 'Aventura Ferroviária',
            'descricao_curta': 'Construa rotas de trem pelo mundo',
            'jogadores_min': 2,
            'jogadores_max': 5,
            'tempo_min': 30,
            'tempo_max': 60,
            'idade_recomendada': 8,
            'peso': 1.8
        }
    ]
    
    # Adicionar jogos criados pelo usuário
    todos_jogos = jogos_exemplo + jogos_criados
    
    return render(request, 'jogos/lista.html', {'jogos': {'results': todos_jogos}})

def jogo_novo(request):
    global jogos_criados
    
    if request.method == 'POST':
        print("Dados recebidos:", request.POST)  # Debug
        
        nome = request.POST.get('nome')
        if nome:
            # Criar novo jogo
            novo_jogo = {
                'id': len(jogos_criados) + 100,  # ID único
                'nome': nome,
                'subtitulo': request.POST.get('subtitulo', ''),
                'descricao_curta': request.POST.get('descricao_curta', ''),
                'historia': request.POST.get('historia', ''),
                'jogadores_min': int(request.POST.get('jogadores_min', 1)),
                'jogadores_max': int(request.POST.get('jogadores_max', 4)),
                'tempo_min': int(request.POST.get('tempo_min', 30)),
                'tempo_max': int(request.POST.get('tempo_max', 60)),
                'idade_recomendada': int(request.POST.get('idade_recomendada', 10)),
                
                # Campos complexos
                'mecanicas': request.POST.getlist('mecanicas[]'),
                'temas': request.POST.getlist('temas[]'),
                'componentes': request.POST.getlist('componentes[]'),
                'condicoes_vitoria': [c for c in request.POST.getlist('condicoes_vitoria[]') if c.strip()],
                'condicoes_derrota': [c for c in request.POST.getlist('condicoes_derrota[]') if c.strip()],
                
                # Estruturas
                'estruturas': [],
                'glossario': []
            }
            
            # Processar estruturas
            estruturas_nomes = request.POST.getlist('estruturas_nome[]')
            estruturas_tipos = request.POST.getlist('estruturas_tipo[]')
            estruturas_desc = request.POST.getlist('estruturas_descricao[]')
            
            for i, nome_est in enumerate(estruturas_nomes):
                if nome_est.strip():
                    estrutura = {
                        'nome': nome_est,
                        'tipo': estruturas_tipos[i] if i < len(estruturas_tipos) else 'FASE',
                        'descricao': estruturas_desc[i] if i < len(estruturas_desc) else '',
                        'condicoes_especiais': []
                    }
                    
                    # Processar condições especiais desta estrutura
                    cond_nomes_key = f'condicoes_especiais_nome[{i}][]'
                    cond_desc_key = f'condicoes_especiais_desc[{i}][]'
                    
                    if cond_nomes_key in request.POST:
                        cond_nomes = request.POST.getlist(cond_nomes_key)
                        cond_desc = request.POST.getlist(cond_desc_key)
                        
                        for j, cond_nome in enumerate(cond_nomes):
                            if cond_nome.strip():
                                estrutura['condicoes_especiais'].append({
                                    'nome': cond_nome,
                                    'descricao': cond_desc[j] if j < len(cond_desc) else ''
                                })
                    
                    novo_jogo['estruturas'].append(estrutura)
            
            # Processar glossário
            glossario_palavras = request.POST.getlist('glossario_palavra[]')
            glossario_definicoes = request.POST.getlist('glossario_definicao[]')
            
            for i, palavra in enumerate(glossario_palavras):
                if palavra.strip():
                    novo_jogo['glossario'].append({
                        'palavra': palavra,
                        'definicao': glossario_definicoes[i] if i < len(glossario_definicoes) else ''
                    })
            
            # Calcular peso automaticamente
            novo_jogo['peso'] = calcular_peso_jogo(novo_jogo)
            
            # Adicionar à lista
            jogos_criados.append(novo_jogo)
            print(f"Jogo completo adicionado: {novo_jogo}")  # Debug
            
            messages.success(request, f'Jogo "{nome}" criado com sucesso!')
            return redirect('jogos_lista')
        else:
            messages.error(request, 'Nome do jogo é obrigatório.')
    
    return render(request, 'jogos/novo.html')

def mecanicas_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    try:
        response = requests.get(f'{settings.API_BASE_URL}mecanicas/?page={page}&per_page={per_page}')
        if response.status_code == 200:
            data = response.json()
        else:
            data = get_api_data('mecanicas', page, per_page)
    except:
        data = get_api_data('mecanicas', page, per_page)
    
    return render(request, 'mecanicas/lista.html', {
        'mecanicas': data['results'],
        'pagination': data
    })

def mecanica_novo(request):
    if request.method == 'POST':
        data = {
            'nome': request.POST.get('nome'),
            'descricao': request.POST.get('descricao', ''),
        }
        try:
            response = requests.post(f'{settings.API_BASE_URL}mecanicas/', json=data)
            if response.status_code == 201:
                messages.success(request, 'Mecânica criada com sucesso!')
                return redirect('mecanicas_lista')
            else:
                messages.error(request, 'Erro ao criar mecânica.')
        except:
            messages.error(request, 'Erro de conexão com a API.')
    return render(request, 'mecanicas/novo.html')

def componentes_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    try:
        response = requests.get(f'{settings.API_BASE_URL}componentes/?page={page}&per_page={per_page}')
        if response.status_code == 200:
            data = response.json()
        else:
            data = get_api_data('componentes', page, per_page)
    except:
        data = get_api_data('componentes', page, per_page)
    
    return render(request, 'componentes/lista.html', {
        'componentes': data['results'],
        'pagination': data
    })

def componente_novo(request):
    if request.method == 'POST':
        data = {
            'nome': request.POST.get('nome'),
            'descricao': request.POST.get('descricao', ''),
        }
        try:
            response = requests.post(f'{settings.API_BASE_URL}componentes/', json=data)
            if response.status_code == 201:
                messages.success(request, 'Componente criado com sucesso!')
                return redirect('componentes_lista')
            else:
                messages.error(request, 'Erro ao criar componente.')
        except:
            messages.error(request, 'Erro de conexão com a API.')
    return render(request, 'componentes/novo.html')

def temas_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    try:
        response = requests.get(f'{settings.API_BASE_URL}temas/?page={page}&per_page={per_page}')
        if response.status_code == 200:
            data = response.json()
        else:
            data = get_api_data('temas', page, per_page)
    except:
        data = get_api_data('temas', page, per_page)
    
    return render(request, 'temas/lista.html', {
        'temas': data['results'],
        'pagination': data
    })

def tema_novo(request):
    if request.method == 'POST':
        data = {
            'nome': request.POST.get('nome'),
            'descricao': request.POST.get('descricao', ''),
        }
        try:
            response = requests.post(f'{settings.API_BASE_URL}temas/', json=data)
            if response.status_code == 201:
                messages.success(request, 'Tema criado com sucesso!')
                return redirect('temas_lista')
            else:
                messages.error(request, 'Erro ao criar tema.')
        except:
            messages.error(request, 'Erro de conexão com a API.')
    return render(request, 'temas/novo.html')

def api_proxy(request, path):
    """Proxy para chamadas da API com suporte a busca"""
    from django.http import JsonResponse
    
    # Extrair parâmetros de busca
    search_query = request.GET.get('search', '').lower()
    
    # Determinar o endpoint
    if path.startswith('api/mecanicas'):
        endpoint = 'mecanicas'
    elif path.startswith('api/temas'):
        endpoint = 'temas'
    elif path.startswith('api/componentes'):
        endpoint = 'componentes'
    else:
        return JsonResponse({'error': 'Endpoint não encontrado'}, status=404)
    
    try:
        # Usar API real
        api_url = f'{settings.API_BASE_URL}{endpoint}/?per_page=1000'
        if search_query:
            api_url += f'&search={search_query}'
        
        response = requests.get(api_url)
        if response.status_code == 200:
            return JsonResponse(response.json())
    except Exception as e:
        print(f"Erro na API: {e}")
    
    # Fallback para dados locais
    data = get_api_data(endpoint, page=1, per_page=1000)
    
    # Filtrar por busca se fornecida
    if search_query:
        filtered_results = []
        for item in data['results']:
            if (search_query in item['nome'].lower() or 
                search_query in item.get('descricao', '').lower()):
                filtered_results.append(item)
        data['results'] = filtered_results
        data['count'] = len(filtered_results)
    
    return JsonResponse(data)
def jogo_excluir(request, jogo_id):
    global jogos_criados
    
    # Remover da lista de jogos criados
    jogos_criados = [jogo for jogo in jogos_criados if jogo['id'] != int(jogo_id)]
    
    messages.success(request, 'Jogo excluído com sucesso!')
    return redirect('jogos_lista')

def jogo_editar(request, jogo_id):
    global jogos_criados
    
    # Encontrar o jogo
    jogo = None
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo = j
            break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    if request.method == 'POST':
        # Atualizar campos básicos
        jogo['nome'] = request.POST.get('nome', jogo['nome'])
        jogo['subtitulo'] = request.POST.get('subtitulo', jogo['subtitulo'])
        jogo['descricao_curta'] = request.POST.get('descricao_curta', jogo['descricao_curta'])
        jogo['historia'] = request.POST.get('historia', jogo.get('historia', ''))
        jogo['jogadores_min'] = int(request.POST.get('jogadores_min', jogo['jogadores_min']))
        jogo['jogadores_max'] = int(request.POST.get('jogadores_max', jogo['jogadores_max']))
        jogo['tempo_min'] = int(request.POST.get('tempo_min', jogo['tempo_min']))
        jogo['tempo_max'] = int(request.POST.get('tempo_max', jogo['tempo_max']))
        jogo['idade_recomendada'] = int(request.POST.get('idade_recomendada', jogo['idade_recomendada']))
        
        # Atualizar campos complexos
        jogo['mecanicas'] = request.POST.getlist('mecanicas[]')
        jogo['temas'] = request.POST.getlist('temas[]')
        jogo['componentes'] = request.POST.getlist('componentes[]')
        jogo['condicoes_vitoria'] = [c for c in request.POST.getlist('condicoes_vitoria[]') if c.strip()]
        jogo['condicoes_derrota'] = [c for c in request.POST.getlist('condicoes_derrota[]') if c.strip()]
        
        # Atualizar estruturas
        jogo['estruturas'] = []
        estruturas_nomes = request.POST.getlist('estruturas_nome[]')
        estruturas_tipos = request.POST.getlist('estruturas_tipo[]')
        estruturas_desc = request.POST.getlist('estruturas_descricao[]')
        
        for i, nome_est in enumerate(estruturas_nomes):
            if nome_est.strip():
                estrutura = {
                    'nome': nome_est,
                    'tipo': estruturas_tipos[i] if i < len(estruturas_tipos) else 'FASE',
                    'descricao': estruturas_desc[i] if i < len(estruturas_desc) else '',
                    'condicoes_especiais': []
                }
                
                # Processar condições especiais
                cond_nomes_key = f'condicoes_especiais_nome[{i}][]'
                cond_desc_key = f'condicoes_especiais_desc[{i}][]'
                
                if cond_nomes_key in request.POST:
                    cond_nomes = request.POST.getlist(cond_nomes_key)
                    cond_desc = request.POST.getlist(cond_desc_key)
                    
                    for j, cond_nome in enumerate(cond_nomes):
                        if cond_nome.strip():
                            estrutura['condicoes_especiais'].append({
                                'nome': cond_nome,
                                'descricao': cond_desc[j] if j < len(cond_desc) else ''
                            })
                
                jogo['estruturas'].append(estrutura)
        
        # Atualizar glossário
        jogo['glossario'] = []
        glossario_palavras = request.POST.getlist('glossario_palavra[]')
        glossario_definicoes = request.POST.getlist('glossario_definicao[]')
        
        for i, palavra in enumerate(glossario_palavras):
            if palavra.strip():
                jogo['glossario'].append({
                    'palavra': palavra,
                    'definicao': glossario_definicoes[i] if i < len(glossario_definicoes) else ''
                })
        
        # Recalcular peso automaticamente
        jogo['peso'] = calcular_peso_jogo(jogo)
        
        messages.success(request, f'Jogo "{jogo["nome"]}" atualizado com sucesso!')
        return redirect('jogos_lista')
    
    return render(request, 'jogos/editar.html', {'jogo': jogo})
def jogo_detalhes(request, jogo_id):
    global jogos_criados
    
    # Encontrar o jogo
    jogo = None
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo = j
            break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    return render(request, 'jogos/detalhes.html', {'jogo': jogo})
def calcular_peso_jogo(jogo_data):
    """Calcula o peso do jogo baseado nas regras de negócio"""
    peso = 0.1  # Peso base
    
    # Peso por tempo (0,1 a cada 30min, máx 1,0)
    tempo_max = int(jogo_data.get('tempo_max', 30))
    peso_tempo = min((tempo_max // 30) * 0.1, 1.0)
    peso += peso_tempo
    
    # Peso por mecânicas (0,1 por mecânica, máx 1,0)
    mecanicas = [m for m in jogo_data.get('mecanicas', []) if m.strip()]
    peso_mecanicas = min(len(mecanicas) * 0.1, 1.0)
    peso += peso_mecanicas
    
    # Peso por componentes (0,1 por componente, máx 1,0)
    componentes = [c for c in jogo_data.get('componentes', []) if c.strip()]
    peso_componentes = min(len(componentes) * 0.1, 1.0)
    peso += peso_componentes
    
    # Peso por condições de vitória (0,1 por condição, máx 0,3)
    condicoes_vitoria = [c for c in jogo_data.get('condicoes_vitoria', []) if c.strip()]
    peso_vitoria = min(len(condicoes_vitoria) * 0.1, 0.3)
    peso += peso_vitoria
    
    # Peso por condições de derrota (0,1 por condição, máx 0,3)
    condicoes_derrota = [c for c in jogo_data.get('condicoes_derrota', []) if c.strip()]
    peso_derrota = min(len(condicoes_derrota) * 0.1, 0.3)
    peso += peso_derrota
    
    # Peso por estruturas (0,1 por estrutura, máx 1,0)
    estruturas = jogo_data.get('estruturas', [])
    peso_estruturas = min(len(estruturas) * 0.1, 1.0)
    peso += peso_estruturas
    
    # Peso por condições especiais (0,1 por condição, máx 1,0)
    total_condicoes_especiais = 0
    for estrutura in estruturas:
        total_condicoes_especiais += len(estrutura.get('condicoes_especiais', []))
    peso_especiais = min(total_condicoes_especiais * 0.1, 1.0)
    peso += peso_especiais
    
    return round(peso, 1)