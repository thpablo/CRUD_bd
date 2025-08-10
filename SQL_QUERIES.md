# Implementação de Consultas SQL Puras

Este documento detalha as consultas SQL puras implementadas no sistema, conforme solicitado pelos requisitos do trabalho de banco de dados.

As consultas foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade.

---
## Consultas Utilizadas nas Rotas Atuais
---

### 1. Consulta Simples: Listar Todas as Pessoas

*   **Onde:** `app/routes.py`, rota `/pessoas`. Arquivo: `app/sql/select_all_pessoas.sql`.
*   **O que:** Seleciona todos os registros da tabela `pessoa` e os ordena pelo nome.
*   **Como:**
    ```python
    sql_query = get_sql_from_file('select_all_pessoas.sql')
    result = db.session.execute(text(sql_query))
    ```

---

### 2. Consulta com Parâmetro: Buscar Pessoa por CPF

*   **Onde:** `app/routes.py`, rota `/assign_role`. Arquivo: `app/sql/select_pessoa_by_cpf.sql`.
*   **O que:** Busca o registro da pessoa com o CPF correspondente.
*   **Como:**
    ```python
    sql_query = get_sql_from_file('select_pessoa_by_cpf.sql')
    result = db.session.execute(text(sql_query), {'cpf': search_cpf}).first()
    ```

---

### 3. Consulta Simples: Listar Todos os Cursos

*   **Onde:** `app/routes.py`, rota `/cursos`. Arquivo: `app/sql/select_all_cursos.sql`.
*   **O que:** Seleciona todos os cursos cadastrados para exibi-los na página.
*   **Como:**
    ```python
    sql_query = get_sql_from_file('select_all_cursos.sql')
    result = db.session.execute(text(sql_query))
    ```

---

### 4. Consulta Complexa: Listar Alunos por Curso (JOIN)

*   **Onde:** `app/routes.py`, rota `/curso/<int:codigo_curso>`. Arquivo: `app/sql/select_alunos_by_curso.sql`.
*   **O que:** Busca o nome e a matrícula de todos os alunos inscritos em um curso específico.
*   **Como:**
    ```python
    sql_alunos_query = get_sql_from_file('select_alunos_by_curso.sql')
    result_alunos = db.session.execute(text(sql_alunos_query), {'codigo': codigo_curso})
    ```
    ```sql
    -- app/sql/select_alunos_by_curso.sql
    SELECT p.nome, a.matricula FROM pessoa p JOIN aluno a ON p.cpf = a.cpf JOIN matriculadoem m ON a.cpf = m.cpf WHERE m.codigo = :codigo ORDER BY p.nome;
    ```

---

### 5. Consulta Complexa: Relatório Geral de PCDs (JOIN e CASE)

*   **Onde:** `app/routes.py`, rota `/relatorio/pcd`. Arquivo: `app/sql/relatorio_geral_pcd.sql`.
*   **O que:** Gera um relatório de todas as pessoas com deficiência, buscando o nome e o papel principal de cada uma.
*   **Como:**
    ```python
    sql_query = get_sql_from_file('relatorio_geral_pcd.sql')
    result = db.session.execute(text(sql_query))
    ```
    ```sql
    -- app/sql/relatorio_geral_pcd.sql
    -- (Query com UNION para buscar Alunos, Docentes e Técnicos PCD)
    SELECT p.cpf, p.nome, pcd.id_pcd, 'Aluno' AS papel FROM ...
    UNION
    SELECT p.cpf, p.nome, pcd.id_pcd, 'Docente' AS papel FROM ...
    UNION
    SELECT p.cpf, p.nome, pcd.id_pcd, 'Técnico Administrativo' AS papel FROM ...
    ```

---

### 6. Consulta Detalhada de Alunos (JOIN)

*   **Onde:** `app/routes.py`, rota `/equipe`. Arquivo: `app/sql/select_all_alunos_info.sql`.
*   **O que:** Obtém uma lista detalhada de todos os alunos, incluindo o nome do curso em que estão matriculados.
*   **Como:**
    ```sql
    -- app/sql/select_all_alunos_info.sql
    SELECT p.cpf, p.nome, a.matricula, c.nome AS nome_curso FROM pessoa p JOIN aluno a ON p.cpf = a.cpf LEFT JOIN matriculadoem m ON a.cpf = m.cpf LEFT JOIN curso c ON m.codigo = c.codigo ORDER BY p.nome;
    ```

---

### 7. Consulta de Membros da Equipe (UNION)

*   **Onde:** `app/routes.py`, rota `/equipe`. Arquivo: `app/sql/select_all_membros_equipe_info.sql`.
*   **O que:** Gera uma lista unificada de todos os membros da equipe da CAIN, independentemente de serem Alunos, Técnicos ou Terceirizados.
*   **Como:**
    ```sql
    -- app/sql/select_all_membros_equipe_info.sql
    -- (Query com UNION para buscar Alunos, Técnicos e Terceirizados que são membros)
    SELECT p.cpf, p.nome, 'Aluno' AS papel_principal, m.id_membro, m.regimedetrabalho, m.categoria FROM ...
    UNION
    SELECT p.cpf, p.nome, 'Técnico Administrativo' AS papel_principal, m.id_membro, m.regimedetrabalho, m.categoria FROM ...
    UNION
    SELECT p.cpf, p.nome, 'Terceirizado' AS papel_principal, m.id_membro, m.regimedetrabalho, m.categoria FROM ...
    ```
---

### 8. Consulta Detalhada de Bolsistas (JOIN e CASE)

*   **Onde:** `app/routes.py`, rota `/equipe`. Arquivo: `app/sql/select_all_bolsistas_info.sql`.
*   **O que:** Obtém uma lista detalhada de todos os bolsistas, incluindo informações pessoais, do curso e detalhes da bolsa (salário, tipo, etc.).
*   **Como:**
    ```sql
    -- app/sql/select_all_bolsistas_info.sql
    SELECT p.nome, p.cpf, a.matricula, c.nome AS nome_curso, b.salario, b.cargahoraria, CASE WHEN bi.id_bolsista IS NOT NULL THEN 'Inclusão' WHEN bp.id_bolsista IS NOT NULL THEN 'Produção' ELSE 'Não especificado' END AS tipo_bolsa FROM pessoa p JOIN aluno a ON p.cpf = a.cpf JOIN membrodaequipe m ON a.id_membro = m.id_membro JOIN bolsista b ON m.id_membro = b.id_bolsista LEFT JOIN bolsistainclusao bi ON b.id_bolsista = bi.id_bolsista LEFT JOIN bolsistaproducao bp ON b.id_bolsista = bp.id_bolsista LEFT JOIN matriculadoem ma ON p.cpf = ma.cpf LEFT JOIN curso c ON ma.codigo = c.codigo ORDER BY p.nome;
    ```

---
## Exemplos Adicionais de Consultas Complexas (Ainda não utilizadas)
---

As seguintes consultas foram criadas e estão disponíveis na pasta `app/sql/` para uso futuro em novas funcionalidades de relatórios.

*   `relatorio_atendimentos_por_membro.sql`
*   `relatorio_recursos_por_categoria.sql`
*   `perfil_alunos_pcd.sql`
*   `materiais_por_bolsista.sql`
