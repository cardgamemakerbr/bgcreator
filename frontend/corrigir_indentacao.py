import re

# Ler o arquivo views.py
with open('web/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Corrigir indentação após loops for
corrected_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    corrected_lines.append(line)
    
    # Se encontrar um for seguido de linha vazia ou sem indentação adequada
    if 'for j in jogos_criados:' in line:
        i += 1
        # Adicionar o conteúdo do loop se estiver faltando
        if i < len(lines) and 'if j[\'id\'] == int(jogo_id):' not in lines[i]:
            corrected_lines.append('        if j[\'id\'] == int(jogo_id):\n')
            corrected_lines.append('            jogo = j\n')
            corrected_lines.append('            break\n')
        continue
    
    i += 1

# Salvar o arquivo corrigido
with open('web/views.py', 'w', encoding='utf-8') as f:
    f.writelines(corrected_lines)

print("Indentação corrigida!")