from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Pessoa, ContatoTelefones, ContatoEmails, Curso, DepartamentoSetor, Aluno, Servidor, Docente, TecnicoAdministrativo, Terceirizado, Cargo, Bolsista, TecnologiaEmprestavel

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    pessoas = Pessoa.query.all()
    return render_template('pessoas.html', pessoas=pessoas)

@app.route('/pessoa/add')
def add_pessoa_form():
    return render_template('add_pessoa.html')

@app.route('/aluno/add', methods=['GET', 'POST'])
def add_aluno():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        codigo_curso = request.form.get('codigo_curso')
        if cpf and nome and matricula and codigo_curso:
            new_pessoa = Pessoa(cpf=cpf, nome=nome)
            db.session.add(new_pessoa)
            db.session.commit()
            new_aluno = Aluno(cpf=cpf, matricula=matricula, codigo_curso=codigo_curso)
            db.session.add(new_aluno)
            db.session.commit()
            return redirect(url_for('pessoas'))
    cursos = Curso.query.all()
    return render_template('add_aluno.html', cursos=cursos)

@app.route('/servidor/add', methods=['GET', 'POST'])
def add_servidor():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        tipo_contrato = request.form.get('tipo_contrato')
        codigo_departamento = request.form.get('codigo_departamento')
        tipo_servidor = request.form.get('tipo_servidor')

        if cpf and nome and tipo_contrato and codigo_departamento and tipo_servidor:
            new_pessoa = Pessoa(cpf=cpf, nome=nome)
            db.session.add(new_pessoa)
            db.session.commit()

            new_servidor = Servidor(cpf=cpf, tipodecontrato=tipo_contrato, codigo_departamento=codigo_departamento)
            db.session.add(new_servidor)
            db.session.commit()

            if tipo_servidor == 'docente':
                siape = request.form.get('siape')
                new_docente = Docente(cpf_servidor=cpf, siape=siape)
                db.session.add(new_docente)
                db.session.commit()
            elif tipo_servidor == 'tecnico':
                siape = request.form.get('siape')
                id_cargo = request.form.get('id_cargo')
                new_tecnico = TecnicoAdministrativo(cpf_servidor=cpf, siape=siape, id_cargo=id_cargo)
                db.session.add(new_tecnico)
                db.session.commit()
            elif tipo_servidor == 'terceirizado':
                id_cargo = request.form.get('id_cargo')
                new_terceirizado = Terceirizado(cpf_servidor=cpf, id_cargo=id_cargo)
                db.session.add(new_terceirizado)
                db.session.commit()

            return redirect(url_for('pessoas'))

    departamentos = DepartamentoSetor.query.all()
    cargos = Cargo.query.all()
    return render_template('add_servidor.html', departamentos=departamentos, cargos=cargos)

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

@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

@app.route('/consulta1', methods=['GET', 'POST'])
def consulta1():
    if request.method == 'POST':
        codigo_curso = request.form.get('codigo_curso')
        alunos = Aluno.query.filter_by(codigo_curso=codigo_curso).all()
        return render_template('resultado_consulta1.html', alunos=alunos)
    cursos = Curso.query.all()
    return render_template('form_consulta1.html', cursos=cursos)

@app.route('/consulta2', methods=['GET', 'POST'])
def consulta2():
    if request.method == 'POST':
        codigo_departamento = request.form.get('codigo_departamento')
        servidores = Servidor.query.filter_by(codigo_departamento=codigo_departamento).all()
        return render_template('resultado_consulta2.html', servidores=servidores)
    departamentos = DepartamentoSetor.query.all()
    return render_template('form_consulta2.html', departamentos=departamentos)

@app.route('/consulta3')
def consulta3():
    bolsistas = Bolsista.query.all()
    return render_template('resultado_consulta3.html', bolsistas=bolsistas)

@app.route('/consulta4')
def consulta4():
    tecnologias = TecnologiaEmprestavel.query.all()
    return render_template('resultado_consulta4.html', tecnologias=tecnologias)

@app.route('/update_pessoa_nome', methods=['POST'])
def update_pessoa_nome():
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    pessoa = Pessoa.query.get_or_404(cpf)
    pessoa.nome = nome
    db.session.commit()
    return redirect(url_for('pessoas'))

@app.route('/delete_pessoa_by_cpf', methods=['POST'])
def delete_pessoa_by_cpf():
    cpf = request.form.get('cpf')
    pessoa = Pessoa.query.get_or_404(cpf)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('pessoas'))
