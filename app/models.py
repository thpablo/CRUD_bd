from . import db
from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Date, Boolean, Text
)
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship

# Association object for MatriculadoEm
class MatriculadoEm(db.Model):
    __tablename__ = 'matriculadoem'
    cpf = Column(String(11), ForeignKey('aluno.cpf'), primary_key=True)
    codigo = Column(Integer, ForeignKey('curso.codigo'), primary_key=True)
    situacao = Column(String(50))
    datainicio = Column(Date)
    datafim = Column(Date)
    aluno = relationship('Aluno', back_populates='cursos_matriculados')
    curso = relationship('Curso', back_populates='alunos_matriculados')

# Association object for EmprestimoMaterial
class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimomaterial'
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'), primary_key=True)
    id_material = Column(Integer, ForeignKey('tecnologiaemprestavel.id_tecnologia'), primary_key=True)
    dataemprestimo = Column(Date, primary_key=True)
    datadevolucao = Column(Date)
    devolucaoestimada = Column(Date)
    pcd = relationship('PCD', back_populates='emprestimos_material')
    tecnologia = relationship('TecnologiaEmprestavel', back_populates='emprestimos')

# Association table for MaterialDisponibilizado
materialdisponibilizado = Table('materialdisponibilizado', db.metadata,
    Column('id_pcd', Integer, ForeignKey('pcd.id_pcd'), primary_key=True),
    Column('id_material', Integer, ForeignKey('materialacessivel.id_material'), primary_key=True)
)

# Association object for DadosDeficienciaPCD
class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'dadosdeficienciapcd'
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'), primary_key=True)
    id_deficiencia = Column(Integer, ForeignKey('deficiencia.id_deficiencia'), primary_key=True)
    grau = Column(String(100))
    observacoes = Column(Text)
    pcd = relationship('PCD', back_populates='dados_deficiencia')
    deficiencia = relationship('Deficiencia', back_populates='dados_pcd')

# Association object for PrestaAssistencia
class PrestaAssistencia(db.Model):
    __tablename__ = 'prestaassistencia'
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'), primary_key=True)
    id_acao = Column(Integer, ForeignKey('acao.id_acao'), primary_key=True)
    id_membro_cain = Column(Integer, ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    datainicio = Column(Date, primary_key=True)
    datafim = Column(Date)
    pcd = relationship('PCD', back_populates='assistencias')
    acao = relationship('Acao', back_populates='prestacoes_assistencia')
    membro_equipe = relationship('MembroDaEquipe', back_populates='prestacoes_assistencia')

# Association object for TabelaFuncoes
class TabelaFuncoes(db.Model):
    __tablename__ = 'tabelafuncoes'
    id_cargo = Column(Integer, ForeignKey('cargo.id_cargo'), primary_key=True)
    funcao = Column(String(255), primary_key=True)
    cargo = relationship('Cargo', back_populates='funcoes')

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    cpf = Column(String(11), primary_key=True)
    nome = Column(String(255), nullable=False)
    emails = relationship('ContatoEmails', back_populates='pessoa', cascade="all, delete-orphan")
    telefones = relationship('ContatoTelefones', back_populates='pessoa', cascade="all, delete-orphan")
    lgbt_info = relationship('PessoaLGBT', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")
    servidor = relationship('Servidor', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")
    aluno = relationship('Aluno', back_populates='pessoa', uselist=False, cascade="all, delete-orphan")

class ContatoEmails(db.Model):
    __tablename__ = 'contatoemails'
    cpf = Column(String(11), ForeignKey('pessoa.cpf'), primary_key=True)
    email = Column(String(100), primary_key=True)
    pessoa = relationship('Pessoa', back_populates='emails')

class ContatoTelefones(db.Model):
    __tablename__ = 'contatotelefones'
    cpf = Column(String(11), ForeignKey('pessoa.cpf'), primary_key=True)
    telefone = Column(String(20), primary_key=True)
    pessoa = relationship('Pessoa', back_populates='telefones')

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoalgbt'
    cpf = Column(String(11), ForeignKey('pessoa.cpf'), primary_key=True)
    nomesocial = Column(String(255), nullable=False)
    pessoa = relationship('Pessoa', back_populates='lgbt_info')

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamentosetor'
    codigo = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False)
    localizacao = Column(String(100))
    telefone = Column(String(20))
    email = Column(String(100))
    servidores = relationship('Servidor', back_populates='departamento')

class Servidor(db.Model):
    __tablename__ = 'servidor'
    cpf = Column(String(11), ForeignKey('pessoa.cpf'), primary_key=True)
    tipodecontrato = Column(String(100), nullable=False)
    codigodepartamentosetor = Column(Integer, ForeignKey('departamentosetor.codigo'), nullable=False)
    pessoa = relationship('Pessoa', back_populates='servidor')
    departamento = relationship('DepartamentoSetor', back_populates='servidores')
    docente = relationship('Docente', back_populates='servidor', uselist=False, cascade="all, delete-orphan")
    tecnico = relationship('TecnicoAdministrativo', back_populates='servidor', uselist=False, cascade="all, delete-orphan")
    terceirizado = relationship('Terceirizado', back_populates='servidor', uselist=False, cascade="all, delete-orphan")

class PCD(db.Model):
    __tablename__ = 'pcd'
    id_pcd = Column(Integer, primary_key=True)
    docente = relationship('Docente', back_populates='pcd', uselist=False)
    tecnico = relationship('TecnicoAdministrativo', back_populates='pcd', uselist=False)
    aluno = relationship('Aluno', back_populates='pcd', uselist=False)
    dados_deficiencia = relationship('DadosDeficienciaPCD', back_populates='pcd', cascade="all, delete-orphan")
    emprestimos_material = relationship('EmprestimoMaterial', back_populates='pcd', cascade="all, delete-orphan")
    materiais_disponibilizados = relationship('MaterialAcessivel', secondary=materialdisponibilizado, back_populates='pcds_com_acesso')
    assistencias = relationship('PrestaAssistencia', back_populates='pcd', cascade="all, delete-orphan")
    periodos_vinculo = relationship('PeriodoDeVinculoPCD', back_populates='pcd', cascade="all, delete-orphan")

class Docente(db.Model):
    __tablename__ = 'docente'
    cpf = Column(String(11), ForeignKey('servidor.cpf'), primary_key=True)
    siape = Column(String(8), nullable=False, unique=True)
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'))
    servidor = relationship('Servidor', back_populates='docente')
    pcd = relationship('PCD', back_populates='docente')

class MembroDaEquipe(db.Model):
    __tablename__ = 'membrodaequipe'
    id_membro = Column(Integer, primary_key=True)
    regimedetrabalho = Column(String(100), nullable=False)
    id_coordenador = Column(Integer, ForeignKey('membrodaequipe.id_membro'))
    coordenador = relationship('MembroDaEquipe', remote_side=[id_membro], backref='equipe_coordenada')
    tecnico_administrativo = relationship('TecnicoAdministrativo', back_populates='membro_equipe', uselist=False)
    terceirizado = relationship('Terceirizado', back_populates='membro_equipe', uselist=False)
    aluno = relationship('Aluno', back_populates='membro_equipe', uselist=False)
    bolsista = relationship('Bolsista', back_populates='membro_info', uselist=False, cascade="all, delete-orphan")
    estagiario = relationship('Estagiario', back_populates='membro_info', uselist=False, cascade="all, delete-orphan")
    periodos_vinculo = relationship('PeriodoDeVinculoMembro', back_populates='membro', cascade="all, delete-orphan")
    prestacoes_assistencia = relationship('PrestaAssistencia', back_populates='membro_equipe', cascade="all, delete-orphan")

class Cargo(db.Model):
    __tablename__ = 'cargo'
    id_cargo = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False)
    tecnicos = relationship('TecnicoAdministrativo', back_populates='cargo')
    terceirizados = relationship('Terceirizado', back_populates='cargo')
    funcoes = relationship('TabelaFuncoes', back_populates='cargo', cascade="all, delete-orphan")

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnicoadministrativo'
    cpf = Column(String(11), ForeignKey('servidor.cpf'), primary_key=True)
    siape = Column(String(8), nullable=False, unique=True)
    id_membro = Column(Integer, ForeignKey('membrodaequipe.id_membro'))
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'))
    id_cargo = Column(Integer, ForeignKey('cargo.id_cargo'))
    servidor = relationship('Servidor', back_populates='tecnico')
    membro_equipe = relationship('MembroDaEquipe', back_populates='tecnico_administrativo')
    pcd = relationship('PCD', back_populates='tecnico')
    cargo = relationship('Cargo', back_populates='tecnicos')

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    cpf = Column(String(11), ForeignKey('servidor.cpf'), primary_key=True)
    id_membro = Column(Integer, ForeignKey('membrodaequipe.id_membro'))
    id_cargo = Column(Integer, ForeignKey('cargo.id_cargo'))
    servidor = relationship('Servidor', back_populates='terceirizado')
    membro_equipe = relationship('MembroDaEquipe', back_populates='terceirizado')
    cargo = relationship('Cargo', back_populates='terceirizados')

class Aluno(db.Model):
    __tablename__ = 'aluno'
    cpf = Column(String(11), ForeignKey('pessoa.cpf'), primary_key=True)
    matricula = Column(String(9), nullable=False)
    id_membro = Column(Integer, ForeignKey('membrodaequipe.id_membro'))
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'))
    pessoa = relationship('Pessoa', back_populates='aluno')
    membro_equipe = relationship('MembroDaEquipe', back_populates='aluno')
    pcd = relationship('PCD', back_populates='aluno')
    cursos_matriculados = relationship('MatriculadoEm', back_populates='aluno', cascade="all, delete-orphan")

class PeriodoDeVinculoPCD(db.Model):
    __tablename__ = 'periododevinculopcd'
    datadeinicio = Column(Date, primary_key=True)
    id_pcd = Column(Integer, ForeignKey('pcd.id_pcd'), primary_key=True)
    datadefim = Column(Date)
    pcd = relationship('PCD', back_populates='periodos_vinculo')

class PeriodoDeVinculoMembro(db.Model):
    __tablename__ = 'periododevinculomembro'
    datadeinicio = Column(Date, primary_key=True)
    id_membro = Column(Integer, ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    datadefim = Column(Date)
    membro = relationship('MembroDaEquipe', back_populates='periodos_vinculo')

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    id_bolsista = Column(Integer, ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    salario = Column(MONEY, nullable=False)
    cargahoraria = Column(Integer)
    membro_info = relationship('MembroDaEquipe', back_populates='bolsista')
    producao = relationship('BolsistaProducao', back_populates='bolsista_info', uselist=False, cascade="all, delete-orphan")
    inclusao = relationship('BolsistaInclusao', back_populates='bolsista_info', uselist=False, cascade="all, delete-orphan")

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsistaproducao'
    id_bolsista = Column(Integer, ForeignKey('bolsista.id_bolsista'), primary_key=True)
    bolsista_info = relationship('Bolsista', back_populates='producao')
    materiais_produzidos = relationship('MaterialAcessivel', back_populates='bolsista_produtor')

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsistainclusao'
    id_bolsista = Column(Integer, ForeignKey('bolsista.id_bolsista'), primary_key=True)
    bolsista_info = relationship('Bolsista', back_populates='inclusao')
    relatorios = relationship('Relatorios', back_populates='bolsista', cascade="all, delete-orphan")
    horarios = relationship('Horarios', back_populates='bolsista', cascade="all, delete-orphan")

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    id_bolsista = Column(Integer, ForeignKey('bolsistainclusao.id_bolsista'), primary_key=True)
    datareferente = Column(Date, primary_key=True)
    relatorios_semanais = Column(String(1000))
    bolsista = relationship('BolsistaInclusao', back_populates='relatorios')

class Horarios(db.Model):
    __tablename__ = 'horarios'
    id_bolsista = Column(Integer, ForeignKey('bolsistainclusao.id_bolsista'), primary_key=True)
    horarios_monitoria = Column(Date, primary_key=True)
    bolsista = relationship('BolsistaInclusao', back_populates='horarios')

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    id_estagiario = Column(Integer, ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    salario = Column(MONEY, nullable=False)
    cargahoraria = Column(Integer)
    membro_info = relationship('MembroDaEquipe', back_populates='estagiario')

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    id_deficiencia = Column(Integer, primary_key=True)
    categoria = Column(String(50), nullable=False)
    dados_pcd = relationship('DadosDeficienciaPCD', back_populates='deficiencia', cascade="all, delete-orphan")

class Acao(db.Model):
    __tablename__ = 'acao'
    id_acao = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(500))
    prestacoes_assistencia = relationship('PrestaAssistencia', back_populates='acao', cascade="all, delete-orphan")

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoriatecnologia'
    id_categoria = Column(Integer, primary_key=True)
    tipocategoria = Column(String(50), nullable=False)
    tecnologias = relationship('Tecnologia', back_populates='categoria')

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    id_tecnologia = Column(Integer, primary_key=True)
    modelo = Column(String(50), nullable=False)
    nserie = Column(Integer, nullable=False)
    localizacao = Column(String(100))
    id_categoria = Column(Integer, ForeignKey('categoriatecnologia.id_categoria'), nullable=False)
    categoria = relationship('CategoriaTecnologia', back_populates='tecnologias')
    emprestavel = relationship('TecnologiaEmprestavel', back_populates='tecnologia_base', uselist=False, cascade="all, delete-orphan")

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologiaemprestavel'
    id_tecnologia = Column(Integer, ForeignKey('tecnologia.id_tecnologia'), primary_key=True)
    status = Column(Boolean, nullable=False)
    tecnologia_base = relationship('Tecnologia', back_populates='emprestavel')
    emprestimos = relationship('EmprestimoMaterial', back_populates='tecnologia', cascade="all, delete-orphan")

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoriamaterial'
    id_categoria = Column(Integer, primary_key=True)
    tipomaterial = Column(String(100), nullable=False)
    materiais = relationship('MaterialAcessivel', back_populates='categoria')

class MaterialAcessivel(db.Model):
    __tablename__ = 'materialacessivel'
    id_material = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    formato = Column(String(100), nullable=False)
    status = Column(String(255), nullable=False)
    localizacao = Column(String(255), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categoriamaterial.id_categoria'), nullable=False)
    id_bolsista = Column(Integer, ForeignKey('bolsistaproducao.id_bolsista'))
    categoria = relationship('CategoriaMaterial', back_populates='materiais')
    bolsista_produtor = relationship('BolsistaProducao', back_populates='materiais_produzidos')
    pcds_com_acesso = relationship('PCD', secondary=materialdisponibilizado, back_populates='materiais_disponibilizados')

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    modalidade = Column(String(20), nullable=False)
    niveldeformacao = Column(String(20), nullable=False)
    alunos_matriculados = relationship('MatriculadoEm', back_populates='curso', cascade="all, delete-orphan")
