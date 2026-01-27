#!/bin/bash

echo "🧪 Executando teste automatizado de senhas do sistema..."
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale Python 3.7+ para executar o teste."
    exit 1
fi

# Instalar dependências se necessário
pip3 install requests > /dev/null 2>&1

# Executar o teste
python3 test_senhas_sistema.py

echo
echo "Teste concluído."