# Sistema de Gerenciamento do CAIN

Este é um sistema web desenvolvido em Flask e SGBD em PostgresSQL para gerenciar as informações do Núcleo de Acessibilidade e Inclusão (CAIN).

## Configuração do Ambiente

Siga as instruções abaixo para configurar e rodar o projeto.

### Pré-requisitos

- Python 3
- PostgreSQL
- As dependências Python listadas em `requirements.txt`

### 1. Configuração do Banco de Dados PostgreSQL

É necessário criar um banco de dados e um usuário específico para esta aplicação no PostgreSQL.

1.  Abra o seu terminal de linha de comando do PostgreSQL (`psql`).
2.  Execute os seguintes comandos SQL para criar o usuário e o banco de dados:

    ```sql
    -- Crie um novo usuário (role) com a senha especificada
    CREATE USER bd_trab_user WITH PASSWORD 'password';

    -- Crie o banco de dados
    CREATE DATABASE bd_trab OWNER bd_trab_user;

    -- Dê ao novo usuário todas as permissões no novo banco de dados para confirmar.
    GRANT ALL PRIVILEGES ON DATABASE bd_trab TO bd_trab_user;
    ```

### 2. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 3. Criação das Tabelas do Banco

O script `create_db.py` lê o arquivo `init.sql` e cria todas as tabelas necessárias no banco de dados que você acabou de configurar. Em seguida, popula com os dados presente no arquivo `populate.sql`. 

Execute o seguinte comando no terminal, na raiz do projeto:

```bash
python3 create_db.py
```

### 4. Executando a Aplicação

Execute o seguinte comando:

```bash
python3 run.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.
