from . import db
from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Date, Boolean, Text
)
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship

# Association object for MatriculadoEm
class MatriculadoEm(db.Model):
    __tablename__ = 'matriculadoem'
    CPF = Column(String(11), ForeignKey('aluno.CPF'), primary_key=True)
    Codigo = Column(Integer, ForeignKey('curso.CODIGO'), primary_key=True)
    Situacao = Column(String(50))
    DataInicio = Column(Date)
    DataFim = Column(Date)
    aluno = relationship('Aluno', back_populates='cursos_matriculados')
    curso = relationship('Curso', back_populates='alunos_matriculados')

# Association object for EmprestimoMaterial
class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimomaterial'
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_MATERIAL = Column(Integer, ForeignKey('tecnologiaemprestavel.ID_TECNOLOGIA'), primary_key=True)
    DataEmprestimo = Column(Date, primary_key=True)
    DataDevolucao = Column(Date)
    DevolucaoEstimada = Column(Date)
    pcd = relationship('PCD', back_populates='emprestimos_material')
    tecnologia = relationship('TecnologiaEmprestavel', back_populates='emprestimos')

# Association table for MaterialDisponibilizado
MaterialDisponibilizado = Table('materialdisponibilizado', db.metadata,
    Column('ID_PCD', Integer, ForeignKey('pcd.ID_PCD'), primary_key=True),
    Column('ID_MATERIAL', Integer, ForeignKey('materialacessivel.ID_MATERIAL'), primary_key=True)
)

# Association object for DadosDeficienciaPCD
class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'dadosdeficienciapcd'
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_DEFICIENCIA = Column(Integer, ForeignKey('deficiencia.ID_DEFICIENCIA'), primary_key=True)
    Grau = Column(String(100))
    Observacoes = Column(Text)
    pcd = relationship('PCD', back_populates='dados_deficiencia')
    deficiencia = relationship('Deficiencia', back_populates='dados_pcd')

# Association object for PrestaAssistencia
class PrestaAssistencia(db.Model):
    __tablename__ = 'prestaassistencia'
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'), primary_key=True)
    ID_ACAO = Column(Integer, ForeignKey('acao.ID_ACAO'), primary_key=True)
    ID_MEMBRO_CAIN = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    DataInicio = Column(Date, primary_key=True)
    DataFim = Column(Date)
    pcd = relationship('PCD', back_populates='assistencias')
    acao = relationship('Acao', back_populates='prestacoes_assistencia')
    membro_equipe = relationship('MembroDaEquipe', back_populates='prestacoes_assistencia')

# Association object for TabelaFuncoes
class TabelaFuncoes(db.Model):
    __tablename__ = 'tabelafuncoes'
    ID_CARGO = Column(Integer, ForeignKey('cargo.ID_CARGO'), primary_key=True)
    Funcao = Column(String(255), primary_key=True)
    cargo = relationship('Cargo', back_populates='funcoes')

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    CPF = Column(String(11), primary_key=True)
    Nome = Column(String(255), nullable=False)
    emails = relationship('ContatoEmails', back_populates='pessoa', cascade="all, delete-orphan")
    telefones = relationship('ContatoTelefones', back_populates='pessoa', cascade="all, delete-orphan")
    lgbt_info = relationship('PessoaLGBT', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")
    servidor = relationship('Servidor', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")
    aluno = relationship('Aluno', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")

class ContatoEmails(db.Model):
    __tablename__ = 'contatoemails'
    CPF = Column(String(11), ForeignKey('pessoa.CPF'), primary_key=True)
    Email = Column(String(100), primary_key=True)
    pessoa = relationship('Pessoa', back_populates='emails')

class ContatoTelefones(db.Model):
    __tablename__ = 'contatotelefones'
    CPF = Column(String(11), ForeignKey('pessoa.CPF'), primary_key=True)
    Telefone = Column(String(20), primary_key=True)
    pessoa = relationship('Pessoa', back_populates='telefones')

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoalgbt'
    CPF = Column(String(11), ForeignKey('pessoa.CPF'), primary_key=True)
    NomeSocial = Column(String(255), nullable=False)
    pessoa = relationship('Pessoa', back_populates='lgbt_info')

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamentosetor'
    CODIGO = Column(Integer, primary_key=True)
    Nome = Column(String(60), nullable=False)
    Localizacao = Column(String(100))
    Telefone = Column(String(20))
    Email = Column(String(100))
    servidores = relationship('Servidor', back_populates='departamento')

class Servidor(db.Model):
    __tablename__ = 'servidor'
    CPF = Column(String(11), ForeignKey('pessoa.CPF'), primary_key=True)
    TipoDeContrato = Column(String(100), nullable=False)
    CodigoDepartamentoSetor = Column(Integer, ForeignKey('departamentosetor.CODIGO'), nullable=False)
    pessoa = relationship('Pessoa', back_populates='servidor')
    departamento = relationship('DepartamentoSetor', back_populates='servidores')
    docente = relationship('Docente', back_populates='servidor', uselist=False, cascade="all, delete-orphan")
    tecnico = relationship('TecnicoAdministrativo', back_populates='servidor', uselist=False, cascade="all, delete-orphan")
    terceirizado = relationship('Terceirizado', back_populates='servidor', uselist=False, cascade="all, delete-orphan")

class PCD(db.Model):
    __tablename__ = 'pcd'
    ID_PCD = Column(Integer, primary_key=True)
    docente = relationship('Docente', back_populates='pcd', uselist=False)
    tecnico = relationship('TecnicoAdministrativo', back_populates='pcd', uselist=False)
    aluno = relationship('Aluno', back_populates='pcd', uselist=False)
    dados_deficiencia = relationship('DadosDeficienciaPCD', back_populates='pcd', cascade="all, delete-orphan")
    emprestimos_material = relationship('EmprestimoMaterial', back_populates='pcd', cascade="all, delete-orphan")
    materiais_disponibilizados = relationship('MaterialAcessivel', secondary=MaterialDisponibilizado, back_populates='pcds_com_acesso')
    assistencias = relationship('PrestaAssistencia', back_populates='pcd', cascade="all, delete-orphan")
    periodos_vinculo = relationship('PeriodoDeVinculoPCD', back_populates='pcd', cascade="all, delete-orphan")

class Docente(db.Model):
    __tablename__ = 'docente'
    CPF = Column(String(11), ForeignKey('servidor.CPF'), primary_key=True)
    SIAPE = Column(String(8), nullable=False, unique=True)
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'))
    servidor = relationship('Servidor', back_populates='docente')
    pcd = relationship('PCD', back_populates='docente')

class MembroDaEquipe(db.Model):
    __tablename__ = 'membrodaequipe'
    ID_MEMBRO = Column(Integer, primary_key=True)
    RegimeDeTrabalho = Column(String(100), nullable=False)
    Categoria = Column(String(100))
    ID_COORDENADOR = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'))
    coordenador = relationship('MembroDaEquipe', remote_side=[ID_MEMBRO], backref='equipe_coordenada')
    tecnico_administrativo = relationship('TecnicoAdministrativo', back_populates='membro_equipe', uselist=False)
    terceirizado = relationship('Terceirizado', back_populates='membro_equipe', uselist=False)
    aluno = relationship('Aluno', back_populates='membro_equipe', uselist=False)
    bolsista = relationship('Bolsista', back_populates='membro_info', uselist=False, cascade="all, delete-orphan")
    estagiario = relationship('Estagiario', back_populates='membro_info', uselist=False, cascade="all, delete-orphan")
    periodos_vinculo = relationship('PeriodoDeVinculoMembro', back_populates='membro', cascade="all, delete-orphan")
    prestacoes_assistencia = relationship('PrestaAssistencia', back_populates='membro_equipe', cascade="all, delete-orphan")

class Cargo(db.Model):
    __tablename__ = 'cargo'
    ID_CARGO = Column(Integer, primary_key=True)
    Nome = Column(String(60), nullable=False)
    tecnicos = relationship('TecnicoAdministrativo', back_populates='cargo')
    terceirizados = relationship('Terceirizado', back_populates='cargo')
    funcoes = relationship('TabelaFuncoes', back_populates='cargo', cascade="all, delete-orphan")

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnicoadministrativo'
    CPF = Column(String(11), ForeignKey('servidor.CPF'), primary_key=True)
    SIAPE = Column(String(8), nullable=False, unique=True)
    ID_MEMBRO = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'))
    ID_CARGO = Column(Integer, ForeignKey('cargo.ID_CARGO'))
    servidor = relationship('Servidor', back_populates='tecnico')
    membro_equipe = relationship('MembroDaEquipe', back_populates='tecnico_administrativo')
    pcd = relationship('PCD', back_populates='tecnico')
    cargo = relationship('Cargo', back_populates='tecnicos')

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    CPF = Column(String(11), ForeignKey('servidor.CPF'), primary_key=True)
    ID_MEMBRO = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_CARGO = Column(Integer, ForeignKey('cargo.ID_CARGO'))
    servidor = relationship('Servidor', back_populates='terceirizado')
    membro_equipe = relationship('MembroDaEquipe', back_populates='terceirizado')
    cargo = relationship('Cargo', back_populates='terceirizados')

class Aluno(db.Model):
    __tablename__ = 'aluno'
    CPF = Column(String(11), ForeignKey('pessoa.CPF'), primary_key=True)
    Matricula = Column(String(9), nullable=False)
    ID_MEMBRO = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'))
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'))
    pessoa = relationship('Pessoa', back_populates='aluno')
    membro_equipe = relationship('MembroDaEquipe', back_populates='aluno')
    pcd = relationship('PCD', back_populates='aluno')
    cursos_matriculados = relationship('MatriculadoEm', back_populates='aluno', cascade="all, delete-orphan")

class PeriodoDeVinculoPCD(db.Model):
    __tablename__ = 'periododevinculopcd'
    DataDeInicio = Column(Date, primary_key=True)
    ID_PCD = Column(Integer, ForeignKey('pcd.ID_PCD'), primary_key=True)
    DataDeFim = Column(Date)
    pcd = relationship('PCD', back_populates='periodos_vinculo')

class PeriodoDeVinculoMembro(db.Model):
    __tablename__ = 'periododevinculomembro'
    DataDeInicio = Column(Date, primary_key=True)
    ID_MEMBRO = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    DataDeFim = Column(Date)
    membro = relationship('MembroDaEquipe', back_populates='periodos_vinculo')

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    ID_BOLSISTA = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    Salario = Column(MONEY, nullable=False)
    CargaHoraria = Column(Integer)
    membro_info = relationship('MembroDaEquipe', back_populates='bolsista')
    producao = relationship('BolsistaProducao', back_populates='bolsista_info', uselist=False, cascade="all, delete-orphan")
    inclusao = relationship('BolsistaInclusao', back_populates='bolsista_info', uselist=False, cascade="all, delete-orphan")

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsistaproducao'
    ID_BOLSISTA = Column(Integer, ForeignKey('bolsista.ID_BOLSISTA'), primary_key=True)
    bolsista_info = relationship('Bolsista', back_populates='producao')
    materiais_produzidos = relationship('MaterialAcessivel', back_populates='bolsista_produtor')

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsistainclusao'
    ID_BOLSISTA = Column(Integer, ForeignKey('bolsista.ID_BOLSISTA'), primary_key=True)
    bolsista_info = relationship('Bolsista', back_populates='inclusao')
    relatorios = relationship('Relatorios', back_populates='bolsista', cascade="all, delete-orphan")
    horarios = relationship('Horarios', back_populates='bolsista', cascade="all, delete-orphan")

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    ID_BOLSISTA = Column(Integer, ForeignKey('bolsistainclusao.ID_BOLSISTA'), primary_key=True)
    DataReferente = Column(Date, primary_key=True)
    Relatorios_Semanais = Column(String(1000))
    bolsista = relationship('BolsistaInclusao', back_populates='relatorios')

class Horarios(db.Model):
    __tablename__ = 'horarios'
    ID_BOLSISTA = Column(Integer, ForeignKey('bolsistainclusao.ID_BOLSISTA'), primary_key=True)
    Horarios_Monitoria = Column(Date, primary_key=True)
    bolsista = relationship('BolsistaInclusao', back_populates='horarios')

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    ID_ESTAGIARIO = Column(Integer, ForeignKey('membrodaequipe.ID_MEMBRO'), primary_key=True)
    Salario = Column(MONEY, nullable=False)
    CargaHoraria = Column(Integer)
    membro_info = relationship('MembroDaEquipe', back_populates='estagiario')

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    ID_DEFICIENCIA = Column(Integer, primary_key=True)
    Categoria = Column(String(50), nullable=False)
    dados_pcd = relationship('DadosDeficienciaPCD', back_populates='deficiencia', cascade="all, delete-orphan")

class Acao(db.Model):
    __tablename__ = 'acao'
    ID_ACAO = Column(Integer, primary_key=True)
    Nome = Column(String(50), nullable=False)
    Descricao = Column(String(500))
    prestacoes_assistencia = relationship('PrestaAssistencia', back_populates='acao', cascade="all, delete-orphan")

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoriatecnologia'
    ID_CATEGORIA = Column(Integer, primary_key=True)
    Tipo_Categoria = Column(String(50), nullable=False)
    tecnologias = relationship('Tecnologia', back_populates='categoria')

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    ID_TECNOLOGIA = Column(Integer, primary_key=True)
    Modelo = Column(String(50), nullable=False)
    N_Serie = Column(Integer, nullable=False)
    Localizacao = Column(String(100))
    ID_Categoria = Column(Integer, ForeignKey('categoriatecnologia.ID_CATEGORIA'), nullable=False)
    categoria = relationship('CategoriaTecnologia', back_populates='tecnologias')
    emprestavel = relationship('TecnologiaEmprestavel', back_populates='tecnologia_base', uselist=False, cascade="all, delete-orphan")

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologiaemprestavel'
    ID_TECNOLOGIA = Column(Integer, ForeignKey('tecnologia.ID_TECNOLOGIA'), primary_key=True)
    STATUS = Column(Boolean, nullable=False)
    tecnologia_base = relationship('Tecnologia', back_populates='emprestavel')
    emprestimos = relationship('EmprestimoMaterial', back_populates='tecnologia', cascade="all, delete-orphan")

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoriamaterial'
    ID_CATEGORIA = Column(Integer, primary_key=True)
    TipoMaterial = Column(String(100), nullable=False)
    materiais = relationship('MaterialAcessivel', back_populates='categoria')

class MaterialAcessivel(db.Model):
    __tablename__ = 'materialacessivel'
    ID_MATERIAL = Column(Integer, primary_key=True)
    Titulo = Column(String(255), nullable=False)
    Formato = Column(String(100), nullable=False)
    Status = Column(String(255), nullable=False)
    Localizacao = Column(String(255), nullable=False)
    ID_CATEGORIA = Column(Integer, ForeignKey('categoriamaterial.ID_CATEGORIA'), nullable=False)
    ID_BOLSISTA = Column(Integer, ForeignKey('bolsistaproducao.ID_BOLSISTA'))
    categoria = relationship('CategoriaMaterial', back_populates='materiais')
    bolsista_produtor = relationship('BolsistaProducao', back_populates='materiais_produzidos')
    pcds_com_acesso = relationship('PCD', secondary=MaterialDisponibilizado, back_populates='materiais_disponibilizados')

class Curso(db.Model):
    __tablename__ = 'curso'
    CODIGO = Column(Integer, primary_key=True)
    Nome = Column(String(50), nullable=False)
    Modalidade = Column(String(20), nullable=False)
    NivelDeFormacao = Column(String(20), nullable=False)
    alunos_matriculados = relationship('MatriculadoEm', back_populates='curso', cascade="all, delete-orphan")
