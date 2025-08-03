from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Pessoa, ContatoTelefones, ContatoEmails, Curso, DepartamentoSetor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    pessoas = Pessoa.query.all()
    return render_template('pessoas.html', pessoas=pessoas)

@app.route('/pessoa/add', methods=['POST'])
def add_pessoa():
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    if cpf and nome:
        new_pessoa = Pessoa(cpf=cpf, nome=nome)
        db.session.add(new_pessoa)
        db.session.commit()
    return redirect(url_for('index'))

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
