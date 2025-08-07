from flask import render_template, request, redirect, url_for
from app import app, db
from flask import flash
from app.models import Pessoa, ContatoTelefones, ContatoEmails, Curso, DepartamentoSetor, Aluno, Servidor, Docente, TecnicoAdministrativo, Terceirizado, Cargo, MatriculadoEm, PessoaLGBT, Deficiencia, PCD, DadosDeficienciaPCD, MembroDaEquipe, PeriodoDeVinculo
from datetime import date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    # Modern query style
    pessoas = db.session.execute(db.select(Pessoa)).scalars().all()
    return render_template('pessoas.html', pessoas=pessoas)

@app.route('/pessoa/add', methods=['GET', 'POST'])
def add_pessoa():
    if request.method == 'POST':
        try:
            cpf = request.form.get('cpf')
            if not cpf:
                flash('CPF é obrigatório.', 'error')
                return redirect(url_for('add_pessoa'))

            # Use session.get for primary key lookups, it's more efficient
            pessoa = db.session.get(Pessoa, cpf)
            if not pessoa:
                pessoa = Pessoa(CPF=cpf, Nome=request.form.get('nome'))
                db.session.add(pessoa)

            # --- PessoaLGBT ---
            if request.form.get('nomesocial'):
                if not pessoa.pessoalgbt:
                    pessoa.pessoalgbt = PessoaLGBT(NomeSocial=request.form.get('nomesocial'))
                else:
                    pessoa.pessoalgbt.NomeSocial = request.form.get('nomesocial')

            # --- Contatos ---
            emails_in_form = request.form.getlist('emails[]')
            for email_str in emails_in_form:
                if email_str:
                    exists = db.session.query(ContatoEmails).filter_by(CPF=cpf, Email=email_str).first()
                    if not exists:
                        db.session.add(ContatoEmails(CPF=cpf, Email=email_str))

            telefones_in_form = request.form.getlist('telefones[]')
            for tel_str in telefones_in_form:
                if tel_str:
                    exists = db.session.query(ContatoTelefones).filter_by(CPF=cpf, Telefone=tel_str).first()
                    if not exists:
                        db.session.add(ContatoTelefones(CPF=cpf, Telefone=tel_str))

            # --- Vínculos e Status ---
            pcd_instance = None
            membro_instance = None

            # --- Status PCD ---
            is_pcd = request.form.get('is_aluno_pcd') or request.form.get('is_tecnico_pcd') or request.form.get('is_docente_pcd')
            if is_pcd:
                pcd_instance = PCD()
                db.session.add(pcd_instance)
                db.session.flush()

                deficiencias = request.form.getlist('deficiencias[]')
                graus = request.form.getlist('graus[]')
                observacoes = request.form.getlist('observacoes[]')
                for i, deficiencia_id_str in enumerate(deficiencias):
                    if deficiencia_id_str:
                        dados_def = DadosDeficienciaPCD(
                            ID_PCD=pcd_instance.ID_PCD,
                            ID_DEFICIENCIA=int(deficiencia_id_str),
                            Grau=graus[i],
                            Observacoes=observacoes[i]
                        )
                        db.session.add(dados_def)

            # --- Status Membro da Equipe CAIN ---
            is_membro = request.form.get('is_aluno_membro') or request.form.get('is_tecnico_membro') or request.form.get('is_terceirizado_membro')
            if is_membro:
                membro_instance = MembroDaEquipe(
                    Categoria=request.form.get('categoria_membro'),
                    RegimeDeTrabalho=request.form.get('regime_trabalho')
                )
                db.session.add(membro_instance)
                db.session.flush()

                data_inicio_str = request.form.get('data_inicio_vinculo')
                if data_inicio_str:
                    vinculo = PeriodoDeVinculo(
                        DataDeInicio=date.fromisoformat(data_inicio_str),
                        DataDeFim=date.fromisoformat(request.form.get('data_fim_vinculo')) if request.form.get('data_fim_vinculo') else None,
                        ID_MEMBRO=membro_instance.ID_MEMBRO
                    )
                    db.session.add(vinculo)

            # --- Vínculo Aluno ---
            if request.form.get('is_aluno'):
                matricula = request.form.get('matricula')
                codigo_curso = request.form.get('codigo_curso')
                if matricula and codigo_curso:
                    aluno = pessoa.aluno
                    if not aluno:
                        aluno = Aluno(Matricula=matricula)
                        pessoa.aluno = aluno

                    if pcd_instance and request.form.get('is_aluno_pcd'):
                        aluno.pcd = pcd_instance

                    if membro_instance and request.form.get('is_aluno_membro'):
                        aluno.membro_da_equipe = membro_instance

                    matricula_exists = db.session.query(MatriculadoEm).filter_by(CPF=cpf, Codigo=codigo_curso).first()
                    if not matricula_exists:
                        curso = db.session.get(Curso, int(codigo_curso))
                        if curso:
                            matricula_obj = MatriculadoEm(Situacao='Cursando', DataInicio=date.today())
                            matricula_obj.curso = curso
                            aluno.matriculas.append(matricula_obj)

            # --- Vínculo Servidor ---
            if request.form.get('is_servidor'):
                servidor = pessoa.servidor
                if not servidor:
                    servidor = Servidor(TipoDeContrato=request.form.get('tipo_contrato'))
                    cod_depto = request.form.get('codigo_departamento')
                    departamento = db.session.get(DepartamentoSetor, int(cod_depto))
                    servidor.departamento = departamento
                    pessoa.servidor = servidor

                tipo_servidor = request.form.get('tipo_servidor')
                if tipo_servidor == 'docente':
                    siape = request.form.get('siape_docente')
                    if siape and not servidor.docente:
                        docente = Docente(SIAPE=siape)
                        if pcd_instance:
                            docente.pcd = pcd_instance
                        servidor.docente = docente

                elif tipo_servidor == 'tecnico':
                    siape = request.form.get('siape_tecnico')
                    id_cargo = request.form.get('id_cargo_tecnico')
                    if siape and id_cargo and not servidor.tecnico_administrativo:
                        tecnico = TecnicoAdministrativo(SIAPE=siape)
                        cargo = db.session.get(Cargo, int(id_cargo))
                        tecnico.cargo = cargo
                        if pcd_instance and request.form.get('is_tecnico_pcd'):
                            tecnico.pcd = pcd_instance
                        if membro_instance and request.form.get('is_tecnico_membro'):
                            tecnico.membro_da_equipe = membro_instance
                        servidor.tecnico_administrativo = tecnico

                elif tipo_servidor == 'terceirizado':
                    id_cargo = request.form.get('id_cargo_terceirizado')
                    if id_cargo and not servidor.terceirizado:
                        terceirizado = Terceirizado()
                        cargo = db.session.get(Cargo, int(id_cargo))
                        terceirizado.cargo = cargo
                        if membro_instance:
                            terceirizado.membro_da_equipe = membro_instance
                        servidor.terceirizado = terceirizado

            db.session.commit()
            flash('Pessoa adicionada com sucesso!', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {e}', 'error')
            print(f"Error in add_pessoa: {e}")
            return redirect(url_for('add_pessoa'))

    # GET request logic
    cursos = db.session.execute(db.select(Curso)).scalars().all()
    departamentos = db.session.execute(db.select(DepartamentoSetor)).scalars().all()
    cargos = db.session.execute(db.select(Cargo)).scalars().all()
    deficiencias = db.session.execute(db.select(Deficiencia)).scalars().all()
    return render_template('add_pessoa.html', cursos=cursos, departamentos=departamentos, cargos=cargos, deficiencias=deficiencias)


@app.route('/pessoa/update/<string:cpf>', methods=['POST'])
def update_pessoa(cpf):
    pessoa = db.session.get(Pessoa, cpf)
    if not pessoa:
        flash('Pessoa não encontrada.', 'error')
        return redirect(url_for('pessoas'))

    pessoa.Nome = request.form.get('nome')
    db.session.commit()
    flash('Pessoa atualizada com sucesso!', 'success')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/delete/<string:cpf>')
def delete_pessoa(cpf):
    pessoa = db.session.get(Pessoa, cpf)
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()
        flash('Pessoa deletada com sucesso!', 'success')
    else:
        flash('Pessoa não encontrada.', 'error')
    return redirect(url_for('pessoas'))

@app.route('/pessoa/edit/<string:cpf>')
def edit_pessoa(cpf):
    pessoa = db.session.get(Pessoa, cpf)
    if not pessoa:
        flash('Pessoa não encontrada.', 'error')
        return redirect(url_for('pessoas'))
    return render_template('pessoa_details.html', pessoa=pessoa)

@app.route('/pessoa/<string:cpf>/add_telefone', methods=['POST'])
def add_telefone(cpf):
    telefone_str = request.form.get('telefone')
    if telefone_str:
        exists = db.session.query(ContatoTelefones).filter_by(CPF=cpf, Telefone=telefone_str).first()
        if not exists:
            new_telefone = ContatoTelefones(CPF=cpf, Telefone=telefone_str)
            db.session.add(new_telefone)
            db.session.commit()
            flash('Telefone adicionado.', 'success')
        else:
            flash('Telefone já existe.', 'info')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_telefone/<string:telefone>')
def delete_telefone(cpf, telefone):
    telefone_obj = db.session.query(ContatoTelefones).filter_by(CPF=cpf, Telefone=telefone).first()
    if telefone_obj:
        db.session.delete(telefone_obj)
        db.session.commit()
        flash('Telefone deletado.', 'success')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/add_email', methods=['POST'])
def add_email(cpf):
    email_str = request.form.get('email')
    if email_str:
        exists = db.session.query(ContatoEmails).filter_by(CPF=cpf, Email=email_str).first()
        if not exists:
            new_email = ContatoEmails(CPF=cpf, Email=email_str)
            db.session.add(new_email)
            db.session.commit()
            flash('Email adicionado.', 'success')
        else:
            flash('Email já existe.', 'info')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_email/<string:email>')
def delete_email(cpf, email):
    email_obj = db.session.query(ContatoEmails).filter_by(CPF=cpf, Email=email).first()
    if email_obj:
        db.session.delete(email_obj)
        db.session.commit()
        flash('Email deletado.', 'success')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/cursos')
def cursos():
    cursos = db.session.execute(db.select(Curso)).scalars().all()
    return render_template('cursos.html', cursos=cursos)

@app.route('/curso/add', methods=['POST'])
def add_curso():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    modalidade = request.form.get('modalidade')
    nivel_formacao = request.form.get('nivel_formacao')
    if codigo and nome:
        new_curso = Curso(
            CODIGO=int(codigo),
            Nome=nome,
            Modalidade=modalidade,
            NivelDeFormacao=nivel_formacao
        )
        db.session.add(new_curso)
        db.session.commit()
        flash('Curso adicionado com sucesso!', 'success')
    return redirect(url_for('cursos'))

@app.route('/departamentos')
def departamentos():
    departamentos = db.session.execute(db.select(DepartamentoSetor)).scalars().all()
    return render_template('departamentos.html', departamentos=departamentos)

@app.route('/departamento/add', methods=['POST'])
def add_departamento():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    localizacao = request.form.get('localizacao')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    if codigo and nome:
        new_departamento = DepartamentoSetor(
            CODIGO=int(codigo),
            Nome=nome,
            Localizacao=localizacao,
            Telefone=telefone,
            Email=email
        )
        db.session.add(new_departamento)
        db.session.commit()
        flash('Departamento adicionado com sucesso!', 'success')
    return redirect(url_for('departamentos'))
