# Documentação das Queries SQL

Este documento detalha as consultas e operações SQL puras implementadas no sistema, conforme solicitado pelos requisitos do projeto. As queries foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade.

---
## 1. Consultas (SELECT)
---

### `select_all_pessoas.sql`
- **Onde:** Rota `/pessoas`
- **O que:** Seleciona o CPF e o nome de todos os registros da tabela `Pessoa`, ordenando pelo nome. É usada para exibir a lista principal de pessoas.

### `select_all_cursos.sql`
- **Onde:** Rota `/cursos`
- **O que:** Seleciona todos os cursos cadastrados. Usada para exibir a lista de cursos.

### `select_alunos_by_curso.sql`
- **Onde:** Rota `/curso/<codigo_curso>`
- **O que:** Utiliza `JOIN` para buscar o nome e a matrícula de todos os alunos inscritos em um curso específico, passando o código do curso como parâmetro.

### `select_all_alunos_info.sql`
- **Onde:** Rota `/equipe`
- **O que:** Busca uma lista detalhada de todos os alunos, incluindo o nome do curso em que estão matriculados, utilizando `LEFT JOIN`.

### `select_all_membros_equipe_info.sql`
- **Onde:** Rota `/equipe`
- **O que:** Gera uma lista unificada de todos os membros da equipe CAIN, usando `UNION` para juntar os resultados de Alunos, Técnicos e Terceirizados que são membros.

### `select_all_bolsistas_info.sql`
- **Onde:** Rota `/equipe`
- **O que:** Retorna uma lista detalhada de todos os bolsistas, usando `JOIN` e `CASE` para determinar o tipo da bolsa (Inclusão ou Produção) e buscar informações pessoais e do curso.

### `relatorio_geral_pcd.sql`
- **Onde:** Rota `/relatorio/pcd`
- **O que:** Gera um relatório de todas as pessoas com deficiência (PCD), identificando seu papel principal (Aluno, Docente, etc.) através de `UNION`.

### `select_person_details_for_role_assignment.sql`
- **Onde:** Rota `/assign_role`
- **O que:** Consulta complexa com múltiplos `LEFT JOIN` e `CASE` para buscar todos os detalhes de uma pessoa por CPF. Verifica se a pessoa é aluna, servidora, o tipo de servidora e se é membro da equipe CAIN. Usada para exibir os papéis atuais de uma pessoa antes de atribuir um novo.

---
## 2. Operações de Atualização (UPDATE)
---

### `update_person_nome.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Executa um `UPDATE` para alterar o nome de uma pessoa com base no seu CPF.

### `update_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Executa um `UPDATE` para alterar o nome social de uma pessoa na tabela `PessoaLGBT`.

---
## 3. Operações de Deleção (DELETE)
---

### `delete_person.sql`
- **Onde:** Rota `/pessoa/delete/<cpf>`
- **O que:** Executa um `DELETE` para remover um registro da tabela `Pessoa`. A operação é restrita pelo banco de dados se a pessoa tiver papéis associados (aluno, servidor).

### `delete_person_emails.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Remove todos os e-mails associados a um CPF na tabela `ContatoEmails`. Usado como parte da estratégia "delete-then-insert" na página de edição.

### `delete_person_telefones.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Remove todos os telefones associados a um CPF na tabela `ContatoTelefones`.

### `delete_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Remove o registro de nome social de uma pessoa da tabela `PessoaLGBT`, caso o campo seja deixado em branco no formulário de edição.

---
## 4. Operações de Inserção (INSERT)
---

### `insert_person_email.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Insere um novo registro de e-mail para uma pessoa na tabela `ContatoEmails`.

### `insert_person_telefone.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Insere um novo registro de telefone para uma pessoa na tabela `ContatoTelefones`.

### `insert_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`
- **O que:** Insere um novo registro de nome social para uma pessoa na tabela `PessoaLGBT`.
