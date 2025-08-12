# Documentação das Queries e Operações SQL

Este documento detalha as consultas e operações SQL puras implementadas no sistema, conforme solicitado pelos requisitos do projeto. As queries foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade.

---
## 1. Consultas (SELECT)
---

### `select_all_pessoas.sql`
- **Onde:** Rota `/pessoas` (quando não há busca).
- **O que:** Seleciona todos os registros da tabela `Pessoa` para exibir a lista principal de pessoas.
- **SQL:**
  ```sql
  SELECT * FROM pessoa ORDER BY nome;
  ```

### `search_pessoas.sql`
- **Onde:** Rota `/pessoas` (com parâmetro de busca `q`).
- **O que:** Filtra os registros da tabela `Pessoa` onde o nome (case-insensitive) ou CPF correspondem ao termo de busca.
- **SQL:**
  ```sql
  SELECT cpf, nome FROM Pessoa WHERE nome ILIKE :query OR cpf LIKE :query ORDER BY nome;
  ```

### `select_all_cursos.sql`
- **Onde:** Rota `/cursos`.
- **O que:** Seleciona todos os cursos cadastrados para exibi-los na página de cursos.
- **SQL:**
  ```sql
  SELECT * FROM curso ORDER BY nome;
  ```

### `select_alunos_by_curso.sql`
- **Onde:** Rota `/curso/<codigo_curso>`.
- **O que:** Utiliza `JOIN` para buscar o nome e a matrícula de todos os alunos inscritos em um curso específico.
- **SQL:**
  ```sql
  SELECT p.nome, a.matricula
  FROM pessoa p
  JOIN aluno a ON p.cpf = a.cpf
  JOIN matriculadoem m ON a.cpf = m.cpf
  WHERE m.codigo = :codigo
  ORDER BY p.nome;
  ```

### `select_all_alunos_info.sql`
- **Onde:** Rota `/equipe`.
- **O que:** Busca uma lista detalhada de todos os alunos, incluindo o nome do curso em que estão matriculados.
- **SQL:**
  ```sql
  SELECT
      p.cpf,
      p.nome,
      a.matricula,
      c.nome AS nome_curso
  FROM pessoa p
  JOIN aluno a ON p.cpf = a.cpf
  LEFT JOIN matriculadoem m ON a.cpf = m.cpf
  LEFT JOIN curso c ON m.codigo = c.codigo
  ORDER BY p.nome;
  ```

### `select_all_membros_equipe_info.sql`
- **Onde:** Rota `/equipe`.
- **O que:** Gera uma lista unificada de todos os membros da equipe CAIN, usando `UNION` para juntar os resultados de Alunos, Técnicos e Terceirizados que são membros.
- **SQL:**
  ```sql
  -- Membros que são Alunos
  SELECT p.cpf, p.nome, 'Aluno' AS papel_principal, m.id_membro, m.regimedetrabalho
  FROM pessoa p JOIN aluno a ON p.cpf = a.cpf JOIN membrodaequipe m ON a.id_membro = m.id_membro
  UNION
  -- Membros que são Técnicos Administrativos
  SELECT p.cpf, p.nome, 'Técnico Administrativo' AS papel_principal, m.id_membro, m.regimedetrabalho
  FROM pessoa p JOIN servidor s ON p.cpf = s.cpf JOIN tecnicoadministrativo t ON s.cpf = t.cpf JOIN membrodaequipe m ON t.id_membro = m.id_membro
  UNION
  -- Membros que são Terceirizados
  SELECT p.cpf, p.nome, 'Terceirizado' AS papel_principal, m.id_membro, m.regimedetrabalho
  FROM pessoa p JOIN servidor s ON p.cpf = s.cpf JOIN terceirizado t ON s.cpf = t.cpf JOIN membrodaequipe m ON t.id_membro = m.id_membro
  ORDER BY nome;
  ```

### `select_all_servidores_info.sql`
- **Onde:** Rota `/equipe`.
- **O que:** Retorna uma lista detalhada de todos os servidores, incluindo seu tipo de contrato, departamento, papel específico (Docente, Técnico, etc.), SIAPE e cargo.
- **SQL:**
  ```sql
  SELECT
      p.cpf, p.nome, s.tipodecontrato, dep.nome AS nome_departamento,
      CASE
          WHEN d.cpf IS NOT NULL THEN 'Docente'
          WHEN ta.cpf IS NOT NULL THEN 'Técnico Administrativo'
          WHEN tz.cpf IS NOT NULL THEN 'Terceirizado'
          ELSE 'Não especificado'
      END AS papel_especifico,
      COALESCE(d.siape, ta.siape) AS siape,
      c.nome AS nome_cargo
  FROM Pessoa p
  JOIN Servidor s ON p.cpf = s.cpf
  LEFT JOIN DepartamentoSetor dep ON s.codigodepartamentosetor = dep.codigo
  LEFT JOIN Docente d ON s.cpf = d.cpf
  LEFT JOIN TecnicoAdministrativo ta ON s.cpf = ta.cpf
  LEFT JOIN Terceirizado tz ON s.cpf = tz.cpf
  LEFT JOIN Cargo c ON ta.id_cargo = c.id_cargo OR tz.id_cargo = c.id_cargo
  ORDER BY p.nome;
  ```

### `select_all_bolsistas_info.sql`
- **Onde:** Rota `/equipe`.
- **O que:** Retorna uma lista detalhada de todos os bolsistas, usando `JOIN` e `CASE` para determinar o tipo da bolsa.
- **SQL:**
  ```sql
  SELECT
      p.nome, p.cpf, a.matricula, c.nome AS nome_curso, b.salario, b.cargahoraria,
      CASE
          WHEN bi.id_bolsista IS NOT NULL THEN 'Inclusão'
          WHEN bp.id_bolsista IS NOT NULL THEN 'Produção'
          ELSE 'Não especificado'
      END AS tipo_bolsa
  FROM pessoa p
  JOIN aluno a ON p.cpf = a.cpf
  JOIN membrodaequipe m ON a.id_membro = m.id_membro
  JOIN bolsista b ON m.id_membro = b.id_bolsista
  LEFT JOIN bolsistainclusao bi ON b.id_bolsista = bi.id_bolsista
  LEFT JOIN bolsistaproducao bp ON b.id_bolsista = bp.id_bolsista
  LEFT JOIN matriculadoem ma ON p.cpf = ma.cpf
  LEFT JOIN curso c ON ma.codigo = c.codigo
  ORDER BY p.nome;
  ```

### `relatorio_geral_pcd.sql`
- **Onde:** Rota `/relatorio/pcd`.
- **O que:** Gera um relatório de todas as pessoas com deficiência (PCD), identificando seu papel principal através de `UNION`.
- **SQL:**
  ```sql
  -- Alunos que são PCD
  SELECT p.cpf, p.nome, pcd.id_pcd, 'Aluno' AS papel
  FROM pessoa p JOIN aluno a ON p.cpf = a.cpf JOIN pcd ON a.id_pcd = pcd.id_pcd
  UNION
  -- Docentes que são PCD
  SELECT p.cpf, p.nome, pcd.id_pcd, 'Docente' AS papel
  FROM pessoa p JOIN servidor s ON p.cpf = s.cpf JOIN docente d ON s.cpf = d.cpf JOIN pcd ON d.id_pcd = pcd.id_pcd
  UNION
  -- Técnicos que são PCD
  SELECT p.cpf, p.nome, pcd.id_pcd, 'Técnico Administrativo' AS papel
  FROM pessoa p JOIN servidor s ON p.cpf = s.cpf JOIN tecnicoadministrativo t ON s.cpf = t.cpf JOIN pcd ON t.id_pcd = pcd.id_pcd
  ORDER BY nome;
  ```

### `select_person_details_for_role_assignment.sql`
- **Onde:** Rota `/assign_role`.
- **O que:** Busca todos os detalhes de uma pessoa por CPF para verificar seus papéis atuais antes de uma nova atribuição.
- **SQL:**
  ```sql
  SELECT
      p.cpf, p.nome, a.cpf IS NOT NULL AS is_aluno, s.cpf IS NOT NULL AS is_servidor,
      CASE
          WHEN d.cpf IS NOT NULL THEN 'Docente'
          WHEN ta.cpf IS NOT NULL THEN 'Técnico Administrativo'
          WHEN tz.cpf IS NOT NULL THEN 'Terceirizado'
          ELSE NULL
      END AS servidor_tipo,
      (a.id_membro IS NOT NULL OR ta.id_membro IS NOT NULL OR tz.id_membro IS NOT NULL) AS is_membro_cain
  FROM Pessoa p
  LEFT JOIN Aluno a ON p.cpf = a.cpf
  LEFT JOIN Servidor s ON p.cpf = s.cpf
  LEFT JOIN Docente d ON s.cpf = d.cpf
  LEFT JOIN TecnicoAdministrativo ta ON s.cpf = ta.cpf
  LEFT JOIN Terceirizado tz ON s.cpf = tz.cpf
  WHERE p.cpf = :cpf;
  ```

### `report_pcd_students_by_assistance.sql`
- **Onde:** Rota `/relatorios/alunos_assistidos`.
- **O que:** Gera um relatório de alunos PCD de um curso específico que receberam assistência de um tipo específico de bolsista.
- **SQL:**
  ```sql
  SELECT DISTINCT
      p.Nome AS NomeAluno, p.CPF, c.Nome AS NomeCurso,
      CASE
          WHEN bi.ID_BOLSISTA IS NOT NULL THEN 'Inclusão'
          WHEN bp.ID_BOLSISTA IS NOT NULL THEN 'Produção'
          ELSE 'Outro'
      END AS TipoBolsista
  FROM Aluno a
  JOIN Pessoa p ON a.CPF = p.CPF
  JOIN MatriculadoEm me ON a.CPF = me.CPF
  JOIN Curso c ON me.Codigo = c.CODIGO
  JOIN PrestaAssistencia pa ON a.ID_PCD = pa.ID_PCD
  JOIN MembroDaEquipe m ON pa.ID_MEMBRO_CAIN = m.ID_MEMBRO
  JOIN Bolsista b ON m.ID_MEMBRO = b.ID_BOLSISTA
  LEFT JOIN BolsistaInclusao bi ON b.ID_BOLSISTA = bi.ID_BOLSISTA
  LEFT JOIN BolsistaProducao bp ON b.ID_BOLSISTA = bp.ID_BOLSISTA
  WHERE a.ID_PCD IS NOT NULL
    AND c.CODIGO = :codigo_curso
    AND (
        (:tipo_bolsista = 'inclusao' AND bi.ID_BOLSISTA IS NOT NULL)
        OR
        (:tipo_bolsista = 'producao' AND bp.ID_BOLSISTA IS NOT NULL)
    )
  ORDER BY p.Nome;
  ```

---
## 2. Operações de Atualização (UPDATE)
---

### `update_person_nome.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Altera o nome de uma pessoa com base no seu CPF.
- **SQL:** `UPDATE Pessoa SET nome = :nome WHERE cpf = :cpf;`

### `update_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Altera o nome social de uma pessoa na tabela `PessoaLGBT`.
- **SQL:** `UPDATE PessoaLGBT SET nomesocial = :nomesocial WHERE cpf = :cpf;`

---
## 3. Operações de Deleção (DELETE)
---

### `delete_person.sql`
- **Onde:** Rota `/pessoa/delete/<cpf>`.
- **O que:** Remove um registro da tabela `Pessoa`.
- **SQL:** `DELETE FROM Pessoa WHERE cpf = :cpf;`

### `delete_person_emails.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Remove todos os e-mails associados a um CPF.
- **SQL:** `DELETE FROM ContatoEmails WHERE cpf = :cpf;`

### `delete_person_telefones.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Remove todos os telefones associados a um CPF.
- **SQL:** `DELETE FROM ContatoTelefones WHERE cpf = :cpf;`

### `delete_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Remove o registro de nome social de uma pessoa.
- **SQL:** `DELETE FROM PessoaLGBT WHERE cpf = :cpf;`

---
## 4. Operações de Inserção (INSERT)
---

### `insert_person_email.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Insere um novo registro de e-mail para uma pessoa.
- **SQL:** `INSERT INTO ContatoEmails (cpf, email) VALUES (:cpf, :email);`

### `insert_person_telefone.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Insere um novo registro de telefone para uma pessoa.
- **SQL:** `INSERT INTO ContatoTelefones (cpf, telefone) VALUES (:cpf, :telefone);`

### `insert_pessoa_lgbt.sql`
- **Onde:** Rota `/pessoa/edit/<cpf>`.
- **O que:** Insere um novo registro de nome social para uma pessoa.
- **SQL:** `INSERT INTO PessoaLGBT (cpf, nomesocial) VALUES (:cpf, :nomesocial);`
