from app import db
from sqlalchemy.orm import relationship

# This file has been completely rewritten to align with the database schema in init.sql.
# All table and column names have been converted to lowercase to match PostgreSQL's default behavior.

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    telefones = relationship("ContatoTelefones", back_populates="pessoa", cascade="all, delete-orphan")
    emails = relationship("ContatoEmails", back_populates="pessoa", cascade="all, delete-orphan")
    pessoalgbt = relationship("PessoaLGBT", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    servidor = relationship("Servidor", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    aluno = relationship("Aluno", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")

class ContatoTelefones(db.Model):
    __tablename__ = 'contatotelefones'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    telefone = db.Column(db.String(20), primary_key=True)
    pessoa = relationship("Pessoa", back_populates="telefones")

class ContatoEmails(db.Model):
    __tablename__ = 'contatoemails'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    email = db.Column(db.String(100), primary_key=True)
    pessoa = relationship("Pessoa", back_populates="emails")

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoalgbt'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    nomesocial = db.Column(db.String(255), nullable=False)
    pessoa = relationship("Pessoa", back_populates="pessoalgbt")

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamentosetor'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    localizacao = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    servidores = relationship("Servidor", back_populates="departamento")

class Servidor(db.Model):
    __tablename__ = 'servidor'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    tipodecontrato = db.Column(db.String(100), nullable=False)
    codigodepartamento = db.Column(db.Integer, db.ForeignKey('departamentosetor.codigo'), nullable=False)
    pessoa = relationship("Pessoa", back_populates="servidor")
    departamento = relationship("DepartamentoSetor", back_populates="servidores")
    docente = relationship("Docente", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    tecnico_administrativo = relationship("TecnicoAdministrativo", back_populates="servidor", uselist=False, cascade="all, delete-orphan")
    terceirizado = relationship("Terceirizado", back_populates="servidor", uselist=False, cascade="all, delete-orphan")

class PCD(db.Model):
    __tablename__ = 'pcd'
    id_pcd = db.Column(db.Integer, primary_key=True)
    docentes = relationship("Docente", back_populates="pcd")
    tecnicos = relationship("TecnicoAdministrativo", back_populates="pcd")
    alunos = relationship("Aluno", back_populates="pcd")
    emprestimos_material = relationship("EmprestimoMaterial", back_populates="pcd")
    materiais_disponibilizados = relationship("MaterialDisponibilizado", back_populates="pcd")
    dados_deficiencia = relationship("DadosDeficienciaPCD", back_populates="pcd", cascade="all, delete-orphan")
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="pcd")

class Docente(db.Model):
    __tablename__ = 'docente'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(8), nullable=False, unique=True)
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'))
    servidor = relationship("Servidor", back_populates="docente")
    pcd = relationship("PCD", back_populates="docentes")

class MembroDaEquipe(db.Model):
    __tablename__ = 'membrodaequipe'
    id_membro = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50))
    regimedetrabalho = db.Column(db.String(100), nullable=False)
    id_coordenador = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'))
    coordenador = relationship("MembroDaEquipe", remote_side=[id_membro], back_populates="equipe_coordenada")
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
    id_cargo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    tecnicos_administrativos = relationship("TecnicoAdministrativo", back_populates="cargo")
    terceirizados = relationship("Terceirizado", back_populates="cargo")
    funcoes = relationship("TabelaFuncoes", back_populates="cargo", cascade="all, delete-orphan")

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnicoadministrativo'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(8), nullable=False, unique=True)
    id_membro = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'))
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'))
    servidor = relationship("Servidor", back_populates="tecnico_administrativo")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="tecnicos_administrativos")
    pcd = relationship("PCD", back_populates="tecnicos")
    cargo = relationship("Cargo", back_populates="tecnicos_administrativos")

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    id_membro = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'))
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'))
    servidor = relationship("Servidor", back_populates="terceirizado")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="terceirizados")
    cargo = relationship("Cargo", back_populates="terceirizados")

class Aluno(db.Model):
    __tablename__ = 'aluno'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    matricula = db.Column(db.String(9), nullable=False)
    id_membro = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'))
    pessoa = relationship("Pessoa", back_populates="aluno")
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="alunos")
    pcd = relationship("PCD", back_populates="alunos")
    matriculas = relationship("MatriculadoEm", back_populates="aluno", cascade="all, delete-orphan")

class PeriodoDeVinculo(db.Model):
    __tablename__ = 'periododevinculo'
    datadeinicio = db.Column(db.Date, primary_key=True)
    datadefim = db.Column(db.Date, nullable=False)
    id_membro = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="periodos_de_vinculo")

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    id_bolsista = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    salario = db.Column(db.Numeric, nullable=False)
    cargahoraria = db.Column(db.Integer)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="bolsista")
    producao = relationship("BolsistaProducao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")
    inclusao = relationship("BolsistaInclusao", back_populates="bolsista", uselist=False, cascade="all, delete-orphan")

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsistaproducao'
    id_bolsista = db.Column(db.Integer, db.ForeignKey('bolsista.id_bolsista'), primary_key=True)
    bolsista = relationship("Bolsista", back_populates="producao")
    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="bolsista_producao")

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsistainclusao'
    id_bolsista = db.Column(db.Integer, db.ForeignKey('bolsista.id_bolsista'), primary_key=True)
    bolsista = relationship("Bolsista", back_populates="inclusao")
    relatorios = relationship("Relatorios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")
    horarios = relationship("Horarios", back_populates="bolsista_inclusao", cascade="all, delete-orphan")

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    id_bolsista = db.Column(db.Integer, db.ForeignKey('bolsistainclusao.id_bolsista'), primary_key=True)
    datareferente = db.Column(db.Date, primary_key=True)
    relatorios_semanais = db.Column(db.String(1000))
    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="relatorios")

class Horarios(db.Model):
    __tablename__ = 'horarios'
    id_bolsista = db.Column(db.Integer, db.ForeignKey('bolsistainclusao.id_bolsista'), primary_key=True)
    horarios_monitoria = db.Column(db.Date, primary_key=True)
    bolsista_inclusao = relationship("BolsistaInclusao", back_populates="horarios")

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    id_estagiario = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    salario = db.Column(db.Numeric, nullable=False)
    cargahoraria = db.Column(db.Integer)
    membro_da_equipe = relationship("MembroDaEquipe", back_populates="estagiario")

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    id_deficiencia = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    dados_pcd = relationship("DadosDeficienciaPCD", back_populates="deficiencia")

class Acao(db.Model):
    __tablename__ = 'acao'
    id_acao = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(500))
    assistencias_prestadas = relationship("PrestaAssistencia", back_populates="acao")

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoriatecnologia'
    id_categoria = db.Column(db.Integer, primary_key=True)
    tipo_categoria = db.Column(db.String(50), nullable=False)
    tecnologias = relationship("Tecnologia", back_populates="categoria")

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    id_tecnologia = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    n_serie = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(100))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoriatecnologia.id_categoria'), nullable=False)
    categoria = relationship("CategoriaTecnologia", back_populates="tecnologias")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="tecnologia", uselist=False, cascade="all, delete-orphan")

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologiaemprestavel'
    id_tecnologia = db.Column(db.Integer, db.ForeignKey('tecnologia.id_tecnologia'), primary_key=True)
    status = db.Column(db.Boolean, nullable=False)
    tecnologia = relationship("Tecnologia", back_populates="tecnologia_emprestavel")
    emprestimos = relationship("EmprestimoMaterial", back_populates="tecnologia_emprestavel")

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoriamaterial'
    id_categoria = db.Column(db.Integer, primary_key=True)
    tipomaterial = db.Column(db.String(100), nullable=False)
    materiais_acessiveis = relationship("MaterialAcessivel", back_populates="categoria")

class MaterialAcessivel(db.Model):
    __tablename__ = 'materialacessivel'
    id_material = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    formato = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoriamaterial.id_categoria'), nullable=False)
    id_bolsista = db.Column(db.Integer, db.ForeignKey('bolsistaproducao.id_bolsista'))
    categoria = relationship("CategoriaMaterial", back_populates="materiais_acessiveis")
    bolsista_producao = relationship("BolsistaProducao", back_populates="materiais_acessiveis")
    disponibilizacoes = relationship("MaterialDisponibilizado", back_populates="material_acessivel")

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    modalidade = db.Column(db.String(20), nullable=False)
    niveldeformacao = db.Column(db.String(20), nullable=False)
    matriculados = relationship("MatriculadoEm", back_populates="curso")

class TabelaFuncoes(db.Model):
    __tablename__ = 'tabelafuncoes'
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'), primary_key=True)
    funcao = db.Column(db.String(255), primary_key=True)
    cargo = relationship("Cargo", back_populates="funcoes")

class MatriculadoEm(db.Model):
    __tablename__ = 'matriculadoem'
    cpf = db.Column(db.String(11), db.ForeignKey('aluno.cpf'), primary_key=True)
    codigo = db.Column(db.Integer, db.ForeignKey('curso.codigo'), primary_key=True)
    situacao = db.Column(db.String(50))
    datainicio = db.Column(db.Date)
    datafim = db.Column(db.Date)
    aluno = relationship("Aluno", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculados")

class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimomaterial'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'), primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey('tecnologiaemprestavel.id_tecnologia'), primary_key=True)
    dataemprestimo = db.Column(db.Date)
    datadevolucao = db.Column(db.Date)
    devolucaoestimada = db.Column(db.Date)
    pcd = relationship("PCD", back_populates="emprestimos_material")
    tecnologia_emprestavel = relationship("TecnologiaEmprestavel", back_populates="emprestimos")

class MaterialDisponibilizado(db.Model):
    __tablename__ = 'materialdisponibilizado'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'), primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey('materialacessivel.id_material'), primary_key=True)
    pcd = relationship("PCD", back_populates="materiais_disponibilizados")
    material_acessivel = relationship("MaterialAcessivel", back_populates="disponibilizacoes")

class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'dadosdeficienciapcd'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'), primary_key=True)
    id_deficiencia = db.Column(db.Integer, db.ForeignKey('deficiencia.id_deficiencia'), primary_key=True)
    grau = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    pcd = relationship("PCD", back_populates="dados_deficiencia")
    deficiencia = relationship("Deficiencia", back_populates="dados_pcd")

class PrestaAssistencia(db.Model):
    __tablename__ = 'prestaassistencia'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id_pcd'), primary_key=True)
    id_acao = db.Column(db.Integer, db.ForeignKey('acao.id_acao'), primary_key=True)
    id_membro_cain = db.Column(db.Integer, db.ForeignKey('membrodaequipe.id_membro'), primary_key=True)
    datainicio = db.Column(db.Date, primary_key=True)
    datafim = db.Column(db.Date)
    pcd = relationship("PCD", back_populates="assistencias_prestadas")
    acao = relationship("Acao", back_populates="assistencias_prestadas")
    membro_cain = relationship("MembroDaEquipe", back_populates="assistencias_prestadas")
