# 🎲 BGCreator

> Aplicação completa para desenvolvedores de board games criarem, documentarem e gerenciarem jogos com sistema de autoria colaborativa e controle de versões.

![Status: Pronto para Produção](https://img.shields.io/badge/Status-Pronto%20para%20Produ%C3%A7%C3%A3o-brightgreen?style=for-the-badge)
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
- [x] **Importação/Exportação JSON** - Templates dinâmicos para construção de manuais
- [x] **Status de Revisão Visual** - Ícones de correção pendente (!) e aprovado (✓)

### 👥 Sistema de Usuários Avançado
- [x] 4 perfis de acesso (Administrador, Autor, Revisor, Leitor)
- [x] **Gerenciamento Unificado** - Usuários, DNS e Backup em uma tela
- [x] **Complexidade de Senhas Configurável** - 4 níveis de segurança
- [x] **Upload de Avatars** - Imagens personalizadas para usuários
- [x] **Deploy Inicial Limpo** - Cadastro do primeiro administrador
- [x] Controle de acesso granular por funcionalidade
- [x] Sistema de co-autor/co-revisor com proteção de autoria
- [x] **Bloqueio de Co-autoria** - Controle administrativo

### 💬 Sistema de Comentários e Avaliações
- [x] **Comentários para Leitores** - Sistema completo de feedback
- [x] **Avaliações 1-5 Estrelas** - Rating visual dos jogos
- [x] **Avatars nos Comentários** - Identificação visual
- [x] **Média de Avaliações** - Cálculo automático

### 🔧 Componentes e Mecânicas
- [x] Biblioteca extensa de mecânicas (90+ pré-definidas)
- [x] **Upload de Imagens para Componentes** - Visualização em quadrados
- [x] **Cadastro Rápido** - Botões inline para criar novos itens
- [x] Sistema de componentes com classificação por tipo
- [x] Catálogo de temas (100+ opções)
- [x] Busca avançada em todos os elementos
- [x] **Correção de Quantidades** - Bug de duplicação resolvido

### 📋 Estruturação de Jogos
- [x] Sistema de fases e ações com classificação
- [x] Condições especiais com tipos específicos
- [x] Capítulo de setup com múltiplas etapas
- [x] Upload de imagens para setup e estruturas
- [x] Condições de vitória e derrota
- [x] **Campo de Idade Corrigido** - Range 1-9 anos

### 📖 Documentação e Glossário
- [x] Glossário visual com imagens (iconografia 40x40px)
- [x] Suporte a Markdown em descrições
- [x] Geração automática de manuais em PDF
- [x] Templates de impressão profissionais
- [x] Sugestões de campos para orientar usuários

### 🔒 Segurança e Deploy
- [x] **Hosts DNS Confiáveis** - Configuração dinâmica para CSRF
- [x] **Middleware de Segurança** - Proteção automática
- [x] **Sistema de Backup Automático** - Diário com limpeza configurável
- [x] **Persistência de Dados** - Arquivos JSON + mídias
- [x] Autenticação completa com controle de sessão

### 🚀 DevOps e Deploy
- [x] Pipeline GitHub Actions para Docker
- [x] Scripts automatizados de build e upload
- [x] Containerização completa (3 containers)
- [x] Deploy via Docker Compose
- [x] **Preparação para Deploy Limpo** - Sem usuários de teste

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

**Para deploy inicial limpo:**
- Sistema inicia sem usuários pré-definidos
- Primeiro acesso: cadastro obrigatório do administrador
- Interface de cadastro inicial aparece automaticamente

**Para desenvolvimento local:**
- Criar usuários via interface de gerenciamento
- Perfis disponíveis: Administrador, Autor, Revisor, Leitor
- Complexidade de senha configurável (4 níveis)

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
- ✅ Comentar e avaliar jogos (1 a 5 estrelas)
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

### ✅ Implementado Recentemente
- [x] **Sistema de Comentários e Avaliações** - Feedback completo para leitores
- [x] **Complexidade de Senhas Configurável** - 4 níveis de segurança
- [x] **Upload de Avatars** - Imagens personalizadas para usuários
- [x] **Ícones de Status de Revisão** - Visual de correções e aprovações
- [x] **Imagens para Componentes** - Upload e visualização
- [x] **Gerenciamento Unificado** - Usuários, DNS e Backup em uma tela
- [x] **Deploy Inicial Limpo** - Sistema sem usuários de teste
- [x] **Cadastro Rápido** - Botões inline para criar itens
- [x] **Importação/Exportação JSON** - Templates dinâmicos
- [x] **Hosts DNS Confiáveis** - Configuração CSRF dinâmica

### 🕰 Próximas Implementações
- [ ] **Backup Automático Diário** - Com limpeza configurável (1-5 dias)
- [ ] **Bloqueio de Co-autoria** - Controle administrativo avançado
- [ ] **Versão Multilíngue** - Inglês e Espanhol
- [ ] **Dicionário para Revisor** - Ferramenta de apoio
- [ ] Relatórios em PDF avançados
- [ ] API REST completa
- [ ] Integração com banco MongoDB real
- [ ] Sistema de notificações
- [ ] Histórico de alterações
- [ ] Templates de jogos
- [ ] Marketplace de componentes