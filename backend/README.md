# 🔧 BGCreator Backend

> API REST em Python para gerenciamento de dados de board games com MongoDB.

## 📋 Visão Geral

O backend do BGCreator é uma API REST construída em Python que fornece endpoints para gerenciamento completo de jogos de tabuleiro, incluindo mecânicas, componentes, temas e sistema de usuários.

## 🏗 Arquitetura

```
backend/
├── app/
│   ├── main.py           # Servidor principal da API
│   ├── models.py         # Modelos de dados (Jogo, Componente, etc.)
│   ├── database.py       # Configuração do MongoDB
│   ├── auth.py          # Sistema de autenticação
│   └── migrations/      # Scripts de migração do banco
│       ├── 0001_initial.py
│       ├── 0002_add_setup.py
│       ├── 0003_add_component_type.py
│       └── 0004_add_user_system.py
├── tests/               # Testes automatizados
├── requirements.txt     # Dependências Python
├── Dockerfile          # Container Docker
└── README.md           # Esta documentação
```

## 🚀 Tecnologias

- **Python 3.10+**: Linguagem principal
- **FastAPI**: Framework web moderno e rápido
- **MongoDB**: Banco de dados NoSQL
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Pytest**: Framework de testes

## 📦 Instalação

### Desenvolvimento Local
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

### Docker
```bash
docker build -t bgcreator-api .
docker run -p 8001:8001 bgcreator-api
```

## 🔗 Endpoints da API

### Jogos
- `GET /api/jogos/` - Listar jogos
- `POST /api/jogos/` - Criar jogo
- `GET /api/jogos/{id}` - Obter jogo específico
- `PUT /api/jogos/{id}` - Atualizar jogo
- `DELETE /api/jogos/{id}` - Excluir jogo

### Mecânicas
- `GET /api/mecanicas/` - Listar mecânicas
- `POST /api/mecanicas/` - Criar mecânica
- `GET /api/mecanicas/{id}` - Obter mecânica específica
- `PUT /api/mecanicas/{id}` - Atualizar mecânica
- `DELETE /api/mecanicas/{id}` - Excluir mecânica

### Componentes
- `GET /api/componentes/` - Listar componentes
- `POST /api/componentes/` - Criar componente
- `GET /api/componentes/{id}` - Obter componente específico
- `PUT /api/componentes/{id}` - Atualizar componente
- `DELETE /api/componentes/{id}` - Excluir componente

### Temas
- `GET /api/temas/` - Listar temas
- `POST /api/temas/` - Criar tema
- `GET /api/temas/{id}` - Obter tema específico
- `PUT /api/temas/{id}` - Atualizar tema
- `DELETE /api/temas/{id}` - Excluir tema

### Usuários
- `GET /api/usuarios/` - Listar usuários
- `POST /api/usuarios/` - Criar usuário
- `GET /api/usuarios/{id}` - Obter usuário específico
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Excluir usuário

### Autenticação
- `POST /api/auth/login` - Fazer login
- `POST /api/auth/logout` - Fazer logout
- `GET /api/auth/me` - Obter usuário atual

## 📊 Modelos de Dados

### Jogo
```python
class Jogo:
    id: str
    nome: str
    subtitulo: Optional[str]
    descricao_curta: Optional[str]
    historia: Optional[str]
    autor: Optional[str]
    co_autor: Optional[str]
    revisor: Optional[str]
    co_revisor: Optional[str]
    versao_manual: str = "1.0.0"
    capa: Optional[str]
    jogadores_min: int
    jogadores_max: int
    tempo_min: int
    tempo_max: int
    idade_recomendada: int
    peso: float
    mecanicas: List[str]
    temas: List[str]
    componentes: List[str]
    condicoes_vitoria: List[str]
    condicoes_derrota: List[str]
    estruturas: List[Estrutura]
    setup: List[Setup]
    glossario: List[TermoGlossario]
```

### Estrutura
```python
class Estrutura:
    nome: str
    tipo: str  # FASE, ACAO, TURNO
    classificacao: str  # NEUTRO, SORTE, TATICO, etc.
    descricao: Optional[str]
    condicoes_especiais: List[CondicaoEspecial]
```

### Setup
```python
class Setup:
    nome: str
    descricao: Optional[str]
    imagens: List[ImagemSetup]
```

### Componente
```python
class Componente:
    id: str
    nome: str
    descricao: Optional[str]
    tipo: str  # NEUTRO, SORTE, TATICO, HABILIDADE, LUDICO, GERENCIAMENTO
```

### Usuario
```python
class Usuario:
    id: str
    nome: str
    login: str
    email: str
    perfil: str  # ADMINISTRADOR, AUTOR, REVISOR, LEITOR
    ativo: bool
    senha_hash: str
```

## 🔒 Sistema de Autenticação

O backend implementa autenticação baseada em sessões com os seguintes perfis:

- **ADMINISTRADOR**: Acesso total
- **AUTOR**: Criação e edição de conteúdo
- **REVISOR**: Revisão de jogos
- **LEITOR**: Apenas leitura

## 🧮 Algoritmos de Cálculo

### Peso do Jogo
```python
def calcular_peso(jogo):
    peso = 0.1  # Base
    peso += min((jogo.tempo_max // 30) * 0.1, 1.0)  # Tempo
    peso += min(len(jogo.mecanicas) * 0.1, 1.0)     # Mecânicas
    peso += min(len(jogo.componentes) * 0.1, 1.0)   # Componentes
    peso += min(len(jogo.condicoes_vitoria) * 0.1, 0.3)  # Vitória
    peso += min(len(jogo.condicoes_derrota) * 0.1, 0.3)  # Derrota
    peso += min(len(jogo.estruturas) * 0.1, 1.0)    # Estruturas
    return round(peso, 1)
```

### Classificação do Jogo
```python
def calcular_classificacao(jogo):
    classificacoes = {tipo: 0 for tipo in TIPOS_CLASSIFICACAO}
    
    # Contar componentes por tipo
    for componente in jogo.componentes:
        tipo = obter_tipo_componente(componente)
        classificacoes[tipo] += 1
    
    # Contar estruturas por classificação
    for estrutura in jogo.estruturas:
        classificacoes[estrutura.classificacao] += 1
        
        # Contar condições especiais
        for condicao in estrutura.condicoes_especiais:
            classificacoes[condicao.tipo] += 1
    
    # Converter para percentuais
    total = sum(classificacoes.values())
    return {tipo: round((count/total)*100, 1) for tipo, count in classificacoes.items()}
```

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar com cobertura
python -m pytest tests/ --cov=app

# Executar testes específicos
python -m pytest tests/test_jogos.py
```

### Estrutura de Testes
```
tests/
├── test_jogos.py        # Testes de jogos
├── test_mecanicas.py    # Testes de mecânicas
├── test_componentes.py  # Testes de componentes
├── test_temas.py        # Testes de temas
├── test_usuarios.py     # Testes de usuários
├── test_auth.py         # Testes de autenticação
└── conftest.py          # Configurações de teste
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Banco de dados
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=bgcreator

# Servidor
HOST=0.0.0.0
PORT=8001
DEBUG=True

# Autenticação
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600
```

### Arquivo de Configuração
```python
# app/config.py
class Settings:
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "bgcreator"
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = True
    secret_key: str = "dev-secret-key"
```

## 📈 Performance

- **Paginação**: Implementada em todos os endpoints de listagem
- **Cache**: Cache em memória para dados frequentemente acessados
- **Índices**: Índices otimizados no MongoDB
- **Validação**: Validação eficiente com Pydantic

## 🚀 Deploy

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["python", "app/main.py"]
```

### Docker Compose
```yaml
api:
  build: ./backend
  ports:
    - "8001:8001"
  environment:
    - MONGODB_URL=mongodb://db:27017
  depends_on:
    - db
```

## 🔄 Migrações

```bash
# Executar migrações
python app/migrations/migrate.py

# Criar nova migração
python app/migrations/create_migration.py "nome_da_migracao"
```

## 📝 Logs

O sistema de logs está configurado para registrar:
- Requisições HTTP
- Erros de validação
- Operações de banco de dados
- Autenticação e autorização

```python
# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🤝 Contribuição

1. Siga os padrões de código Python (PEP 8)
2. Escreva testes para novas funcionalidades
3. Documente APIs com docstrings
4. Use type hints em todas as funções
5. Mantenha cobertura de testes acima de 80%