from app import db

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

class PCD(db.Model):
    __tablename__ = 'pcd'
    id = db.Column(db.Integer, primary_key=True)

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)

class Acao(db.Model):
    __tablename__ = 'acao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamento_setor'
    codigo = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    localizacao = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Cargo(db.Model):
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    modalidade = db.Column(db.String(50))
    nivel_formacao = db.Column(db.String(50))

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoriatecnologia'
    id = db.Column(db.Integer, primary_key=True)
    tipocategoria = db.Column(db.String(100), nullable=False)

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoriamaterial'
    id = db.Column(db.Integer, primary_key=True)
    tipomaterial = db.Column(db.String(100), nullable=False)

class MembroDaEquipe(db.Model):
    __tablename__ = 'membrodaequipe'
    chave = db.Column(db.String(50), primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    regimedetrabalho = db.Column(db.String(50))
    coordenador = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'))

class ContatoTelefones(db.Model):
    __tablename__ = 'contatotelefones'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    telefone = db.Column(db.String(20), primary_key=True)

class ContatoEmails(db.Model):
    __tablename__ = 'contatoemails'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    email = db.Column(db.String(100), primary_key=True)

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoalgbt'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    nomesocial = db.Column(db.String(255), nullable=False)

class Servidor(db.Model):
    __tablename__ = 'servidor'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    tipodecontrato = db.Column(db.String(50))
    codigo_departamento = db.Column(db.String(50), db.ForeignKey('departamento_setor.codigo'), nullable=False)

class Aluno(db.Model):
    __tablename__ = 'aluno'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    matricula = db.Column(db.String(50), nullable=False, unique=True)
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))

class DadosDeficiencia_PCD(db.Model):
    __tablename__ = 'dadosdeficiencia_pcd'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_deficiencia = db.Column(db.Integer, db.ForeignKey('deficiencia.id'), primary_key=True)
    grau = db.Column(db.String(50))
    observacoes = db.Column(db.Text)

class TabelaFuncoes(db.Model):
    __tablename__ = 'tabelafuncoes'
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), primary_key=True)
    funcao = db.Column(db.String(255), primary_key=True)

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(150))
    patrimonio_nserie = db.Column(db.String(100), nullable=False, unique=True)
    localizacao = db.Column(db.String(255))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoriatecnologia.id'), nullable=False)

class PeriodoDeVinculo(db.Model):
    __tablename__ = 'periododevinculo'
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), primary_key=True)
    datadeinicio = db.Column(db.Date, nullable=False, primary_key=True)
    datadefim = db.Column(db.Date)

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), primary_key=True)
    salario = db.Column(db.Numeric(10, 2))
    cargahorariasemanal = db.Column(db.Integer)

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), primary_key=True)
    salario = db.Column(db.Numeric(10, 2))
    cargahorariasemanal = db.Column(db.Integer)

class Docente(db.Model):
    __tablename__ = 'docente'
    cpf_servidor = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(20), nullable=False, unique=True)
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnicoadministrativo'
    cpf_servidor = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(20), nullable=False, unique=True)
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    cpf_servidor = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    chave_membrodaequipe = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)

class MatriculadoEm(db.Model):
    __tablename__ = 'matriculadoem'
    cpf_aluno = db.Column(db.String(11), db.ForeignKey('aluno.cpf'), primary_key=True)
    codigo_curso = db.Column(db.String(50), db.ForeignKey('curso.codigo'), primary_key=True)
    situacao = db.Column(db.String(50))
    datainicio = db.Column(db.Date, nullable=False)
    datafim = db.Column(db.Date)

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologiaemprestavel'
    id_tecnologia = db.Column(db.Integer, db.ForeignKey('tecnologia.id'), primary_key=True)
    status = db.Column(db.String(50), nullable=False)

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsistaproducao'
    chave_bolsista = db.Column(db.String(50), db.ForeignKey('bolsista.chave_membrodaequipe'), primary_key=True)

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsistainclusao'
    chave_bolsista = db.Column(db.String(50), db.ForeignKey('bolsista.chave_membrodaequipe'), primary_key=True)

class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimomaterial'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_tecnologiaemprestavel = db.Column(db.Integer, db.ForeignKey('tecnologiaemprestavel.id_tecnologia'), primary_key=True)
    dataemprestimo = db.Column(db.Date, nullable=False, primary_key=True)
    devolucaoestimada = db.Column(db.Date, nullable=False)
    datadevolucao = db.Column(db.Date)

class MaterialAcessivel(db.Model):
    __tablename__ = 'materialacessivel'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    formato = db.Column(db.String(50))
    status = db.Column(db.String(50))
    localizacao = db.Column(db.String(255))
    id_categoriamaterial = db.Column(db.Integer, db.ForeignKey('categoriamaterial.id'), nullable=False)
    chave_bolsistaproducao = db.Column(db.String(50), db.ForeignKey('bolsistaproducao.chave_bolsista'), nullable=False)

class MaterialDisponibilizado(db.Model):
    __tablename__ = 'materialdisponibilizado'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_materialacessivel = db.Column(db.Integer, db.ForeignKey('materialacessivel.id'), primary_key=True)

class PrestaAssistencia(db.Model):
    __tablename__ = 'prestaassistencia'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_acao = db.Column(db.Integer, db.ForeignKey('acao.id'), primary_key=True)
    id_membrocain = db.Column(db.String(50), db.ForeignKey('membrodaequipe.chave'), primary_key=True)
    datainicio = db.Column(db.Date, nullable=False, primary_key=True)
    datafim = db.Column(db.Date)

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    chave_bolsistainclusao = db.Column(db.String(50), db.ForeignKey('bolsistainclusao.chave_bolsista'), primary_key=True)
    relatoriosemanal = db.Column(db.Text, nullable=False)
    dataentrega = db.Column(db.Date, nullable=False, primary_key=True)

class Horarios(db.Model):
    __tablename__ = 'horarios'
    chave_bolsistainclusao = db.Column(db.String(50), db.ForeignKey('bolsistainclusao.chave_bolsista'), primary_key=True)
    horariodemonitoria = db.Column(db.String(255), nullable=False, primary_key=True)
