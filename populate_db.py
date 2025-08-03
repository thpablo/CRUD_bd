from app import db
from app import app
from app.models import (
    Pessoa, PCD, Deficiencia, Acao, DepartamentoSetor, Cargo, Curso,
    CategoriaTecnologia, CategoriaMaterial, MembroDaEquipe, ContatoTelefones,
    ContatoEmails, PessoaLGBT, Servidor, Aluno, DadosDeficiencia_PCD,
    TabelaFuncoes, Tecnologia, PeriodoDeVinculo, Bolsista, Estagiario,
    Docente, TecnicoAdministrativo, Terceirizado, MatriculadoEm,
    TecnologiaEmprestavel, BolsistaProducao, BolsistaInclusao,
    EmprestimoMaterial, MaterialAcessivel, MaterialDisponibilizado,
    PrestaAssistencia, Relatorios, Horarios
)
from datetime import date

def populate_db():
    with app.app_context():
        db.create_all()

        # Pessoas
        pessoa1 = Pessoa(cpf='11111111111', nome='Ana Silva')
        pessoa2 = Pessoa(cpf='22222222222', nome='Bruno Costa')
        pessoa3 = Pessoa(cpf='33333333333', nome='Carla Dias')
        db.session.add_all([pessoa1, pessoa2, pessoa3])
        db.session.commit()

        # PCD
        pcd1 = PCD()
        pcd2 = PCD()
        db.session.add_all([pcd1, pcd2])
        db.session.commit()

        # Deficiencia
        deficiencia1 = Deficiencia(categoria='Visual')
        deficiencia2 = Deficiencia(categoria='Auditiva')
        db.session.add_all([deficiencia1, deficiencia2])
        db.session.commit()

        # Acao
        acao1 = Acao(nome='Acompanhamento Pedagógico', descricao='Apoio nas atividades acadêmicas.')
        acao2 = Acao(nome='Tradução em Libras', descricao='Tradução para a Língua Brasileira de Sinais.')
        db.session.add_all([acao1, acao2])
        db.session.commit()

        # Departamento/Setor
        depto1 = DepartamentoSetor(codigo='DCC', nome='Departamento de Ciência da Computação', localizacao='ICEB III', telefone='3559-1234', email='dcc@ufop.edu.br')
        depto2 = DepartamentoSetor(codigo='PROACE', nome='Pró-Reitoria de Assuntos Comunitários e Estudantis', localizacao='Centro de Vivência', telefone='3559-5678', email='proace@ufop.edu.br')
        db.session.add_all([depto1, depto2])
        db.session.commit()

        # Cargo
        cargo1 = Cargo(nome='Técnico em Assuntos Educacionais')
        cargo2 = Cargo(nome='Tradutor e Intérprete de Libras')
        db.session.add_all([cargo1, cargo2])
        db.session.commit()

        # Curso
        curso1 = Curso(codigo='BCC', nome='Bacharelado em Ciência da Computação', modalidade='Presencial', nivel_formacao='Graduação')
        curso2 = Curso(codigo='PED', nome='Licenciatura em Pedagogia', modalidade='Presencial', nivel_formacao='Graduação')
        db.session.add_all([curso1, curso2])
        db.session.commit()

        # CategoriaTecnologia
        cat_tec1 = CategoriaTecnologia(tipocategoria='Software Leitor de Tela')
        cat_tec2 = CategoriaTecnologia(tipocategoria='Hardware de Aumento')
        db.session.add_all([cat_tec1, cat_tec2])
        db.session.commit()

        # CategoriaMaterial
        cat_mat1 = CategoriaMaterial(tipomaterial='Audiolivro')
        cat_mat2 = CategoriaMaterial(tipomaterial='Vídeo com Legendas')
        db.session.add_all([cat_mat1, cat_mat2])
        db.session.commit()

        # MembroDaEquipe
        membro1 = MembroDaEquipe(chave='M01', categoria='Técnico', regimedetrabalho='Presencial')
        membro2 = MembroDaEquipe(chave='M02', categoria='Bolsista', regimedetrabalho='Híbrido', coordenador='M01')
        db.session.add_all([membro1, membro2])
        db.session.commit()

        # ContatoTelefones
        tel1 = ContatoTelefones(cpf='11111111111', telefone='(31) 99999-1111')
        tel2 = ContatoTelefones(cpf='22222222222', telefone='(31) 99999-2222')
        db.session.add_all([tel1, tel2])
        db.session.commit()

        # ContatoEmails
        email1 = ContatoEmails(cpf='11111111111', email='ana.silva@aluno.ufop.edu.br')
        email2 = ContatoEmails(cpf='22222222222', email='bruno.costa@ufop.edu.br')
        db.session.add_all([email1, email2])
        db.session.commit()

        # PessoaLGBT
        lgbt1 = PessoaLGBT(cpf='33333333333', nomesocial='Carla')
        db.session.add(lgbt1)
        db.session.commit()

        # Servidor
        servidor1 = Servidor(cpf='22222222222', tipodecontrato='Efetivo', codigo_departamento='DCC')
        servidor2 = Servidor(cpf='33333333333', tipodecontrato='Efetivo', codigo_departamento='PROACE')
        db.session.add_all([servidor1, servidor2])
        db.session.commit()

        # Aluno
        aluno1 = Aluno(cpf='11111111111', matricula='18.1.1234', id_pcd=1)
        aluno2 = Aluno(cpf='33333333333', matricula='19.2.5678', chave_membrodaequipe='M02')
        db.session.add_all([aluno1, aluno2])
        db.session.commit()

        # DadosDeficiencia_PCD
        dados_def1 = DadosDeficiencia_PCD(id_pcd=1, id_deficiencia=1, grau='Severo', observacoes='Necessita de software leitor de tela.')
        db.session.add(dados_def1)
        db.session.commit()

        # TabelaFuncoes
        funcao1 = TabelaFuncoes(id_cargo=1, funcao='Aconselhamento acadêmico')
        funcao2 = TabelaFuncoes(id_cargo=2, funcao='Interpretação em eventos')
        db.session.add_all([funcao1, funcao2])
        db.session.commit()

        # Tecnologia
        tec1 = Tecnologia(modelo='JAWS', patrimonio_nserie='LIC-12345', localizacao='LabInclusao', id_categoria=1)
        tec2 = Tecnologia(modelo='Lupa Eletrônica', patrimonio_nserie='PAT-67890', localizacao='Sala de Recursos', id_categoria=2)
        db.session.add_all([tec1, tec2])
        db.session.commit()

        # PeriodoDeVinculo
        vinculo1 = PeriodoDeVinculo(chave_membrodaequipe='M01', datadeinicio=date(2020, 1, 15))
        vinculo2 = PeriodoDeVinculo(chave_membrodaequipe='M02', datadeinicio=date(2023, 3, 1), datadefim=date(2024, 3, 1))
        db.session.add_all([vinculo1, vinculo2])
        db.session.commit()

        # Bolsista
        bolsista1 = Bolsista(chave_membrodaequipe='M02', salario=700.00, cargahorariasemanal=20)
        db.session.add(bolsista1)
        db.session.commit()

        # Docente
        docente1 = Docente(cpf_servidor='22222222222', siape='1234567', id_pcd=2)
        db.session.add(docente1)
        db.session.commit()

        # TecnicoAdministrativo
        tecnico1 = TecnicoAdministrativo(cpf_servidor='33333333333', siape='7654321', chave_membrodaequipe='M01', id_cargo=1)
        db.session.add(tecnico1)
        db.session.commit()

        # MatriculadoEm
        mat1 = MatriculadoEm(cpf_aluno='11111111111', codigo_curso='BCC', situacao='Ativo', datainicio=date(2018, 3, 5))
        mat2 = MatriculadoEm(cpf_aluno='33333333333', codigo_curso='PED', situacao='Ativo', datainicio=date(2019, 8, 1))
        db.session.add_all([mat1, mat2])
        db.session.commit()

        # TecnologiaEmprestavel
        tec_emp1 = TecnologiaEmprestavel(id_tecnologia=2, status='Disponível')
        db.session.add(tec_emp1)
        db.session.commit()

        # BolsistaProducao
        bolsista_prod1 = BolsistaProducao(chave_bolsista='M02')
        db.session.add(bolsista_prod1)
        db.session.commit()

        # EmprestimoMaterial
        emprestimo1 = EmprestimoMaterial(id_pcd=1, id_tecnologiaemprestavel=2, dataemprestimo=date(2024, 5, 10), devolucaoestimada=date(2024, 6, 10))
        db.session.add(emprestimo1)
        db.session.commit()

        # MaterialAcessivel
        mat_acessivel1 = MaterialAcessivel(titulo='Introdução à Computação', formato='PDF Acessível', status='Disponível', localizacao='/materiais/intro_comp.pdf', id_categoriamaterial=1, chave_bolsistaproducao='M02')
        db.session.add(mat_acessivel1)
        db.session.commit()

        # MaterialDisponibilizado
        mat_disp1 = MaterialDisponibilizado(id_pcd=1, id_materialacessivel=1)
        db.session.add(mat_disp1)
        db.session.commit()

        # PrestaAssistencia
        assistencia1 = PrestaAssistencia(id_pcd=1, id_acao=1, id_membrocain='M01', datainicio=date(2024, 1, 1))
        db.session.add(assistencia1)
        db.session.commit()

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_db()
