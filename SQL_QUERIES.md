# Implementação de Consultas SQL Puras

Este documento detalha as 4 consultas SQL puras implementadas no sistema, conforme solicitado pelos requisitos do trabalho de banco de dados.

As consultas foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade. Elas são carregadas e executadas no `app/routes.py` através de uma função auxiliar.

---

### 1. Consulta Simples: Listar Todas as Pessoas

*   **Onde:** No arquivo `app/routes.py`, dentro da função `pessoas()` que atende a rota `/pessoas`. A consulta em si está em `app/sql/select_all_pessoas.sql`.
*   **O que:** A consulta seleciona todos os registros da tabela `pessoa` e os ordena pelo nome. O resultado é usado para exibir a lista de todas as pessoas cadastradas no sistema.
*   **Como:** O código na rota agora carrega o SQL do arquivo e o executa:
    ```python
    # app/routes.py
    @app.route('/pessoas')
    def pessoas():
        sql_query = get_sql_from_file('select_all_pessoas.sql')
        result = db.session.execute(text(sql_query))
        all_pessoas = result.mappings().all()
        return render_template('pessoas.html', pessoas=all_pessoas)

    # app/sql/select_all_pessoas.sql
    SELECT * FROM pessoa ORDER BY nome;
    ```

---

### 2. Consulta com Parâmetro: Buscar Pessoa por CPF

*   **Onde:** No arquivo `app/routes.py`, dentro da função `assign_role()` que atende a rota `/assign_role`. A consulta está em `app/sql/select_pessoa_by_cpf.sql`.
*   **O que:** Quando um CPF é pesquisado na tela "Atribuir Papel", esta consulta busca no banco de dados o registro da pessoa com o CPF correspondente.
*   **Como:** A rota carrega o SQL do arquivo e passa o parâmetro `:cpf` de forma segura:
    ```python
    # app/routes.py
    @app.route('/assign_role', methods=['GET', 'POST'])
    def assign_role():
        # ... (lógica do GET)
        sql_query = get_sql_from_file('select_pessoa_by_cpf.sql')
        result = db.session.execute(text(sql_query), {'cpf': search_cpf}).first()
        pessoa = result.mappings() if result else None
        # ...

    # app/sql/select_pessoa_by_cpf.sql
    SELECT * FROM pessoa WHERE cpf = :cpf;
    ```

---

### 3. Consulta Simples: Listar Todos os Cursos

*   **Onde:** No arquivo `app/routes.py`, dentro da função `cursos()` que atende a rota `/cursos`. A consulta está em `app/sql/select_all_cursos.sql`.
*   **O que:** A consulta seleciona todos os cursos cadastrados para exibi-los na página de cursos.
*   **Como:** A rota carrega o SQL do arquivo:
    ```python
    # app/routes.py
    @app.route('/cursos', methods=['GET', 'POST'])
    def cursos():
        # ... (lógica do POST)
        sql_query = get_sql_from_file('select_all_cursos.sql')
        result = db.session.execute(text(sql_query))
        all_cursos = result.mappings().all()
        return render_template('cursos.html', cursos=all_cursos)

    # app/sql/select_all_cursos.sql
    SELECT * FROM curso ORDER BY nome;
    ```

---

### 4. Consulta Complexa: Listar Alunos por Curso (JOIN)

*   **Onde:** Na rota `/curso/<int:codigo_curso>` (`alunos_por_curso()`) em `app/routes.py`. A consulta está em `app/sql/select_alunos_by_curso.sql`.
*   **O que:** Busca o nome e a matrícula de todos os alunos inscritos em um curso específico, juntando as tabelas `pessoa`, `aluno` e `matriculadoem`.
*   **Como:** A rota carrega a consulta complexa do arquivo e a executa com o código do curso como parâmetro:
    ```python
    # app/routes.py
    @app.route('/curso/<int:codigo_curso>')
    def alunos_por_curso(codigo_curso):
        # ... (busca detalhes do curso)
        sql_alunos_query = get_sql_from_file('select_alunos_by_curso.sql')
        result_alunos = db.session.execute(text(sql_alunos_query), {'codigo': codigo_curso})
        alunos = result_alunos.mappings().all()
        return render_template('alunos_por_curso.html', curso=curso, alunos=alunos)

    # app/sql/select_alunos_by_curso.sql
    SELECT p.nome, a.matricula
    FROM pessoa p
    JOIN aluno a ON p.cpf = a.cpf
    JOIN matriculadoem m ON a.cpf = m.cpf
    WHERE m.codigo = :codigo
    ORDER BY p.nome;
    ```
