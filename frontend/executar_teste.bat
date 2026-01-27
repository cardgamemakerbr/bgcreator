@echo off
echo 🧪 Executando teste automatizado de senhas do sistema...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.7+ para executar o teste.
    pause
    exit /b 1
)

REM Instalar dependências se necessário
pip install requests >nul 2>&1

REM Executar o teste
python test_senhas_sistema.py

echo.
echo Teste concluído. Pressione qualquer tecla para continuar...
pause >nul