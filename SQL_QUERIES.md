# Implementação de Consultas SQL Puras

Este documento detalha as consultas SQL puras implementadas no sistema, conforme solicitado pelos requisitos do trabalho de banco de dados.

As consultas foram externalizadas para arquivos `.sql` individuais na pasta `app/sql/` para melhor organização e manutenibilidade.

---
## Consultas Utilizadas nas Rotas Atuais
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
        # ... (dentro da lógica do GET)
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
---
## Exemplos Adicionais de Consultas Complexas
---

As seguintes consultas foram criadas e estão disponíveis na pasta `app/sql/` para uso futuro em novas funcionalidades de relatórios.

### 5. Relatório de Atendimentos por Membro da Equipe

*   **Onde:** `app/sql/relatorio_atendimentos_por_membro.sql`
*   **O que:** Conta quantos atendimentos (`PrestaAssistencia`) cada membro da equipe realizou. É útil para gerar relatórios sobre a produtividade da equipe. A complexidade está em obter o nome do membro, que exige múltiplos `LEFT JOIN`s e `COALESCE` para unificar os resultados de Alunos, Técnicos e Terceirizados.
*   **Como:**
    ```sql
    SELECT
        m.id_membro,
        COALESCE(p_aluno.nome, p_servidor.nome) AS nome_membro,
        COUNT(pa.id_pcd) AS total_atendimentos
    FROM membrodaequipe m
    JOIN prestaassistencia pa ON m.id_membro = pa.id_membro_cain
    LEFT JOIN aluno a ON m.id_membro = a.id_membro
    LEFT JOIN pessoa p_aluno ON a.cpf = p_aluno.cpf
    LEFT JOIN tecnicoadministrativo ta ON m.id_membro = ta.id_membro
    LEFT JOIN terceirizado t ON m.id_membro = t.id_membro
    LEFT JOIN servidor s ON ta.cpf = s.cpf OR t.cpf = s.cpf
    LEFT JOIN pessoa p_servidor ON s.cpf = p_servidor.cpf
    GROUP BY m.id_membro, nome_membro
    ORDER BY total_atendimentos DESC;
    ```

---

### 6. Relatório de Recursos de Acessibilidade por Categoria

*   **Onde:** `app/sql/relatorio_recursos_por_categoria.sql`
*   **O que:** Agrupa as tecnologias por sua categoria, conta o total de itens em cada uma e também conta quantos desses itens estão disponíveis para empréstimo.
*   **Como:** Utiliza `LEFT JOIN` para incluir todas as tecnologias (mesmo as não emprestáveis) e uma expressão `CASE` dentro da função de agregação `SUM` para realizar a contagem condicional dos itens disponíveis.
    ```sql
    SELECT
        ct.tipocategoria,
        COUNT(t.id_tecnologia) AS total_de_itens,
        SUM(CASE WHEN te.status = true THEN 1 ELSE 0 END) AS disponiveis_para_emprestimo
    FROM categoriatecnologia ct
    JOIN tecnologia t ON ct.id_categoria = t.id_categoria
    LEFT JOIN tecnologiaemprestavel te ON t.id_tecnologia = te.id_tecnologia
    GROUP BY ct.tipocategoria
    ORDER BY ct.tipocategoria;
    ```

---

### 7. Perfil de Alunos com Deficiência (PCD)

*   **Onde:** `app/sql/perfil_alunos_pcd.sql`
*   **O que:** Lista o nome, matrícula e curso de cada aluno que é PCD e agrega todas as suas deficiências registradas em uma única coluna de texto.
*   **Como:** É uma consulta avançada que usa a função de agregação `string_agg` (específica do PostgreSQL) e múltiplos `JOIN`s para conectar seis tabelas diferentes.
    ```sql
    SELECT
        p.nome,
        a.matricula,
        c.nome AS nome_curso,
        string_agg(d.categoria, ', ') AS deficiencias
    FROM pessoa p
    JOIN aluno a ON p.cpf = a.cpf
    JOIN pcd ON a.id_pcd = pcd.id_pcd
    JOIN dadosdeficienciapcd ddpcd ON pcd.id_pcd = ddpcd.id_pcd
    JOIN deficiencia d ON ddpcd.id_deficiencia = d.id_deficiencia
    LEFT JOIN matriculadoem m ON a.cpf = m.cpf
    LEFT JOIN curso c ON m.codigo = c.codigo
    GROUP BY p.nome, a.matricula, c.nome
    ORDER BY p.nome;
    ```

---

### 8. Materiais Produzidos por Bolsistas

*   **Onde:** `app/sql/materiais_por_bolsista.sql`
*   **O que:** Mostra todos os materiais acessíveis que foram produzidos, quem os produziu (o nome do bolsista) e a qual categoria o material pertence.
*   **Como:** Demonstra uma longa cadeia de `JOIN`s para conectar a tabela `materialacessivel` até a tabela `pessoa` (para obter o nome do bolsista), passando por `categoriadematerial`, `bolsistaproducao`, `bolsista`, `membrodaequipe` e `aluno`.
    ```sql
    SELECT
        ma.titulo AS material,
        cm.tipomaterial AS categoria_material,
        p.nome AS nome_bolsista,
        ma.status
    FROM materialacessivel ma
    JOIN categoriamaterial cm ON ma.id_categoria = cm.id_categoria
    JOIN bolsistaproducao bp ON ma.id_bolsista = bp.id_bolsista
    JOIN bolsista b ON bp.id_bolsista = b.id_bolsista
    JOIN membrodaequipe m ON b.id_bolsista = m.id_membro
    JOIN aluno a ON m.id_membro = a.id_membro
    JOIN pessoa p ON a.cpf = p.cpf
    ORDER BY p.nome, ma.titulo;
    ```
