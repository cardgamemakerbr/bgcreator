# Configurações de Backup Automático - BGCreator

## Funcionalidades Implementadas

### ✅ Backup Automático Diário
- Executa automaticamente 1 vez por dia na primeira inicialização
- Cria arquivo ZIP com todos os dados e mídias
- Nomenclatura: `bgcreator_backup_auto_YYYYMMDD_HHMMSS.zip`

### ✅ Limpeza Automática
- Remove backups mais antigos que 5 dias automaticamente
- Configurável via parâmetro `dias_manter` na função `limpar_backups_antigos()`
- Executa junto com o backup automático

### ✅ Controle de Execução
- Arquivo `ultimo_backup.txt` controla quando foi o último backup
- Evita múltiplos backups no mesmo dia
- Reseta automaticamente a cada novo dia

## Estrutura do Backup

```
bgcreator_backup_auto_YYYYMMDD_HHMMSS.zip
├── dados.json                 # Todos os dados do sistema
└── media/                     # Arquivos de mídia
    ├── capas/                 # Imagens de capas
    ├── setup/                 # Imagens de setup
    ├── glossario/             # Imagens de glossário
    ├── componentes/           # Imagens de componentes
    └── avatars/               # Avatars de usuários
```

## Dados Incluídos no Backup

- ✅ Jogos criados
- ✅ Mecânicas personalizadas
- ✅ Componentes personalizados
- ✅ Temas personalizados
- ✅ Usuários criados
- ✅ Comentários e avaliações
- ✅ Configurações de complexidade de senha
- ✅ Senhas do sistema
- ✅ Todas as imagens e mídias

## Configurações Padrão

```python
# Dias para manter backups (padrão: 5)
DIAS_MANTER_BACKUP = 5

# Diretório de backups
BACKUP_DIR = 'backups'

# Arquivo de controle
CONTROLE_BACKUP = 'ultimo_backup.txt'

# Diretórios de mídia incluídos
MEDIA_DIRS = [
    'media/capas',
    'media/setup', 
    'media/glossario',
    'media/componentes',
    'media/avatars'
]
```

## Como Alterar Configurações

### Alterar Dias de Retenção
No arquivo `views.py`, linha ~2850:
```python
limpar_backups_antigos(5)  # Altere o número aqui
```

### Desabilitar Backup Automático
No arquivo `views.py`, comente as linhas ~2830-2860:
```python
# if not globals().get('_backup_executado', False):
#     # ... código do backup automático
```

### Alterar Horário de Execução
O backup executa na primeira inicialização do dia.
Para alterar, modifique a lógica de comparação de datas.

## Monitoramento

### Logs de Backup
- Mensagens são exibidas no console do Django
- Sucesso: "Backup automático criado: filename.zip"
- Erro: "Erro ao criar backup automático: erro"

### Verificar Status
- Arquivo `ultimo_backup.txt` contém a data do último backup
- Diretório `backups/` contém todos os backups disponíveis

## Restauração

### Via Interface Web
1. Acesse "Backup do Sistema" no menu administrativo
2. Clique em "Restaurar Backup"
3. Selecione o arquivo ZIP
4. Confirme a restauração

### Via Código
```python
# Exemplo de restauração programática
import zipfile
import json

def restaurar_backup(backup_path):
    with zipfile.ZipFile(backup_path, 'r') as zipf:
        # Ler dados
        dados_json = zipf.read('dados.json').decode('utf-8')
        backup_data = json.loads(dados_json)
        
        # Restaurar dados globais
        global jogos_criados, usuarios_criados
        jogos_criados.clear()
        jogos_criados.extend(backup_data.get('jogos', []))
        # ... outros dados
        
        # Extrair mídias
        for file_info in zipf.infolist():
            if file_info.filename.startswith('media/'):
                zipf.extract(file_info, '.')
```

## Troubleshooting

### Backup não está sendo criado
1. Verificar permissões de escrita no diretório
2. Verificar espaço em disco
3. Verificar logs de erro no console

### Backup muito grande
1. Limpar mídias antigas desnecessárias
2. Reduzir dias de retenção
3. Implementar backup incremental (futuro)

### Restauração falhou
1. Verificar integridade do arquivo ZIP
2. Verificar permissões de escrita
3. Verificar estrutura do backup

## Melhorias Futuras

- [ ] Backup incremental
- [ ] Compressão otimizada
- [ ] Upload para cloud storage
- [ ] Notificações por email
- [ ] Interface de agendamento
- [ ] Backup de banco MongoDB real
- [ ] Criptografia de backups
- [ ] Verificação de integridade automática