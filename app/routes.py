from flask import render_template, request, redirect, url_for
from app import app, db
from flask import flash
from app.models import Pessoa, ContatoTelefones, ContatoEmails, Curso, DepartamentoSetor, Aluno, Servidor, Docente, TecnicoAdministrativo, Terceirizado, Cargo, MatriculadoEm, PessoaLGBT, Deficiencia, PCD, DadosDeficiencia_PCD, MembroDaEquipe, PeriodoDeVinculo
from datetime import date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    pessoas = Pessoa.query.all()
    return render_template('pessoas.html', pessoas=pessoas)

@app.route('/pessoa/add', methods=['GET', 'POST'])
def add_pessoa():
    if request.method == 'POST':
        try:
            cpf = request.form.get('cpf')
            if not cpf:
                flash('CPF é obrigatório.', 'error')
                return redirect(url_for('add_pessoa'))

            # --- Pessoa e Contatos ---
            pessoa = Pessoa.query.get(cpf)
            if not pessoa:
                pessoa = Pessoa(cpf=cpf, nome=request.form.get('nome'))
                db.session.add(pessoa)

            if request.form.get('nomesocial'):
                pessoalgbt = PessoaLGBT.query.get(cpf)
                if not pessoalgbt:
                    pessoalgbt = PessoaLGBT(cpf=cpf, nomesocial=request.form.get('nomesocial'))
                    db.session.add(pessoalgbt)

            emails = request.form.getlist('emails[]')
            for email in emails:
                if email:
                    if not ContatoEmails.query.get((cpf, email)):
                        db.session.add(ContatoEmails(cpf=cpf, email=email))

            telefones = request.form.getlist('telefones[]')
            for telefone in telefones:
                if telefone:
                    if not ContatoTelefones.query.get((cpf, telefone)):
                        db.session.add(ContatoTelefones(cpf=cpf, telefone=telefone))

            # --- Vínculos e Status ---
            aluno_instance = None
            servidor_instance = None
            docente_instance = None
            tecnico_instance = None
            terceirizado_instance = None

            # --- Vínculo Aluno ---
            if request.form.get('is_aluno'):
                matricula = request.form.get('matricula')
                codigo_curso = request.form.get('codigo_curso')
                if matricula and codigo_curso:
                    aluno_instance = Aluno.query.get(cpf)
                    if not aluno_instance:
                        aluno_instance = Aluno(cpf=cpf, matricula=matricula)
                        db.session.add(aluno_instance)
                    if not MatriculadoEm.query.get((cpf, codigo_curso)):
                        db.session.add(MatriculadoEm(cpf_aluno=cpf, codigo_curso=codigo_curso, datainicio=date.today()))

            # --- Vínculo Servidor ---
            if request.form.get('is_servidor'):
                tipo_contrato = request.form.get('tipo_contrato')
                codigo_departamento = request.form.get('codigo_departamento')
                if tipo_contrato and codigo_departamento:
                    servidor_instance = Servidor.query.get(cpf)
                    if not servidor_instance:
                        servidor_instance = Servidor(cpf=cpf, tipodecontrato=tipo_contrato, codigo_departamento=codigo_departamento)
                        db.session.add(servidor_instance)

                    tipo_servidor = request.form.get('tipo_servidor')
                    if tipo_servidor == 'docente':
                        siape = request.form.get('siape_docente')
                        if siape and not Docente.query.get(cpf):
                            docente_instance = Docente(cpf_servidor=cpf, siape=siape)
                            db.session.add(docente_instance)
                    elif tipo_servidor == 'tecnico':
                        siape = request.form.get('siape_tecnico')
                        id_cargo = request.form.get('id_cargo_tecnico')
                        if siape and id_cargo and not TecnicoAdministrativo.query.get(cpf):
                            tecnico_instance = TecnicoAdministrativo(cpf_servidor=cpf, siape=siape, id_cargo=id_cargo)
                            db.session.add(tecnico_instance)
                    elif tipo_servidor == 'terceirizado':
                        id_cargo = request.form.get('id_cargo_terceirizado')
                        if id_cargo and not Terceirizado.query.get(cpf):
                            terceirizado_instance = Terceirizado(cpf_servidor=cpf, id_cargo=id_cargo)
                            db.session.add(terceirizado_instance)

            # --- Status PCD ---
            is_pcd = request.form.get('is_aluno_pcd') or request.form.get('is_tecnico_pcd') or request.form.get('tipo_servidor') == 'docente'
            if is_pcd:
                pcd_instance = PCD()
                db.session.add(pcd_instance)
                db.session.flush()

                deficiencias = request.form.getlist('deficiencias[]')
                graus = request.form.getlist('graus[]')
                observacoes = request.form.getlist('observacoes[]')
                for i, deficiencia_id in enumerate(deficiencias):
                    if deficiencia_id:
                        db.session.add(DadosDeficiencia_PCD(id_pcd=pcd_instance.id, id_deficiencia=deficiencia_id, grau=graus[i], observacoes=observacoes[i]))

                if aluno_instance and request.form.get('is_aluno_pcd'):
                    aluno_instance.id_pcd = pcd_instance.id
                if docente_instance:
                    docente_instance.id_pcd = pcd_instance.id
                if tecnico_instance and request.form.get('is_tecnico_pcd'):
                    tecnico_instance.id_pcd = pcd_instance.id

            # --- Status Membro da Equipe CAIN ---
            is_membro = request.form.get('is_aluno_membro') or request.form.get('is_tecnico_membro') or request.form.get('tipo_servidor') == 'terceirizado'
            if is_membro:
                membro_instance = MembroDaEquipe.query.get(cpf)
                if not membro_instance:
                    membro_instance = MembroDaEquipe(chave=cpf, categoria=request.form.get('categoria_membro'), regimedetrabalho=request.form.get('regime_trabalho'))
                    db.session.add(membro_instance)

                data_inicio_str = request.form.get('data_inicio_vinculo')
                if data_inicio_str:
                    data_inicio = date.fromisoformat(data_inicio_str)
                    data_fim_str = request.form.get('data_fim_vinculo')
                    data_fim = date.fromisoformat(data_fim_str) if data_fim_str else None
                    db.session.add(PeriodoDeVinculo(chave_membrodaequipe=cpf, datadeinicio=data_inicio, datadefim=data_fim))

                if aluno_instance and request.form.get('is_aluno_membro'):
                    aluno_instance.chave_membrodaequipe = cpf
                if tecnico_instance and request.form.get('is_tecnico_membro'):
                    tecnico_instance.chave_membrodaequipe = cpf
                if terceirizado_instance:
                    terceirizado_instance.chave_membrodaequipe = cpf

            db.session.commit()
            flash('Pessoa adicionada com sucesso!', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {e}', 'error')
            return redirect(url_for('add_pessoa'))

    cursos = Curso.query.all()
    departamentos = DepartamentoSetor.query.all()
    cargos = Cargo.query.all()
    deficiencias = Deficiencia.query.all()
    return render_template('add_pessoa.html', cursos=cursos, departamentos=departamentos, cargos=cargos, deficiencias=deficiencias)


@app.route('/pessoa/update/<string:cpf>', methods=['POST'])
def update_pessoa(cpf):
    pessoa = Pessoa.query.get_or_404(cpf)
    pessoa.nome = request.form.get('nome')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/pessoa/delete/<string:cpf>')
def delete_pessoa(cpf):
    pessoa = Pessoa.query.get_or_404(cpf)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/pessoa/edit/<string:cpf>')
def edit_pessoa(cpf):
    pessoa = Pessoa.query.get_or_404(cpf)
    return render_template('pessoa_details.html', pessoa=pessoa)

@app.route('/pessoa/<string:cpf>/add_telefone', methods=['POST'])
def add_telefone(cpf):
    telefone = request.form.get('telefone')
    if telefone:
        new_telefone = ContatoTelefones(cpf=cpf, telefone=telefone)
        db.session.add(new_telefone)
        db.session.commit()
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_telefone/<string:telefone>')
def delete_telefone(cpf, telefone):
    telefone_obj = ContatoTelefones.query.filter_by(cpf=cpf, telefone=telefone).first_or_404()
    db.session.delete(telefone_obj)
    db.session.commit()
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/add_email', methods=['POST'])
def add_email(cpf):
    email = request.form.get('email')
    if email:
        new_email = ContatoEmails(cpf=cpf, email=email)
        db.session.add(new_email)
        db.session.commit()
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_email/<string:email>')
def delete_email(cpf, email):
    email_obj = ContatoEmails.query.filter_by(cpf=cpf, email=email).first_or_404()
    db.session.delete(email_obj)
    db.session.commit()
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/cursos')
def cursos():
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos)

@app.route('/curso/add', methods=['POST'])
def add_curso():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    modalidade = request.form.get('modalidade')
    nivel_formacao = request.form.get('nivel_formacao')
    if codigo and nome:
        new_curso = Curso(codigo=codigo, nome=nome, modalidade=modalidade, nivel_formacao=nivel_formacao)
        db.session.add(new_curso)
        db.session.commit()
    return redirect(url_for('cursos'))

@app.route('/departamentos')
def departamentos():
    departamentos = DepartamentoSetor.query.all()
    return render_template('departamentos.html', departamentos=departamentos)

@app.route('/departamento/add', methods=['POST'])
def add_departamento():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    localizacao = request.form.get('localizacao')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    if codigo and nome:
        new_departamento = DepartamentoSetor(codigo=codigo, nome=nome, localizacao=localizacao, telefone=telefone, email=email)
        db.session.add(new_departamento)
        db.session.commit()
    return redirect(url_for('departamentos'))
