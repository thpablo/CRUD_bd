from app import db
from sqlalchemy.orm import relationship

# This file has been completely rewritten to align with the database schema in init.sql.
# Naming conventions for tables have been converted to lowercase to match PostgreSQL's default behavior.
# Relationships are defined with back_populates for clarity and consistency.

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    CPF = db.Column(db.String(11), primary_key=True)
    Nome = db.Column(db.String(255), nullable=False)

    telefones = relationship("ContatoTelefones", back_populates="pessoa", cascade="all, delete-orphan")
    emails = relationship("ContatoEmails", back_populates="pessoa", cascade="all, delete-orphan")
    pessoalgbt = relationship("PessoaLGBT", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    servidor = relationship("Servidor", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    aluno = relationship("Aluno", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")

class ContatoTelefones(db.Model):
    __tablename__ = 'contatotelefones'
    CPF = db.Column(db.String(11), db.ForeignKey('pessoa.CPF'), primary_key=True)
    Telefone = db.Column(db.String(20), primary_key=True)
    pessoa = relationship("Pessoa", back_populates="telefones")

class ContatoEmails(db.Model):
    __tablename__ = 'contatoemails'
    CPF = db.Column(db.String(11), db.ForeignKey('pessoa.CPF'), primary_key=True)
    Email = db.Column(db.String(100), primary_key=True)
    pessoa = relationship("Pessoa", back_populates="emails")

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoalgbt'
    CPF = db.Column(db.String(11), db.ForeignKey('pessoa.CPF'), primary_key=True)
    NomeSocial = db.Column(db.String(255), nullable=False)
    pessoa = relationship("Pessoa", back_populates="pessoalgbt")

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamentosetor'
    CODIGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    Localizacao = db.Column(db.String(100), nullable=False)
    Telefone = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    servidores = relationship("Servidor", back_populates="departamento")

class Servidor(db.Model):
    __tablename__ = 'servidor'
    CPF = db.Column(db.String(11), db.ForeignKey('pessoa.CPF'), primary_key=True)
    TipoDeContrato = db.Column(db.String(100), nullable=False)
    CodigoDepartamento = db.Column(db.Integer, db.ForeignKey('departamentosetor.CODIGO'), nullable=False)
    pessoa = relationship("Pessoa", back_populates="servidor")
    departamento = relationship("DepartamentoSetor", back_populates="servidores")
    docente = relationship("Docente", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    tecnico_administrativo = relationship("TecnicoAdministrativo", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    terceirizado = relationship("Terceirizado", back_populates="servidor", uselist=False, cascade="all, delete-orphan")

class PCD(db.Model):
    __tablename__ = 'pcd'
    ID_PCD = db.Column(db.Integer, primary_key=True)
    docentes = relationship("Docente", back_populates="pcd")
    tecnicos = relationship("TecnicoAdministrativo", back_populates="pcd")
    alunos = relationship("Aluno", back_populates="pcd")
    emprestimos_material = relationship("EmprestimoMaterial", back_populates="pcd")
    materiais_disponibilizados = relationship("MaterialDisponibilizado", back_populates="pcd")
    dados_deficiencia = relationship("DadosDeficienciaPCD", back_populates="pcd", cascade="all, delete-orphan")
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="pcd")

class Docente(db.Model):
    __tablename__ = 'docente'
    CPF = db.Column(db.String(11), db.ForeignKey('servidor.CPF'), primary_key=True)
    SIAPE = db.Column(db.String(8), nullable=False, unique=True)
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'))
    servidor = relationship("Servidor", back_populates="docente")
    pcd = relationship("PCD", back_populates="docentes")

class MembroDaEquipe(db.Model):
    __tablename__ = 'membrodaequipe'
    ID_MEMBRO = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(50))
    RegimeDeTrabalho = db.Column(db.String(100), nullable=False)
    ID_COORDENADOR = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'))
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
    __tablename__ = 'cargo'
    ID_CARGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    tecnicos_administrativos = relationship("TecnicoAdministrativo", back_populates="cargo")
    terceirizados = relationship("Terceirizado", back_populates="cargo")
    funcoes = relationship("TabelaFuncoes", back_populates="cargo", cascade="all, delete-orphan")

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnicoadministrativo'
    CPF = db.Column(db.String(11), db.ForeignKey('servidor.CPF'), primary_key=True)
    SIAPE = db.Column(db.String(8), nullable=False, unique=True)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'))
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('cargo.ID_CARGO'))
    servidor = relationship("Servidor", back_populates="tecnico_administrativo")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="tecnicos_administrativos")
    pcd = relationship("PCD", back_populates="tecnicos")
    cargo = relationship("Cargo", back_populates="tecnicos_administrativos")

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    CPF = db.Column(db.String(11), db.ForeignKey('servidor.CPF'), primary_key=True)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('cargo.ID_CARGO'))
    servidor = relationship("Servidor", back_populates="terceirizado")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="terceirizados")
    cargo = relationship("Cargo", back_populates="terceirizados")

class Aluno(db.Model):
    __tablename__ = 'aluno'
    CPF = db.Column(db.String(11), db.ForeignKey('pessoa.CPF'), primary_key=True)
    Matricula = db.Column(db.String(9), nullable=False)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'))
    pessoa = relationship("Pessoa", back_populates="aluno")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="alunos")
    pcd = relationship("PCD", back_populates="alunos")
    matriculas = relationship("MatriculadoEm", back_populates="aluno", cascade="all, delete-orphan")

class PeriodoDeVinculo(db.Model):
    __tablename__ = 'periododevinculo'
    DataDeInicio = db.Column(db.Date, primary_key=True)
    DataDeFim = db.Column(db.Date, nullable=False)
    ID_MEMBRO = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="periodos_de_vinculo")

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    Salario = db.Column(db.Numeric, nullable=False)
    CargaHoraria = db.Column(db.Integer)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="bolsista")
    producao = relationship("BolsistaProducao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")
    inclusao = relationship("BolsistaInclusao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsistaproducao'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('bolsista.ID_BOLSISTA'), primary_key=True)
    bolsista = relationship("Bolsista", back_populates="producao")
    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="bolsista_producao")

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsistainclusao'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('bolsista.ID_BOLSISTA'), primary_key=True)
    bolsista = relationship("Bolsista", back_populates="inclusao")
    relatorios = relationship("Relatorios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")
    horarios = relationship("Horarios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('bolsistainclusao.ID_BOLSISTA'), primary_key=True)
    DataReferente = db.Column(db.Date, primary_key=True)
    Relatorios_Semanais = db.Column(db.String(1000))
    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="relatorios")

class Horarios(db.Model):
    __tablename__ = 'horarios'
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('bolsistainclusao.ID_BOLSISTA'), primary_key=True)
    Horarios_Monitoria = db.Column(db.Date, primary_key=True)
    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="horarios")

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    ID_ESTAGIARIO = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    Salario = db.Column(db.Numeric, nullable=False)
    CargaHoraria = db.Column(db.Integer)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="estagiario")

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    ID_DEFICIENCIA = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(50), nullable=False)
    dados_pcd = relationship("DadosDeficienciaPCD", back_populates="deficiencia")

class Acao(db.Model):
    __tablename__ = 'acao'
    ID_ACAO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Descricao = db.Column(db.String(500))
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="acao")

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoriatecnologia'
    ID_CATEGORIA = db.Column(db.Integer, primary_key=True)
    Tipo_Categoria = db.Column(db.String(50), nullable=False)
    tecnologias = relationship("Tecnologia", back_populates="categoria")

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    ID_TECNOLOGIA = db.Column(db.Integer, primary_key=True)
    Modelo = db.Column(db.String(50), nullable=False)
    N_Serie = db.Column(db.Integer, nullable=False)
    Localizacao = db.Column(db.String(100))
    ID_Categoria = db.Column(db.Integer, db.ForeignKey('categoriatecnologia.ID_CATEGORIA'), nullable=False)
    categoria = relationship("CategoriaTecnologia", back_populates="tecnologias")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="tecnologia", uselist=False, cascade="all, delete-orphan")

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologiaemprestavel'
    ID_TECNOLOGIA = db.Column(db.Integer, db.ForeignKey('tecnologia.ID_TECNOLOGIA'), primary_key=True)
    STATUS = db.Column(db.Boolean, nullable=False)
    tecnologia = relationship("Tecnologia", back_populates="tecnologia_emprestavel")
    emprestimos = relationship("EmprestimoMaterial", back_populates="tecnologia_emprestavel")

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoriamaterial'
    ID_CATEGORIA = db.Column(db.Integer, primary_key=True)
    TipoMaterial = db.Column(db.String(100), nullable=False)
    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="categoria")

class MaterialAcessivel(db.Model):
    __tablename__ = 'materialacessivel'
    ID_MATERIAL = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(255), nullable=False)
    Formato = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(255), nullable=False)
    Localizacao = db.Column(db.String(255), nullable=False)
    ID_CATEGORIA = db.Column(db.Integer, db.ForeignKey('categoriamaterial.ID_CATEGORIA'), nullable=False)
    ID_BOLSISTA = db.Column(db.Integer, db.ForeignKey('bolsistaproducao.ID_BOLSISTA'))
    categoria = relationship("CategoriaMaterial", back_populates="materiais_acessiveis")
    bolsista_producao = relationship("BolsistaProducao", back_populates="materiais_acessiveis")
    disponibilizacoes = relationship("MaterialDisponibilizado", back_populates="material_acessivel")

class Curso(db.Model):
    __tablename__ = 'curso'
    CODIGO = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(50), nullable=False)
    Modalidade = db.Column(db.String(20), nullable=False)
    NivelDeFormacao = db.Column(db.String(20), nullable=False)
    matriculados = relationship("MatriculadoEm", back_populates="curso")

class TabelaFuncoes(db.Model):
    __tablename__ = 'tabelafuncoes'
    ID_CARGO = db.Column(db.Integer, db.ForeignKey('cargo.ID_CARGO'), primary_key=True)
    Funcao = db.Column(db.String(255), primary_key=True)
    cargo = relationship("Cargo", back_populates="funcoes")

class MatriculadoEm(db.Model):
    __tablename__ = 'matriculadoem'
    CPF = db.Column(db.String(11), db.ForeignKey('aluno.CPF'), primary_key=True)
    Codigo = db.Column(db.Integer, db.ForeignKey('curso.CODIGO'), primary_key=True)
    Situacao = db.Column(db.String(50))
    DataInicio = db.Column(db.Date)
    DataFim = db.Column(db.Date)
    aluno = relationship("Aluno", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculados")

class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimomaterial'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_MATERIAL = db.Column(db.Integer, db.ForeignKey('tecnologiaemprestavel.ID_TECNOLOGIA'), primary_key=True)
    DataEmprestimo = db.Column(db.Date)
    DataDevolucao = db.Column(db.Date)
    DevolucaoEstimada = db.Column(db.Date)
    pcd = relationship("PCD", back_populates="emprestimos_material")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="emprestimos")

class MaterialDisponibilizado(db.Model):
    __tablename__ = 'materialdisponibilizado'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_MATERIAL = db.Column(db.Integer, db.ForeignKey('materialacessivel.ID_MATERIAL'), primary_key=True)
    pcd = relationship("PCD", back_populates="materiais_disponibilizados")
    material_acessivel = relationship("MaterialAcessivel", back_populates="disponibilizacoes")

class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'dadosdeficienciapcd'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_DEFICIENCIA = db.Column(db.Integer, db.ForeignKey('deficiencia.ID_DEFICIENCIA'), primary_key=True)
    Grau = db.Column(db.String(100))
    Observacoes = db.Column(db.Text)
    pcd = relationship("PCD", back_populates="dados_deficiencia")
    deficiencia = relationship("Deficiencia", back_populates="dados_pcd")

class PrestaAssistencia(db.Model):
    __tablename__ = 'prestaassistencia'
    ID_PCD = db.Column(db.Integer, db.ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_ACAO = db.Column(db.Integer, db.ForeignKey('acao.ID_ACAO'), primary_key=True)
    ID_MEMBRO_CAIN = db.Column(db.Integer, db.ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    DataInicio = db.Column(db.Date, primary_key=True)
    DataFim = db.Column(db.Date)
    pcd = relationship("PCD", back_populates="assistencias_prestadas")
    acao = relationship("Acao", back_populates="assistencias_prestadas")
    membro_cain = relationship("MembroDaEquipe", back_populates="assistencias_prestadas")
