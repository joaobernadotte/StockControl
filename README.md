# StockControl

Sistema de gerenciamento de estoque desenvolvido em **Python** e **MySQL**, com foco no controle de produtos, movimentações de estoque e acompanhamento de níveis mínimos.

O projeto foi desenvolvido como parte do meu aprendizado em desenvolvimento de software, aplicando conceitos de programação, organização de código, banco de dados e testes automatizados.

## Funcionalidades

- Cadastro de produtos.
- Listagem de produtos cadastrados.
- Atualização de informações dos produtos.
- Exclusão de produtos, respeitando o histórico de movimentações.
- Consulta de produtos por ID.
- Relatório de produtos com estoque baixo.
- Registro de entradas e saídas de estoque.
- Controle automático da quantidade após cada movimentação.
- Histórico de movimentações armazenado no banco de dados.
- Validação de dados para evitar operações inválidas.

## Tecnologias utilizadas

- **Python** — lógica e desenvolvimento da aplicação.
- **MySQL** — armazenamento e gerenciamento dos dados.
- **mysql-connector-python** — comunicação entre Python e MySQL.
- **python-dotenv** — gerenciamento de variáveis de ambiente.
- **Pytest** — testes automatizados.
- **Git e GitHub** — versionamento e publicação do projeto.

## Estrutura do projeto

```text
StockControl/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── validacoes.py
│   └── servicos.py
│
├── tests/
│   ├── test_validacoes.py
│   ├── test_database.py
│   ├── test_servicos.py
│   └── test_main.py
│
├── .gitignore
├── .env
└── README.md
```

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.
- MySQL Server.
- Git (opcional).

## Instalação

**1. Clone o repositório:**

```bash
git clone URL_DO_REPOSITORIO
```

**2. Entre na pasta do projeto:**

```bash
cd StockControl
```

**3. Crie um ambiente virtual:**

```bash
python -m venv .venv
```

**4. Ative o ambiente virtual:**

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**5. Instale as dependências:**

```bash
python -m pip install mysql-connector-python python-dotenv pytest
```

## Configuração do banco de dados

Crie um banco de dados no MySQL:

```sql
CREATE DATABASE stockcontrol;
```

Configure as credenciais de acesso em um arquivo `.env`, na raiz do projeto:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=stockcontrol
DB_PORT=3306
```

As tabelas necessárias devem ser criadas conforme a estrutura utilizada pela aplicação.

## Executando o projeto

Com o ambiente virtual ativado e o banco de dados configurado, execute:

```bash
python -m src.main
```

## Executando os testes

Para executar os testes automatizados:

```bash
python -m pytest -v
```

O projeto possui testes para validações, operações de banco de dados, serviços e funcionalidades do menu principal.

## Objetivo do projeto

O StockControl tem como objetivo consolidar meus conhecimentos em Python, SQL, integração com banco de dados, organização de projetos e boas práticas de desenvolvimento.

O projeto continua em desenvolvimento e poderá receber novas funcionalidades e melhorias.

---

**Desenvolvido como projeto de aprendizado e portfólio.**