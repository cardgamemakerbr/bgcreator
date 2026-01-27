from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
import re
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        global usuario_logado
        if usuario_logado is None:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        global usuario_logado
        if usuario_logado is None:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        if usuario_logado['perfil'] != 'ADMINISTRADOR':
            messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def autor_or_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        global usuario_logado
        if usuario_logado is None:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        if usuario_logado['perfil'] not in ['AUTOR', 'ADMINISTRADOR']:
            messages.error(request, 'Acesso negado. Apenas autores e administradores podem acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def editor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        global usuario_logado
        if usuario_logado is None:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        if usuario_logado['perfil'] not in ['AUTOR', 'REVISOR', 'ADMINISTRADOR']:
            messages.error(request, 'Acesso negado. Apenas autores, revisores e administradores podem editar jogos.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_or_reviewer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        global usuario_logado
        if usuario_logado is None:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        if usuario_logado['perfil'] not in ['ADMINISTRADOR', 'REVISOR']:
            messages.error(request, 'Acesso negado. Apenas administradores e revisores podem acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def validar_senha(senha):
    """Valida senha baseado na complexidade configurada"""
    global complexidade_senha
    import re
    
    if complexidade_senha == 1:  # Desativado
        return True, ""
    
    elif complexidade_senha == 2:  # Letras e números, mínimo 6
        if len(senha) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres"
        if not re.search(r'[a-zA-Z]', senha) or not re.search(r'\d', senha):
            return False, "Senha deve conter letras e números"
    
    elif complexidade_senha == 3:  # Maiúscula, minúscula, números, mínimo 8
        if len(senha) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        if not re.search(r'[a-z]', senha):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        if not re.search(r'[A-Z]', senha):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        if not re.search(r'\d', senha):
            return False, "Senha deve conter pelo menos um número"
    
    elif complexidade_senha == 4:  # Completa, mínimo 10
        if len(senha) < 10:
            return False, "Senha deve ter pelo menos 10 caracteres"
        if not re.search(r'[a-z]', senha):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        if not re.search(r'[A-Z]', senha):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        if not re.search(r'\d', senha):
            return False, "Senha deve conter pelo menos um número"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            return False, "Senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>)"
    
    # Se chegou até aqui, a senha passou em todas as validações
    return True, ""
    
def processar_markdown(texto):
    """Processa texto markdown básico"""
    if not texto:
        return ""
    
    # Negrito **texto**
    texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
    
    # Itálico *texto*
    texto = re.sub(r'\*(.*?)\*', r'<em>\1</em>', texto)
    
    # Quebras de linha duplas para parágrafos
    texto = texto.replace('\r\n\r\n', '</p><p>')
    texto = texto.replace('\n\n', '</p><p>')
    
    # Quebras de linha simples para <br>
    texto = texto.replace('\r\n', '<br>')
    texto = texto.replace('\n', '<br>')
    
    # Envolver em parágrafo se não estiver vazio
    if texto.strip():
        if not texto.startswith('<p>'):
            texto = f'<p>{texto}</p>'
    
    return mark_safe(texto)

# Lista para armazenar dados criados
mecanicas_criadas = []
componentes_criados = []
temas_criados = []
jogos_criados = []
usuarios_criados = []
comentarios_criados = []
usuario_logado = None
complexidade_senha = 1  # 1=Desativado, 2=Letras+números 6+, 3=Maiúsc+minúsc+números 8+, 4=Completa 10+

def salvar_imagem_glossario(arquivo):
    """Salva imagem do glossário e retorna o caminho"""
    if arquivo:
        try:
            # Criar diretório se não existir
            glossario_dir = 'media/glossario'
            if not os.path.exists(glossario_dir):
                os.makedirs(glossario_dir)
            
            # Salvar arquivo
            filename = f"glossario_{arquivo.name}"
            filepath = os.path.join(glossario_dir, filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            
            return f'/media/glossario/{filename}'
        except Exception as e:
            print(f"Erro ao salvar imagem do glossário: {e}")
            return None
    return None

def salvar_imagem_capa(arquivo):
    """Salva imagem da capa e retorna o caminho"""
    if arquivo:
        try:
            # Criar diretório se não existir
            capas_dir = 'media/capas'
            if not os.path.exists(capas_dir):
                os.makedirs(capas_dir)
            
            # Salvar arquivo
            filename = f"capa_{arquivo.name}"
            filepath = os.path.join(capas_dir, filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            
            return f'/media/capas/{filename}'
        except Exception as e:
            print(f"Erro ao salvar capa: {e}")
            return None
    return None

def salvar_imagem_setup(arquivo):
    """Salva imagem do setup e retorna o caminho"""
    if arquivo:
        try:
            # Criar diretório se não existir
            setup_dir = 'media/setup'
            if not os.path.exists(setup_dir):
                os.makedirs(setup_dir)
            
            # Salvar arquivo
            filename = f"setup_{arquivo.name}"
            filepath = os.path.join(setup_dir, filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            
            return f'/media/setup/{filename}'
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")
            return None
    return None

def get_api_data(endpoint, page=1, per_page=1000, busca=None):
    """Busca dados da API real do backend com fallback local"""
    global mecanicas_criadas, componentes_criados, temas_criados
    
    try:
        response = requests.get(f'{settings.API_BASE_URL}{endpoint}/?page={page}&per_page={per_page}')
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao conectar com API: {e}")
    
    # Fallback para dados locais
    mecanicas_completas = [
        ('Alocação de Trabalhadores (Worker Placement)', 'Posicionar peões em locais do tabuleiro para bloquear a ação para outros e ganhar recursos.'),
        ('Construção de Baralho (Deck Building)', 'Jogadores compram cartas para melhorar seu próprio baralho durante a partida.'),
        ('Controle de Área (Area Control)', 'Ganhar bônus ou pontos por ter a maioria de unidades em um território específico.'),
        ('Colecionar Conjuntos (Set Collection)', 'Acumular itens do mesmo tipo para multiplicar a pontuação final.'),
        ('Draft de Cartas', 'Escolher uma carta de uma mão e passar o restante para o próximo jogador.'),
        ('Rolagem de Dados', 'Uso de dados para determinar o sucesso ou a força de uma ação.'),
        ('Gestão de Mão', 'Otimizar o uso das cartas que você possui para maximizar jogadas.'),
        ('Movimentação em Grid', 'Mover peças em um tabuleiro dividido em quadrados ou espaços definidos.'),
        ('Leilão / Licitação', 'Disputar um item ou recurso através de lances de moeda ou pontos.'),
        ('Colocação de Peças (Tile Placement)', 'Construir o mapa ou cenário encaixando peças como um quebra-cabeça.'),
        ('Cooperativo', 'Todos os jogadores trabalham juntos contra o sistema do jogo.'),
        ('Traidor Oculto', 'Um jogador trabalha secretamente para impedir que o grupo vença.'),
        ('Dedução Social', 'Tentar descobrir a identidade ou intenção dos outros jogadores através da fala e comportamento.'),
        ('Memória', 'Jogadores devem lembrar a posição ou face de componentes ocultos.'),
        ('Sorte na Medida (Push Your Luck)', 'Decidir entre parar com o lucro atual ou arriscar tudo por um prêmio maior.'),
        ('Negociação', 'Troca livre de recursos e favores entre os participantes.'),
        ('Movimento Ponto-a-Ponto', 'Mover-se através de rotas fixas que conectam locais específicos.'),
        ('Sistema de Pontos de Ação', 'Você tem um orçamento fixo de pontos para gastar em diversas ações por turno.'),
        ('Reconhecimento de Padrões', 'Identificar formas ou cores no tabuleiro para completar objetivos.'),
        ('Storytelling', 'Criar uma narrativa conjunta baseada nos eventos do jogo.'),
        ('Campanha / Legado', 'O jogo evolui entre sessões, com mudanças permanentes nos componentes.'),
        ('Destreza', 'Testes físicos como equilíbrio, mira ou rapidez motora.'),
        ('Eliminação de Jogadores', 'Jogadores saem da partida antes dela acabar ao perderem condições de vitória.'),
        ('Simulação', 'Tenta replicar fielmente uma situação real (guerra, economia, voo).'),
        ('Escolha Simultânea de Ações', 'Todos decidem o que fazer ao mesmo tempo e revelam as ações juntos.'),
        ('Pegar e Entregar', 'Coletar um recurso em um ponto do mapa e transportá-lo até outro para ganhar pontos.'),
        ('Tabuleiro Modular', 'O mapa é montado de forma diferente a cada partida.'),
        ('Alocação de Dados', 'Usar os valores sorteados nos dados como se fossem "trabalhadores" para ativar ações.'),
        ('Construção de Motor (Engine Building)', 'Criar uma sequência de habilidades que se alimentam para gerar recursos infinitos.'),
        ('Apostas', 'Arriscar recursos prevendo quem será o vencedor ou qual evento ocorrerá.'),
        ('Programação de Movimento', 'Planejar várias jogadas com antecedência e executá-las em ordem.'),
        ('Influência em Área', 'Similar ao controle, mas focado no peso político ou de presença em uma região.'),
        ('Movimento Oculto', 'Um jogador move sua peça em um mapa secreto, invisível aos outros.'),
        ('Gerenciamento de Recursos', 'Administrar estoques limitados (comida, dinheiro, madeira) para evoluir.'),
        ('Árvore Tecnológica', 'Gastar recursos para desbloquear melhorias permanentes em uma ordem lógica.'),
        ('Atuação / Mímica', 'Usar o corpo e expressões para comunicar uma palavra ou ideia.'),
        ('Desenhar (Paper-and-Pencil)', 'Usar papel e caneta para registrar progresso ou solucionar enigmas.'),
        ('Rolar e Escrever', 'Rolar dados e marcar os resultados em uma folha individual.'),
        ('Virar e Escrever', 'Revelar cartas e marcar os resultados em uma folha individual.'),
        ('Conexões de Rotas', 'Criar caminhos contínuos entre dois pontos do tabuleiro.'),
        ('Controle de Unidades', 'Comandar soldados ou peças individuais em combate ou exploração.'),
        ('Resolução de Conflitos por Cartas', 'Usar valores de cartas em vez de dados para decidir combates.'),
        ('Ciclo de Dia/Noite', 'As regras mudam dependendo da fase de tempo atual no jogo.'),
        ('Ordem de Turno Variável', 'A ordem de quem joga primeiro muda a cada rodada.'),
        ('Poderes Variáveis de Jogadores', 'Cada pessoa começa com uma habilidade única e diferente das outras.'),
        ('Votação', 'O grupo decide o resultado de um evento através do voto.'),
        ('Componente de Tempo Real', 'Jogar contra um cronômetro, sem turnos definidos.'),
        ('Captura de Peças', 'Remover peças do oponente do tabuleiro (como no Xadrez).'),
        ('Linha do Tempo', 'Organizar eventos ou cartas em ordem cronológica correta.'),
        ('Quebra-cabeça', 'Resolver um desafio lógico de encaixe ou sequência.'),
        ('Empilhamento', 'Colocar peças umas sobre as outras sem deixá-las cair.'),
        ('Mercado Dinâmico', 'Preços que variam conforme os jogadores compram ou vendem itens.'),
        ('Contratos', 'Cumprir requisitos específicos de recursos para ganhar recompensas.'),
        ('Eventos Aleatórios', 'Cartas ou dados que mudam as regras globais temporariamente.'),
        ('Movimento por Grade Hexagonal', 'Movimentação estratégica em espaços de 6 lados (favos).'),
        ('Manobra de Combate', 'Posicionamento tático para ganhar vantagem em lutas.'),
        ('Reforço de Unidades', 'Adicionar mais peças ao tabuleiro durante o jogo.'),
        ('Escondidinho (Hidden Information)', 'Informações que apenas alguns jogadores conhecem.'),
        ('Blefe', 'Tentar convencer os outros de algo falso para ganhar vantagem.'),
        ('Corridas', 'Ganha quem chegar primeiro a um ponto específico do tabuleiro.'),
        ('Labirinto', 'Paredes ou caminhos que se movem durante a partida.'),
        ('Resolução de Enigmas', 'Decifrar códigos ou charadas para avançar.'),
        ('Troca de Cartas', 'Trocar itens da mão diretamente com outros jogadores.'),
        ('Drafting de Dados', 'Escolher dados de um conjunto comum para usar em seu turno.'),
        ('Bag Building', 'Adicionar fichas ou peças em um saco para serem sorteadas depois.'),
        ('Tableau Building', 'Construir uma área de jogo à sua frente com cartas que dão bônus.'),
        ('Movimento em Trilhas', 'Avançar um marcador em uma trilha de progresso ou pontuação.'),
        ('Rodondel', 'Uma roda de ações onde seu movimento limita o que você pode fazer.'),
        ('Sistema de Herança', 'Habilidades passadas de um personagem morto para o próximo.'),
        ('RPG Lite', 'Elementos simples de evolução de personagem e narrativa.'),
        ('Alocação de Trabalhadores com Dados', 'Seus trabalhadores têm valores (dados) que ditam a força da ação.'),
        ('Combate Baseado em Cartas', 'Ataques e defesas resolvidos puramente por baralho.'),
        ('Controle de Fluxo', 'Gerenciar a velocidade com que o jogo avança.'),
        ('Escalonamento', 'O jogo fica mais difícil ou recompensador conforme o tempo passa.'),
        ('Investimento', 'Gastar agora para colher frutos muito maiores no final do jogo.'),
        ('Maioria de Área', 'Ganhar pontos por ter mais presença, mesmo sem controle total.'),
        ('Movimento por Cordas/Régua', 'Usar ferramentas físicas para medir a distância de movimento.'),
        ('Multiplicadores de Pontos', 'Itens que dobram ou triplicam o valor de outros recursos.'),
        ('Oráculo/Previsão', 'Ver cartas que ainda vão sair para planejar o futuro.'),
        ('Padrões Geométricos', 'Organizar peças em formatos específicos (linhas, L, quadrados).'),
        ('Peças Empinháveis', 'Peças que se encaixam verticalmente para economizar espaço ou indicar nível.'),
        ('Posicionamento Tático', 'Onde você está no tabuleiro é mais importante do que o que você tem.'),
        ('Produção Automática', 'Recursos que você ganha todo turno sem precisar de ações.'),
        ('Recrutamento', 'Adicionar novos aliados ou unidades ao seu exército/grupo.'),
        ('Recuperação de Ações', 'Gastar um turno para "pegar de volta" cartas ou trabalhadores usados.'),
        ('Remoção de Peças', 'Estratégia focada em limpar o tabuleiro do oponente.'),
        ('Reputação / Karma', 'Um medidor de "moralidade" que abre ou fecha caminhos no jogo.'),
        ('Rodadas de Pontuação Intermediária', 'Pontuar várias vezes durante o jogo, não só no fim.'),
        ('Seleção de Ações em Grade', 'Escolher ações baseadas em coordenadas de uma tabela.'),
        ('Sistema de Fome/Sobrevivência', 'Obrigação de gastar recursos apenas para manter as peças vivas.'),
        ('Solo (Modo Carreira)', 'Regras específicas para jogar sozinho e evoluir.'),
        ('Tabuleiro Giratório', 'Partes do tabuleiro que giram, mudando as conexões.'),
        ('Territórios Conquestáveis', 'Regiões que mudam de dono constantemente através de combate.'),
        ('Testes de Habilidade', 'Comparar um valor de atributo contra uma dificuldade (estilo RPG).'),
        ('Trapaça Permitida', 'Regras que permitem quebrar normas se não for pego (raro e específico).'),
        ('Trocas Assimétricas', 'Um recurso vale muito para você, mas pouco para o outro.'),
        ('Uso de Aplicativo Integrado', 'O jogo exige um tablet ou celular para rodar eventos.'),
        ('Uso de Áudio', 'Sons ou narrações que fazem parte da mecânica de jogo.'),
        ('Vantagem do Primeiro Jogador', 'Um bônus compensatório para quem inicia a partida.'),
        ('Zona de Controle', 'Espaço ao redor de uma unidade que impede o movimento de inimigos.')
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
        ('Safari / Animais', 'Observação e preservação da vida selvagem africana.'),
        ('Fantasia Medieval', 'Magia, reinos e criaturas místicas.'),
        ('Exploração Espacial', 'Viagens entre galáxias e descobertas alienígenas.'),
        ('Cyberpunk', 'Futuro distópico, neon e tecnologia invasiva.'),
        ('Steampunk', 'Tecnologia a vapor inspirada na era vitoriana.'),
        ('Zumbis / Apocalipse', 'Sobrevivência após o colapso da civilização.'),
        ('Egito Antigo', 'Construção de monumentos e divindades do Nilo.'),
        ('Mitologia Grega', 'Deuses do Olimpo e heróis lendários.'),
        ('Piratas / Naval', 'Tesouros, saques e exploração dos mares.'),
        ('Faroeste', 'Xerifes, duelos e a vida no velho oeste americano.'),
        ('Segunda Guerra Mundial', 'Conflitos históricos entre Aliados e Eixo.'),
        ('Civilização', 'Desenvolvimento de um povo desde a pedra até a era espacial.'),
        ('Natureza / Ecossistemas', 'Foco na flora, fauna e equilíbrio ambiental.'),
        ('Medicina / Pandemia', 'Tratamento de doenças e gestão de crises de saúde.'),
        ('Política / Eleições', 'Campanhas eleitorais e manobras de poder.'),
        ('Esportes', 'Simulação de partidas de futebol, corridas ou lutas.'),
        ('Religião / Espiritualidade', 'Liderança de fés ou busca por iluminação.'),
        ('Abstrato', 'Sem tema definido, focado puramente na lógica.'),
        ('Literatura Clássica', 'Jogos baseados em obras de grandes autores.'),
        ('Cinema / Hollywood', 'Produção de filmes e fama nos estúdios.'),
        ('Moda / Design', 'Criação de tendências e desfiles de alta costura.'),
        ('Arqueologia', 'Descoberta de fósseis e artefatos antigos.'),
        ('Submarino / Abismo', 'Exploração das profundezas oceânicas desconhecidas.'),
        ('Sobrevivência na Selva', 'Busca por recursos em ambientes tropicais hostis.'),
        ('Pós-Apocalipse Nuclear', 'Vida após a devastação por bombas atômicas.'),
        ('Colonização de Marte', 'Estabelecimento de bases no planeta vermelho.'),
        ('Invasão Alienígena', 'Defesa da Terra contra forças extraterrestres.'),
        ('Mundo dos Sonhos', 'Cenários surreais e lógica onírica.'),
        ('Circo', 'Gerenciamento de espetáculos e artistas itinerantes.'),
        ('Transporte Ferroviário', 'Expansão de linhas de trem e logística.'),
        ('Mineração', 'Extração de minérios e pedras preciosas.'),
        ('Alquimia / Magia', 'Mistura de ingredientes para criar poções e feitiços.'),
        ('Guerra Fria', 'Espionagem e tensão entre superpotências.'),
        ('Renascimento Italiano', 'Arte, ciência e política das cidades-estado.'),
        ('Roma Antiga', 'Legiões, senado e glória imperial.'),
        ('Pré-História', 'Vida entre homens das cavernas e dinossauros.'),
        ('Arte / Museus', 'Curadoria de exposições e leilões de obras famosas.'),
        ('Aviação', 'História dos aviões, pilotagem e companhias aéreas.'),
        ('Império Asteca/Maia', 'Civilizações mesoamericanas e rituais sagrados.'),
        ('Contos de Fadas', 'Histórias dos irmãos Grimm e folclore infantil.'),
        ('Guerra de Gangues', 'Conflito pelo controle do submundo urbano.'),
        ('Economia / Mercado de Ações', 'Investimentos financeiros e especulação.'),
        ('Ecologia / Poluição', 'Limpeza do planeta e energias renováveis.'),
        ('Exploração de Cavernas', 'Espeleologia e perigos subterrâneos.'),
        ('Fábrica / Automação', 'Otimização de linhas de montagem industriais.'),
        ('Festival de Música', 'Organização de shows e logística de público.'),
        ('Florestas Encantadas', 'Seres mágicos que vivem em bosques protegidos.'),
        ('Gladiadores', 'Combate na arena por fama e liberdade.'),
        ('Insetos / Micromundo', 'A vida sob a perspectiva de formigas ou abelhas.'),
        ('Inteligência Artificial', 'O despertar e a evolução das máquinas.'),
        ('Jardim / Botânica', 'Cultivo de flores raras e paisagismo.'),
        ('Jornalismo', 'Busca por furos de reportagem e edição de notícias.'),
        ('Luta Livre', 'O show e a força do wrestling profissional.'),
        ('Máfia', 'Crime organizado, lealdade e família.'),
        ('Mercado Árabe', 'Trocas comerciais em bazares e caravanas.'),
        ('Monstros Gigantes', 'Criaturas colossais destruindo cidades.'),
        ('Montanha-Russa', 'Design de engenharia focado em diversão.'),
        ('Natal / Festividades', 'Temas sazonais e espírito natalino.'),
        ('Navegação Astral', 'Viagens místicas entre planos de existência.'),
        ('Noite de Gala / Cassino', 'Glamour, apostas altas e jogos de azar.'),
        ('Ópera / Teatro', 'Dramas de palco e produção de grandes peças.'),
        ('Orfanato Abandonado', 'Terror gótico e exploração urbana.'),
        ('Padaria / Doces', 'Confeitaria e gerenciamento de vitrines.'),
        ('Paranormal', 'Caça-fantasmas e eventos inexplicaveis.'),
        ('Pescaria', 'Competição de pesca em rios ou mar aberto.'),
        ('Petróleo / Energia', 'Extração de óleo e matrizes energéticas.'),
        ('Pirâmides', 'Mistérios da engenharia e sepulturas egípcias.'),
        ('Planetas Alienígenas', 'Vida em ecossistemas fora da Terra.'),
        ('Polícia vs Ladrão', 'Perseguições e planos de assalto.'),
        ('Prisão', 'Vida no cárcere e planos de fuga.'),
        ('Psicologia / Mente Humana', 'Viagem pelo subconsciente e memórias.'),
        ('Reality Show', 'Busca pela audiência através de desafios públicos.'),
        ('Restaurante', 'Atendimento a clientes e eficiência de cozinha.'),
        ('Samurai', 'Código do Bushido e batalhas feudais japonesas.'),
        ('Saúde Mental', 'Empatia e gestão de emoções/clínicas.'),
        ('Seitas Misteriosas', 'Rituais sombrios e sociedades secretas.'),
        ('Shopping Center', 'Consumismo e gestão de lojas.'),
        ('Sistema Solar', 'Astronomia focada nos nossos planetas vizinhos.'),
        ('Tecnologia Futurista', 'Gadgets avançados e ciência de ponta.'),
        ('Tribos Indígenas', 'Cultura, sobrevivência e harmonia com a terra.'),
        ('Universidades / Escolas', 'Vida acadêmica e exames.'),
        ('Viagem pelo Mundo', 'Turismo e visitas a pontos turísticos globais.'),
        ('Vida Marinha', 'Exploração dos oceanos e criaturas aquáticas.'),
        ('Vulcões', 'Atividade vulcânica e formação geológica.'),
        ('Western Espacial', 'Faroeste ambientado no espaço sideral.'),
        ('Xerife do Condado', 'Manutenção da ordem em cidades pequenas.'),
        ('Yoga / Meditação', 'Práticas espirituais e bem-estar.'),
        ('Zoologia', 'Estudo e preservação de espécies animais.'),
        ('Agricultura Moderna', 'Tecnologia aplicada ao cultivo de alimentos.'),
        ('Biotecnologia', 'Manipulação genética e engenharia biológica.'),
        ('Clima Extremo', 'Sobrevivência em condições climáticas adversas.'),
        ('Democracia Antiga', 'Sistemas políticos da Grécia clássica.'),
        ('Energia Renovavel', 'Sustentabilidade e tecnologias limpas.'),
        ('Folclore Mundial', 'Lendas e mitos de diferentes culturas.'),
        ('Genoma Humano', 'Pesquisa genética e medicina personalizada.'),
        ('Habitat Espacial', 'Construção de estações orbitais.'),
        ('Idade do Gelo', 'Sobrevivência durante períodos glaciais.'),
        ('Jazz / Blues', 'Cultura musical afro-americana.')
    ]
    
    componentes_completos = [
        ('Meeple de Madeira', 'Boneco humanoide que representa trabalhadores.', 'NEUTRO'),
        ('Dados D6', 'O clássico dado de 6 faces para sorteios.', 'SORTE'),
        ('Dados Poliédricos', 'Dados de 4, 8, 10, 12 ou 20 faces.', 'SORTE'),
        ('Cartas Standard', 'Cartas de tamanho padrão de baralho.', 'TATICO'),
        ('Cartas Mini', 'Versões reduzidas para economizar espaço na mesa.', 'TATICO'),
        ('Tabuleiro Principal', 'A base onde o jogo central acontece.', 'NEUTRO'),
        ('Tabuleiros Individuais', 'Área de controle particular de cada jogador.', 'GERENCIAMENTO'),
        ('Moedas de Metal', 'Dinheiro físico durável e temático.', 'GERENCIAMENTO'),
        ('Moedas de Papel/Cartão', 'Dinheiro econômico em cartão rígido.', 'GERENCIAMENTO'),
        ('Cubos de Madeira', 'Representação genérica de recursos variados.', 'GERENCIAMENTO'),
        ('Miniaturas de Plástico', 'Esculturas detalhadas de personagens.', 'LUDICO'),
        ('Marcadores de Pontuação', 'Pinos ou fichas para a trilha de pontos.', 'GERENCIAMENTO'),
        ('Ampulheta', 'Medidor físico de tempo para turnos rápidos.', 'HABILIDADE'),
        ('Escudo de Jogador', 'Divisória para ocultar cartas e recursos.', 'TATICO'),
        ('Fichas de Poker', 'Tokens pesados usados como moedas ou apostas.', 'GERENCIAMENTO'),
        ('Tiles Hexagonais', 'Peças de 6 lados para montar mapas modulares.', 'TATICO'),
        ('Tiles Quadrados', 'Peças quadradas para construção de cenário.', 'TATICO'),
        ('Marcador de Primeiro Jogador', 'Item que identifica quem inicia a rodada.', 'NEUTRO'),
        ('Saco de Pano (Bag)', 'Para sorteio cego de peças (Bag building).', 'SORTE'),
        ('Gemas de Plástico/Acrílico', 'Pedras coloridas para representar joias.', 'LUDICO'),
        ('Peões de Plástico', 'Marcadores simples em formato de "pino".', 'NEUTRO'),
        ('Discos de Madeira', 'Marcadores circulares achatados.', 'NEUTRO'),
        ('Cartas de Referência', 'Resumo de regras para consulta rápida.', 'NEUTRO'),
        ('Manual de Regras', 'O livro de instruções oficial do jogo.', 'NEUTRO'),
        ('Livro de Cenários', 'Guia com missões e montagens específicas.', 'LUDICO'),
        ('Divisórias de Caixa (Insert)', 'Organizador interno para os componentes.', 'GERENCIAMENTO'),
        ('Adesivos', 'Para modificar o tabuleiro permanentemente (Legacy).', 'LUDICO'),
        ('Canetas Dry-Erase', 'Para escrever e apagar em tabuleiros plastificados.', 'HABILIDADE'),
        ('Lápis', 'Para preencher blocos de papel.', 'HABILIDADE'),
        ('Blocos de Pontuação', 'Folhas descartáveis para calcular o fim do jogo.', 'GERENCIAMENTO'),
        ('Clip de Plástico', 'Para encaixar na borda de cartas e indicar valores.', 'GERENCIAMENTO'),
        ('Suporte de Cartas', 'Acessório para manter as cartas em pé na mesa.', 'NEUTRO'),
        ('Torre de Dados', 'Estrutura para rolar dados sem que eles voem longe.', 'SORTE'),
        ('Bandeja de Dados', 'Superfície forrada para silenciar e conter os dados.', 'SORTE'),
        ('Marcadores de Dano', 'Tokens de coração ou sangue para vida.', 'GERENCIAMENTO'),
        ('Peças de Encaixe', 'Componentes que se conectam mecanicamente.', 'HABILIDADE'),
        ('Engrenagens de Papelão', 'Discos que giram afetando o jogo.', 'TATICO'),
        ('Bússola de Papelão', 'Para indicar direção de vento ou movimento.', 'TATICO'),
        ('Luva de Cartas (Sleeves)', 'Plásticos para proteger as cartas.', 'NEUTRO'),
        ('Meeples de Animais', 'Figuras de madeira em formato de bicho.', 'LUDICO'),
        ('Recipientes de Armazenamento', 'Potes plásticos para separar recursos.', 'GERENCIAMENTO'),
        ('Cartas Transparentes', 'Para sobrepor informações a outras cartas.', 'TATICO'),
        ('Espelho', 'Componente reflexivo para jogos de laser ou ótica.', 'HABILIDADE'),
        ('Peças de Resina Especiais', 'Componentes premium com textura realística.', 'LUDICO'),
        ('Playmat de Neoprene', 'Tapete de borracha para organizar a mesa.', 'NEUTRO'),
        ('Marcadores de Nível', 'Tokens que indicam a evolução de um item.', 'GERENCIAMENTO'),
        ('Relógio de Xadrez', 'Dispositivo para controle rigoroso de tempo.', 'HABILIDADE'),
        ('Cartas de Evento', 'Baralho que altera o jogo a cada rodada.', 'SORTE'),
        ('Tiles de Terreno', 'Peças que representam montanhas, florestas, etc.', 'TATICO')
    ]
    
    if endpoint == 'mecanicas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(mecanicas_completas)]
        dados.extend(mecanicas_criadas)
    elif endpoint == 'temas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(temas_completos)]
        dados.extend(temas_criados)
    elif endpoint == 'componentes':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao, 'tipo': tipo} for i, (nome, descricao, tipo) in enumerate(componentes_completos)]
        dados.extend(componentes_criados)
    else:
        dados = []
    
    # Paginação
    start = (page - 1) * per_page
    end = start + per_page
    
    # Aplicar filtro de busca se fornecido
    if busca:
        busca_lower = busca.lower()
        dados_filtrados = []
        for item in dados:
            if (busca_lower in item['nome'].lower() or 
                busca_lower in item.get('descricao', '').lower() or
                (endpoint == 'componentes' and busca_lower in item.get('tipo', '').lower())):
                dados_filtrados.append(item)
        dados = dados_filtrados
    
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
    global jogos_criados, usuario_logado
    
    # Se não estiver logado, redirecionar para login
    if usuario_logado is None:
        return redirect('login')
    
    # Contar jogos reais (exemplos + criados)
    jogos_exemplo = 2  # Catan e Ticket to Ride
    total_jogos = jogos_exemplo + len(jogos_criados)
    
    # Usar dados locais para contagem
    mecanicas_data = get_api_data('mecanicas', page=1, per_page=1000)
    temas_data = get_api_data('temas', page=1, per_page=1000)
    componentes_data = get_api_data('componentes', page=1, per_page=1000)
    
    total_mecanicas = mecanicas_data['count']
    total_temas = temas_data['count']
    total_componentes = componentes_data['count']
    
    # Jogos recentes (últimos 5 criados)
    jogos_recentes = jogos_criados[-5:] if jogos_criados else []
    
    return render(request, 'home.html', {
        'total_jogos': total_jogos,
        'total_mecanicas': total_mecanicas,
        'total_componentes': total_componentes,
        'total_temas': total_temas,
        'jogos_recentes': jogos_recentes,
    })

@login_required
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
            'peso': 2.3,
            'setup': [],
            'mecanicas': ['Construção', 'Negociação'],
            'temas': ['Medieval', 'Colonização']
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
            'peso': 1.8,
            'setup': [],
            'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
            'temas': ['Transporte', 'Viagem']
        }
    ]
    
    # Adicionar jogos criados pelo usuário
    todos_jogos = jogos_exemplo + jogos_criados
    
    # Processar busca
    busca = request.GET.get('busca', '').strip().lower()
    if busca:
        jogos_filtrados = []
        for jogo in todos_jogos:
            # Buscar no nome
            if busca in jogo.get('nome', '').lower():
                jogos_filtrados.append(jogo)
                continue
            
            # Buscar no ID
            if busca in str(jogo.get('id', '')):
                jogos_filtrados.append(jogo)
                continue
            
            # Buscar no subtítulo
            if busca in jogo.get('subtitulo', '').lower():
                jogos_filtrados.append(jogo)
                continue
            
            # Buscar nas mecânicas
            mecanicas = jogo.get('mecanicas', [])
            if any(busca in str(mecanica).lower() for mecanica in mecanicas):
                jogos_filtrados.append(jogo)
                continue
            
            # Buscar nos temas
            temas = jogo.get('temas', [])
            if any(busca in str(tema).lower() for tema in temas):
                jogos_filtrados.append(jogo)
                continue
        
        todos_jogos = jogos_filtrados
    
    return render(request, 'jogos/lista.html', {'jogos': {'results': todos_jogos}})

@autor_or_admin_required
def jogo_novo(request):
    global jogos_criados, usuarios_criados, usuario_logado
    
    # Buscar usuários para dropdowns
    usuarios_sistema = [
        {'nome': 'Admin Sistema', 'perfil': 'ADMINISTRADOR'},
        {'nome': 'Autor Sistema', 'perfil': 'AUTOR'},
        {'nome': 'Revisor Sistema', 'perfil': 'REVISOR'},
    ]
    todos_usuarios = usuarios_sistema + usuarios_criados
    autores = [u for u in todos_usuarios if u['perfil'] in ['AUTOR', 'ADMINISTRADOR']]
    revisores = [u for u in todos_usuarios if u['perfil'] in ['REVISOR', 'ADMINISTRADOR']]
    
    if request.method == 'POST':
        print("Dados recebidos:", request.POST)  # Debug
        
        nome = request.POST.get('nome')
        if nome:
            # Processar upload da capa
            capa_path = None
            if 'capa' in request.FILES:
                capa_path = salvar_imagem_capa(request.FILES['capa'])
            
            # Preencher autor/revisor automaticamente baseado no usuário logado
            autor_automatico = ''
            revisor_automatico = ''
            
            if usuario_logado:
                if usuario_logado['perfil'] == 'AUTOR':
                    autor_automatico = usuario_logado['nome']
                elif usuario_logado['perfil'] == 'REVISOR':
                    revisor_automatico = usuario_logado['nome']
                elif usuario_logado['perfil'] == 'ADMINISTRADOR':
                    # Administrador pode ser tanto autor quanto revisor
                    autor_automatico = usuario_logado['nome']
                    revisor_automatico = usuario_logado['nome']
            
            # Criar novo jogo
            novo_jogo = {
                'id': len(jogos_criados) + 100,  # ID único
                'nome': nome,
                'subtitulo': request.POST.get('subtitulo', ''),
                'descricao_curta': request.POST.get('descricao_curta', ''),
                'historia': request.POST.get('historia', ''),
                'autor': autor_automatico,
                'revisor': revisor_automatico,
                'capa': capa_path,
                'jogadores_min': int(request.POST.get('jogadores_min', 1)),
                'jogadores_max': int(request.POST.get('jogadores_max', 4)),
                'tempo_min': int(request.POST.get('tempo_min', 30)),
                'tempo_max': int(request.POST.get('tempo_max', 60)),
                'idade_recomendada': int(request.POST.get('idade_recomendada', 10)),
                
                # Campos complexos
                'mecanicas': [m for m in request.POST.getlist('mecanicas[]') if m.strip()],
                'temas': [t for t in request.POST.getlist('temas[]') if t.strip()],
                'componentes': [],
                'condicoes_vitoria': [c for c in request.POST.getlist('condicoes_vitoria[]') if c.strip()],
                'condicoes_derrota': [c for c in request.POST.getlist('condicoes_derrota[]') if c.strip()],
                
                # Estruturas e setup
                'estruturas': [],
                'setup': [],
                'glossario': []
            }
            
            # Processar componentes com quantidade
            componentes_nomes = request.POST.getlist('componentes[]')
            componentes_qtds = request.POST.getlist('componentes_qtd[]')
            
            for i, nome_comp in enumerate(componentes_nomes):
                if nome_comp.strip():
                    qtd = componentes_qtds[i] if i < len(componentes_qtds) else '1'
                    novo_jogo['componentes'].append(f"{nome_comp} (x{qtd})")
            
            # Processar estruturas
            estruturas_nomes = request.POST.getlist('estruturas_nome[]')
            estruturas_tipos = request.POST.getlist('estruturas_tipo[]')
            estruturas_classificacoes = request.POST.getlist('estruturas_classificacao[]')
            estruturas_desc = request.POST.getlist('estruturas_descricao[]')
            
            for i, nome_est in enumerate(estruturas_nomes):
                if nome_est.strip():
                    estrutura = {
                        'nome': nome_est,
                        'tipo': estruturas_tipos[i] if i < len(estruturas_tipos) else 'FASE',
                        'classificacao': estruturas_classificacoes[i] if i < len(estruturas_classificacoes) else 'NEUTRO',
                        'descricao': estruturas_desc[i] if i < len(estruturas_desc) else '',
                        'condicoes_especiais': []
                    }
                    
                    # Processar condições especiais desta estrutura
                    cond_nomes_key = f'condicoes_especiais_nome[{i}][]'
                    cond_desc_key = f'condicoes_especiais_desc[{i}][]'
                    cond_tipo_key = f'condicoes_especiais_tipo[{i}][]'
                    
                    if cond_nomes_key in request.POST:
                        cond_nomes = request.POST.getlist(cond_nomes_key)
                        cond_desc = request.POST.getlist(cond_desc_key)
                        cond_tipos = request.POST.getlist(cond_tipo_key)
                        
                        for j, cond_nome in enumerate(cond_nomes):
                            if cond_nome.strip():
                                estrutura['condicoes_especiais'].append({
                                    'nome': cond_nome,
                                    'descricao': cond_desc[j] if j < len(cond_desc) else '',
                                    'tipo': cond_tipos[j] if j < len(cond_tipos) else 'NEUTRO'
                                })
                    
                    novo_jogo['estruturas'].append(estrutura)
            
            # Processar setup
            novo_jogo['setup'] = []
            setup_nomes = request.POST.getlist('setup_nome[]')
            setup_desc = request.POST.getlist('setup_descricao[]')
            
            for i, nome_setup in enumerate(setup_nomes):
                if nome_setup.strip():
                    setup = {
                        'nome': nome_setup,
                        'descricao': setup_desc[i] if i < len(setup_desc) else '',
                        'imagens': []
                    }
                    
                    # Processar imagens do setup
                    img_desc_key = f'setup_img_desc[{i}][]'
                    
                    if img_desc_key in request.POST:
                        img_desc = request.POST.getlist(img_desc_key)
                        
                        for j, desc in enumerate(img_desc):
                            if desc.strip():
                                # Verificar se há arquivo de imagem correspondente
                                img_file_key = f'setup_img_file[{i}][]'
                                if img_file_key in request.FILES:
                                    files = request.FILES.getlist(img_file_key)
                                    if j < len(files) and files[j]:
                                        # Salvar imagem no sistema de arquivos
                                        caminho_imagem = salvar_imagem_setup(files[j])
                                        setup['imagens'].append({
                                            'descricao': desc,
                                            'imagem': caminho_imagem
                                        })
                                    else:
                                        setup['imagens'].append({
                                            'descricao': desc,
                                            'imagem': None
                                        })
                                else:
                                    setup['imagens'].append({
                                        'descricao': desc,
                                        'imagem': None
                                    })
                    
                    novo_jogo['setup'].append(setup)
            
            # Processar glossário
            glossario_palavras = request.POST.getlist('glossario_palavra[]')
            glossario_definicoes = request.POST.getlist('glossario_definicao[]')
            
            for i, palavra in enumerate(glossario_palavras):
                if palavra.strip():
                    # Processar imagem do glossário
                    imagem_path = None
                    if 'glossario_imagem[]' in request.FILES:
                        imagens = request.FILES.getlist('glossario_imagem[]')
                        if i < len(imagens) and imagens[i]:
                            imagem_path = salvar_imagem_glossario(imagens[i])
                    
                    novo_jogo['glossario'].append({
                        'palavra': palavra,
                        'definicao': glossario_definicoes[i] if i < len(glossario_definicoes) else '',
                        'imagem': imagem_path
                    })
            
            # Calcular peso automaticamente
            novo_jogo['peso'] = calcular_peso_jogo(novo_jogo)
            
            # Usar versão manual personalizada do formulário ou calcular automaticamente
            versao_personalizada = request.POST.get('versao_manual')
            if versao_personalizada and versao_personalizada.strip():
                novo_jogo['versao_manual'] = versao_personalizada.strip()
            else:
                novo_jogo['versao_manual'] = calcular_versao_manual(novo_jogo)
            
            # Adicionar à lista
            jogos_criados.append(novo_jogo)
            print(f"Jogo completo adicionado: {novo_jogo}")  # Debug
            
            messages.success(request, f'Jogo "{nome}" criado com sucesso!')
            return redirect('jogos_lista')
        else:
            messages.error(request, 'Nome do jogo é obrigatório.')
    
    return render(request, 'jogos/novo.html', {
        'autores': autores, 
        'revisores': revisores,
        'usuario_logado': usuario_logado
    })

@autor_or_admin_required
def mecanicas_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    busca = request.GET.get('busca', '').strip()
    
    data = get_api_data('mecanicas', page, per_page, busca)
    
    return render(request, 'mecanicas/lista.html', {
        'mecanicas': data['results'],
        'pagination': data
    })

@autor_or_admin_required
def mecanica_novo(request):
    global mecanicas_criadas
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        if nome:
            nova_mecanica = {
                'id': len(mecanicas_criadas) + 1000,
                'nome': nome,
                'descricao': descricao
            }
            mecanicas_criadas.append(nova_mecanica)
            messages.success(request, 'Mecânica criada com sucesso!')
        else:
            messages.error(request, 'Nome é obrigatório!')
        return redirect('mecanicas_lista')
    return render(request, 'mecanicas/novo.html')

@autor_or_admin_required
def componentes_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    busca = request.GET.get('busca', '').strip()
    
    data = get_api_data('componentes', page, per_page, busca)
    
    return render(request, 'componentes/lista.html', {
        'componentes': data['results'],
        'pagination': data
    })

@autor_or_admin_required
def componente_novo(request):
    global componentes_criados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        tipo = request.POST.get('tipo', 'TATICO')
        if nome:
            novo_componente = {
                'id': len(componentes_criados) + 2000,
                'nome': nome,
                'descricao': descricao,
                'tipo': tipo
            }
            componentes_criados.append(novo_componente)
            messages.success(request, 'Componente criado com sucesso!')
        else:
            messages.error(request, 'Nome é obrigatório!')
        return redirect('componentes_lista')
    return render(request, 'componentes/novo.html')

@autor_or_admin_required
def temas_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    busca = request.GET.get('busca', '').strip()
    
    data = get_api_data('temas', page, per_page, busca)
    
    return render(request, 'temas/lista.html', {
        'temas': data['results'],
        'pagination': data
    })

@autor_or_admin_required
def tema_novo(request):
    global temas_criados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        if nome:
            novo_tema = {
                'id': len(temas_criados) + 3000,
                'nome': nome,
                'descricao': descricao
            }
            temas_criados.append(novo_tema)
            messages.success(request, 'Tema criado com sucesso!')
        else:
            messages.error(request, 'Nome é obrigatório!')
        return redirect('temas_lista')
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
    data = get_api_data(endpoint, page=1, per_page=1000, busca=search_query)
    
    return JsonResponse(data)

@admin_required
def jogo_excluir(request, jogo_id):
    global jogos_criados
    
    # Remover da lista de jogos criados
    jogos_criados = [jogo for jogo in jogos_criados if jogo['id'] != int(jogo_id)]
    
    messages.success(request, 'Jogo excluído com sucesso!')
    return redirect('jogos_lista')

@editor_required
def jogo_editar(request, jogo_id):
    global jogos_criados, usuarios_criados
    
    # Buscar usuários para dropdowns
    usuarios_sistema = [
        {'nome': 'Admin Sistema', 'perfil': 'ADMINISTRADOR'},
        {'nome': 'Autor Sistema', 'perfil': 'AUTOR'},
        {'nome': 'Revisor Sistema', 'perfil': 'REVISOR'},
    ]
    todos_usuarios = usuarios_sistema + usuarios_criados
    autores = [u for u in todos_usuarios if u['perfil'] in ['AUTOR', 'ADMINISTRADOR']]
    revisores = [u for u in todos_usuarios if u['perfil'] in ['REVISOR', 'ADMINISTRADOR']]
    
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
        # Processar upload da capa
        if 'capa' in request.FILES:
            capa_path = salvar_imagem_capa(request.FILES['capa'])
            if capa_path:
                jogo['capa'] = capa_path
        elif request.POST.get('capa_existente'):
            # Preservar capa existente se não há nova imagem
            jogo['capa'] = request.POST.get('capa_existente')
        
        # Atualizar campos básicos
        jogo['nome'] = request.POST.get('nome', jogo['nome'])
        jogo['subtitulo'] = request.POST.get('subtitulo', jogo['subtitulo'])
        jogo['descricao_curta'] = request.POST.get('descricao_curta', jogo['descricao_curta'])
        jogo['historia'] = request.POST.get('historia', jogo.get('historia', ''))
        # Atualizar autor/revisor com proteção (adicionar co-autor/co-revisor se já existir)
        if usuario_logado:
            if usuario_logado['perfil'] == 'AUTOR':
                if jogo.get('autor') and jogo['autor'] != usuario_logado['nome']:
                    # Já existe autor diferente, adicionar como co-autor
                    jogo['co_autor'] = usuario_logado['nome']
                else:
                    # Não existe autor ou é o mesmo usuário
                    jogo['autor'] = usuario_logado['nome']
            elif usuario_logado['perfil'] == 'REVISOR':
                if jogo.get('revisor') and jogo['revisor'] != usuario_logado['nome']:
                    # Já existe revisor diferente, adicionar como co-revisor
                    jogo['co_revisor'] = usuario_logado['nome']
                else:
                    # Não existe revisor ou é o mesmo usuário
                    jogo['revisor'] = usuario_logado['nome']
            elif usuario_logado['perfil'] == 'ADMINISTRADOR':
                # Administrador pode atualizar ambos sem proteção
                jogo['autor'] = usuario_logado['nome']
                jogo['revisor'] = usuario_logado['nome']
        jogo['jogadores_min'] = int(request.POST.get('jogadores_min', jogo['jogadores_min']))
        jogo['jogadores_max'] = int(request.POST.get('jogadores_max', jogo['jogadores_max']))
        jogo['tempo_min'] = int(request.POST.get('tempo_min', jogo['tempo_min']))
        jogo['tempo_max'] = int(request.POST.get('tempo_max', jogo['tempo_max']))
        jogo['idade_recomendada'] = int(request.POST.get('idade_recomendada', jogo['idade_recomendada']))
        
        # Atualizar campos complexos
        jogo['mecanicas'] = [m for m in request.POST.getlist('mecanicas[]') if m.strip()]
        jogo['temas'] = [t for t in request.POST.getlist('temas[]') if t.strip()]
        
        # Processar componentes com quantidade
        jogo['componentes'] = []
        componentes_nomes = request.POST.getlist('componentes[]')
        componentes_qtds = request.POST.getlist('componentes_qtd[]')
        
        for i, nome_comp in enumerate(componentes_nomes):
            if nome_comp.strip():
                qtd = componentes_qtds[i] if i < len(componentes_qtds) else '1'
                jogo['componentes'].append(f"{nome_comp} (x{qtd})")
        jogo['condicoes_vitoria'] = [c for c in request.POST.getlist('condicoes_vitoria[]') if c.strip()]
        jogo['condicoes_derrota'] = [c for c in request.POST.getlist('condicoes_derrota[]') if c.strip()]
        
        # Atualizar estruturas
        jogo['estruturas'] = []
        estruturas_nomes = request.POST.getlist('estruturas_nome[]')
        estruturas_tipos = request.POST.getlist('estruturas_tipo[]')
        estruturas_classificacoes = request.POST.getlist('estruturas_classificacao[]')
        estruturas_desc = request.POST.getlist('estruturas_descricao[]')
        
        for i, nome_est in enumerate(estruturas_nomes):
            if nome_est.strip():
                estrutura = {
                    'nome': nome_est,
                    'tipo': estruturas_tipos[i] if i < len(estruturas_tipos) else 'FASE',
                    'classificacao': estruturas_classificacoes[i] if i < len(estruturas_classificacoes) else 'NEUTRO',
                    'descricao': estruturas_desc[i] if i < len(estruturas_desc) else '',
                    'condicoes_especiais': []
                }
                
                # Processar condições especiais
                cond_nomes_key = f'condicoes_especiais_nome[{i}][]'
                cond_desc_key = f'condicoes_especiais_desc[{i}][]'
                cond_tipo_key = f'condicoes_especiais_tipo[{i}][]'
                
                if cond_nomes_key in request.POST:
                    cond_nomes = request.POST.getlist(cond_nomes_key)
                    cond_desc = request.POST.getlist(cond_desc_key)
                    cond_tipos = request.POST.getlist(cond_tipo_key)
                    
                    for j, cond_nome in enumerate(cond_nomes):
                        if cond_nome.strip():
                            estrutura['condicoes_especiais'].append({
                                'nome': cond_nome,
                                'descricao': cond_desc[j] if j < len(cond_desc) else '',
                                'tipo': cond_tipos[j] if j < len(cond_tipos) else 'NEUTRO'
                            })
                
                jogo['estruturas'].append(estrutura)
        
        # Atualizar setup
        jogo['setup'] = []
        setup_nomes = request.POST.getlist('setup_nome[]')
        setup_desc = request.POST.getlist('setup_descricao[]')
        
        for i, nome_setup in enumerate(setup_nomes):
            if nome_setup.strip():
                setup = {
                    'nome': nome_setup,
                    'descricao': setup_desc[i] if i < len(setup_desc) else '',
                    'imagens': []
                }
                
                # Processar imagens do setup
                img_desc_key = f'setup_img_desc[{i}][]'
                
                if img_desc_key in request.POST:
                    img_desc = request.POST.getlist(img_desc_key)
                    
                    for j, desc in enumerate(img_desc):
                        if desc.strip():
                            # Preservar imagem existente ou usar nova
                            imagem_path = None
                            
                            # Verificar se há arquivo de imagem correspondente
                            img_file_key = f'setup_img_file[{i}][]'
                            if img_file_key in request.FILES:
                                files = request.FILES.getlist(img_file_key)
                                if j < len(files) and files[j]:
                                    # Salvar nova imagem
                                    imagem_path = salvar_imagem_setup(files[j])
                            
                            # Se não há nova imagem, tentar preservar a existente
                            if not imagem_path:
                                img_existente_key = f'setup_img_existente[{i}][]'
                                if img_existente_key in request.POST:
                                    imagens_existentes = request.POST.getlist(img_existente_key)
                                    if j < len(imagens_existentes) and imagens_existentes[j]:
                                        imagem_path = imagens_existentes[j]
                            
                            setup['imagens'].append({
                                'descricao': desc,
                                'imagem': imagem_path
                            })
                
                jogo['setup'].append(setup)
        
        # Atualizar glossário
        jogo['glossario'] = []
        glossario_palavras = request.POST.getlist('glossario_palavra[]')
        glossario_definicoes = request.POST.getlist('glossario_definicao[]')
        imagens_existentes = request.POST.getlist('glossario_imagem_existente[]')
        
        for i, palavra in enumerate(glossario_palavras):
            if palavra.strip():
                # Preservar imagem existente ou usar nova
                imagem_path = None
                
                # Verificar se há nova imagem sendo enviada
                if 'glossario_imagem[]' in request.FILES:
                    imagens = request.FILES.getlist('glossario_imagem[]')
                    if i < len(imagens) and imagens[i]:
                        imagem_path = salvar_imagem_glossario(imagens[i])
                
                # Se não há nova imagem, usar a existente
                if not imagem_path and i < len(imagens_existentes) and imagens_existentes[i]:
                    imagem_path = imagens_existentes[i]
                
                jogo['glossario'].append({
                    'palavra': palavra,
                    'definicao': glossario_definicoes[i] if i < len(glossario_definicoes) else '',
                    'imagem': imagem_path
                })
        
        # Recalcular peso automaticamente
        jogo['peso'] = calcular_peso_jogo(jogo)
        
        # Usar versão manual personalizada do formulário ou incrementar automaticamente
        versao_personalizada = request.POST.get('versao_manual')
        if versao_personalizada and versao_personalizada.strip():
            jogo['versao_manual'] = versao_personalizada.strip()
        else:
            # Incrementar versão do manual (patch) ao editar
            versao_atual = jogo.get('versao_manual', '1.0.0')
            partes = versao_atual.split('.')
            major = int(partes[0]) if len(partes) > 0 else 1
            minor = int(partes[1]) if len(partes) > 1 else 0
            patch = int(partes[2]) if len(partes) > 2 else 0
            
            # Sempre incrementar patch ao editar (alteração de campo existente)
            jogo['versao_manual'] = f"{major}.{minor}.{patch + 1}"
        
        messages.success(request, f'Jogo "{jogo["nome"]}" atualizado com sucesso!')
        return redirect('jogos_lista')
    
    return render(request, 'jogos/editar.html', {
        'jogo': jogo, 
        'autores': autores, 
        'revisores': revisores,
        'usuario_logado': usuario_logado
    })

@admin_required
def jogo_copiar(request, jogo_id):
    global jogos_criados
    
    # Encontrar o jogo original
    jogo_original = None
    
    # Buscar nos jogos criados
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo_original = j
            break
    
    # Buscar nos jogos de exemplo se não encontrou
    if not jogo_original:
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
                'peso': 2.3,
                'setup': [],
                'mecanicas': ['Construção', 'Negociação'],
                'temas': ['Medieval', 'Colonização'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
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
                'peso': 1.8,
                'setup': [],
                'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
                'temas': ['Transporte', 'Viagem'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
            }
        ]
        
        for j in jogos_exemplo:
            if j['id'] == int(jogo_id):
                jogo_original = j
                break
    
    if not jogo_original:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    # Criar cópia do jogo
    import copy
    jogo_copia = copy.deepcopy(jogo_original)
    
    # Atualizar dados da cópia
    jogo_copia['id'] = len(jogos_criados) + 100  # Novo ID único
    jogo_copia['nome'] = f"{jogo_original['nome']} - Cópia"
    
    # Incrementar versão major (1.X.X → 2.X.X) para cópias
    versao_original = jogo_original.get('versao_manual', '1.0.0')
    partes = versao_original.split('.')
    major_original = int(partes[0]) if len(partes) > 0 else 1
    minor = int(partes[1]) if len(partes) > 1 else 0
    
    # Nova versão com major incrementado
    nova_versao_major = major_original + 1
    jogo_copia['versao_manual'] = f"{nova_versao_major}.{minor}.0"
    
    # Adicionar à lista de jogos criados
    jogos_criados.append(jogo_copia)
    
    messages.success(request, f'Cópia do jogo "{jogo_original["nome"]}" criada com sucesso!')
    return redirect('jogo_detalhes', jogo_id=jogo_copia['id'])

@login_required
def jogo_detalhes(request, jogo_id):
    global jogos_criados, comentarios_criados, usuario_logado
    
    # Encontrar o jogo
    jogo = None
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo = j
            break
    
    # Buscar nos jogos de exemplo se não encontrou
    if not jogo:
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
                'peso': 2.3,
                'versao_manual': '1.0.0',
                'autor': 'Klaus Teuber',
                'revisor': 'João Silva',
                'setup': [],
                'mecanicas': ['Construção', 'Negociação'],
                'temas': ['Medieval', 'Colonização'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
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
                'peso': 1.8,
                'versao_manual': '1.0.0',
                'autor': 'Alan R. Moon',
                'revisor': 'Admin Sistema',
                'setup': [],
                'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
                'temas': ['Transporte', 'Viagem'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
            }
        ]
        
        for j in jogos_exemplo:
            if j['id'] == int(jogo_id):
                jogo = j
                break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    # Processar markdown nos campos de texto
    jogo_processado = jogo.copy()
    if jogo.get('descricao_curta'):
        jogo_processado['descricao_curta_html'] = processar_markdown(jogo['descricao_curta'])
    if jogo.get('historia'):
        jogo_processado['historia_html'] = processar_markdown(jogo['historia'])
    
    # Processar condições de vitória e derrota
    if jogo.get('condicoes_vitoria'):
        jogo_processado['condicoes_vitoria_html'] = [processar_markdown(c) for c in jogo['condicoes_vitoria']]
    if jogo.get('condicoes_derrota'):
        jogo_processado['condicoes_derrota_html'] = [processar_markdown(c) for c in jogo['condicoes_derrota']]
    
    # Processar setup
    if jogo.get('setup'):
        setup_processado = []
        for setup in jogo['setup']:
            setup_copy = setup.copy()
            if setup.get('descricao'):
                setup_copy['descricao_html'] = processar_markdown(setup['descricao'])
            setup_processado.append(setup_copy)
        jogo_processado['setup_processado'] = setup_processado
    
    # Processar estruturas
    if jogo.get('estruturas'):
        estruturas_processadas = []
        for estrutura in jogo['estruturas']:
            estrutura_copy = estrutura.copy()
            if estrutura.get('descricao'):
                estrutura_copy['descricao_html'] = processar_markdown(estrutura['descricao'])
            
            # Processar condições especiais
            if estrutura.get('condicoes_especiais'):
                condicoes_processadas = []
                for condicao in estrutura['condicoes_especiais']:
                    condicao_copy = condicao.copy()
                    if condicao.get('descricao'):
                        condicao_copy['descricao_html'] = processar_markdown(condicao['descricao'])
                    condicoes_processadas.append(condicao_copy)
                estrutura_copy['condicoes_especiais_processadas'] = condicoes_processadas
            
            estruturas_processadas.append(estrutura_copy)
        jogo_processado['estruturas_processadas'] = estruturas_processadas
    
    # Processar glossário
    if jogo.get('glossario'):
        glossario_processado = []
        for termo in jogo['glossario']:
            termo_copy = termo.copy()
            if termo.get('definicao'):
                termo_copy['definicao_html'] = processar_markdown(termo['definicao'])
            glossario_processado.append(termo_copy)
        jogo_processado['glossario_processado'] = glossario_processado
    
    # Calcular classificações
    classificacoes = calcular_classificacao_jogo(jogo)
    
    # Processar comentário se enviado
    if request.method == 'POST' and 'comentario' in request.POST:
        comentario_texto = request.POST.get('comentario', '').strip()
        avaliacao = request.POST.get('avaliacao')
        
        if comentario_texto and avaliacao and usuario_logado:
            from datetime import datetime
            novo_comentario = {
                'id': len(comentarios_criados) + 1,
                'jogo_id': int(jogo_id),
                'usuario': usuario_logado['nome'],
                'comentario': comentario_texto,
                'avaliacao': int(avaliacao),
                'created_at': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            comentarios_criados.append(novo_comentario)
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('jogo_detalhes', jogo_id=jogo_id)
    
    # Buscar comentários do jogo
    comentarios_jogo = [c for c in comentarios_criados if c['jogo_id'] == int(jogo_id)]
    
    # Calcular média de avaliações
    media_avaliacoes = 0
    if comentarios_jogo:
        media_avaliacoes = round(sum(c['avaliacao'] for c in comentarios_jogo) / len(comentarios_jogo), 1)
    
    return render(request, 'jogos/detalhes.html', {
        'jogo': jogo_processado, 
        'classificacoes': classificacoes,
        'comentarios': comentarios_jogo,
        'media_avaliacoes': media_avaliacoes
    })

def jogo_imprimir(request, jogo_id):
    global jogos_criados
    
    # Encontrar o jogo
    jogo = None
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo = j
            break
    
    # Buscar nos jogos de exemplo se não encontrou
    if not jogo:
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
                'peso': 2.3,
                'versao_manual': '1.0.0',
                'autor': 'Klaus Teuber',
                'revisor': 'João Silva',
                'setup': [],
                'mecanicas': ['Construção', 'Negociação'],
                'temas': ['Medieval', 'Colonização'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
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
                'peso': 1.8,
                'versao_manual': '1.0.0',
                'autor': 'Alan R. Moon',
                'revisor': 'Admin Sistema',
                'setup': [],
                'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
                'temas': ['Transporte', 'Viagem'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
            }
        ]
        
        for j in jogos_exemplo:
            if j['id'] == int(jogo_id):
                jogo = j
                break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    # Processar markdown nos campos de texto
    jogo_processado = jogo.copy()
    if jogo.get('descricao_curta'):
        jogo_processado['descricao_curta_html'] = processar_markdown(jogo['descricao_curta'])
    if jogo.get('historia'):
        jogo_processado['historia_html'] = processar_markdown(jogo['historia'])
    
    # Processar condições de vitória e derrota
    if jogo.get('condicoes_vitoria'):
        jogo_processado['condicoes_vitoria_html'] = [processar_markdown(c) for c in jogo['condicoes_vitoria']]
    if jogo.get('condicoes_derrota'):
        jogo_processado['condicoes_derrota_html'] = [processar_markdown(c) for c in jogo['condicoes_derrota']]
    
    # Processar setup
    if jogo.get('setup'):
        setup_processado = []
        for setup in jogo['setup']:
            setup_copy = setup.copy()
            if setup.get('descricao'):
                setup_copy['descricao_html'] = processar_markdown(setup['descricao'])
            setup_processado.append(setup_copy)
        jogo_processado['setup_processado'] = setup_processado
    
    # Processar estruturas
    if jogo.get('estruturas'):
        estruturas_processadas = []
        for estrutura in jogo['estruturas']:
            estrutura_copy = estrutura.copy()
            if estrutura.get('descricao'):
                estrutura_copy['descricao_html'] = processar_markdown(estrutura['descricao'])
            
            # Processar condições especiais
            if estrutura.get('condicoes_especiais'):
                condicoes_processadas = []
                for condicao in estrutura['condicoes_especiais']:
                    condicao_copy = condicao.copy()
                    if condicao.get('descricao'):
                        condicao_copy['descricao_html'] = processar_markdown(condicao['descricao'])
                    condicoes_processadas.append(condicao_copy)
                estrutura_copy['condicoes_especiais_processadas'] = condicoes_processadas
            
            estruturas_processadas.append(estrutura_copy)
        jogo_processado['estruturas_processadas'] = estruturas_processadas
    
    # Processar glossário
    if jogo.get('glossario'):
        glossario_processado = []
        for termo in jogo['glossario']:
            termo_copy = termo.copy()
            if termo.get('definicao'):
                termo_copy['definicao_html'] = processar_markdown(termo['definicao'])
            glossario_processado.append(termo_copy)
        jogo_processado['glossario_processado'] = glossario_processado
    
    # Calcular classificações
    classificacoes = calcular_classificacao_jogo(jogo)
    
    return render(request, 'jogos/imprimir.html', {'jogo': jogo_processado, 'classificacoes': classificacoes})

def calcular_versao_manual(jogo_data):
    """Calcula a versão do manual baseado no conteúdo do jogo"""
    # Versão base do jogo (sempre 1)
    versao_jogo = 1
    
    # Contar apenas campos preenchidos para versão minor
    campos_preenchidos = 0
    
    # Campos básicos (cada um conta como 1)
    if jogo_data.get('nome') and jogo_data['nome'].strip(): campos_preenchidos += 1
    if jogo_data.get('subtitulo') and jogo_data['subtitulo'].strip(): campos_preenchidos += 1
    if jogo_data.get('descricao_curta') and jogo_data['descricao_curta'].strip(): campos_preenchidos += 1
    if jogo_data.get('historia') and jogo_data['historia'].strip(): campos_preenchidos += 1
    
    # Listas de itens (cada item conta como 1)
    mecanicas = [m for m in jogo_data.get('mecanicas', []) if m and m.strip()]
    temas = [t for t in jogo_data.get('temas', []) if t and t.strip()]
    componentes = [c for c in jogo_data.get('componentes', []) if c and c.strip()]
    
    # Contar apenas se há itens
    if mecanicas: campos_preenchidos += len(mecanicas)
    if temas: campos_preenchidos += len(temas)
    if componentes: campos_preenchidos += len(componentes)
    
    # Condições
    vitorias = [c for c in jogo_data.get('condicoes_vitoria', []) if c and c.strip()]
    derrotas = [c for c in jogo_data.get('condicoes_derrota', []) if c and c.strip()]
    if vitorias: campos_preenchidos += len(vitorias)
    if derrotas: campos_preenchidos += len(derrotas)
    
    # Setup
    setup = jogo_data.get('setup', [])
    if setup: campos_preenchidos += len(setup)
    
    # Estruturas
    estruturas = jogo_data.get('estruturas', [])
    if estruturas: 
        campos_preenchidos += len(estruturas)
        # Condições especiais
        for estrutura in estruturas:
            condicoes = estrutura.get('condicoes_especiais', [])
            if condicoes: campos_preenchidos += len(condicoes)
    
    # Glossário
    glossario = jogo_data.get('glossario', [])
    if glossario: campos_preenchidos += len(glossario)
    
    # Versão minor: 0 se vazio, senão baseado em campos (máximo 20)
    versao_minor = min(campos_preenchidos, 20) if campos_preenchidos > 0 else 0
    
    # Versão patch: sempre 0 para jogos novos, incrementa apenas com edições
    versao_patch = 0
    
    return f"{versao_jogo}.{versao_minor}.{versao_patch}"

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

def calcular_classificacao_jogo(jogo_data):
    """Calcula as classificações do jogo baseado em componentes, estruturas e condições especiais"""
    classificacoes = {
        'NEUTRO': 0,
        'SORTE': 0,
        'TATICO': 0,
        'HABILIDADE': 0,
        'LUDICO': 0,
        'GERENCIAMENTO': 0
    }
    
    # Mapeamento de componentes para classificações
    componentes_classificacao = {
        'Meeple de Madeira': 'NEUTRO', 'Dados D6': 'SORTE', 'Dados Poliédricos': 'SORTE',
        'Cartas Standard': 'TATICO', 'Cartas Mini': 'TATICO', 'Tabuleiro Principal': 'NEUTRO',
        'Tabuleiros Individuais': 'GERENCIAMENTO', 'Moedas de Metal': 'GERENCIAMENTO',
        'Moedas de Papel/Cartão': 'GERENCIAMENTO', 'Cubos de Madeira': 'GERENCIAMENTO',
        'Miniaturas de Plástico': 'LUDICO', 'Marcadores de Pontuação': 'GERENCIAMENTO',
        'Ampulheta': 'HABILIDADE', 'Escudo de Jogador': 'TATICO', 'Fichas de Poker': 'GERENCIAMENTO',
        'Tiles Hexagonais': 'TATICO', 'Tiles Quadrados': 'TATICO', 'Marcador de Primeiro Jogador': 'NEUTRO',
        'Saco de Pano (Bag)': 'SORTE', 'Gemas de Plástico/Acrílico': 'LUDICO', 'Peões de Plástico': 'NEUTRO',
        'Discos de Madeira': 'NEUTRO', 'Cartas de Referência': 'NEUTRO', 'Manual de Regras': 'NEUTRO',
        'Livro de Cenários': 'LUDICO', 'Divisórias de Caixa (Insert)': 'GERENCIAMENTO',
        'Adesivos': 'LUDICO', 'Canetas Dry-Erase': 'HABILIDADE', 'Lápis': 'HABILIDADE',
        'Blocos de Pontuação': 'GERENCIAMENTO', 'Clip de Plástico': 'GERENCIAMENTO',
        'Suporte de Cartas': 'NEUTRO', 'Torre de Dados': 'SORTE', 'Bandeja de Dados': 'SORTE',
        'Marcadores de Dano': 'GERENCIAMENTO', 'Peças de Encaixe': 'HABILIDADE',
        'Engrenagens de Papelão': 'TATICO', 'Bússola de Papelão': 'TATICO',
        'Luva de Cartas (Sleeves)': 'NEUTRO', 'Meeples de Animais': 'LUDICO',
        'Recipientes de Armazenamento': 'GERENCIAMENTO', 'Cartas Transparentes': 'TATICO',
        'Espelho': 'HABILIDADE', 'Peças de Resina Especiais': 'LUDICO', 'Playmat de Neoprene': 'NEUTRO',
        'Marcadores de Nível': 'GERENCIAMENTO', 'Relógio de Xadrez': 'HABILIDADE',
        'Cartas de Evento': 'SORTE', 'Tiles de Terreno': 'TATICO'
    }
    
    # Contar componentes
    for componente in jogo_data.get('componentes', []):
        nome_comp = componente.split(' (x')[0].strip()  # Remove quantidade
        if nome_comp in componentes_classificacao:
            classificacoes[componentes_classificacao[nome_comp]] += 1
    
    # Contar estruturas
    for estrutura in jogo_data.get('estruturas', []):
        classificacao = estrutura.get('classificacao', 'NEUTRO')
        if classificacao in classificacoes:
            classificacoes[classificacao] += 1
        
        # Contar condições especiais
        for condicao in estrutura.get('condicoes_especiais', []):
            tipo_condicao = condicao.get('tipo', 'NEUTRO')
            if tipo_condicao in classificacoes:
                classificacoes[tipo_condicao] += 1
    
    # Calcular percentuais
    total = sum(classificacoes.values())
    if total == 0:
        return {'NEUTRO': 100, 'SORTE': 0, 'TATICO': 0, 'HABILIDADE': 0, 'LUDICO': 0, 'GERENCIAMENTO': 0}
    
    percentuais = {}
    for tipo, count in classificacoes.items():
        percentuais[tipo] = round((count / total) * 100, 1)
    
    return percentuais

@autor_or_admin_required
def mecanica_editar(request, item_id):
    global mecanicas_criadas
    # Buscar dados da mecânica dos dados locais
    mecanicas_data = get_api_data('mecanicas', page=1, per_page=1000)
    item = None
    for mecanica in mecanicas_data['results']:
        if mecanica['id'] == item_id:
            item = mecanica
            break
    
    if not item:
        messages.error(request, 'Mecânica não encontrada!')
        return redirect('mecanicas_lista')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        
        # Atualizar se for item criado pelo usuário (ID >= 1000)
        if item_id >= 1000:
            for i, m in enumerate(mecanicas_criadas):
                if m['id'] == item_id:
                    mecanicas_criadas[i]['nome'] = nome
                    mecanicas_criadas[i]['descricao'] = descricao
                    break
            messages.success(request, 'Mecânica atualizada com sucesso!')
        else:
            messages.warning(request, 'Não é possível editar mecânicas pré-definidas do sistema.')
        
        return redirect('mecanicas_lista')
    
    return render(request, 'mecanicas/editar.html', {'item': item})

@autor_or_admin_required
def componente_editar(request, item_id):
    global componentes_criados
    # Buscar dados do componente dos dados locais
    componentes_data = get_api_data('componentes', page=1, per_page=1000)
    item = None
    for componente in componentes_data['results']:
        if componente['id'] == item_id:
            item = componente
            break
    
    if not item:
        messages.error(request, 'Componente não encontrado!')
        return redirect('componentes_lista')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        tipo = request.POST.get('tipo', 'TATICO')
        
        # Atualizar se for item criado pelo usuário (ID >= 2000)
        if item_id >= 2000:
            for i, c in enumerate(componentes_criados):
                if c['id'] == item_id:
                    componentes_criados[i]['nome'] = nome
                    componentes_criados[i]['descricao'] = descricao
                    componentes_criados[i]['tipo'] = tipo
                    break
            messages.success(request, 'Componente atualizado com sucesso!')
        else:
            messages.warning(request, 'Não é possível editar componentes pré-definidos do sistema.')
        
        return redirect('componentes_lista')
    
    return render(request, 'componentes/editar.html', {'item': item})
@autor_or_admin_required
def tema_editar(request, item_id):
    global temas_criados
    # Buscar dados do tema dos dados locais
    temas_data = get_api_data('temas', page=1, per_page=1000)
    item = None
    for tema in temas_data['results']:
        if tema['id'] == item_id:
            item = tema
            break
    
    if not item:
        messages.error(request, 'Tema não encontrado!')
        return redirect('temas_lista')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        
        # Atualizar se for item criado pelo usuário (ID >= 3000)
        if item_id >= 3000:
            for i, t in enumerate(temas_criados):
                if t['id'] == item_id:
                    temas_criados[i]['nome'] = nome
                    temas_criados[i]['descricao'] = descricao
                    break
            messages.success(request, 'Tema atualizado com sucesso!')
        else:
            messages.warning(request, 'Não é possível editar temas pré-definidos do sistema.')
        
        return redirect('temas_lista')
    
    return render(request, 'temas/editar.html', {'item': item})

@admin_required
def mecanica_excluir(request, item_id):
    global mecanicas_criadas
    # Verificar se é um item criado pelo usuário (ID >= 1000)
    if item_id >= 1000:
        mecanicas_criadas = [m for m in mecanicas_criadas if m['id'] != item_id]
        messages.success(request, 'Mecânica excluída com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir mecânicas pré-definidas do sistema.')
    return redirect('mecanicas_lista')

@admin_required
def componente_excluir(request, item_id):
    global componentes_criados
    # Verificar se é um item criado pelo usuário (ID >= 2000)
    if item_id >= 2000:
        componentes_criados = [c for c in componentes_criados if c['id'] != item_id]
        messages.success(request, 'Componente excluído com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir componentes pré-definidos do sistema.')
    return redirect('componentes_lista')

@admin_required
def tema_excluir(request, item_id):
    global temas_criados
    # Verificar se é um item criado pelo usuário (ID >= 3000)
    if item_id >= 3000:
        temas_criados = [t for t in temas_criados if t['id'] != item_id]
        messages.success(request, 'Tema excluído com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir temas pré-definidos do sistema.')
    return redirect('temas_lista')

def login_view(request):
    global usuario_logado, usuarios_criados
    
    if request.method == 'POST':
        login = request.POST.get('login')
        senha = request.POST.get('senha')
        
        # Usuários do sistema
        usuarios_sistema = [
            {'login': 'admin', 'senha': 'admin', 'nome': 'Admin Sistema', 'perfil': 'ADMINISTRADOR', 'ativo': True},
            {'login': 'autor', 'senha': '123', 'nome': 'Autor Sistema', 'perfil': 'AUTOR', 'ativo': True},
            {'login': 'revisor', 'senha': '123', 'nome': 'Revisor Sistema', 'perfil': 'REVISOR', 'ativo': True},
            {'login': 'leitor', 'senha': '123', 'nome': 'Leitor Teste', 'perfil': 'LEITOR', 'ativo': True},
        ]
        
        # Verificar usuários do sistema + criados
        todos_usuarios = usuarios_sistema + usuarios_criados
        
        for usuario in todos_usuarios:
            if usuario['login'] == login and usuario.get('ativo', True):
                # Para usuários do sistema, usar senhas fixas
                if usuario.get('id', 0) <= 10:  # Usuários do sistema
                    if ((login == 'admin' and senha == 'admin') or 
                        (login in ['autor', 'revisor', 'leitor'] and senha == '123')):
                        usuario_logado = usuario
                        request.session['usuario_perfil'] = usuario['perfil']
                        messages.success(request, f'Bem-vindo, {usuario["nome"]}!')
                        return redirect('home')
                else:  # Usuários criados - verificar senha armazenada
                    if usuario.get('senha') == senha:
                        usuario_logado = usuario
                        request.session['usuario_perfil'] = usuario['perfil']
                        messages.success(request, f'Bem-vindo, {usuario["nome"]}!')
                        return redirect('home')
        
        messages.error(request, 'Login ou senha inválidos!')
    
    return render(request, 'login.html')

def logout_view(request):
    global usuario_logado
    usuario_logado = None
    request.session.pop('usuario_perfil', None)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

@login_required
def perfil(request):
    global usuario_logado
    
    if request.method == 'POST':
        nome = request.POST.get('nome', usuario_logado['nome'])
        email = request.POST.get('email', usuario_logado.get('email', ''))
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirma_senha = request.POST.get('confirma_senha')
        
        # Atualizar nome e email
        usuario_logado['nome'] = nome
        usuario_logado['email'] = email
        
        # Atualizar senha se fornecida
        if nova_senha:
            if nova_senha == confirma_senha:
                # Para usuários do sistema, verificar senha atual
                if usuario_logado.get('id', 0) <= 10:
                    if usuario_logado['login'] == 'admin' and senha_atual == 'admin':
                        # Não podemos alterar senhas de usuários do sistema
                        messages.warning(request, 'Não é possível alterar a senha de usuários do sistema.')
                    else:
                        messages.error(request, 'Senha atual incorreta.')
                else:
                    # Usuário criado - verificar senha atual
                    if usuario_logado.get('senha') == senha_atual:
                        usuario_logado['senha'] = nova_senha
                        # Atualizar também na lista de usuários criados
                        for i, u in enumerate(usuarios_criados):
                            if u['id'] == usuario_logado['id']:
                                usuarios_criados[i]['senha'] = nova_senha
                                break
                        messages.success(request, 'Senha alterada com sucesso!')
                    else:
                        messages.error(request, 'Senha atual incorreta.')
            else:
                messages.error(request, 'Nova senha e confirmação não conferem!')
        else:
            messages.success(request, 'Perfil atualizado com sucesso!')
        
        return redirect('perfil')
    
    return render(request, 'perfil.html', {'usuario': usuario_logado})

@admin_required
def configurar_complexidade_senha(request):
    global complexidade_senha
    
    if request.method == 'POST':
        nova_complexidade = int(request.POST.get('complexidade', 1))
        complexidade_senha = nova_complexidade
        
        niveis = {
            1: 'Desativado',
            2: 'Letras e números, mínimo 6 dígitos',
            3: 'Letras maiúsculas e minúsculas, números, mínimo 8 dígitos',
            4: 'Letras maiúsculas e minúsculas, números, caractere especial, mínimo 10 dígitos'
        }
        
        messages.success(request, f'Complexidade de senha alterada para: {niveis[nova_complexidade]}')
        return redirect('usuarios_lista')
    
@admin_required
def usuarios_lista(request):
    global usuarios_criados, complexidade_senha
    
    # Usuários de exemplo
    usuarios_exemplo = [
        {'id': 1, 'nome': 'Admin Sistema', 'login': 'admin', 'email': 'admin@bgcreator.com', 'perfil': 'ADMINISTRADOR', 'ativo': True},
        {'id': 2, 'nome': 'Autor Sistema', 'login': 'autor', 'email': 'autor@bgcreator.com', 'perfil': 'AUTOR', 'ativo': True},
        {'id': 3, 'nome': 'Revisor Sistema', 'login': 'revisor', 'email': 'revisor@bgcreator.com', 'perfil': 'REVISOR', 'ativo': True},
        {'id': 4, 'nome': 'Leitor Teste', 'login': 'leitor', 'email': 'leitor@bgcreator.com', 'perfil': 'LEITOR', 'ativo': True},
    ]
    
    todos_usuarios = usuarios_exemplo + usuarios_criados
    
    # Processar busca
    busca = request.GET.get('busca', '').strip().lower()
    if busca:
        usuarios_filtrados = []
        for usuario in todos_usuarios:
            if (busca in usuario.get('nome', '').lower() or 
                busca in usuario.get('login', '').lower() or
                busca in usuario.get('perfil', '').lower()):
                usuarios_filtrados.append(usuario)
        todos_usuarios = usuarios_filtrados
    
    return render(request, 'usuarios/lista.html', {
        'usuarios': todos_usuarios,
        'complexidade_senha': complexidade_senha
    })

@admin_required
def usuario_novo(request):
    global usuarios_criados
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        login = request.POST.get('login')
        email = request.POST.get('email')
        perfil = request.POST.get('perfil')
        ativo = request.POST.get('ativo') == 'on'
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')
        
        if nome and login and email and senha:
            # Verificar se login já existe
            usuarios_sistema = [
                {'login': 'admin', 'email': 'admin@bgcreator.com'},
                {'login': 'autor', 'email': 'autor@bgcreator.com'},
                {'login': 'revisor', 'email': 'revisor@bgcreator.com'},
                {'login': 'leitor', 'email': 'leitor@bgcreator.com'},
            ]
            
            todos_usuarios = usuarios_sistema + usuarios_criados
            
            # Verificar login duplicado
            for usuario in todos_usuarios:
                if usuario['login'].lower() == login.lower():
                    messages.error(request, f'Login "{login}" já está em uso!')
                    return render(request, 'usuarios/novo.html')
                if usuario.get('email', '').lower() == email.lower():
                    messages.error(request, f'E-mail "{email}" já está em uso!')
                    return render(request, 'usuarios/novo.html')
            
            if senha == confirma_senha:
                # Validar complexidade da senha
                senha_valida, erro_senha = validar_senha(senha)
                if not senha_valida:
                    messages.error(request, erro_senha)
                    return render(request, 'usuarios/novo.html')
                
                novo_usuario = {
                    'id': len(usuarios_criados) + 1000,
                    'nome': nome,
                    'login': login,
                    'email': email,
                    'perfil': perfil,
                    'ativo': ativo,
                    'senha': senha  # Armazenar senha (em produção usar hash)
                }
                usuarios_criados.append(novo_usuario)
                messages.success(request, f'Usuário "{nome}" criado com sucesso!')
                return redirect('usuarios_lista')
            else:
                messages.error(request, 'Senhas não conferem!')
        else:
            messages.error(request, 'Nome, login, e-mail e senha são obrigatórios!')
    
    return render(request, 'usuarios/novo.html')

@admin_required
def usuario_editar(request, user_id):
    global usuarios_criados
    
    # Encontrar usuário
    usuario = None
    for u in usuarios_criados:
        if u['id'] == user_id:
            usuario = u
            break
    
    if not usuario:
        messages.error(request, 'Usuário não encontrado!')
        return redirect('usuarios_lista')
    
    if request.method == 'POST':
        nome_novo = request.POST.get('nome', usuario['nome'])
        login_novo = request.POST.get('login', usuario['login'])
        email_novo = request.POST.get('email', usuario.get('email', ''))
        
        # Verificar duplicatas apenas se mudou login ou email
        if login_novo.lower() != usuario['login'].lower() or email_novo.lower() != usuario.get('email', '').lower():
            usuarios_sistema = [
                {'id': 1, 'login': 'admin', 'email': 'admin@bgcreator.com'},
                {'id': 2, 'login': 'autor', 'email': 'autor@bgcreator.com'},
                {'id': 3, 'login': 'revisor', 'email': 'revisor@bgcreator.com'},
                {'id': 4, 'login': 'leitor', 'email': 'leitor@bgcreator.com'},
            ]
            
            todos_usuarios = usuarios_sistema + [u for u in usuarios_criados if u['id'] != user_id]
            
            for u in todos_usuarios:
                if u['login'].lower() == login_novo.lower():
                    messages.error(request, f'Login "{login_novo}" já está em uso!')
                    return render(request, 'usuarios/editar.html', {'usuario': usuario})
                if u.get('email', '').lower() == email_novo.lower():
                    messages.error(request, f'E-mail "{email_novo}" já está em uso!')
                    return render(request, 'usuarios/editar.html', {'usuario': usuario})
        
        usuario['nome'] = nome_novo
        usuario['login'] = login_novo
        usuario['email'] = email_novo
        usuario['perfil'] = request.POST.get('perfil', usuario['perfil'])
        usuario['ativo'] = request.POST.get('ativo') == 'on'
        
        # Atualizar senha se fornecida
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')
        if senha:
            if senha == confirma_senha:
                # Validar complexidade da senha
                senha_valida, erro_senha = validar_senha(senha)
                if not senha_valida:
                    messages.error(request, erro_senha)
                    return render(request, 'usuarios/editar.html', {'usuario': usuario})
                
                usuario['senha'] = senha  # Atualizar senha
                messages.success(request, 'Senha atualizada com sucesso!')
            else:
                messages.error(request, 'Senhas não conferem!')
                return render(request, 'usuarios/editar.html', {'usuario': usuario})
        
        messages.success(request, f'Usuário "{usuario["nome"]}" atualizado com sucesso!')
        return redirect('usuarios_lista')
    
    return render(request, 'usuarios/editar.html', {'usuario': usuario})

@admin_required
def usuario_excluir(request, user_id):
    global usuarios_criados
    
    # Verificar se é usuário criado (ID >= 1000)
    if user_id >= 1000:
        usuarios_criados = [u for u in usuarios_criados if u['id'] != user_id]
        messages.success(request, 'Usuário excluído com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir usuários do sistema.')
    
    return redirect('usuarios_lista')

@admin_required
def usuario_bloquear(request, user_id):
    global usuarios_criados
    
    # Verificar se é usuário criado (ID >= 1000)
    if user_id >= 1000:
        for i, u in enumerate(usuarios_criados):
            if u['id'] == user_id:
                usuarios_criados[i]['ativo'] = not usuarios_criados[i]['ativo']
                status = 'desbloqueado' if usuarios_criados[i]['ativo'] else 'bloqueado'
                messages.success(request, f'Usuário {status} com sucesso!')
                break
    else:
        messages.warning(request, 'Não é possível bloquear usuários do sistema.')
    
    return redirect('usuarios_lista')

@login_required
def jogo_revisao_leitura(request, jogo_id):
    """Versão somente leitura da revisão para autores"""
    global jogos_criados
    
    # Verificar se é autor
    if not usuario_logado or usuario_logado['perfil'] != 'AUTOR':
        messages.error(request, 'Acesso negado.')
        return redirect('jogos_lista')
    
    # Encontrar o jogo (mesmo código da função principal)
    jogo = None
    for j in jogos_criados:
        if j['id'] == int(jogo_id):
            jogo = j
            break
    
    if not jogo:
        jogos_exemplo = [
            {
                'id': 1, 'nome': 'Catan', 'subtitulo': 'Colonizadores de Catan',
                'descricao_curta': 'Jogo de estratégia sobre colonização',
                'jogadores_min': 3, 'jogadores_max': 4, 'tempo_min': 60, 'tempo_max': 90,
                'idade_recomendada': 10, 'peso': 2.3, 'versao_manual': '1.0.0',
                'autor': 'Klaus Teuber', 'revisor': 'João Silva', 'setup': [],
                'mecanicas': ['Construção', 'Negociação'], 'temas': ['Medieval', 'Colonização'],
                'componentes': [], 'condicoes_vitoria': [], 'condicoes_derrota': [],
                'estruturas': [], 'glossario': []
            },
            {
                'id': 2, 'nome': 'Ticket to Ride', 'subtitulo': 'Aventura Ferroviária',
                'descricao_curta': 'Construa rotas de trem pelo mundo',
                'jogadores_min': 2, 'jogadores_max': 5, 'tempo_min': 30, 'tempo_max': 60,
                'idade_recomendada': 8, 'peso': 1.8, 'versao_manual': '1.0.0',
                'autor': 'Alan R. Moon', 'revisor': 'Admin Sistema', 'setup': [],
                'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
                'temas': ['Transporte', 'Viagem'], 'componentes': [],
                'condicoes_vitoria': [], 'condicoes_derrota': [], 'estruturas': [], 'glossario': []
            }
        ]
        
        for j in jogos_exemplo:
            if j['id'] == int(jogo_id):
                jogo = j
                break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    return render(request, 'jogos/revisao_leitura.html', {'jogo': jogo})

import zipfile
import json
from datetime import datetime
from django.http import HttpResponse, FileResponse
import shutil

@admin_required
def backup_sistema(request):
    global jogos_criados, mecanicas_criadas, componentes_criados, temas_criados, usuarios_criados, comentarios_criados
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'criar_backup':
            # Criar backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'bgcreator_backup_{timestamp}.zip'
            backup_path = os.path.join('backups', backup_filename)
            
            # Criar diretório de backup se não existir
            os.makedirs('backups', exist_ok=True)
            
            # Dados para backup
            backup_data = {
                'timestamp': timestamp,
                'jogos': jogos_criados,
                'mecanicas': mecanicas_criadas,
                'componentes': componentes_criados,
                'temas': temas_criados,
                'usuarios': usuarios_criados,
                'comentarios': comentarios_criados,
                'complexidade_senha': complexidade_senha
            }
            
            # Criar arquivo ZIP
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Adicionar dados JSON
                zipf.writestr('dados.json', json.dumps(backup_data, indent=2, ensure_ascii=False))
                
                # Adicionar arquivos de mídia
                media_dirs = ['media/capas', 'media/setup', 'media/glossario']
                for media_dir in media_dirs:
                    if os.path.exists(media_dir):
                        for root, dirs, files in os.walk(media_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, 'media')
                                zipf.write(file_path, f'media/{arcname}')
            
            messages.success(request, f'Backup criado com sucesso: {backup_filename}')
            
        elif action == 'restaurar_backup':
            # Restaurar backup
            if 'backup_file' in request.FILES:
                backup_file = request.FILES['backup_file']
                
                # Salvar arquivo temporariamente
                temp_path = f'temp_{backup_file.name}'
                with open(temp_path, 'wb+') as destination:
                    for chunk in backup_file.chunks():
                        destination.write(chunk)
                
                try:
                    # Extrair e restaurar dados
                    with zipfile.ZipFile(temp_path, 'r') as zipf:
                        # Ler dados JSON
                        dados_json = zipf.read('dados.json').decode('utf-8')
                        backup_data = json.loads(dados_json)
                        
                        # Restaurar dados
                        jogos_criados.clear()
                        jogos_criados.extend(backup_data.get('jogos', []))
                        
                        mecanicas_criadas.clear()
                        mecanicas_criadas.extend(backup_data.get('mecanicas', []))
                        
                        componentes_criados.clear()
                        componentes_criados.extend(backup_data.get('componentes', []))
                        
                        temas_criados.clear()
                        temas_criados.extend(backup_data.get('temas', []))
                        
                        usuarios_criados.clear()
                        usuarios_criados.extend(backup_data.get('usuarios', []))
                        
                        comentarios_criados.clear()
                        comentarios_criados.extend(backup_data.get('comentarios', []))
                        
                        # Restaurar configuração de complexidade
                        complexidade_senha = backup_data.get('complexidade_senha', 1)
                        
                        # Restaurar arquivos de mídia
                        for file_info in zipf.infolist():
                            if file_info.filename.startswith('media/'):
                                zipf.extract(file_info, '.')
                    
                    messages.success(request, 'Backup restaurado com sucesso!')
                    
                except Exception as e:
                    messages.error(request, f'Erro ao restaurar backup: {str(e)}')
                
                finally:
                    # Remover arquivo temporário
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            else:
                messages.error(request, 'Nenhum arquivo de backup selecionado.')
    
    # Listar backups existentes
    backups = []
    if os.path.exists('backups'):
        for filename in os.listdir('backups'):
            if filename.endswith('.zip'):
                filepath = os.path.join('backups', filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'size': round(stat.st_size / 1024 / 1024, 2),  # MB
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime('%d/%m/%Y %H:%M')
                })
    
    return render(request, 'backup/sistema.html', {'backups': backups})

@admin_required
def backup_download(request, filename):
    backup_path = os.path.join('backups', filename)
    if os.path.exists(backup_path):
        return FileResponse(open(backup_path, 'rb'), as_attachment=True, filename=filename)
    else:
        messages.error(request, 'Arquivo de backup não encontrado.')
        return redirect('backup_sistema')

@admin_required
def backup_delete(request, filename):
    backup_path = os.path.join('backups', filename)
    if os.path.exists(backup_path):
        os.remove(backup_path)
        messages.success(request, f'Backup {filename} excluído com sucesso.')
    else:
        messages.error(request, 'Arquivo de backup não encontrado.')
    return redirect('backup_sistema')

@admin_or_reviewer_required
def jogo_revisao(request, jogo_id):
    global jogos_criados, usuario_logado
    
    # Verificar se é administrador ou revisor
    if not usuario_logado or usuario_logado['perfil'] not in ['ADMINISTRADOR', 'REVISOR']:
        messages.error(request, 'Acesso negado. Apenas administradores e revisores podem acessar a revisão.')
        return redirect('jogos_lista')
    
    # Encontrar o jogo
    jogo = None
    jogo_index = None
    for i, j in enumerate(jogos_criados):
        if j['id'] == int(jogo_id):
            jogo = j
            jogo_index = i
            break
    
    # Buscar nos jogos de exemplo se não encontrou
    if not jogo:
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
                'peso': 2.3,
                'versao_manual': '1.0.0',
                'autor': 'Klaus Teuber',
                'revisor': 'João Silva',
                'setup': [],
                'mecanicas': ['Construção', 'Negociação'],
                'temas': ['Medieval', 'Colonização'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
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
                'peso': 1.8,
                'versao_manual': '1.0.0',
                'autor': 'Alan R. Moon',
                'revisor': 'Admin Sistema',
                'setup': [],
                'mecanicas': ['Colecionar Conjuntos', 'Construção de Rotas'],
                'temas': ['Transporte', 'Viagem'],
                'componentes': [],
                'condicoes_vitoria': [],
                'condicoes_derrota': [],
                'estruturas': [],
                'glossario': []
            }
        ]
        
        for j in jogos_exemplo:
            if j['id'] == int(jogo_id):
                jogo = j
                break
    
    if not jogo:
        messages.error(request, 'Jogo não encontrado!')
        return redirect('jogos_lista')
    
    if request.method == 'POST':
        # Processar dados da revisão
        from datetime import datetime
        
        # Inicializar estrutura de revisão se não existir
        if 'revisao' not in jogo:
            jogo['revisao'] = {}
        
        # Salvar status de cada seção
        secoes = [
            'secao_informacoes_basicas', 'secao_mecanicas', 'secao_temas',
            'secao_componentes', 'secao_condicoes', 'secao_setup',
            'secao_estruturas', 'secao_glossario'
        ]
        
        revisor_nome = usuario_logado['nome'] if usuario_logado else 'Revisor'
        data_revisao = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        for secao in secoes:
            status = request.POST.get(secao, '')
            if status:
                jogo['revisao'][secao] = {
                    'status': status,
                    'revisor': revisor_nome,
                    'data': data_revisao
                }
                
                # Salvar observações de correção se existirem
                correcao_key = f'correcao_{secao}'
                observacoes = request.POST.get(correcao_key, '').strip()
                if observacoes:
                    jogo['revisao'][secao]['observacoes'] = observacoes
        
        # Atualizar revisor do jogo com proteção de autoria
        if usuario_logado:
            if usuario_logado['perfil'] == 'REVISOR':
                if jogo.get('revisor') and jogo['revisor'] != usuario_logado['nome']:
                    jogo['co_revisor'] = usuario_logado['nome']
                else:
                    jogo['revisor'] = usuario_logado['nome']
            elif usuario_logado['perfil'] == 'ADMINISTRADOR':
                jogo['revisor'] = usuario_logado['nome']
        
        # Atualizar jogo na lista se for jogo criado
        if jogo_index is not None:
            jogos_criados[jogo_index] = jogo
        
        messages.success(request, f'Revisão do jogo "{jogo["nome"]}" salva com sucesso!')
        return redirect('jogos_lista')
    
    return render(request, 'jogos/revisao.html', {'jogo': jogo})