# Projeto PIM - Plataforma de Integração e Monitoramento

## Descrição

Este projeto é um **Sistema de PIM (Projeto Integrado Multidisciplinar)** que combina uma **interface gráfica com Tkinter**, um **backend com FastAPI** e um **banco de dados SQLite**.  

O objetivo é fornecer um sistema interativo para cadastro, gerenciamento e visualização de informações, integrando front-end e back-end de forma prática e funcional.

---

## Funcionalidades

### Interface Gráfica (Tkinter)
- Tela de login e cadastro de usuários.
- CRUD (Create, Read, Update, Delete) de entidades, como:
  - Professores
  - Alunos
  - Turmas
  - Atividades
- Feedback visual e interação com o usuário.
- Controle de progresso e estatísticas simples.

### Backend (FastAPI)
- API REST para gerenciar dados persistidos no SQLite.
- Endpoints seguros para login, cadastro e operações CRUD.
- Validação de dados e tratamento de erros.
- Possibilidade de expansão para autenticação JWT e autorização por usuário.

### Banco de Dados (SQLite)
- Armazenamento local dos dados do sistema.
- Tabelas para usuários, professores, alunos, turmas e atividades.
- Persistência simples e eficiente, sem necessidade de servidor externo.

---

## Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter**: Para criação da interface gráfica.
- **FastAPI**: Para criar a API do backend.
- **SQLite**: Banco de dados leve e embutido.
