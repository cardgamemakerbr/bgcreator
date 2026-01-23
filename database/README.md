# 🗄️ BGCreator Database

> Configuração e estrutura do banco de dados MongoDB para o sistema BGCreator.

## 📋 Visão Geral

O BGCreator utiliza MongoDB como banco de dados principal para armazenar informações de jogos, usuários, mecânicas, componentes e temas. Durante o desenvolvimento, os dados são mantidos em memória no frontend para facilitar testes e prototipagem.

## 🏗 Arquitetura

```
database/
├── init/                 # Scripts de inicialização
│   ├── 01-create-db.js  # Criação do banco
│   ├── 02-indexes.js    # Criação de índices
│   └── 03-seed-data.js  # Dados iniciais
├── schemas/             # Esquemas de validação
│   ├── jogo.json       # Schema do jogo
│   ├── usuario.json    # Schema do usuário
│   ├── mecanica.json   # Schema da mecânica
│   ├── componente.json # Schema do componente
│   └── tema.json       # Schema do tema
├── migrations/          # Scripts de migração
├── backups/            # Backups automáticos
├── docker-compose.yml  # Configuração do container
└── README.md          # Esta documentação
```

## 🚀 Tecnologias

- **MongoDB 6.0+**: Banco de dados NoSQL
- **Docker**: Containerização
- **MongoDB Compass**: Interface gráfica (desenvolvimento)
- **Mongoose**: ODM para Node.js (futuro)

## 📦 Instalação

### Docker (Recomendado)
```bash
cd database
docker-compose up -d
```

### Instalação Local
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community

# Windows
# Baixar do site oficial do MongoDB
```

## 🗃️ Estrutura do Banco

### Database: `bgcreator`

#### Collections

1. **jogos** - Jogos de tabuleiro
2. **usuarios** - Usuários do sistema
3. **mecanicas** - Mecânicas de jogos
4. **componentes** - Componentes de jogos
5. **temas** - Temas de jogos
6. **sessoes** - Sessões de usuário
7. **logs** - Logs do sistema

## 📊 Esquemas de Dados

### Jogo
```json
{
  "_id": "ObjectId",
  "nome": "String (required)",
  "subtitulo": "String (optional)",
  "descricao_curta": "String (optional)",
  "historia": "String (optional)",
  "autor": "String (optional)",
  "co_autor": "String (optional)",
  "revisor": "String (optional)",
  "co_revisor": "String (optional)",
  "versao_manual": "String (default: '1.0.0')",
  "capa": "String (URL/path)",
  "jogadores_min": "Number (required, min: 1)",
  "jogadores_max": "Number (required, min: 1)",
  "tempo_min": "Number (required, min: 1)",
  "tempo_max": "Number (required, min: 1)",
  "idade_recomendada": "Number (required, min: 3)",
  "peso": "Number (calculated)",
  "mecanicas": ["String"],
  "temas": ["String"],
  "componentes": ["String"],
  "condicoes_vitoria": ["String"],
  "condicoes_derrota": ["String"],
  "estruturas": [
    {
      "nome": "String (required)",
      "tipo": "String (enum: FASE, ACAO, TURNO)",
      "classificacao": "String (enum: NEUTRO, SORTE, TATICO, HABILIDADE, LUDICO, GERENCIAMENTO)",
      "descricao": "String (optional)",
      "condicoes_especiais": [
        {
          "nome": "String (required)",
          "descricao": "String (optional)",
          "tipo": "String (enum: NEUTRO, SORTE, TATICO, HABILIDADE, LUDICO, GERENCIAMENTO)"
        }
      ]
    }
  ],
  "setup": [
    {
      "nome": "String (required)",
      "descricao": "String (optional)",
      "imagens": [
        {
          "descricao": "String (required)",
          "imagem": "String (URL/path)"
        }
      ]
    }
  ],
  "glossario": [
    {
      "palavra": "String (required)",
      "definicao": "String (required)",
      "imagem": "String (URL/path, optional)"
    }
  ],
  "created_at": "Date (auto)",
  "updated_at": "Date (auto)",
  "created_by": "ObjectId (ref: usuarios)",
  "updated_by": "ObjectId (ref: usuarios)"
}
```

### Usuario
```json
{
  "_id": "ObjectId",
  "nome": "String (required)",
  "login": "String (required, unique)",
  "email": "String (required, unique)",
  "perfil": "String (enum: ADMINISTRADOR, AUTOR, REVISOR, LEITOR)",
  "ativo": "Boolean (default: true)",
  "senha_hash": "String (required)",
  "ultimo_login": "Date",
  "created_at": "Date (auto)",
  "updated_at": "Date (auto)"
}
```

### Mecanica
```json
{
  "_id": "ObjectId",
  "nome": "String (required, unique)",
  "descricao": "String (optional)",
  "categoria": "String (optional)",
  "exemplos": ["String"],
  "created_at": "Date (auto)",
  "updated_at": "Date (auto)",
  "created_by": "ObjectId (ref: usuarios)"
}
```

### Componente
```json
{
  "_id": "ObjectId",
  "nome": "String (required, unique)",
  "descricao": "String (optional)",
  "tipo": "String (enum: NEUTRO, SORTE, TATICO, HABILIDADE, LUDICO, GERENCIAMENTO)",
  "material": "String (optional)",
  "dimensoes": "String (optional)",
  "created_at": "Date (auto)",
  "updated_at": "Date (auto)",
  "created_by": "ObjectId (ref: usuarios)"
}
```

### Tema
```json
{
  "_id": "ObjectId",
  "nome": "String (required, unique)",
  "descricao": "String (optional)",
  "categoria": "String (optional)",
  "popularidade": "Number (default: 0)",
  "created_at": "Date (auto)",
  "updated_at": "Date (auto)",
  "created_by": "ObjectId (ref: usuarios)"
}
```

### Sessao
```json
{
  "_id": "ObjectId",
  "usuario_id": "ObjectId (ref: usuarios)",
  "token": "String (unique)",
  "ip_address": "String",
  "user_agent": "String",
  "created_at": "Date (auto)",
  "expires_at": "Date (required)",
  "ativo": "Boolean (default: true)"
}
```

## 🔍 Índices

### Índices Principais
```javascript
// Jogos
db.jogos.createIndex({ "nome": "text", "descricao_curta": "text" })
db.jogos.createIndex({ "autor": 1 })
db.jogos.createIndex({ "created_at": -1 })
db.jogos.createIndex({ "peso": 1 })

// Usuários
db.usuarios.createIndex({ "login": 1 }, { unique: true })
db.usuarios.createIndex({ "email": 1 }, { unique: true })
db.usuarios.createIndex({ "perfil": 1 })

// Mecânicas
db.mecanicas.createIndex({ "nome": "text", "descricao": "text" })
db.mecanicas.createIndex({ "nome": 1 }, { unique: true })

// Componentes
db.componentes.createIndex({ "nome": "text", "descricao": "text" })
db.componentes.createIndex({ "tipo": 1 })

// Temas
db.temas.createIndex({ "nome": "text", "descricao": "text" })
db.temas.createIndex({ "popularidade": -1 })

// Sessões
db.sessoes.createIndex({ "token": 1 }, { unique: true })
db.sessoes.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 })
```

## 🔧 Configuração

### Docker Compose
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    container_name: bgcreator-db
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: bgcreator
    volumes:
      - mongodb_data:/data/db
      - ./init:/docker-entrypoint-initdb.d
    networks:
      - bgcreator-network

volumes:
  mongodb_data:

networks:
  bgcreator-network:
    driver: bridge
```

### Configuração de Produção
```javascript
// mongod.conf
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled

replication:
  replSetName: "bgcreator-rs"
```

## 🛡️ Segurança

### Autenticação
```javascript
// Criar usuário administrador
use bgcreator
db.createUser({
  user: "bgcreator_admin",
  pwd: "secure_password",
  roles: [
    { role: "readWrite", db: "bgcreator" },
    { role: "dbAdmin", db: "bgcreator" }
  ]
})
```

### Validação de Schema
```javascript
// Validação para collection jogos
db.createCollection("jogos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nome", "jogadores_min", "jogadores_max", "tempo_min", "tempo_max", "idade_recomendada"],
      properties: {
        nome: {
          bsonType: "string",
          minLength: 1,
          maxLength: 200
        },
        jogadores_min: {
          bsonType: "int",
          minimum: 1,
          maximum: 20
        },
        peso: {
          bsonType: "double",
          minimum: 0.1,
          maximum: 5.0
        }
      }
    }
  }
})
```

## 📊 Dados Iniciais

### Mecânicas (90+ itens)
```javascript
// Exemplos de mecânicas pré-definidas
db.mecanicas.insertMany([
  {
    nome: "Alocação de Trabalhadores (Worker Placement)",
    descricao: "Posicionar peões em locais do tabuleiro para bloquear a ação para outros e ganhar recursos.",
    categoria: "Estratégia"
  },
  {
    nome: "Construção de Baralho (Deck Building)",
    descricao: "Jogadores compram cartas para melhorar seu próprio baralho durante a partida.",
    categoria: "Cartas"
  }
  // ... mais 88 mecânicas
])
```

### Componentes (48 itens)
```javascript
db.componentes.insertMany([
  {
    nome: "Meeple de Madeira",
    descricao: "Boneco humanoide que representa trabalhadores.",
    tipo: "NEUTRO",
    material: "Madeira"
  },
  {
    nome: "Dados D6",
    descricao: "O clássico dado de 6 faces para sorteios.",
    tipo: "SORTE",
    material: "Plástico"
  }
  // ... mais 46 componentes
])
```

### Temas (100+ itens)
```javascript
db.temas.insertMany([
  {
    nome: "Fantasia Medieval",
    descricao: "Magia, reinos e criaturas místicas.",
    categoria: "Fantasia",
    popularidade: 95
  },
  {
    nome: "Exploração Espacial",
    descricao: "Viagens entre galáxias e descobertas alienígenas.",
    categoria: "Ficção Científica",
    popularidade: 88
  }
  // ... mais 98 temas
])
```

## 🔄 Migrações

### Script de Migração
```javascript
// migration_001_add_versioning.js
db.jogos.updateMany(
  { versao_manual: { $exists: false } },
  { $set: { versao_manual: "1.0.0" } }
)

// migration_002_add_coauthor.js
db.jogos.updateMany(
  { co_autor: { $exists: false } },
  { $set: { co_autor: null, co_revisor: null } }
)
```

### Executar Migrações
```bash
# Executar todas as migrações
mongo bgcreator migrations/run_all.js

# Executar migração específica
mongo bgcreator migrations/migration_001.js
```

## 📈 Performance

### Otimizações
- **Índices Compostos**: Para consultas complexas
- **Projeção**: Retornar apenas campos necessários
- **Agregação**: Pipeline otimizado para relatórios
- **Sharding**: Para escalabilidade horizontal

### Consultas Otimizadas
```javascript
// Busca de jogos com filtros
db.jogos.find(
  { 
    $text: { $search: "estratégia" },
    peso: { $gte: 2.0, $lte: 4.0 }
  },
  { nome: 1, peso: 1, autor: 1 }
).sort({ created_at: -1 }).limit(20)

// Agregação para estatísticas
db.jogos.aggregate([
  { $group: { 
    _id: "$autor", 
    total_jogos: { $sum: 1 },
    peso_medio: { $avg: "$peso" }
  }},
  { $sort: { total_jogos: -1 } }
])
```

## 🔄 Backup e Restore

### Backup Automático
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --db bgcreator --out /backups/bgcreator_$DATE
tar -czf /backups/bgcreator_$DATE.tar.gz /backups/bgcreator_$DATE
rm -rf /backups/bgcreator_$DATE
```

### Restore
```bash
# Restaurar backup
tar -xzf bgcreator_20231201_120000.tar.gz
mongorestore --db bgcreator bgcreator_20231201_120000/bgcreator/
```

### Backup Incremental
```javascript
// Backup apenas de documentos modificados
db.jogos.find({
  updated_at: { 
    $gte: ISODate("2023-12-01T00:00:00Z") 
  }
})
```

## 📊 Monitoramento

### Métricas Importantes
- **Conexões Ativas**: Número de conexões simultâneas
- **Operações por Segundo**: Read/Write operations
- **Tempo de Resposta**: Latência das consultas
- **Uso de Memória**: RAM utilizada pelo MongoDB
- **Espaço em Disco**: Crescimento do banco

### Comandos de Monitoramento
```javascript
// Status do servidor
db.serverStatus()

// Estatísticas do banco
db.stats()

// Operações lentas
db.setProfilingLevel(2, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(5)

// Índices utilizados
db.jogos.find().explain("executionStats")
```

## 🚀 Deploy

### Produção
```bash
# Configurar replica set
mongo --eval "rs.initiate()"

# Configurar usuários
mongo admin --eval "
  db.createUser({
    user: 'admin',
    pwd: 'secure_password',
    roles: ['root']
  })
"

# Habilitar autenticação
echo "security.authorization: enabled" >> /etc/mongod.conf
systemctl restart mongod
```

### Docker Swarm
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
    volumes:
      - mongodb_data:/data/db
    networks:
      - bgcreator-overlay

networks:
  bgcreator-overlay:
    driver: overlay
    attachable: true
```

## 🤝 Contribuição

### Padrões de Dados
- **Nomes**: camelCase para campos
- **Datas**: ISO 8601 format
- **IDs**: ObjectId do MongoDB
- **Validação**: Schema validation habilitada

### Checklist de Alterações
- [ ] Schema atualizado
- [ ] Índices criados/atualizados
- [ ] Migração documentada
- [ ] Backup testado
- [ ] Performance verificada