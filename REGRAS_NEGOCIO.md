# 📋 Regras de Negócio - BGCreator

## RN01 - Navegação Global
**Descrição**: O menu principal deve ser persistente em todas as páginas da aplicação.

**Componentes**: JOGO, MECÂNICAS, COMPONENTES, TEMAS

**Implementação**: Menu fixo no topo da página com navegação entre seções.

---

## RN02 - Operações CRUD Padrão
**Descrição**: Cada seção deve prover operações básicas de gerenciamento.

**Operações Obrigatórias**:
- **Novo**: Criar novo registro
- **Lista**: Visualizar todos os itens
- **Editar**: Alterar dados existentes  
- **Renomear**: Alteração rápida de nome/título

**Aplicável a**: Mecânicas, Temas, Componentes, Jogos

---

## RN03 - Sistema de Busca
**Descrição**: A listagem de jogos deve permitir filtros múltiplos.

**Critérios de Busca**:
- Nome do jogo (busca textual)
- ID do jogo
- Mecânica associada
- Tema associado

**Implementação**: Endpoint `/api/jogos/buscar/?q=termo`

---

## RN04 - Upload de Imagens
**Descrição**: Sistema deve suportar upload de imagens para capas e glossário.

**Especificações**:
- **Formatos**: JPG, PNG
- **Tamanho máximo**: 5MB
- **Resolução recomendada**: 800x600px
- **Armazenamento**: Sistema de arquivos local

---

## RN05 - Cálculo Automático de Peso

### Fórmula Base
```
Peso = 0.1 + P_tempo + P_mecanica + P_componentes + P_vitoria + P_derrota + P_estrutura + P_especial
```

### Tabela de Parâmetros

| Categoria | Regra de Incremento | Limite Máximo |
|-----------|-------------------|---------------|
| **Tempo Médio** | +0,1 a cada 30 minutos | 1,0 |
| **Mecânicas** | +0,1 por mecânica selecionada | 1,0 |
| **Componentes** | +0,1 por componente adicionado | 1,0 |
| **Condições de Vitória** | +0,1 por condição | 0,3 |
| **Condições de Derrota** | +0,1 por condição | 0,3 |
| **Estruturas** | +0,1 por (Fase/Ação/Rodada) | 1,0 |
| **Condições Especiais** | +0,1 por condição especial | 0,5 |

### Exemplos de Cálculo

**Jogo Simples**:
- Tempo: 30min → +0,1
- 1 Mecânica → +0,1  
- 2 Componentes → +0,2
- 1 Condição Vitória → +0,1
- **Peso Total**: 0.1 + 0.1 + 0.1 + 0.2 + 0.1 = **0.6**

**Jogo Complexo**:
- Tempo: 180min → +0,6 (limitado a 1,0)
- 8 Mecânicas → +0,8 (limitado a 1,0)
- 15 Componentes → +1,0 (limitado a 1,0)
- 3 Condições Vitória → +0,3
- 2 Condições Derrota → +0,2 (limitado a 0,3)
- 5 Estruturas → +0,5 (limitado a 1,0)
- **Peso Total**: 0.1 + 0.6 + 0.8 + 1.0 + 0.3 + 0.2 + 0.5 = **3.5**

---

## RN06 - Restrições de Formulário

### Listas Pré-definidas

**Jogadores**: 0 a 50 (seleção de intervalo)

**Tempo Médio (minutos)**:
```
5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 80, 100, 120, 140, 180, 200, 240, 300, 360
```

**Idade Recomendada**:
```
2+, 4+, 6+, 8+, 10+, 11+, 12+, 14+, 16+, 18+
```

### Validações
- **Jogadores mín ≤ Jogadores máx**
- **Tempo mín ≤ Tempo máx**
- **Nome do jogo**: obrigatório, máximo 200 caracteres
- **Descrição curta**: obrigatória

---

## RN07 - Estrutura Hierárquica

### Tipos de Estrutura
- **Fase**: Etapa principal do jogo
- **Ação**: Ação específica dentro de uma fase
- **Rodada**: Ciclo completo de jogadas

### Condições Especiais
- São sub-itens vinculados a uma estrutura específica
- Cada condição especial adiciona 0,1 ao peso
- Respeitam o limite máximo de 0,5 para a categoria

### Exemplo de Hierarquia
```
Jogo: "Colonizadores"
├── Fase: "Preparação" (Peso: +0,1)
│   ├── Condição Especial: "Distribuir recursos iniciais" (Peso: +0,1)
│   └── Condição Especial: "Posicionar peças" (Peso: +0,1)
├── Rodada: "Turno do Jogador" (Peso: +0,1)
│   ├── Ação: "Rolar dados" (Peso: +0,1)
│   └── Ação: "Construir" (Peso: +0,1)
└── Fase: "Pontuação Final" (Peso: +0,1)
```

---

## RN08 - Glossário Visual

### Composição Obrigatória
- **Palavra**: Termo técnico (máx. 100 caracteres)
- **Definição**: Texto explicativo (obrigatório)
- **Imagem**: Upload opcional para auxílio visual

### Regras
- Cada jogo pode ter múltiplos termos no glossário
- Termos devem ser únicos por jogo
- Imagens seguem as mesmas regras de upload (RN04)

---

## RN09 - Integridade Referencial

### Relacionamentos Obrigatórios
- Condições de Vitória/Derrota → Jogo
- Estruturas → Jogo
- Condições Especiais → Estrutura
- Glossário → Jogo

### Regras de Exclusão
- **Jogo excluído**: Remove todas as dependências
- **Mecânica/Tema/Componente excluído**: Remove apenas a associação
- **Estrutura excluída**: Remove condições especiais vinculadas

---

## RN10 - Validações de Negócio

### Ao Salvar Jogo
1. Recalcular peso automaticamente
2. Validar intervalo de jogadores
3. Validar intervalo de tempo
4. Verificar existência de mecânicas/temas/componentes selecionados

### Ao Modificar Dependências
1. Recalcular peso de todos os jogos afetados
2. Atualizar timestamps de modificação
3. Manter histórico de alterações (futuro)

---

## RN11 - Performance e Limites

### Limites por Jogo
- **Mecânicas**: máximo 20
- **Componentes**: máximo 50  
- **Temas**: máximo 10
- **Condições de Vitória**: máximo 10
- **Condições de Derrota**: máximo 10
- **Estruturas**: máximo 20
- **Condições Especiais por Estrutura**: máximo 10

### Cache
- Peso calculado é armazenado no banco
- Recálculo apenas quando dependências mudam
- Cache de listas para melhor performance