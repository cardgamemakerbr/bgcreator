# Senhas dos usuários do sistema (alteráveis)
SENHAS_SISTEMA = {
    'admin': 'admin',
    'autor': '123',
    'revisor': '123',
    'leitor': '123'
}

def get_senha(login):
    return SENHAS_SISTEMA.get(login, '123')

def set_senha(login, nova_senha):
    SENHAS_SISTEMA[login] = nova_senha