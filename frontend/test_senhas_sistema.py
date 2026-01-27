#!/usr/bin/env python3
"""
Teste automatizado para validar alteração de senhas do sistema BGCreator
"""

import os
import sys
import json
import requests
import time
from pathlib import Path

# Configurações do teste
BASE_URL = "http://localhost:8000"
DATA_FILE = "data/bgcreator_data.json"

class TesteSenhasSistema:
    def __init__(self):
        self.session = requests.Session()
        self.resultados = []
        
    def log(self, mensagem, sucesso=True):
        status = "[OK]" if sucesso else "[ERRO]"
        print(f"{status} {mensagem}")
        self.resultados.append({"mensagem": mensagem, "sucesso": sucesso})
        
    def fazer_login(self, login, senha):
        """Tenta fazer login com as credenciais fornecidas"""
        try:
            # Primeiro, pegar o CSRF token
            response = self.session.get(f"{BASE_URL}/login/")
            if response.status_code != 200:
                return False, "Erro ao acessar página de login"
                
            # Extrair CSRF token
            csrf_token = None
            for line in response.text.split('\n'):
                if 'csrfmiddlewaretoken' in line:
                    start = line.find('value="') + 7
                    end = line.find('"', start)
                    csrf_token = line[start:end]
                    break
                    
            if not csrf_token:
                return False, "CSRF token não encontrado"
                
            # Fazer login
            data = {
                'login': login,
                'senha': senha,
                'csrfmiddlewaretoken': csrf_token
            }
            
            response = self.session.post(f"{BASE_URL}/login/", data=data)
            
            # Verificar se foi redirecionado (sucesso) ou voltou para login (erro)
            if response.url.endswith('/login/'):
                return False, "Credenciais inválidas"
            else:
                return True, "Login realizado com sucesso"
                
        except Exception as e:
            return False, f"Erro durante login: {str(e)}"
            
    def alterar_senha(self, senha_atual, nova_senha):
        """Altera a senha do usuário logado"""
        try:
            # Acessar página de perfil
            response = self.session.get(f"{BASE_URL}/perfil/")
            if response.status_code != 200:
                return False, "Erro ao acessar página de perfil"
                
            # Extrair CSRF token
            csrf_token = None
            for line in response.text.split('\n'):
                if 'csrfmiddlewaretoken' in line:
                    start = line.find('value="') + 7
                    end = line.find('"', start)
                    csrf_token = line[start:end]
                    break
                    
            if not csrf_token:
                return False, "CSRF token não encontrado"
                
            # Alterar senha
            data = {
                'nome': 'Admin Sistema',
                'email': 'admin@bgcreator.com',
                'senha_atual': senha_atual,
                'nova_senha': nova_senha,
                'confirma_senha': nova_senha,
                'csrfmiddlewaretoken': csrf_token
            }
            
            response = self.session.post(f"{BASE_URL}/perfil/", data=data)
            
            # Verificar se houve mensagem de sucesso
            if "alterada com sucesso" in response.text:
                return True, "Senha alterada com sucesso"
            else:
                return False, "Erro ao alterar senha"
                
        except Exception as e:
            return False, f"Erro durante alteração: {str(e)}"
            
    def verificar_persistencia(self, login, nova_senha):
        """Verifica se a senha foi persistida no arquivo JSON"""
        try:
            if not Path(DATA_FILE).exists():
                return False, "Arquivo de dados não encontrado"
                
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            senhas_sistema = dados.get('senhas_sistema', {})
            senha_salva = senhas_sistema.get(login)
            
            if senha_salva == nova_senha:
                return True, "Senha persistida corretamente no arquivo"
            else:
                return False, f"Senha não persistida. Esperado: {nova_senha}, Encontrado: {senha_salva}"
                
        except Exception as e:
            return False, f"Erro ao verificar persistência: {str(e)}"
            
    def executar_teste(self):
        """Executa o teste completo"""
        print("[TESTE] Iniciando teste de alteracao de senhas do sistema...")
        print("=" * 60)
        
        # Teste 1: Login com senha padrão admin/admin
        sucesso, msg = self.fazer_login("admin", "admin")
        self.log(f"Teste 1 - Login admin/admin: {msg}", sucesso)
        
        if not sucesso:
            self.log("[ERRO] Teste falhou no login inicial. Abortando.", False)
            return self.gerar_relatorio()
            
        # Teste 2: Alterar senha para 123456
        sucesso, msg = self.alterar_senha("admin", "123456")
        self.log(f"Teste 2 - Alterar senha para 123456: {msg}", sucesso)
        
        if not sucesso:
            self.log("[ERRO] Teste falhou na alteracao de senha. Abortando.", False)
            return self.gerar_relatorio()
            
        # Aguardar salvamento
        time.sleep(1)
        
        # Teste 3: Logout e login com admin/123456
        self.session.get(f"{BASE_URL}/logout/")
        time.sleep(1)
        
        sucesso, msg = self.fazer_login("admin", "123456")
        self.log(f"Teste 3 - Login admin/123456: {msg}", sucesso)
        
        if not sucesso:
            self.log("[ERRO] Login com nova senha falhou. Sistema nao funcionou.", False)
            return self.gerar_relatorio()
            
        # Teste 4: Restaurar senha para admin
        sucesso, msg = self.alterar_senha("123456", "admin")
        self.log(f"Teste 4 - Restaurar senha para admin: {msg}", sucesso)
        
        return self.gerar_relatorio()
        
    def gerar_relatorio(self):
        """Gera relatório final do teste"""
        print("\n" + "=" * 60)
        print("[RELATORIO] RELATORIO FINAL DO TESTE")
        print("=" * 60)
        
        total_testes = len(self.resultados)
        testes_sucesso = sum(1 for r in self.resultados if r["sucesso"])
        testes_falha = total_testes - testes_sucesso
        
        print(f"Total de testes: {total_testes}")
        print(f"Sucessos: {testes_sucesso}")
        print(f"Falhas: {testes_falha}")
        print(f"Taxa de sucesso: {(testes_sucesso/total_testes)*100:.1f}%")
        
        if testes_falha > 0:
            print("\n[ERRO] TESTES QUE FALHARAM:")
            for resultado in self.resultados:
                if not resultado["sucesso"]:
                    print(f"  - {resultado['mensagem']}")
        else:
            print("\n[OK] Funcionalidade de mudanca de senhas validada com sucesso!")
                    
        status_final = "[OK] TODOS OS TESTES PASSARAM" if testes_falha == 0 else "[ERRO] ALGUNS TESTES FALHARAM"
        print(f"\n{status_final}")
        
        return testes_falha == 0

if __name__ == "__main__":
    # Verificar se o servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"[INFO] Servidor BGCreator detectado em {BASE_URL}")
    except:
        print(f"[ERRO] Servidor BGCreator nao esta rodando em {BASE_URL}")
        print("   Inicie o servidor com: python manage.py runserver")
        sys.exit(1)
        
    # Executar teste
    teste = TesteSenhasSistema()
    sucesso = teste.executar_teste()
    
    # Código de saída
    sys.exit(0 if sucesso else 1)