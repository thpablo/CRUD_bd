# Implementação de Consultas SQL Puras

Este documento detalha as 4 consultas SQL puras implementadas no sistema, conforme solicitado pelos requisitos do trabalho de banco de dados.

---

### 1. Consulta Simples: Listar Todas as Pessoas

*   **Onde:** No arquivo `app/routes.py`, dentro da função `pessoas()` que atende a rota `/pessoas`.
*   **O que:** A consulta seleciona todos os registros da tabela `pessoa` e os ordena pelo nome. O resultado é usado para exibir a lista de todas as pessoas cadastradas no sistema.
*   **Como:** A chamada ao ORM (`Pessoa.query.all()`) foi substituída pelo seguinte código:
    ```python
    from sqlalchemy import text

    @app.route('/pessoas')
    def pessoas():
        sql = text("SELECT * FROM pessoa ORDER BY nome")
        result = db.session.execute(sql)
        all_pessoas = result.mappings().all()
        return render_template('pessoas.html', pessoas=all_pessoas)
    ```

---

### 2. Consulta com Parâmetro: Buscar Pessoa por CPF

*   **Onde:** No arquivo `app/routes.py`, dentro da função `assign_role()` que atende a rota `/assign_role`.
*   **O que:** Quando um CPF é pesquisado na tela "Atribuir Papel", esta consulta busca no banco de dados o registro da pessoa com o CPF correspondente.
*   **Como:** A busca pelo ORM (`Pessoa.query.get()`) foi substituída por uma consulta SQL pura com um parâmetro nomeado (`:cpf`) para prevenir SQL Injection:
    ```python
    @app.route('/assign_role', methods=['GET', 'POST'])
    def assign_role():
        # ... (dentro da lógica do GET)
        search_cpf = request.args.get('search_cpf')
        if search_cpf:
            # ... (validação do CPF)
            sql = text("SELECT * FROM pessoa WHERE cpf = :cpf")
            result = db.session.execute(sql, {'cpf': search_cpf}).first()
            pessoa = result.mappings() if result else None
            # ...
    ```

---

### 3. Consulta Simples: Listar Todos os Cursos

*   **Onde:** No arquivo `app/routes.py`, dentro da função `cursos()` que atende a rota `/cursos`.
*   **O que:** A consulta seleciona todos os cursos cadastrados para exibi-los na página de cursos.
*   **Como:** A chamada ao ORM (`Curso.query.all()`) foi substituída pelo seguinte código:
    ```python
    @app.route('/cursos', methods=['GET', 'POST'])
    def cursos():
        # ... (lógica do POST)
        sql = text("SELECT * FROM curso ORDER BY nome")
        result = db.session.execute(sql)
        all_cursos = result.mappings().all()
        return render_template('cursos.html', cursos=all_cursos)
    ```

---

### 4. Consulta Complexa: Listar Alunos por Curso (JOIN)

*   **Onde:** Em uma nova rota `/curso/<int:codigo_curso>` implementada no arquivo `app/routes.py`, na função `alunos_por_curso()`.
*   **O que:** Esta consulta é um exemplo mais avançado que busca o nome e a matrícula de todos os alunos inscritos em um curso específico. Ela realiza a junção (`JOIN`) de três tabelas: `pessoa`, `aluno` e `matriculadoem`.
*   **Como:** A consulta é executada quando o usuário clica no nome de um curso na lista. O código implementado é:
    ```python
    @app.route('/curso/<int:codigo_curso>')
    def alunos_por_curso(codigo_curso):
        # ... (busca detalhes do curso)
        sql_alunos = text("""
            SELECT p.nome, a.matricula
            FROM pessoa p
            JOIN aluno a ON p.cpf = a.cpf
            JOIN matriculadoem m ON a.cpf = m.cpf
            WHERE m.codigo = :codigo
            ORDER BY p.nome
        """)
        result_alunos = db.session.execute(sql_alunos, {'codigo': codigo_curso})
        alunos = result_alunos.mappings().all()
        return render_template('alunos_por_curso.html', curso=curso, alunos=alunos)
    ```
