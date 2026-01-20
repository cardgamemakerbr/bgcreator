from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.conf import settings

# Lista para armazenar dados criados
mecanicas_criadas = []
componentes_criados = []
temas_criados = []
jogos_criados = []

def get_api_data(endpoint, page=1, per_page=1000):
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
        ('Meeple de Madeira', 'Boneco humanoide que representa trabalhadores.'),
        ('Dados D6', 'O clássico dado de 6 faces para sorteios.'),
        ('Dados Poliédricos', 'Dados de 4, 8, 10, 12 ou 20 faces.'),
        ('Cartas Standard', 'Cartas de tamanho padrão de baralho.'),
        ('Cartas Mini', 'Versões reduzidas para economizar espaço na mesa.'),
        ('Tabuleiro Principal', 'A base onde o jogo central acontece.'),
        ('Tabuleiros Individuais', 'Área de controle particular de cada jogador.'),
        ('Moedas de Metal', 'Dinheiro físico durável e temático.'),
        ('Moedas de Papel/Cartão', 'Dinheiro econômico em cartão rígido.'),
        ('Cubos de Madeira', 'Representação genérica de recursos variados.'),
        ('Miniaturas de Plástico', 'Esculturas detalhadas de personagens.'),
        ('Marcadores de Pontuação', 'Pinos ou fichas para a trilha de pontos.'),
        ('Ampulheta', 'Medidor físico de tempo para turnos rápidos.'),
        ('Escudo de Jogador', 'Divisória para ocultar cartas e recursos.'),
        ('Fichas de Poker', 'Tokens pesados usados como moedas ou apostas.'),
        ('Tiles Hexagonais', 'Peças de 6 lados para montar mapas modulares.'),
        ('Tiles Quadrados', 'Peças quadradas para construção de cenário.'),
        ('Marcador de Primeiro Jogador', 'Item que identifica quem inicia a rodada.'),
        ('Saco de Pano (Bag)', 'Para sorteio cego de peças (Bag building).'),
        ('Gemas de Plástico/Acrílico', 'Pedras coloridas para representar joias.'),
        ('Peões de Plástico', 'Marcadores simples em formato de "pino".'),
        ('Discos de Madeira', 'Marcadores circulares achatados.'),
        ('Cartas de Referência', 'Resumo de regras para consulta rápida.'),
        ('Manual de Regras', 'O livro de instruções oficial do jogo.'),
        ('Livro de Cenários', 'Guia com missões e montagens específicas.'),
        ('Divisórias de Caixa (Insert)', 'Organizador interno para os componentes.'),
        ('Adesivos', 'Para modificar o tabuleiro permanentemente (Legacy).'),
        ('Canetas Dry-Erase', 'Para escrever e apagar em tabuleiros plastificados.'),
        ('Lápis', 'Para preencher blocos de papel.'),
        ('Blocos de Pontuação', 'Folhas descartáveis para calcular o fim do jogo.'),
        ('Clip de Plástico', 'Para encaixar na borda de cartas e indicar valores.'),
        ('Suporte de Cartas', 'Acessório para manter as cartas em pé na mesa.'),
        ('Torre de Dados', 'Estrutura para rolar dados sem que eles voem longe.'),
        ('Bandeja de Dados', 'Superfície forrada para silenciar e conter os dados.'),
        ('Marcadores de Dano', 'Tokens de coração ou sangue para vida.'),
        ('Peças de Encaixe', 'Componentes que se conectam mecanicamente.'),
        ('Engrenagens de Papelão', 'Discos que giram afetando o jogo.'),
        ('Bússola de Papelão', 'Para indicar direção de vento ou movimento.'),
        ('Luva de Cartas (Sleeves)', 'Plásticos para proteger as cartas.'),
        ('Meeples de Animais', 'Figuras de madeira em formato de bicho.'),
        ('Recipientes de Armazenamento', 'Potes plásticos para separar recursos.'),
        ('Cartas Transparentes', 'Para sobrepor informações a outras cartas.'),
        ('Espelho', 'Componente reflexivo para jogos de laser ou ótica.'),
        ('Peças de Resina Especiais', 'Componentes premium com textura realística.'),
        ('Playmat de Neoprene', 'Tapete de borracha para organizar a mesa.'),
        ('Marcadores de Nível', 'Tokens que indicam a evolução de um item.'),
        ('Relógio de Xadrez', 'Dispositivo para controle rigoroso de tempo.'),
        ('Cartas de Evento', 'Baralho que altera o jogo a cada rodada.'),
        ('Tiles de Terreno', 'Peças que representam montanhas, florestas, etc.')
    ]
    
    if endpoint == 'mecanicas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(mecanicas_completas)]
        dados.extend(mecanicas_criadas)
    elif endpoint == 'temas':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(temas_completos)]
        dados.extend(temas_criados)
    elif endpoint == 'componentes':
        dados = [{'id': i+1, 'nome': nome, 'descricao': descricao} for i, (nome, descricao) in enumerate(componentes_completos)]
        dados.extend(componentes_criados)
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
    
    # Usar dados locais para contagem
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
                'componentes': [],
                'condicoes_vitoria': [c for c in request.POST.getlist('condicoes_vitoria[]') if c.strip()],
                'condicoes_derrota': [c for c in request.POST.getlist('condicoes_derrota[]') if c.strip()],
                
                # Estruturas
                'estruturas': [],
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
    
    data = get_api_data('mecanicas', page, per_page)
    
    return render(request, 'mecanicas/lista.html', {
        'mecanicas': data['results'],
        'pagination': data
    })

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

def componentes_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    data = get_api_data('componentes', page, per_page)
    
    return render(request, 'componentes/lista.html', {
        'componentes': data['results'],
        'pagination': data
    })

def componente_novo(request):
    global componentes_criados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        if nome:
            novo_componente = {
                'id': len(componentes_criados) + 2000,
                'nome': nome,
                'descricao': descricao
            }
            componentes_criados.append(novo_componente)
            messages.success(request, 'Componente criado com sucesso!')
        else:
            messages.error(request, 'Nome é obrigatório!')
        return redirect('componentes_lista')
    return render(request, 'componentes/novo.html')

def temas_lista(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    data = get_api_data('temas', page, per_page)
    
    return render(request, 'temas/lista.html', {
        'temas': data['results'],
        'pagination': data
    })

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

def jogo_imprimir(request, jogo_id):
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
    
    return render(request, 'jogos/imprimir.html', {'jogo': jogo})

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
        
        # Atualizar se for item criado pelo usuário (ID >= 2000)
        if item_id >= 2000:
            for i, c in enumerate(componentes_criados):
                if c['id'] == item_id:
                    componentes_criados[i]['nome'] = nome
                    componentes_criados[i]['descricao'] = descricao
                    break
            messages.success(request, 'Componente atualizado com sucesso!')
        else:
            messages.warning(request, 'Não é possível editar componentes pré-definidos do sistema.')
        
        return redirect('componentes_lista')
    
    return render(request, 'componentes/editar.html', {'item': item})
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

def mecanica_excluir(request, item_id):
    global mecanicas_criadas
    # Verificar se é um item criado pelo usuário (ID >= 1000)
    if item_id >= 1000:
        mecanicas_criadas = [m for m in mecanicas_criadas if m['id'] != item_id]
        messages.success(request, 'Mecânica excluída com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir mecânicas pré-definidas do sistema.')
    return redirect('mecanicas_lista')

def componente_excluir(request, item_id):
    global componentes_criados
    # Verificar se é um item criado pelo usuário (ID >= 2000)
    if item_id >= 2000:
        componentes_criados = [c for c in componentes_criados if c['id'] != item_id]
        messages.success(request, 'Componente excluído com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir componentes pré-definidos do sistema.')
    return redirect('componentes_lista')

def tema_excluir(request, item_id):
    global temas_criados
    # Verificar se é um item criado pelo usuário (ID >= 3000)
    if item_id >= 3000:
        temas_criados = [t for t in temas_criados if t['id'] != item_id]
        messages.success(request, 'Tema excluído com sucesso!')
    else:
        messages.warning(request, 'Não é possível excluir temas pré-definidos do sistema.')
    return redirect('temas_lista')