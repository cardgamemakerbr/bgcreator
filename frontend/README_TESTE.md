# 🧪 Teste Automatizado - Sistema de Senhas

## 📋 Descrição

Este teste automatizado valida a funcionalidade de alteração de senhas dos usuários do sistema BGCreator, garantindo que:

1. ✅ Login funciona com senha padrão
2. ✅ Alteração de senha é processada corretamente
3. ✅ Nova senha é persistida no arquivo de dados
4. ✅ Login funciona com a nova senha
5. ✅ Senha é restaurada ao estado original

## 🚀 Como Executar

### Windows
```bash
# Executar script automatizado
executar_teste.bat

# Ou executar diretamente
python test_senhas_sistema.py
```

### Linux/Mac
```bash
# Dar permissão de execução
chmod +x executar_teste.sh

# Executar script automatizado
./executar_teste.sh

# Ou executar diretamente
python3 test_senhas_sistema.py
```

## 📋 Pré-requisitos

1. **Servidor BGCreator rodando** em `http://localhost:8000`
2. **Python 3.7+** instalado
3. **Biblioteca requests** (`pip install requests`)

## 🔍 O que o Teste Verifica

### Teste 1: Login Inicial
- Acessa página de login
- Extrai token CSRF
- Faz login com credenciais padrão (admin/admin)
- Verifica redirecionamento de sucesso

### Teste 2: Alteração de Senha
- Acessa página de perfil
- Preenche formulário de alteração
- Submete nova senha
- Verifica mensagem de sucesso

### Teste 3: Persistência
- Lê arquivo `data/bgcreator_data.json`
- Verifica se nova senha foi salva
- Confirma integridade dos dados

### Teste 4: Validação da Nova Senha
- Faz logout
- Tenta login com nova senha
- Confirma autenticação bem-sucedida

### Teste 5: Restauração
- Restaura senha padrão
- Garante estado original do sistema

## 📊 Saída do Teste

```
🧪 Iniciando teste de alteração de senhas do sistema...
============================================================
✅ Teste 1 - Login com senha padrão: Login realizado com sucesso
✅ Teste 2 - Alteração de senha: Senha alterada com sucesso
✅ Teste 3 - Verificação de persistência: Senha persistida corretamente no arquivo
✅ Teste 4 - Login com nova senha: Login realizado com sucesso
✅ Teste 5 - Restaurar senha padrão: Senha alterada com sucesso

============================================================
📊 RELATÓRIO FINAL DO TESTE
============================================================
Total de testes: 5
Sucessos: 5
Falhas: 0
Taxa de sucesso: 100.0%

✅ TODOS OS TESTES PASSARAM
```

## 🐛 Solução de Problemas

### Erro: Servidor não está rodando
```bash
# Inicie o servidor BGCreator
cd frontend
python manage.py runserver
```

### Erro: Módulo requests não encontrado
```bash
# Instale a dependência
pip install requests
```

### Erro: Arquivo de dados não encontrado
- Certifique-se de que o diretório `data/` existe
- Execute o sistema pelo menos uma vez para criar o arquivo

## 🔧 Personalização

Para testar outros usuários, modifique as variáveis no arquivo `test_senhas_sistema.py`:

```python
# Alterar usuário de teste
def executar_teste(self):
    # Trocar "admin" por "autor", "revisor" ou "leitor"
    sucesso, msg = self.fazer_login("autor", "123")
```

## 📝 Logs e Debug

O teste gera logs detalhados de cada etapa. Para debug adicional, modifique:

```python
# Adicionar mais logs
def log(self, mensagem, sucesso=True, debug=False):
    if debug:
        print(f"🔍 DEBUG: {mensagem}")
```

---

**Desenvolvido para BGCreator v1.0**  
**Compatível com Python 3.7+**