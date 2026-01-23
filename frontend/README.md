# 🎨 BGCreator Frontend

> Interface web em Django para criação e gerenciamento de board games com sistema colaborativo de autoria.

## 📋 Visão Geral

O frontend do BGCreator é uma aplicação web Django que fornece uma interface completa e intuitiva para criação, edição e gerenciamento de jogos de tabuleiro, com sistema de usuários, controle de versões e geração de manuais profissionais.

## 🏗 Arquitetura

```
frontend/
├── web/                    # App principal Django
│   ├── views.py           # Lógica de negócio e controllers
│   ├── urls.py            # Roteamento de URLs
│   ├── models.py          # Modelos Django (não utilizados - dados em memória)
│   ├── forms.py           # Formulários Django
│   └── templatetags/      # Filtros e tags customizadas
│       └── markdown_extras.py
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── home.html         # Página inicial
│   ├── login.html        # Página de login
│   ├── jogos/            # Templates de jogos
│   │   ├── lista.html
│   │   ├── novo.html
│   │   ├── editar.html
│   │   ├── detalhes.html
│   │   └── imprimir.html
│   ├── mecanicas/        # Templates de mecânicas
│   ├── componentes/      # Templates de componentes
│   ├── temas/           # Templates de temas
│   └── usuarios/        # Templates de usuários
├── media/               # Upload de arquivos
│   ├── capas/          # Imagens de capa
│   ├── setup/          # Imagens de setup
│   └── glossario/      # Imagens do glossário
├── static/             # Arquivos estáticos
├── requirements.txt    # Dependências Python
├── manage.py          # Utilitário Django
├── Dockerfile         # Container Docker
└── README.md         # Esta documentação
```

## 🚀 Tecnologias

- **Django 4.2+**: Framework web Python
- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome 6**: Biblioteca de ícones
- **JavaScript**: Interatividade do frontend
- **HTML5/CSS3**: Estrutura e estilização
- **Markdown**: Formatação de texto

## 📦 Instalação

### Desenvolvimento Local
```bash
cd frontend
pip install -r requirements.txt
python manage.py runserver
```

### Docker
```bash
docker build -t bgcreator-web .
docker run -p 8000:8000 bgcreator-web
```

## 🎯 Funcionalidades Principais

### 🎮 Gerenciamento de Jogos
- **CRUD Completo**: Criar, visualizar, editar e excluir jogos
- **Sistema de Cópia**: Duplicar jogos com incremento de versão
- **Upload de Imagens**: Capas, setup e glossário
- **Busca Avançada**: Filtros por nome, mecânicas, temas
- **Versionamento**: Controle automático e manual de versões

### 👥 Sistema de Usuários
- **4 Perfis**: Administrador, Autor, Revisor, Leitor
- **Autenticação**: Login/logout com sessões
- **Controle de Acesso**: Permissões granulares por funcionalidade
- **Gerenciamento**: CRUD de usuários (apenas admin)

### 📝 Sistema de Autoria
- **Autor/Revisor**: Atribuição automática baseada no perfil
- **Co-Autor/Co-Revisor**: Proteção de autoria existente
- **Histórico**: Preservação de contribuições anteriores

### 📊 Classificação e Métricas
- **Peso Automático**: Cálculo baseado em complexidade
- **6 Classificações**: Neutro, Sorte, Tático, Habilidade, Lúdico, Gerenciamento
- **Calculadoras**: Percentuais em tempo real
- **Visualização**: Badges coloridos e gráficos

### 📄 Geração de Manuais
- **Templates Profissionais**: Layout otimizado para impressão
- **Markdown**: Suporte a formatação rica
- **Índice Automático**: Geração baseada no conteúdo
- **Imagens**: Integração completa com uploads
- **PDF**: Impressão direta do navegador

## 🎨 Interface do Usuário

### Design System
- **Cores Primárias**: Azul (#0d6efd), Verde (#198754), Vermelho (#dc3545)
- **Tipografia**: Sistema de fontes do Bootstrap
- **Ícones**: Font Awesome 6 para consistência visual
- **Responsividade**: Mobile-first design

### Componentes Principais

#### Navegação
```html
<!-- Menu principal com controle de acesso -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
    <!-- Links condicionais baseados no perfil -->
</nav>
```

#### Cards de Informação
```html
<!-- Card padrão para exibição de dados -->
<div class="card mb-4">
    <div class="card-header">
        <h5><i class="fas fa-icon"></i> Título</h5>
    </div>
    <div class="card-body">
        <!-- Conteúdo -->
    </div>
</div>
```

#### Formulários Dinâmicos
```html
<!-- Formulários com adição/remoção dinâmica -->
<div id="dynamic-form">
    <!-- Campos que podem ser adicionados/removidos -->
</div>
```

## 🔧 Views e Funcionalidades

### Decoradores de Acesso
```python
@login_required
def view_function(request):
    # Requer login

@admin_required
def admin_view(request):
    # Apenas administradores

@autor_or_admin_required
def author_view(request):
    # Autores e administradores

@editor_required
def editor_view(request):
    # Autores, revisores e administradores
```

### Processamento de Dados

#### Markdown
```python
def processar_markdown(texto):
    # Converte **negrito** e *itálico*
    # Processa quebras de linha
    # Retorna HTML seguro
```

#### Cálculos
```python
def calcular_peso_jogo(jogo_data):
    # Algoritmo de cálculo de complexidade
    
def calcular_classificacao_jogo(jogo_data):
    # Distribuição percentual por tipo
    
def calcular_versao_manual(jogo_data):
    # Versionamento automático baseado em conteúdo
```

#### Upload de Imagens
```python
def salvar_imagem_capa(arquivo):
    # Salva em media/capas/
    
def salvar_imagem_setup(arquivo):
    # Salva em media/setup/
    
def salvar_imagem_glossario(arquivo):
    # Salva em media/glossario/
```

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: 768px - 992px
- **Large**: > 992px

### Adaptações Mobile
- Menu colapsível
- Cards empilhados
- Formulários otimizados
- Botões touch-friendly

## 🎯 Páginas Principais

### Home (`/`)
- Dashboard com estatísticas
- Jogos recentes
- Links rápidos
- Informações do usuário

### Lista de Jogos (`/jogos/`)
- Tabela responsiva
- Busca em tempo real
- Filtros avançados
- Ações por linha (ver, editar, copiar, excluir)

### Novo Jogo (`/jogos/novo/`)
- Formulário multi-seção
- Upload de imagens
- Campos dinâmicos
- Validação client-side
- Sugestões de preenchimento

### Editar Jogo (`/jogos/{id}/editar/`)
- Preservação de dados existentes
- Controle de versões
- Sistema de co-autoria
- Validação de permissões

### Detalhes do Jogo (`/jogos/{id}/`)
- Visualização completa
- Classificações visuais
- Imagens organizadas
- Ações contextuais

### Imprimir Manual (`/jogos/{id}/imprimir/`)
- Layout profissional
- Índice automático
- Quebras de página
- Otimizado para PDF

### Login (`/login/`)
- Formulário simples
- Validação de credenciais
- Redirecionamento inteligente
- Usuários de teste

## 🔒 Segurança

### Controle de Acesso
```python
# Verificação de permissões em cada view
if usuario_logado['perfil'] not in ['AUTOR', 'ADMINISTRADOR']:
    messages.error(request, 'Acesso negado.')
    return redirect('home')
```

### Upload Seguro
```python
# Validação de tipos de arquivo
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']

# Sanitização de nomes
filename = secure_filename(arquivo.name)
```

### Proteção CSRF
```html
<!-- Token CSRF em todos os formulários -->
{% csrf_token %}
```

## 📊 Dados em Memória

### Estrutura de Armazenamento
```python
# Listas globais para armazenamento
jogos_criados = []
mecanicas_criadas = []
componentes_criados = []
temas_criados = []
usuarios_criados = []
usuario_logado = None
```

### Dados Pré-definidos
- **90+ Mecânicas**: Biblioteca completa de mecânicas de jogos
- **100+ Temas**: Catálogo extenso de temas
- **48 Componentes**: Componentes classificados por tipo
- **Usuários Sistema**: Admin e usuários de teste

## 🎨 Customização CSS

### Classes Utilitárias
```css
/* Badges coloridos por classificação */
.badge.bg-primary { /* Tático */ }
.badge.bg-warning { /* Sorte */ }
.badge.bg-success { /* Habilidade */ }
.badge.bg-info { /* Lúdico */ }
.badge.bg-dark { /* Gerenciamento */ }
.badge.bg-light { /* Neutro */ }

/* Layout de impressão */
@media print {
    .no-print { display: none !important; }
    .page-break { page-break-before: always; }
}
```

## 🧪 Testes

### Testes de Views
```bash
python manage.py test web.tests.test_views
```

### Testes de Templates
```bash
python manage.py test web.tests.test_templates
```

### Testes de Formulários
```bash
python manage.py test web.tests.test_forms
```

## 🚀 Deploy

### Configurações de Produção
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📈 Performance

### Otimizações
- **Lazy Loading**: Imagens carregadas sob demanda
- **Minificação**: CSS e JS minificados
- **Cache**: Templates e dados estáticos
- **Compressão**: Gzip habilitado

### Métricas
- **Tempo de Carregamento**: < 2s
- **Tamanho da Página**: < 500KB
- **Lighthouse Score**: > 90

## 🔄 Fluxos de Trabalho

### Criação de Jogo
1. Login do usuário
2. Acesso ao formulário
3. Preenchimento assistido
4. Upload de imagens
5. Validação automática
6. Cálculo de métricas
7. Salvamento e redirecionamento

### Sistema de Revisão
1. Autor cria/edita jogo
2. Revisor acessa para revisão
3. Sistema protege autoria original
4. Adiciona co-revisor se necessário
5. Incrementa versão automaticamente

### Geração de Manual
1. Processamento de Markdown
2. Organização de seções
3. Geração de índice
4. Aplicação de template
5. Otimização para impressão

## 🤝 Contribuição

### Padrões de Código
- **PEP 8**: Estilo Python
- **HTML5**: Semântica correta
- **Bootstrap**: Classes utilitárias
- **JavaScript**: ES6+

### Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug específico
docs: atualiza documentação
style: ajustes de formatação
refactor: refatoração de código
test: adiciona/modifica testes
```

### Checklist de PR
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Responsividade testada
- [ ] Acessibilidade verificada
- [ ] Performance otimizada