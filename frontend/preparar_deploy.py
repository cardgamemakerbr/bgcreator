#!/usr/bin/env python3
"""
Script para preparar o BGCreator para deploy inicial
Remove todos os usuários do sistema e limpa dados de teste
"""

import os
import json
from pathlib import Path

def limpar_dados_sistema():
    """Remove todos os dados de teste e usuários do sistema"""
    
    # Arquivo de dados
    data_file = 'data/bgcreator_data.json'
    
    # Dados limpos para deploy inicial
    dados_limpos = {
        'jogos_criados': [],
        'mecanicas_criadas': [],
        'componentes_criados': [],
        'temas_criados': [],
        'usuarios_criados': [],  # Lista vazia - sem usuários
        'comentarios_criados': [],
        'complexidade_senha': 1,  # Desativado por padrão
        'usuarios_sistema_status': {
            '1': False,  # admin desativado
            '2': False,  # autor desativado
            '3': False,  # revisor desativado
            '4': False   # leitor desativado
        },
        'senhas_sistema': {
            'admin': 'admin',
            'autor': '123',
            'revisor': '123',
            'leitor': '123'
        },
        'timestamp': '2024-01-01T00:00:00'
    }
    
    # Criar diretório se não existir
    Path('data').mkdir(exist_ok=True)
    
    # Salvar dados limpos
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(dados_limpos, f, ensure_ascii=False, indent=2)
        print(f"Dados limpos salvos em {data_file}")
        return True
    except Exception as e:
        print(f"Erro ao salvar dados limpos: {e}")
        return False

def limpar_arquivos_media():
    """Remove arquivos de mídia de teste"""
    
    media_dirs = [
        'media/capas',
        'media/setup', 
        'media/glossario',
        'media/componentes',
        'media/avatars'
    ]
    
    arquivos_removidos = 0
    
    for media_dir in media_dirs:
        if os.path.exists(media_dir):
            for arquivo in os.listdir(media_dir):
                arquivo_path = os.path.join(media_dir, arquivo)
                if os.path.isfile(arquivo_path):
                    try:
                        os.remove(arquivo_path)
                        arquivos_removidos += 1
                    except Exception as e:
                        print(f"Erro ao remover {arquivo_path}: {e}")
    
    print(f"{arquivos_removidos} arquivos de midia removidos")

def limpar_backups():
    """Remove backups de teste"""
    
    if os.path.exists('backups'):
        backups_removidos = 0
        for arquivo in os.listdir('backups'):
            if arquivo.endswith('.zip'):
                arquivo_path = os.path.join('backups', arquivo)
                try:
                    os.remove(arquivo_path)
                    backups_removidos += 1
                except Exception as e:
                    print(f"Erro ao remover backup {arquivo}: {e}")
        
        print(f"{backups_removidos} backups removidos")
    
    # Remover arquivo de controle de backup
    if os.path.exists('ultimo_backup.txt'):
        os.remove('ultimo_backup.txt')
        print("Arquivo de controle de backup removido")

def criar_readme_deploy():
    """Cria README com instruções de deploy"""
    
    readme_content = """# 🚀 BGCreator - Deploy Inicial

## ✅ Sistema Preparado para Produção

Este sistema foi preparado para deploy inicial com:

- ✅ **Dados limpos**: Sem usuários de teste
- ✅ **Mídia limpa**: Sem arquivos de exemplo  
- ✅ **Backups limpos**: Sem backups de desenvolvimento
- ✅ **Configuração inicial**: Pronto para primeiro administrador

## 🔧 Primeiro Acesso

1. **Acesse a aplicação** pela primeira vez
2. **Será exibida automaticamente** a tela de cadastro do administrador
3. **Preencha os dados** do primeiro administrador do sistema
4. **Após o cadastro**, faça login normalmente

## 📋 Funcionalidades Implementadas

### ✅ Sistema de Usuários
- Cadastro inicial automático do administrador
- 4 perfis de acesso (Admin, Autor, Revisor, Leitor)
- Sistema de avatars
- Complexidade de senhas configurável (4 níveis)
- Controle de ativação/desativação

### ✅ Sistema de Jogos
- CRUD completo com versionamento
- Sistema de cópia com incremento major
- Upload de imagens (capas, setup, glossário)
- Cálculo automático de peso/complexidade
- Sistema de classificação (6 tipos)
- Busca avançada

### ✅ Sistema de Revisão
- Ícones de status de revisão nos jogos:
  - ⚠️ Correções pendentes
  - ✅ Totalmente aprovado (8/8)
  - 🕐 Em revisão (parcial)
  - ➖ Sem revisão (0/8)
- Controle de co-autor/co-revisor
- Bloqueios configuráveis

### ✅ Sistema de Componentes
- Upload de imagens para componentes
- Visualização em listas e detalhes
- Classificação por tipos

### ✅ Sistema de Comentários
- Comentários para leitores
- Avaliação de 1 a 5 estrelas
- Exibição de avatars nos comentários

### ✅ Sistema de Backup
- Backup automático diário
- Limpeza automática (manter 5 dias)
- Backup manual via interface
- Restauração completa

## 🔐 Níveis de Complexidade de Senha

1. **Desativado**: Sem restrições
2. **Básico**: Letras e números, mínimo 6 dígitos  
3. **Médio**: Maiúsculas, minúsculas, números, mínimo 8 dígitos
4. **Alto**: Maiúsculas, minúsculas, números, caractere especial, mínimo 10 dígitos

## 🏗️ Arquitetura

```
bgcreator/
├── frontend/           # Django Frontend
│   ├── templates/      # Templates HTML
│   ├── media/         # Upload de imagens
│   ├── data/          # Dados persistidos
│   └── backups/       # Backups do sistema
├── backend/           # API Python (futuro)
├── database/          # MongoDB (futuro)
└── docker-compose.yml # Orquestração
```

## 🚀 Como Executar

### Produção (Docker)
```bash
docker-compose up --build
```

### Desenvolvimento
```bash
cd frontend
pip install -r requirements.txt
python manage.py runserver
```

## 📊 Dados Pré-definidos

- **90+ mecânicas** de board games
- **100+ temas** categorizados
- **48 componentes** com classificação
- **Sistema completo** de estruturas e condições

## 🎯 Status: PRONTO PARA PRODUÇÃO

**Data de Preparação**: {timestamp}
**Versão**: 1.0.0
**Status**: ✅ Deploy Ready
"""
    
    from datetime import datetime
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    readme_content = readme_content.format(timestamp=timestamp)
    
    try:
        with open('DEPLOY_README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("README de deploy criado: DEPLOY_README.md")
    except Exception as e:
        print(f"Erro ao criar README: {e}")

def main():
    """Função principal"""
    print("Preparando BGCreator para Deploy Inicial...")
    print("=" * 50)
    
    # Limpar dados
    if limpar_dados_sistema():
        print("Dados do sistema limpos")
    
    # Limpar mídia
    limpar_arquivos_media()
    
    # Limpar backups
    limpar_backups()
    
    # Criar README
    criar_readme_deploy()
    
    print("=" * 50)
    print("BGCreator preparado para deploy!")
    print("")
    print("Proximos passos:")
    print("1. Fazer deploy da aplicacao")
    print("2. Acessar pela primeira vez")
    print("3. Cadastrar o administrador principal")
    print("4. Configurar complexidade de senhas")
    print("5. Comecar a usar o sistema!")
    print("")
    print("Consulte DEPLOY_README.md para mais detalhes")

if __name__ == "__main__":
    main()