# Implementação de Consultas SQL Puras

Este documento detalha as consultas SQL puras implementadas no sistema, conforme solicitado pelos requisitos do trabalho de banco de dados.

As consultas foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade.

---
## Consultas Utilizadas nas Rotas Atuais
---

### 1. Consulta Simples: Listar Todas as Pessoas

*   **Onde:** No arquivo `app/routes.py`, dentro da função `pessoas()` que atende a rota `/pessoas`. A consulta em si está em `app/sql/select_all_pessoas.sql`.
*   **O que:** A consulta seleciona todos os registros da tabela `pessoa` e os ordena pelo nome.
*   **Como:**
    ```python
    # app/routes.py
    sql_query = get_sql_from_file('select_all_pessoas.sql')
    result = db.session.execute(text(sql_query))
    all_pessoas = result.mappings().all()
    ```
    ```sql
    -- app/sql/select_all_pessoas.sql
    SELECT * FROM pessoa ORDER BY nome;
    ```

---

### 2. Consulta com Parâmetro: Buscar Pessoa por CPF

*   **Onde:** No arquivo `app/routes.py`, dentro da função `assign_role()` que atende a rota `/assign_role`. A consulta está em `app/sql/select_pessoa_by_cpf.sql`.
*   **O que:** Busca no banco de dados o registro da pessoa com o CPF correspondente.
*   **Como:**
    ```python
    # app/routes.py
    sql_query = get_sql_from_file('select_pessoa_by_cpf.sql')
    result = db.session.execute(text(sql_query), {'cpf': search_cpf}).first()
    pessoa = result if result else None
    ```
    ```sql
    -- app/sql/select_pessoa_by_cpf.sql
    SELECT * FROM pessoa WHERE cpf = :cpf;
    ```

---

### 3. Consulta Simples: Listar Todos os Cursos

*   **Onde:** No arquivo `app/routes.py`, dentro da função `cursos()` que atende a rota `/cursos`. A consulta está em `app/sql/select_all_cursos.sql`.
*   **O que:** A consulta seleciona todos os cursos cadastrados para exibi-los na página.
*   **Como:**
    ```python
    # app/routes.py
    sql_query = get_sql_from_file('select_all_cursos.sql')
    result = db.session.execute(text(sql_query))
    all_cursos = result.mappings().all()
    ```
    ```sql
    -- app/sql/select_all_cursos.sql
    SELECT * FROM curso ORDER BY nome;
    ```

---

### 4. Consulta Complexa: Listar Alunos por Curso (JOIN)

*   **Onde:** Na rota `/curso/<int:codigo_curso>` (`alunos_por_curso()`) em `app/routes.py`. A consulta está em `app/sql/select_alunos_by_curso.sql`.
*   **O que:** Busca o nome e a matrícula de todos os alunos inscritos em um curso específico, juntando as tabelas `pessoa`, `aluno` e `matriculadoem`.
*   **Como:**
    ```python
    # app/routes.py
    sql_alunos_query = get_sql_from_file('select_alunos_by_curso.sql')
    result_alunos = db.session.execute(text(sql_alunos_query), {'codigo': codigo_curso})
    alunos = result_alunos.mappings().all()
    ```
    ```sql
    -- app/sql/select_alunos_by_curso.sql
    SELECT p.nome, a.matricula
    FROM pessoa p
    JOIN aluno a ON p.cpf = a.cpf
    JOIN matriculadoem m ON a.cpf = m.cpf
    WHERE m.codigo = :codigo
    ORDER BY p.nome;
    ```
---

### 5. Consulta Complexa: Relatório Geral de PCDs (JOIN e CASE)

*   **Onde:** Na rota `/relatorio/pcd` (`relatorio_pcd()`) em `app/routes.py`. A consulta está em `app/sql/relatorio_geral_pcd.sql`.
*   **O que:** Gera um relatório de todas as pessoas com deficiência (PCD), buscando o nome e o papel principal (Aluno, Docente, etc.) de cada uma.
*   **Como:** A consulta utiliza múltiplos `LEFT JOIN`s para conectar a tabela `pcd` com a tabela `pessoa` através dos diferentes papéis que uma pessoa pode ter. A cláusula `CASE` é usada para identificar e exibir o papel.
    ```python
    # app/routes.py
    @app.route('/relatorio/pcd')
    def relatorio_pcd():
        sql_query = get_sql_from_file('relatorio_geral_pcd.sql')
        result = db.session.execute(text(sql_query))
        pcds = result.mappings().all()
        return render_template('relatorio_pcd.html', pcds=pcds)
    ```
    ```sql
    -- app/sql/relatorio_geral_pcd.sql
    SELECT
        p.cpf,
        p.nome,
        pcd.id_pcd,
        CASE
            WHEN a.cpf IS NOT NULL THEN 'Aluno'
            WHEN d.cpf IS NOT NULL THEN 'Docente'
            WHEN t.cpf IS NOT NULL THEN 'Técnico Administrativo'
            ELSE 'Não especificado'
        END AS papel
    FROM pcd
    LEFT JOIN aluno a ON pcd.id_pcd = a.id_pcd
    LEFT JOIN docente d ON pcd.id_pcd = d.id_pcd
    LEFT JOIN tecnicoadministrativo t ON pcd.id_pcd = t.id_pcd
    LEFT JOIN pessoa p ON p.cpf = a.cpf OR p.cpf = d.cpf OR p.cpf = t.cpf
    WHERE p.cpf IS NOT NULL
    ORDER BY p.nome;
    ```

---
## Exemplos Adicionais de Consultas Complexas (Ainda não utilizadas)
---

As seguintes consultas foram criadas e estão disponíveis na pasta `app/sql/` para uso futuro em novas funcionalidades de relatórios.

*   `relatorio_atendimentos_por_membro.sql`
*   `relatorio_recursos_por_categoria.sql`
*   `perfil_alunos_pcd.sql`
*   `materiais_por_bolsista.sql`
