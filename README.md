# 🎲 BGCreator

> Aplicação para ajudar desenvolvedores de board games a criar novos jogos e padronizar a documentação do jogo.

![Status: Em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

## ✨ Funcionalidades

- [x] Gerenciamento de jogos (CRUD)
- [x] Sistema de mecânicas de jogo
- [x] Gerenciamento de componentes
- [x] Sistema de temas
- [x] Cálculo automático de peso/complexidade
- [x] Upload de imagens para capas
- [x] Glossário visual com imagens
- [ ] Relatórios em PDF (em desenvolvimento)
- [ ] Sistema de exportação (em desenvolvimento)

## 🛠 Tecnologias

- **Backend**: Python com API REST
- **Frontend**: Django
- **Database**: MongoDB
- **Containerização**: Docker (3 containers)
- **Deploy**: Docker Compose

## 📦 Pré-requisitos

- Docker
- Docker Compose
- Python 3.10+

## 🚀 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/bgcreator.git
   cd bgcreator
   ```

2. Execute com Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Acesse a aplicação:
   - Frontend: http://localhost:8000
   - API Backend: http://localhost:8001
   - MongoDB: localhost:27017

## 🏗 Arquitetura

```
bgcreator/
├── backend/           # API Python
├── frontend/          # Django Frontend
├── database/          # MongoDB configs
├── docker-compose.yml
└── README.md
```

## 🧪 Testes

Execute os testes do backend:
```bash
cd backend && python -m pytest tests/
```

Execute os testes do frontend:
```bash
cd frontend && python manage.py test
```

## 📋 Regras de Negócio

### Cálculo de Peso (Complexidade)
O peso do jogo é calculado automaticamente baseado em:
- Tempo médio: +0,1 a cada 30min (máx: 1,0)
- Mecânicas: +0,1 por mecânica (máx: 1,0)
- Componentes: +0,1 por componente (máx: 1,0)
- Condições de vitória: +0,1 por condição (máx: 0,3)
- Condições de derrota: +0,1 por condição (máx: 0,3)
- Fases/Ações: +0,1 por estrutura (máx: 1,0)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.