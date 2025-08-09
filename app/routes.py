import os
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import text
from . import app, db
from .models import (
    Pessoa, Curso, DepartamentoSetor, Cargo, Deficiencia, PessoaLGBT,
    ContatoEmails, ContatoTelefones, Aluno, Servidor, Docente,
    TecnicoAdministrativo, Terceirizado, PCD, DadosDeficienciaPCD,
    MembroDaEquipe, PeriodoDeVinculoMembro, MatriculadoEm
)

def get_sql_from_file(filename):
    """Reads a SQL query from a file in the app/sql directory."""
    sql_dir = os.path.join(os.path.dirname(__file__), 'sql')
    with open(os.path.join(sql_dir, filename), 'r') as f:
        return f.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    sql_query = get_sql_from_file('select_all_pessoas.sql')
    result = db.session.execute(text(sql_query))
    all_pessoas = result.mappings().all()
    return render_template('pessoas.html', pessoas=all_pessoas)

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        modalidade = request.form.get('modalidade')
        nivel_formacao = request.form.get('niveldeformacao')

        if not all([codigo, nome]):
            flash('Código e Nome são campos obrigatórios.', 'error')
        elif not codigo.isdigit():
            flash('Código deve ser um valor numérico.', 'error')
        else:
            new_curso = Curso(
                codigo=codigo,
                nome=nome,
                modalidade=modalidade,
                niveldeformacao=nivel_formacao
            )
            db.session.add(new_curso)
            db.session.commit()
            flash('Curso added successfully!', 'success')
        return redirect(url_for('cursos'))

    sql_query = get_sql_from_file('select_all_cursos.sql')
    result = db.session.execute(text(sql_query))
    all_cursos = result.mappings().all()
    return render_template('cursos.html', cursos=all_cursos)

@app.route('/curso/<int:codigo_curso>')
def alunos_por_curso(codigo_curso):
    # First, get course details
    sql_curso = text("SELECT * FROM curso WHERE codigo = :codigo")
    result_curso = db.session.execute(sql_curso, {'codigo': codigo_curso}).first()
    curso = result_curso if result_curso else None

    # Now, get the students with a JOIN
    sql_alunos_query = get_sql_from_file('select_alunos_by_curso.sql')
    result_alunos = db.session.execute(text(sql_alunos_query), {'codigo': codigo_curso})
    alunos = result_alunos.mappings().all()

    return render_template('alunos_por_curso.html', curso=curso, alunos=alunos)

@app.route('/departamentos', methods=['GET', 'POST'])
def departamentos():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        if not all([codigo, nome]):
            flash('Código e Nome são campos obrigatórios.', 'error')
        elif not codigo.isdigit():
            flash('Código deve ser um valor numérico.', 'error')
        else:
            new_departamento = DepartamentoSetor(
                codigo=codigo,
                nome=nome,
                localizacao=localizacao,
                telefone=telefone,
                email=email
            )
            db.session.add(new_departamento)
            db.session.commit()
            flash('Departamento added successfully!', 'success')
        return redirect(url_for('departamentos'))

    all_departamentos = DepartamentoSetor.query.all()
    return render_template('departamentos.html', departamentos=all_departamentos)

@app.route('/pessoa/add', methods=['GET', 'POST'])
def add_pessoa():
    if request.method == 'POST':
        try:
            cpf_form = request.form.get('cpf')
            if not cpf_form or not cpf_form.isdigit() or len(cpf_form) != 11:
                flash('CPF inválido. Deve conter exatamente 11 dígitos numéricos.', 'error')
                return redirect(url_for('add_pessoa'))

            if Pessoa.query.get(cpf_form):
                flash('CPF já cadastrado.', 'error')
                return redirect(url_for('add_pessoa'))

            new_pessoa = Pessoa(cpf=cpf_form, nome=request.form.get('nome'))
            db.session.add(new_pessoa)

            if request.form.get('nomesocial'):
                new_pessoa.lgbt_info = PessoaLGBT(nomesocial=request.form.get('nomesocial'))

            for email_form in request.form.getlist('emails[]'):
                if email_form:
                    new_pessoa.emails.append(ContatoEmails(email=email_form))

            for telefone_form in request.form.getlist('telefones[]'):
                if telefone_form:
                    new_pessoa.telefones.append(ContatoTelefones(telefone=telefone_form))

            db.session.commit()
            flash('Pessoa adicionada com sucesso! Agora você pode atribuir papéis a ela.', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao adicionar a pessoa: {e}', 'error')
            print(e)

    return render_template('add_pessoa.html')

@app.route('/pessoa/edit/<string:cpf>', methods=['GET', 'POST'])
def edit_pessoa(cpf):
    pessoa = Pessoa.query.get_or_404(cpf)

    if request.method == 'POST':
        try:
            # Update basic info
            pessoa.nome = request.form.get('nome')

            # Update LGBT Info
            nomesocial = request.form.get('nomesocial')
            if nomesocial and not pessoa.lgbt_info:
                pessoa.lgbt_info = PessoaLGBT(nomesocial=nomesocial)
            elif nomesocial and pessoa.lgbt_info:
                pessoa.lgbt_info.nomesocial = nomesocial
            elif not nomesocial and pessoa.lgbt_info:
                db.session.delete(pessoa.lgbt_info)

            # Update Contacts (simple delete and re-add strategy)
            for email in pessoa.emails:
                db.session.delete(email)
            for telefone in pessoa.telefones:
                db.session.delete(telefone)

            for email_form in request.form.getlist('emails[]'):
                if email_form:
                    pessoa.emails.append(ContatoEmails(email=email_form))
            for telefone_form in request.form.getlist('telefones[]'):
                if telefone_form:
                    pessoa.telefones.append(ContatoTelefones(telefone=telefone_form))

            # --- Handle Roles (Aluno, Servidor) ---
            # This logic can get very complex. It needs to handle creation, update, and deletion.

            # Handle Aluno Role
            is_aluno_form = request.form.get('is_aluno')
            if is_aluno_form and not pessoa.aluno:
                # Create Aluno role
                aluno_obj = Aluno(matricula=request.form.get('matricula'))
                pessoa.aluno = aluno_obj
                # Note: This doesn't handle PCD/Membro status yet. That's a further complexity.
            elif is_aluno_form and pessoa.aluno:
                # Update Aluno role
                pessoa.aluno.matricula = request.form.get('matricula')
            elif not is_aluno_form and pessoa.aluno:
                # Delete Aluno role
                db.session.delete(pessoa.aluno)

            # Handle Servidor Role (simplified for now)
            is_servidor_form = request.form.get('is_servidor')
            if is_servidor_form and not pessoa.servidor:
                # Create Servidor role - logic would be similar to assign_role
                flash('A criação de novos papéis de servidor deve ser feita na tela "Atribuir Papel".', 'warning')
            elif not is_servidor_form and pessoa.servidor:
                # Delete Servidor role
                db.session.delete(pessoa.servidor)

            # A full implementation would need to handle all sub-roles (Docente, etc.)
            # and PCD/Membro statuses, which is extremely complex for a single update function.
            # The current implementation is a simplified version focusing on basic updates.

            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar a pessoa: {e}', 'error')
            print(e)

    # GET Request
    cursos = Curso.query.all()
    departamentos = DepartamentoSetor.query.all()
    cargos = Cargo.query.all()
    deficiencias = Deficiencia.query.all()
    return render_template('edit_pessoa.html', pessoa=pessoa, cursos=cursos, departamentos=departamentos, cargos=cargos, deficiencias=deficiencias)

@app.route('/assign_role', methods=['GET', 'POST'])
def assign_role():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        pessoa = Pessoa.query.get_or_404(cpf)

        try:
            # --- Flags and Shared Objects ---
            is_pcd = any([
                request.form.get('is_aluno_pcd'),
                request.form.get('tipo_servidor') == 'docente',
                request.form.get('is_tecnico_pcd')
            ])

            is_membro = any([
                request.form.get('is_aluno_membro'),
                request.form.get('is_tecnico_membro'),
                request.form.get('tipo_servidor') == 'terceirizado'
            ])

            pcd_obj = None
            if is_pcd:
                pcd_obj = PCD()
                db.session.add(pcd_obj)
                db.session.flush()
                deficiencia_ids = request.form.getlist('deficiencias[]')
                graus = request.form.getlist('graus[]')
                observacoes = request.form.getlist('observacoes[]')
                for i, def_id in enumerate(deficiencia_ids):
                    if def_id:
                        dados = DadosDeficienciaPCD(
                            id_pcd=pcd_obj.id_pcd,
                            id_deficiencia=def_id,
                            grau=graus[i],
                            observacoes=observacoes[i]
                        )
                        db.session.add(dados)

            membro_obj = None
            if is_membro:
                membro_obj = MembroDaEquipe(
                    regimedetrabalho=request.form.get('regimedetrabalho'),
                    categoria=request.form.get('categoria_membro')
                )
                db.session.add(membro_obj)
                db.session.flush()
                if request.form.get('datadeinicio'):
                    vinculo = PeriodoDeVinculoMembro(
                        id_membro=membro_obj.id_membro,
                        datadeinicio=request.form.get('datadeinicio'),
                        datadefim=request.form.get('datadefim') or None
                    )
                    db.session.add(vinculo)

            # --- Roles ---
            if request.form.get('is_aluno') and not pessoa.aluno:
                aluno_obj = Aluno(
                    matricula=request.form.get('matricula'),
                    id_pcd=pcd_obj.id_pcd if pcd_obj and request.form.get('is_aluno_pcd') else None,
                    id_membro=membro_obj.id_membro if membro_obj and request.form.get('is_aluno_membro') else None
                )
                pessoa.aluno = aluno_obj

                curso_codigo = request.form.get('codigo_curso')
                if curso_codigo:
                    matricula_rel = MatriculadoEm(
                        cpf=pessoa.cpf,
                        codigo=curso_codigo
                    )
                    db.session.add(matricula_rel)

            if request.form.get('is_servidor') and not pessoa.servidor:
                servidor_obj = Servidor(
                    tipodecontrato=request.form.get('tipodecontrato'),
                    codigodepartamentosetor=request.form.get('codigo_departamento')
                )
                pessoa.servidor = servidor_obj

                tipo_servidor = request.form.get('tipo_servidor')
                if tipo_servidor == 'docente':
                    docente_obj = Docente(
                        siape=request.form.get('siape_docente'),
                        id_pcd=pcd_obj.id_pcd if pcd_obj else None
                    )
                    servidor_obj.docente = docente_obj
                elif tipo_servidor == 'tecnico':
                    tecnico_obj = TecnicoAdministrativo(
                        siape=request.form.get('siape_tecnico'),
                        id_cargo=request.form.get('id_cargo_tecnico'),
                        id_pcd=pcd_obj.id_pcd if pcd_obj and request.form.get('is_tecnico_pcd') else None,
                        id_membro=membro_obj.id_membro if membro_obj and request.form.get('is_tecnico_membro') else None
                    )
                    servidor_obj.tecnico = tecnico_obj
                elif tipo_servidor == 'terceirizado':
                    terceirizado_obj = Terceirizado(
                        id_cargo=request.form.get('id_cargo_terceirizado'),
                        id_membro=membro_obj.id_membro if membro_obj else None
                    )
                    servidor_obj.terceirizado = terceirizado_obj

            db.session.commit()
            flash(f'Papéis atribuídos com sucesso para {pessoa.nome}!', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atribuir papéis: {e}', 'error')
            print(e)
            return redirect(url_for('assign_role', search_cpf=cpf))

    # --- GET Request Handling ---
    pessoa = None
    search_cpf = request.args.get('search_cpf')
    if search_cpf:
        if not search_cpf.isdigit() or len(search_cpf) != 11:
            flash('CPF de busca inválido. Deve conter exatamente 11 dígitos numéricos.', 'error')
        else:
            sql_query = get_sql_from_file('select_pessoa_by_cpf.sql')
            result = db.session.execute(text(sql_query), {'cpf': search_cpf}).first()
            pessoa = result if result else None
            if not pessoa:
                flash('Pessoa com o CPF informado não encontrada.', 'error')

    cursos = Curso.query.all()
    departamentos = DepartamentoSetor.query.all()
    cargos = Cargo.query.all()
    deficiencias = Deficiencia.query.all()
    return render_template('assign_role.html', pessoa=pessoa, cursos=cursos, departamentos=departamentos, cargos=cargos, deficiencias=deficiencias)
