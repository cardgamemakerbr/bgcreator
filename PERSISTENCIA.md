# 🗄️ Sistema de Persistência de Dados - BGCreator

## 📊 Problema Resolvido

**ANTES**: Dados armazenados apenas em memória (variáveis globais)
- ❌ Dados perdidos a cada reinicialização
- ❌ Sem persistência entre atualizações
- ❌ Risco de perda total em produção

**AGORA**: Sistema de persistência em arquivo JSON
- ✅ Dados salvos automaticamente
- ✅ Persistência entre reinicializações
- ✅ Backup automático dos dados
- ✅ Seguro para produção

## 🔧 Como Funciona

### Arquivo de Dados
- **Local**: `frontend/data/bgcreator_data.json`
- **Formato**: JSON estruturado
- **Encoding**: UTF-8 com suporte a caracteres especiais

### Dados Persistidos
```json
{
  "jogos_criados": [...],
  "mecanicas_criadas": [...],
  "componentes_criados": [...],
  "temas_criados": [...],
  "usuarios_criados": [...],
  "comentarios_criados": [...],
  "complexidade_senha": 1,
  "usuarios_sistema_status": {...},
  "timestamp": "2024-01-27T10:30:00"
}
```

### Funções Principais
- `salvar_dados()`: Salva todos os dados no arquivo
- `carregar_dados()`: Carrega dados na inicialização

## 🚀 Para Produção

### Estrutura de Diretórios
```
bgcreator/
├── frontend/
│   ├── data/                    # Dados persistidos
│   │   ├── .gitkeep            # Mantém diretório no Git
│   │   └── bgcreator_data.json # Dados (ignorado pelo Git)
│   ├── media/                  # Arquivos de mídia
│   │   ├── avatars/           # Avatares dos usuários
│   │   ├── capas/             # Capas dos jogos
│   │   ├── setup/             # Imagens de setup
│   │   └── glossario/         # Imagens do glossário
│   └── backups/               # Backups do sistema
```

### Proteção no Git
- ✅ `frontend/data/.gitkeep` - Mantém estrutura
- ✅ `frontend/data/bgcreator_data.json` - Ignorado (dados sensíveis)
- ✅ `frontend/media/` - Ignorado (arquivos grandes)
- ✅ `frontend/backups/` - Ignorado (backups locais)

## 🛡️ Segurança

### Backup Automático
- Sistema de backup já implementado
- Backups em ZIP com dados + mídias
- Limpeza automática de backups antigos

### Recuperação
1. **Dados corrompidos**: Restaurar do backup mais recente
2. **Perda total**: Usar backup completo (.zip)
3. **Migração**: Copiar `data/` e `media/` para novo servidor

## 📝 Logs de Inicialização
```
Dados carregados com sucesso. Timestamp: 2024-01-27T10:30:00
```
ou
```
Arquivo de dados não encontrado. Usando dados padrão.
```

## ⚠️ Importante para Deploy

1. **Criar diretórios**:
   ```bash
   mkdir -p frontend/data
   mkdir -p frontend/media/{avatars,capas,setup,glossario}
   mkdir -p frontend/backups
   ```

2. **Permissões**:
   ```bash
   chmod 755 frontend/data
   chmod 755 frontend/media
   chmod 755 frontend/backups
   ```

3. **Primeira execução**: Sistema criará arquivo de dados automaticamente

4. **Backup regular**: Configurar backup automático dos diretórios `data/` e `media/`

## 🔄 Migração de Dados

Para migrar dados existentes:
1. Fazer backup completo via interface
2. Copiar arquivo `bgcreator_data.json` 
3. Copiar diretório `media/` completo
4. Restaurar no novo ambiente

**Status**: ✅ PRONTO PARA PRODUÇÃO