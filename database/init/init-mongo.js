// Inicialização do banco BGCreator
db = db.getSiblingDB('bgcreator');

// Criar coleções básicas
db.createCollection('mecanicas');
db.createCollection('temas');
db.createCollection('componentes');
db.createCollection('jogos');

// Inserir dados iniciais - Mecânicas
db.mecanicas.insertMany([
    { nome: "Deck Building", descricao: "Construção de baralho durante o jogo" },
    { nome: "Worker Placement", descricao: "Colocação de trabalhadores em espaços limitados" },
    { nome: "Area Control", descricao: "Controle de territórios no tabuleiro" },
    { nome: "Engine Building", descricao: "Construção de motor de pontuação" },
    { nome: "Tile Placement", descricao: "Colocação de peças no tabuleiro" },
    { nome: "Set Collection", descricao: "Coleta de conjuntos de cartas/peças" },
    { nome: "Drafting", descricao: "Seleção de cartas passando entre jogadores" },
    { nome: "Roll and Write", descricao: "Rolar dados e marcar em planilha" }
]);

// Inserir dados iniciais - Temas
db.temas.insertMany([
    { nome: "Medieval", descricao: "Ambientação medieval com castelos e cavaleiros" },
    { nome: "Ficção Científica", descricao: "Futuro, espaço e tecnologia avançada" },
    { nome: "Fantasia", descricao: "Magia, criaturas místicas e mundos fantásticos" },
    { nome: "Histórico", descricao: "Baseado em eventos históricos reais" },
    { nome: "Moderno", descricao: "Ambientação contemporânea" },
    { nome: "Abstrato", descricao: "Sem tema específico, foco na mecânica" },
    { nome: "Aventura", descricao: "Exploração e descobertas" },
    { nome: "Econômico", descricao: "Gestão de recursos e economia" }
]);

// Inserir dados iniciais - Componentes
db.componentes.insertMany([
    { nome: "Cartas", descricao: "Cartas de jogo padrão" },
    { nome: "Dados", descricao: "Dados de 6 faces ou especiais" },
    { nome: "Tabuleiro", descricao: "Tabuleiro principal do jogo" },
    { nome: "Peões", descricao: "Figuras representando jogadores" },
    { nome: "Cubos", descricao: "Cubos de madeira coloridos" },
    { nome: "Tokens", descricao: "Fichas de papelão" },
    { nome: "Miniaturas", descricao: "Figuras detalhadas em plástico" },
    { nome: "Tiles", descricao: "Peças de tabuleiro modulares" },
    { nome: "Marcadores", descricao: "Marcadores de pontuação ou recursos" },
    { nome: "Moedas", descricao: "Moedas de metal ou papelão" }
]);

print("Dados iniciais inseridos com sucesso!");