from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import (
    Pessoa, ContatoTelefones, ContatoEmails, Curso, DepartamentoSetor, Aluno,
    Servidor, Docente, TecnicoAdministrativo, Terceirizado, Cargo, MatriculadoEm,
    PessoaLGBT, Deficiencia, PCD, DadosDeficienciaPCD, MembroDaEquipe, PeriodoDeVinculo
)
from datetime import date

# Note: This file has been completely refactored to use the new lowercase model attributes.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
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

            pessoa = db.session.get(Pessoa, cpf)
            if not pessoa:
                pessoa = Pessoa(cpf=cpf, nome=request.form.get('nome'))
                db.session.add(pessoa)

            if request.form.get('nomesocial'):
                if not pessoa.pessoalgbt:
                    pessoa.pessoalgbt = PessoaLGBT(nomesocial=request.form.get('nomesocial'))
                else:
                    pessoa.pessoalgbt.nomesocial = request.form.get('nomesocial')

            for email_str in request.form.getlist('emails[]'):
                if email_str and not db.session.query(ContatoEmails).filter_by(cpf=cpf, email=email_str).first():
                    db.session.add(ContatoEmails(cpf=cpf, email=email_str))

            for tel_str in request.form.getlist('telefones[]'):
                if tel_str and not db.session.query(ContatoTelefones).filter_by(cpf=cpf, telefone=tel_str).first():
                    db.session.add(ContatoTelefones(cpf=cpf, telefone=tel_str))

            pcd_instance = None
            if request.form.get('is_aluno_pcd') or request.form.get('is_tecnico_pcd') or request.form.get('is_docente_pcd'):
                pcd_instance = PCD()
                db.session.add(pcd_instance)
                db.session.flush()
                for i, def_id in enumerate(request.form.getlist('deficiencias[]')):
                    if def_id:
                        db.session.add(DadosDeficienciaPCD(id_pcd=pcd_instance.id_pcd, id_deficiencia=int(def_id), grau=request.form.getlist('graus[]')[i], observacoes=request.form.getlist('observacoes[]')[i]))

            membro_instance = None
            if request.form.get('is_aluno_membro') or request.form.get('is_tecnico_membro') or request.form.get('is_terceirizado_membro'):
                membro_instance = MembroDaEquipe(categoria=request.form.get('categoria_membro'), regimedetrabalho=request.form.get('regime_trabalho'))
                db.session.add(membro_instance)
                db.session.flush()
                if request.form.get('data_inicio_vinculo'):
                    db.session.add(PeriodoDeVinculo(datadeinicio=date.fromisoformat(request.form.get('data_inicio_vinculo')), datadefim=date.fromisoformat(request.form.get('data_fim_vinculo')) if request.form.get('data_fim_vinculo') else None, id_membro=membro_instance.id_membro))

            if request.form.get('is_aluno'):
                if request.form.get('matricula') and request.form.get('codigo_curso'):
                    if not pessoa.aluno:
                        pessoa.aluno = Aluno(matricula=request.form.get('matricula'))
                    if pcd_instance and request.form.get('is_aluno_pcd'):
                        pessoa.aluno.pcd = pcd_instance
                    if membro_instance and request.form.get('is_aluno_membro'):
                        pessoa.aluno.membro_da_equipe = membro_instance
                    if not db.session.query(MatriculadoEm).filter_by(cpf=cpf, codigo=int(request.form.get('codigo_curso'))).first():
                        curso = db.session.get(Curso, int(request.form.get('codigo_curso')))
                        if curso:
                            mat = MatriculadoEm(situacao='Cursando', datainicio=date.today())
                            mat.curso = curso
                            pessoa.aluno.matriculas.append(mat)

            if request.form.get('is_servidor'):
                if not pessoa.servidor:
                    depto = db.session.get(DepartamentoSetor, int(request.form.get('codigo_departamento')))
                    pessoa.servidor = Servidor(tipodecontrato=request.form.get('tipo_contrato'), departamento=depto)

                tipo = request.form.get('tipo_servidor')
                if tipo == 'docente' and request.form.get('siape_docente') and not pessoa.servidor.docente:
                    docente = Docente(siape=request.form.get('siape_docente'))
                    if pcd_instance: docente.pcd = pcd_instance
                    pessoa.servidor.docente = docente
                elif tipo == 'tecnico' and request.form.get('siape_tecnico') and request.form.get('id_cargo_tecnico') and not pessoa.servidor.tecnico_administrativo:
                    tecnico = TecnicoAdministrativo(siape=request.form.get('siape_tecnico'), cargo=db.session.get(Cargo, int(request.form.get('id_cargo_tecnico'))))
                    if pcd_instance and request.form.get('is_tecnico_pcd'): tecnico.pcd = pcd_instance
                    if membro_instance and request.form.get('is_tecnico_membro'): tecnico.membro_da_equipe = membro_instance
                    pessoa.servidor.tecnico_administrativo = tecnico
                elif tipo == 'terceirizado' and request.form.get('id_cargo_terceirizado') and not pessoa.servidor.terceirizado:
                    terceirizado = Terceirizado(cargo=db.session.get(Cargo, int(request.form.get('id_cargo_terceirizado'))))
                    if membro_instance: terceirizado.membro_da_equipe = membro_instance
                    pessoa.servidor.terceirizado = terceirizado

            db.session.commit()
            flash('Pessoa adicionada com sucesso!', 'success')
            return redirect(url_for('pessoas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {e}', 'error')
            print(f"Error in add_pessoa: {e}")
            return redirect(url_for('add_pessoa'))

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
    pessoa.nome = request.form.get('nome')
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
    tel = request.form.get('telefone')
    if tel and not db.session.query(ContatoTelefones).filter_by(cpf=cpf, telefone=tel).first():
        db.session.add(ContatoTelefones(cpf=cpf, telefone=tel))
        db.session.commit()
        flash('Telefone adicionado.', 'success')
    else:
        flash('Telefone já existe ou é inválido.', 'info')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_telefone/<string:telefone>')
def delete_telefone(cpf, telefone):
    tel_obj = db.session.query(ContatoTelefones).filter_by(cpf=cpf, telefone=telefone).first()
    if tel_obj:
        db.session.delete(tel_obj)
        db.session.commit()
        flash('Telefone deletado.', 'success')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/add_email', methods=['POST'])
def add_email(cpf):
    email_str = request.form.get('email')
    if email_str and not db.session.query(ContatoEmails).filter_by(cpf=cpf, email=email_str).first():
        db.session.add(ContatoEmails(cpf=cpf, email=email_str))
        db.session.commit()
        flash('Email adicionado.', 'success')
    else:
        flash('Email já existe ou é inválido.', 'info')
    return redirect(url_for('edit_pessoa', cpf=cpf))

@app.route('/pessoa/<string:cpf>/delete_email/<string:email>')
def delete_email(cpf, email):
    email_obj = db.session.query(ContatoEmails).filter_by(cpf=cpf, email=email).first()
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
    if request.form.get('codigo') and request.form.get('nome'):
        new_curso = Curso(codigo=int(request.form.get('codigo')), nome=request.form.get('nome'), modalidade=request.form.get('modalidade'), niveldeformacao=request.form.get('nivel_formacao'))
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
    if request.form.get('codigo') and request.form.get('nome'):
        new_departamento = DepartamentoSetor(codigo=int(request.form.get('codigo')), nome=request.form.get('nome'), localizacao=request.form.get('localizacao'), telefone=request.form.get('telefone'), email=request.form.get('email'))
        db.session.add(new_departamento)
        db.session.commit()
        flash('Departamento adicionado com sucesso!', 'success')
    return redirect(url_for('departamentos'))
