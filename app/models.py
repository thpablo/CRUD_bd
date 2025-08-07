from app import db
from sqlalchemy.orm import relationship

# This file has been completely rewritten to align with the database schema in init.sql.
# Naming conventions for tables (CamelCase) and columns (as defined in init.sql) are followed.
# Relationships are defined with back_populates for clarity and consistency.

class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    CPF = db.Column(db.String(11), primary_key=True)
    Nome = db.Column(db.String(255), nullable=False)

    telefones = relationship("ContatoTelefones", back_populates="pessoa", cascade="all, delete-orphan")
    emails = relationship("ContatoEmails", back_populates="pessoa", cascade="all, delete-orphan")
    pessoalgbt = relationship("PessoaLGBT", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    servidor = relationship("Servidor", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    aluno = relationship("Aluno", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")

class ContatoTelefones(db.Model):
    __tablename__ = 'ContatoTelefones'
    CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), primary_key=True)
    Telefone = db.Column(db.String(20), primary_key=True)

    pessoa = relationship("Pessoa", back_populates="telefones")

class ContatoEmails(db.Model):
    __tablename__ = 'ContatoEmails'
    CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), primary_key=True)
    Email = db.Column(db.String(100), primary_key=True)

    pessoa = relationship("Pessoa", back_populates="emails")

class PessoaLGBT(db.Model):
    __tablename__ = 'PessoaLGBT'
    CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), primary_key=True)
    NomeSocial = db.Column(db.String(255), nullable=False)

    pessoa = relationship("Pessoa", back_populates="pessoalgbt")

class DepartamentoSetor(db.Model):
    __tablename__ = 'DepartamentoSetor'
    CODIGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    Localizacao = db.Column(db.String(100), nullable=False)
    Telefone = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100), nullable=False)

    servidores = relationship("Servidor", back_populates="departamento")

class Servidor(db.Model):
    __tablename__ = 'Servidor'
    CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), primary_key=True)
    TipoDeContrato = db.Column(db.String(100), nullable=False)
    CodigoDepartamento = db.Column(db.Integer, db.ForeignKey('DepartamentoSetor.CODIGO'), nullable=False)

    pessoa = relationship("Pessoa", back_populates="servidor")
    departamento = relationship("DepartamentoSetor", back_populates="servidores")
    docente = relationship("Docente", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    tecnico_administrativo = relationship("TecnicoAdministrativo", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    terceirizado = relationship("Terceirizado", back_populates="servidor", uselist=False, cascade="all, delete-orphan")

class PCD(db.Model):
    __tablename__ = 'PCD'
    ID_PCD = db.Column(db.Integer, primary_key=True)

    docentes = relationship("Docente", back_populates="pcd")
    tecnicos = relationship("TecnicoAdministrativo", back_populates="pcd")
    alunos = relationship("Aluno", back_populates="pcd")
    emprestimos_material = relationship("EmprestimoMaterial", back_populates="pcd")
    materiais_disponibilizados = relationship("MaterialDisponibilizado", back_populates="pcd")
    dados_deficiencia = relationship("DadosDeficienciaPCD", back_populates="pcd", cascade="all, delete-orphan")
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="pcd")

class Docente(db.Model):
    __tablename__ = 'Docente'
    CPF = db.Column(db.String(11), db.ForeignKey('Servidor.CPF'), primary_key=True)
    SIAPE = db.Column(db.String(8), nullable=False, unique=True)
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'))

    servidor = relationship("Servidor", back_populates="docente")
    pcd = relationship("PCD", back_populates="docentes")

class MembroDaEquipe(db.Model):
    __tablename__ = 'MembroDaEquipe'
    ID_MEMBRO = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(50))
    RegimeDeTrabalho = db.Column(db.String(100), nullable=False)
    ID_COORDENADOR = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'))

    coordenador = relationship("MembroDaEquipe", remote_side=[ID_MEMBRO], back_populates="equipe_coordenada")
    equipe_coordenada = relationship("MembroDaEquipe", back_populates="coordenador")
    tecnicos_administrativos = relationship("TecnicoAdministrativo", back_populates="membro_da_equipe")
    terceirizados = relationship("Terceirizado", back_populates="membro_da_equipe")
    alunos = relationship("Aluno", back_populates="membro_da_equipe")
    periodos_de_vinculo = relationship("PeriodoDeVinculo", back_populates="membro_da_equipe", cascade="all, delete-orphan")
    bolsista = relationship("Bolsista", back_populates="membro_da_equipe", uselist=False, cascade="all, delete-orphan")
    estagiario = relationship("Estagiario", back_populates="membro_da_equipe", uselist=False, cascade="all, delete-orphan")
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="membro_cain")

class Cargo(db.Model):
    __tablename__ = 'Cargo'
    ID_CARGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)

    tecnicos_administrativos = relationship("TecnicoAdministrativo", back_populates="cargo")
    terceirizados = relationship("Terceirizado", back_populates="cargo")
    funcoes = relationship("TabelaFuncoes", back_populates="cargo", cascade="all, delete-orphan")

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'TecnicoAdministrativo'
    CPF = db.Column(db.String(11), db.ForeignKey('Servidor.CPF'), primary_key=True)
    SIAPE = db.Column(db.String(8), nullable=False, unique=True)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'))
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'))
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('Cargo.ID_CARGO'))

    servidor = relationship("Servidor", back_populates="tecnico_administrativo")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="tecnicos_administrativos")
    pcd = relationship("PCD", back_populates="tecnicos")
    cargo = relationship("Cargo", back_populates="tecnicos_administrativos")

class Terceirizado(db.Model):
    __tablename__ = 'Terceirizado'
    CPF = db.Column(db.String(11), db.ForeignKey('Servidor.CPF'), primary_key=True)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'))
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('Cargo.ID_CARGO'))

    servidor = relationship("Servidor", back_populates="terceirizado")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="terceirizados")
    cargo = relationship("Cargo", back_populates="terceirizados")

class Aluno(db.Model):
    __tablename__ = 'Aluno'
    CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), primary_key=True)
    Matricula = db.Column(db.String(9), nullable=False)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'))
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'))

    pessoa = relationship("Pessoa", back_populates="aluno")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="alunos")
    pcd = relationship("PCD", back_populates="alunos")
    matriculas = relationship("MatriculadoEm", back_populates="aluno", cascade="all, delete-orphan")

class PeriodoDeVinculo(db.Model):
    __tablename__ = 'PeriodoDeVinculo'
    DataDeInicio = db.Column(db.Date, primary_key=True)
    DataDeFim = db.Column(db.Date, nullable=False)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'), primary_key=True)

    membro_da_equipe = relationship("MembroDaEquipe", back_populates="periodos_de_vinculo")

class Bolsista(db.Model):
    __tablename__ = 'Bolsista'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'), primary_key=True)
    Salario = db.Column(db.Numeric, nullable=False)
    CargaHoraria = db.Column(db.Integer)

    membro_da_equipe = relationship("MembroDaEquipe", back_populates="bolsista")
    producao = relationship("BolsistaProducao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")
    inclusao = relationship("BolsistaInclusao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")

class BolsistaProducao(db.Model):
    __tablename__ = 'BolsistaProducao'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('Bolsista.ID_BOLSISTA'), primary_key=True)

    bolsista = relationship("Bolsista", back_populates="producao")
    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="bolsista_producao")

class BolsistaInclusao(db.Model):
    __tablename__ = 'BolsistaInclusao'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('Bolsista.ID_BOLSISTA'), primary_key=True)

    bolsista = relationship("Bolsista", back_populates="inclusao")
    relatorios = relationship("Relatorios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")
    horarios = relationship("Horarios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")

class Relatorios(db.Model):
    __tablename__ = 'Relatorios'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('BolsistaInclusao.ID_BOLSISTA'), primary_key=True)
    DataReferente = db.Column(db.Date, primary_key=True)
    Relatorios_Semanais = db.Column(db.String(1000))

    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="relatorios")

class Horarios(db.Model):
    __tablename__ = 'Horarios'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('BolsistaInclusao.ID_BOLSISTA'), primary_key=True)
    Horarios_Monitoria = db.Column(db.Date, primary_key=True)

    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="horarios")

class Estagiario(db.Model):
    __tablename__ = 'Estagiario'
    ID_ESTAGIARIO = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'), primary_key=True)
    Salario = db.Column(db.Numeric, nullable=False)
    CargaHoraria = db.Column(db.Integer)

    membro_da_equipe = relationship("MembroDaEquipe", back_populates="estagiario")

class Deficiencia(db.Model):
    __tablename__ = 'Deficiencia'
    ID_DEFICIENCIA = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(50), nullable=False)

    dados_pcd = relationship("DadosDeficienciaPCD", back_populates="deficiencia")

class Acao(db.Model):
    __tablename__ = 'Acao'
    ID_ACAO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Descricao = db.Column(db.String(500))

    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="acao")

class CategoriaTecnologia(db.Model):
    __tablename__ = 'CategoriaTecnologia'
    ID_CATEGORIA = db.Column(db.Integer, primary_key=True)
    Tipo_Categoria = db.Column(db.String(50), nullable=False)

    tecnologias = relationship("Tecnologia", back_populates="categoria")

class Tecnologia(db.Model):
    __tablename__ = 'Tecnologia'
    ID_TECNOLOGIA = db.Column(db.Integer, primary_key=True)
    Modelo = db.Column(db.String(50), nullable=False)
    N_Serie = db.Column(db.Integer, nullable=False)
    Localizacao = db.Column(db.String(100))
    ID_Categoria = db.Column(db.Integer, db.ForeignKey('CategoriaTecnologia.ID_CATEGORIA'), nullable=False)

    categoria = relationship("CategoriaTecnologia", back_populates="tecnologias")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="tecnologia", uselist=False, cascade="all, delete-orphan")

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'TecnologiaEmprestavel'
    ID_TECNOLOGIA = db.Column(db.Integer, db.ForeignKey('Tecnologia.ID_TECNOLOGIA'), primary_key=True)
    STATUS = db.Column(db.Boolean, nullable=False)

    tecnologia = relationship("Tecnologia", back_populates="tecnologia_emprestavel")
    emprestimos = relationship("EmprestimoMaterial", back_populates="tecnologia_emprestavel")

class CategoriaMaterial(db.Model):
    __tablename__ = 'CategoriaMaterial'
    ID_CATEGORIA = db.Column(db.Integer, primary_key=True)
    TipoMaterial = db.Column(db.String(100), nullable=False)

    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="categoria")

class MaterialAcessivel(db.Model):
    __tablename__ = 'MaterialAcessivel'
    ID_MATERIAL = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(255), nullable=False)
    Formato = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(255), nullable=False)
    Localizacao = db.Column(db.String(255), nullable=False)
    ID_CATEGORIA = db.Column(db.Integer, db.ForeignKey('CategoriaMaterial.ID_CATEGORIA'), nullable=False)
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('BolsistaProducao.ID_BOLSISTA'))

    categoria = relationship("CategoriaMaterial", back_populates="materiais_acessiveis")
    bolsista_producao = relationship("BolsistaProducao", back_populates="materiais_acessiveis")
    disponibilizacoes = relationship("MaterialDisponibilizado", back_populates="material_acessivel")

class Curso(db.Model):
    __tablename__ = 'Curso'
    CODIGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Modalidade = db.Column(db.String(20), nullable=False)
    NivelDeFormacao = db.Column(db.String(20), nullable=False)

    matriculados = relationship("MatriculadoEm", back_populates="curso")

class TabelaFuncoes(db.Model):
    __tablename__ = 'TabelaFuncoes'
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('Cargo.ID_CARGO'), primary_key=True)
    Funcao = db.Column(db.String(255), primary_key=True)

    cargo = relationship("Cargo", back_populates="funcoes")

class MatriculadoEm(db.Model):
    __tablename__ = 'MatriculadoEm'
    CPF = db.Column(db.String(11), db.ForeignKey('Aluno.CPF'), primary_key=True)
    Codigo = db.Column(db.Integer, db.ForeignKey('Curso.CODIGO'), primary_key=True)
    Situacao = db.Column(db.String(50))
    DataInicio = db.Column(db.Date)
    DataFim = db.Column(db.Date)

    aluno = relationship("Aluno", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculados")

class EmprestimoMaterial(db.Model):
    __tablename__ = 'EmprestimoMaterial'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'), primary_key=True)
    ID_MATERIAL = db.Column(db.Integer, db.ForeignKey('TecnologiaEmprestavel.ID_TECNOLOGIA'), primary_key=True)
    DataEmprestimo = db.Column(db.Date)
    DataDevolucao = db.Column(db.Date)
    DevolucaoEstimada = db.Column(db.Date)

    pcd = relationship("PCD", back_populates="emprestimos_material")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="emprestimos")

class MaterialDisponibilizado(db.Model):
    __tablename__ = 'MaterialDisponibilizado'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'), primary_key=True)
    ID_MATERIAL = db.Column(db.Integer, db.ForeignKey('MaterialAcessivel.ID_MATERIAL'), primary_key=True)

    pcd = relationship("PCD", back_populates="materiais_disponibilizados")
    material_acessivel = relationship("MaterialAcessivel", back_populates="disponibilizacoes")

class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'DadosDeficienciaPCD'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'), primary_key=True)
    ID_DEFICIENCIA = db.Column(db.Integer, db.ForeignKey('Deficiencia.ID_DEFICIENCIA'), primary_key=True)
    Grau = db.Column(db.String(100))
    Observacoes = db.Column(db.Text)

    pcd = relationship("PCD", back_populates="dados_deficiencia")
    deficiencia = relationship("Deficiencia", back_populates="dados_pcd")

class PrestaAssistencia(db.Model):
    __tablename__ = 'PrestaAssistencia'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('PCD.ID_PCD'), primary_key=True)
    ID_ACAO = db.Column(db.Integer, db.ForeignKey('Acao.ID_ACAO'), primary_key=True)
    ID_MEMBRO_CAIN = db.Column(db.Integer, db.ForeignKey('MembroDaEquipe.ID_MEMBRO'), primary_key=True)
    DataInicio = db.Column(db.Date, primary_key=True)
    DataFim = db.Column(db.Date)

    pcd = relationship("PCD", back_populates="assistencias_prestadas")
    acao = relationship("Acao", back_populates="assistencias_prestadas")
    membro_cain = relationship("MembroDaEquipe", back_populates="assistencias_prestadas")
