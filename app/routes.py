from flask import render_template, request, redirect, url_for, flash
from . import app, db
from .models import (
    Pessoa, Curso, DepartamentoSetor, Cargo, Deficiencia, PessoaLGBT,
    ContatoEmails, ContatoTelefones, Aluno, Servidor, Docente,
    TecnicoAdministrativo, Terceirizado, PCD, DadosDeficienciaPCD,
    MembroDaEquipe, PeriodoDeVinculoMembro, MatriculadoEm
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def pessoas():
    all_pessoas = Pessoa.query.all()
    return render_template('pessoas.html', pessoas=all_pessoas)

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        modalidade = request.form.get('modalidade')
        nivel_formacao = request.form.get('nivel_formacao')

        if not all([codigo, nome]):
            flash('Código and Nome are required fields.', 'error')
        else:
            new_curso = Curso(
                CODIGO=codigo,
                Nome=nome,
                Modalidade=modalidade,
                NivelDeFormacao=nivel_formacao
            )
            db.session.add(new_curso)
            db.session.commit()
            flash('Curso added successfully!', 'success')
        return redirect(url_for('cursos'))

    all_cursos = Curso.query.all()
    return render_template('cursos.html', cursos=all_cursos)

@app.route('/departamentos', methods=['GET', 'POST'])
def departamentos():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        if not all([codigo, nome]):
            flash('Código and Nome are required fields.', 'error')
        else:
            new_departamento = DepartamentoSetor(
                CODIGO=codigo,
                Nome=nome,
                Localizacao=localizacao,
                Telefone=telefone,
                Email=email
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
            # Basic Pessoa Info
            cpf = request.form.get('cpf')
            if not cpf or Pessoa.query.get(cpf):
                flash('CPF is required and must be unique.', 'error')
                return redirect(url_for('add_pessoa'))

            new_pessoa = Pessoa(CPF=cpf, Nome=request.form.get('nome'))
            db.session.add(new_pessoa)

            # PessoaLGBT Info
            if request.form.get('nomesocial'):
                new_pessoa.lgbt_info = PessoaLGBT(NomeSocial=request.form.get('nomesocial'))

            # Contact Info
            for email in request.form.getlist('emails[]'):
                if email:
                    new_pessoa.emails.append(ContatoEmails(Email=email))
            for telefone in request.form.getlist('telefones[]'):
                if telefone:
                    new_pessoa.telefones.append(ContatoTelefones(Telefone=telefone))

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
                            ID_PCD=pcd_obj.ID_PCD,
                            ID_DEFICIENCIA=def_id,
                            Grau=graus[i],
                            Observacoes=observacoes[i]
                        )
                        db.session.add(dados)

            membro_obj = None
            if is_membro:
                membro_obj = MembroDaEquipe(
                    RegimeDeTrabalho=request.form.get('regime_trabalho'),
                    Categoria=request.form.get('categoria_membro')
                )
                db.session.add(membro_obj)
                db.session.flush()
                if request.form.get('data_inicio_vinculo'):
                    vinculo = PeriodoDeVinculoMembro(
                        ID_MEMBRO=membro_obj.ID_MEMBRO,
                        DataDeInicio=request.form.get('data_inicio_vinculo'),
                        DataDeFim=request.form.get('data_fim_vinculo') or None
                    )
                    db.session.add(vinculo)

            # --- Roles ---
            if request.form.get('is_aluno'):
                aluno_obj = Aluno(
                    Matricula=request.form.get('matricula'),
                    ID_PCD=pcd_obj.ID_PCD if pcd_obj and request.form.get('is_aluno_pcd') else None,
                    ID_MEMBRO=membro_obj.ID_MEMBRO if membro_obj and request.form.get('is_aluno_membro') else None
                )
                new_pessoa.aluno = aluno_obj

                curso_codigo = request.form.get('codigo_curso')
                if curso_codigo:
                    matricula_rel = MatriculadoEm(
                        CPF=new_pessoa.CPF,
                        Codigo=curso_codigo
                    )
                    db.session.add(matricula_rel)

            if request.form.get('is_servidor'):
                servidor_obj = Servidor(
                    TipoDeContrato=request.form.get('tipo_contrato'),
                    CodigoDepartamentoSetor=request.form.get('codigo_departamento')
                )
                new_pessoa.servidor = servidor_obj

                tipo_servidor = request.form.get('tipo_servidor')
                if tipo_servidor == 'docente':
                    docente_obj = Docente(
                        SIAPE=request.form.get('siape_docente'),
                        ID_PCD=pcd_obj.ID_PCD if pcd_obj else None
                    )
                    servidor_obj.docente = docente_obj
                elif tipo_servidor == 'tecnico':
                    tecnico_obj = TecnicoAdministrativo(
                        SIAPE=request.form.get('siape_tecnico'),
                        ID_CARGO=request.form.get('id_cargo_tecnico'),
                        ID_PCD=pcd_obj.ID_PCD if pcd_obj and request.form.get('is_tecnico_pcd') else None,
                        ID_MEMBRO=membro_obj.ID_MEMBRO if membro_obj and request.form.get('is_tecnico_membro') else None
                    )
                    servidor_obj.tecnico = tecnico_obj
                elif tipo_servidor == 'terceirizado':
                    terceirizado_obj = Terceirizado(
                        ID_CARGO=request.form.get('id_cargo_terceirizado'),
                        ID_MEMBRO=membro_obj.ID_MEMBRO if membro_obj else None
                    )
                    servidor_obj.terceirizado = terceirizado_obj

            db.session.commit()
            flash('Pessoa adicionada com sucesso!', 'success')
            return redirect(url_for('pessoas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao adicionar a pessoa: {e}', 'error')
            print(e)

    # --- GET Request Handling ---
    cursos = Curso.query.all()
    departamentos = DepartamentoSetor.query.all()
    cargos = Cargo.query.all()
    deficiencias = Deficiencia.query.all()
    return render_template('add_pessoa.html', cursos=cursos, departamentos=departamentos, cargos=cargos, deficiencias=deficiencias)

@app.route('/pessoa/edit/<string:cpf>', methods=['GET', 'POST'])
def edit_pessoa(cpf):
    return f"Edit Pessoa {cpf} - Not Implemented"
