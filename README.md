# 🎲 BGCreator

> Aplicação completa para desenvolvedores de board games criarem, documentarem e gerenciarem jogos com sistema de autoria colaborativa e controle de versões.

![Status: Em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

## ✨ Funcionalidades

### 🎮 Gerenciamento de Jogos
- [x] CRUD completo de jogos com versionamento automático
- [x] Sistema de cópia de jogos com incremento de versão major
- [x] Controle manual de versões (major.minor.patch)
- [x] Upload de imagens para capas dos jogos
- [x] Cálculo automático de peso/complexidade
- [x] Sistema de classificação (Neutro, Sorte, Tático, Habilidade, Lúdico, Gerenciamento)
- [x] Calculadoras em tempo real de distribuição de classificação

### 📝 Sistema de Autoria Colaborativa
- [x] Campos de autor e revisor com atribuição automática
- [x] Sistema de co-autor e co-revisor para proteção de autoria
- [x] Controle de acesso baseado em perfis de usuário
- [x] Histórico de contribuições preservado

### 🔧 Componentes e Mecânicas
- [x] Biblioteca extensa de mecânicas (90+ pré-definidas)
- [x] Sistema de componentes com classificação por tipo
- [x] Catálogo de temas (100+ opções)
- [x] Busca avançada em todos os elementos
- [x] Criação de elementos personalizados

### 📋 Estruturação de Jogos
- [x] Sistema de fases e ações com classificação
- [x] Condições especiais com tipos específicos
- [x] Capítulo de setup com múltiplas etapas
- [x] Upload de imagens para setup e estruturas
- [x] Condições de vitória e derrota

### 📖 Documentação e Glossário
- [x] Glossário visual com imagens (iconografia 40x40px)
- [x] Suporte a Markdown em descrições
- [x] Geração automática de manuais em PDF
- [x] Templates de impressão profissionais
- [x] Sugestões de campos para orientar usuários

### 👥 Sistema de Usuários
- [x] Autenticação completa com login/logout
- [x] 4 perfis de acesso (Administrador, Autor, Revisor, Leitor)
- [x] Gerenciamento completo de usuários (CRUD)
- [x] Controle de acesso granular por funcionalidade
- [x] Validação de duplicatas (login/email)

### 🔍 Busca e Navegação
- [x] Busca global em jogos, mecânicas, temas e componentes
- [x] Filtros por nome, descrição e classificação
- [x] Interface responsiva com Bootstrap 5
- [x] Iconografia Font Awesome

### 🚀 DevOps e Deploy
- [x] Pipeline GitHub Actions para Docker
- [x] Scripts automatizados de build e upload
- [x] Containerização completa (3 containers)
- [x] Deploy via Docker Compose

---

## 🛠 Tecnologias

- **Backend**: Python 3.10+ com API REST
- **Frontend**: Django com templates Bootstrap 5
- **Database**: MongoDB (desenvolvimento em memória)
- **Containerização**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Upload**: Docker Hub (cardgamemakerbr/*)

## 📦 Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (desenvolvimento local)
- Git

## 🚀 Como executar

### Produção (Docker)
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/bgcreator.git
cd bgcreator

# Execute com Docker Compose
docker-compose up --build

# Acesse a aplicação
# Frontend: http://localhost:8000
# API Backend: http://localhost:8001
# MongoDB: localhost:27017
```

### Desenvolvimento Local
```bash
# Backend
cd backend
pip install -r requirements.txt
python app/main.py

# Frontend
cd frontend
pip install -r requirements.txt
python manage.py runserver
```

## 👤 Usuários de Teste

| Login | Senha | Perfil | Descrição |
|-------|-------|--------|-----------|
| admin | admin | Administrador | Acesso total |
| joao | 123 | Autor | Criação e edição |

## 🏗 Arquitetura

```
bgcreator/
├── backend/              # API Python FastAPI
│   ├── app/
│   │   ├── models.py     # Modelos de dados
│   │   ├── main.py       # Servidor API
│   │   └── migrations/   # Migrações do banco
│   ├── requirements.txt
│   └── README.md
├── frontend/             # Django Frontend
│   ├── web/
│   │   ├── views.py      # Lógica de negócio
│   │   ├── urls.py       # Rotas
│   │   └── templatetags/ # Filtros customizados
│   ├── templates/        # Templates HTML
│   ├── media/           # Upload de imagens
│   ├── requirements.txt
│   └── README.md
├── database/            # Configurações MongoDB
│   └── README.md
├── .github/workflows/   # CI/CD GitHub Actions
├── docker-compose.yml   # Orquestração containers
└── README.md           # Este arquivo
```

## 🧪 Testes

```bash
# Backend
cd backend && python -m pytest tests/

# Frontend
cd frontend && python manage.py test
```

## 📋 Regras de Negócio

### Cálculo de Peso (Complexidade)
O peso do jogo é calculado automaticamente baseado em:
- **Tempo médio**: +0,1 a cada 30min (máx: 1,0)
- **Mecânicas**: +0,1 por mecânica (máx: 1,0)
- **Componentes**: +0,1 por componente (máx: 1,0)
- **Condições de vitória**: +0,1 por condição (máx: 0,3)
- **Condições de derrota**: +0,1 por condição (máx: 0,3)
- **Fases/Ações**: +0,1 por estrutura (máx: 1,0)
- **Condições especiais**: +0,1 por condição (máx: 1,0)

### Sistema de Versões
- **Formato**: 1.X.X (sempre inicia com 1)
- **Minor**: Incrementa com adição de conteúdo
- **Patch**: Incrementa com edições
- **Major**: Incrementa com cópias de jogos
- **Controle manual**: 6 botões para ajuste fino

### Classificação de Jogos
Distribuição percentual baseada em:
- **Componentes**: Cada tipo contribui para classificação
- **Estruturas**: Classificação por fase/ação
- **Condições especiais**: Tipo específico por condição

### Sistema de Autoria
- **Autor original**: Preservado sempre
- **Co-autor**: Adicionado quando novo autor edita
- **Revisor original**: Preservado sempre
- **Co-revisor**: Adicionado quando novo revisor edita
- **Administradores**: Podem substituir sem proteção

## 🔐 Controle de Acesso

### Administrador
- ✅ Acesso total à aplicação
- ✅ Gerenciamento de usuários
- ✅ Todas as operações CRUD

### Autor
- ✅ Criar e editar jogos
- ✅ Gerenciar mecânicas, componentes e temas
- ❌ Gerenciamento de usuários
- ❌ Exclusão de itens

### Revisor
- ✅ Editar jogos (revisão)
- ❌ Gerenciamento de usuários
- ❌ Mecânicas, componentes e temas
- ❌ Exclusão de itens

### Leitor
- ✅ Visualizar e imprimir jogos
- ❌ Todas as outras operações

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔄 Roadmap

- [ ] Relatórios em PDF avançados
- [ ] Sistema de exportação (JSON/XML)
- [ ] Módulo de backup e restauração
- [ ] API REST completa
- [ ] Integração com banco MongoDB real
- [ ] Sistema de notificações
- [ ] Histórico de alterações
- [ ] Comentários e anotações
- [ ] Templates de jogos
- [ ] Marketplace de componentes