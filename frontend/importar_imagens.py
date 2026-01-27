#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import json
from pathlib import Path

def importar_imagens_componentes():
    """Importa imagens da pasta ./imagens/componentes para media/componentes"""
    
    # Caminhos
    pasta_origem = Path("../imagens/componentes")
    pasta_destino = Path("media/componentes")
    arquivo_dados = Path("data/bgcreator_data.json")
    
    # Criar pasta de destino se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    # Mapeamento de nomes de arquivos para nomes de componentes
    mapeamento = {
        "Ampulheta.png": "Ampulheta",
        "Cartas de Referência.png": "Cartas de Referência", 
        "Cartas Mini.png": "Cartas Mini",
        "Cartas Standard.png": "Cartas Standard",
        "Cubos de Madeira.png": "Cubos de Madeira",
        "dado d6.jpg": "Dados D6",
        "Dados Poliédricos.jpg": "Dados Poliédricos",
        "Discos de Madeira.jpg": "Discos de Madeira",
        "Escudo de Jogador.jpg": "Escudo de Jogador",
        "Fichas de Poker.jpg": "Fichas de Poker",
        "Gemas de PlásticoAcrílico.jpg": "Gemas de Plástico/Acrílico",
        "Manual de Regras.png": "Manual de Regras",
        "Marcador de Primeiro Jogador.jpg": "Marcador de Primeiro Jogador",
        "Marcadores de Pontuação.jpg": "Marcadores de Pontuação",
        "Meeple de Madeira.jpg": "Meeple de Madeira",
        "Miniaturas de Plástico.jpg": "Miniaturas de Plástico",
        "Moedas de Metal.jpg": "Moedas de Metal",
        "Moedas de PapelCartão.jpg": "Moedas de Papel/Cartão",
        "Peões de Plástico.jpg": "Peões de Plástico",
        "Saco de Pano.jpg": "Saco de Pano (Bag)",
        "Tabuleiro Principal.jpg": "Tabuleiro Principal",
        "Tabuleiros Individuais.jpg": "Tabuleiros Individuais",
        "Tiles Hexagonais.jpg": "Tiles Hexagonais",
        "Tiles Quadrados.jpg": "Tiles Quadrados"
    }
    
    # Carregar dados existentes
    dados = {}
    if arquivo_dados.exists():
        with open(arquivo_dados, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    
    componentes_criados = dados.get('componentes_criados', [])
    
    # Processar cada imagem
    imagens_importadas = 0
    for arquivo, nome_componente in mapeamento.items():
        arquivo_origem = pasta_origem / arquivo
        
        if arquivo_origem.exists():
            # Copiar imagem para pasta de destino
            extensao = arquivo_origem.suffix
            nome_destino = f"componente_{arquivo}"
            arquivo_destino = pasta_destino / nome_destino
            
            try:
                shutil.copy2(arquivo_origem, arquivo_destino)
                caminho_imagem = f"/media/componentes/{nome_destino}"
                
                # Verificar se já existe componente com este nome
                componente_existente = None
                for i, comp in enumerate(componentes_criados):
                    if comp['nome'] == nome_componente:
                        componente_existente = i
                        break
                
                if componente_existente is not None:
                    # Atualizar componente existente
                    componentes_criados[componente_existente]['imagem'] = caminho_imagem
                    print(f"Atualizada imagem do componente: {nome_componente}")
                else:
                    # Criar novo componente com imagem
                    novo_id = len(componentes_criados) + 2000
                    novo_componente = {
                        'id': novo_id,
                        'nome': nome_componente,
                        'descricao': f'Componente importado com imagem',
                        'tipo': 'NEUTRO',
                        'imagem': caminho_imagem
                    }
                    componentes_criados.append(novo_componente)
                    print(f"Criado novo componente com imagem: {nome_componente}")
                
                imagens_importadas += 1
                
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
        else:
            print(f"Arquivo nao encontrado: {arquivo}")
    
    # Salvar dados atualizados
    dados['componentes_criados'] = componentes_criados
    with open(arquivo_dados, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"\nImportacao concluida!")
    print(f"{imagens_importadas} imagens importadas")
    print(f"Imagens salvas em: {pasta_destino}")
    print(f"Dados atualizados em: {arquivo_dados}")

if __name__ == "__main__":
    print("Iniciando importacao de imagens dos componentes...")
    importar_imagens_componentes()