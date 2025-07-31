from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Pessoa

@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)

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
    return render_template('update_pessoa.html', pessoa=pessoa)
