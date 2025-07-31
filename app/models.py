from app import db

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    telefones = db.relationship('ContatoTelefones', backref='pessoa', lazy=True)
    emails = db.relationship('ContatoEmails', backref='pessoa', lazy=True)
    lgbt = db.relationship('PessoaLGBT', backref='pessoa', uselist=False, lazy=True)
    servidor = db.relationship('Servidor', backref='pessoa', uselist=False, lazy=True)
    aluno = db.relationship('Aluno', backref='pessoa', uselist=False, lazy=True)

class ContatoTelefones(db.Model):
    __tablename__ = 'contato_telefones'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

class ContatoEmails(db.Model):
    __tablename__ = 'contato_emails'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class PessoaLGBT(db.Model):
    __tablename__ = 'pessoa_lgbt'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    nome_social = db.Column(db.String(100), nullable=False)

class Servidor(db.Model):
    __tablename__ = 'servidor'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    tipo_contrato = db.Column(db.String(50), nullable=False)
    codigo_departamento = db.Column(db.Integer, db.ForeignKey('departamento_setor.codigo'))

class Aluno(db.Model):
    __tablename__ = 'aluno'
    cpf = db.Column(db.String(11), db.ForeignKey('pessoa.cpf'), primary_key=True)
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    chave_membro_equipe = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))
    codigo_curso = db.Column(db.Integer, db.ForeignKey('curso.codigo'))

class DepartamentoSetor(db.Model):
    __tablename__ = 'departamento_setor'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    modalidade = db.Column(db.String(50))
    nivel_formacao = db.Column(db.String(50))

class MembroDaEquipe(db.Model):
    __tablename__ = 'membro_da_equipe'
    chave = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50))
    regime_trabalho = db.Column(db.String(50))
    coordenador_chave = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'))

class PCD(db.Model):
    __tablename__ = 'pcd'
    id = db.Column(db.Integer, primary_key=True)

class Deficiencia(db.Model):
    __tablename__ = 'deficiencia'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100))

class Acao(db.Model):
    __tablename__ = 'acao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))

class CategoriaTecnologia(db.Model):
    __tablename__ = 'categoria_tecnologia'
    id = db.Column(db.Integer, primary_key=True)
    tipo_categoria = db.Column(db.String(100))

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100))
    patrimonio_ns = db.Column(db.String(100))
    localizacao = db.Column(db.String(100))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_tecnologia.id'))

class TecnologiaEmprestavel(db.Model):
    __tablename__ = 'tecnologia_emprestavel'
    id = db.Column(db.Integer, db.ForeignKey('tecnologia.id'), primary_key=True)
    status = db.Column(db.String(50))

class CategoriaMaterial(db.Model):
    __tablename__ = 'categoria_material'
    id = db.Column(db.Integer, primary_key=True)
    tipo_material = db.Column(db.String(100))

class MaterialAcessivel(db.Model):
    __tablename__ = 'material_acessivel'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    formato = db.Column(db.String(50))
    status = db.Column(db.String(50))
    localizacao = db.Column(db.String(100))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_material.id'))
    chave_bolsista = db.Column(db.Integer, db.ForeignKey('bolsista_producao.chave'))

class EmprestimoMaterial(db.Model):
    __tablename__ = 'emprestimo_material'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey('tecnologia_emprestavel.id'), primary_key=True)
    data_emprestimo = db.Column(db.Date)
    data_devolucao = db.Column(db.Date)
    devolucao_estimada = db.Column(db.Date)

class MaterialDisponibilizado(db.Model):
    __tablename__ = 'material_disponibilizado'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey('material_acessivel.id'), primary_key=True)

class DadosDeficienciaPCD(db.Model):
    __tablename__ = 'dados_deficiencia_pcd'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_deficiencia = db.Column(db.Integer, db.ForeignKey('deficiencia.id'), primary_key=True)
    grau = db.Column(db.String(50))
    observacoes = db.Column(db.String(200))

class PrestaAssistencia(db.Model):
    __tablename__ = 'presta_assistencia'
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'), primary_key=True)
    id_acao = db.Column(db.Integer, db.ForeignKey('acao.id'), primary_key=True)
    id_membro_cain = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'), primary_key=True)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)

class Docente(db.Model):
    __tablename__ = 'docente'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(20))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))

class TecnicoAdministrativo(db.Model):
    __tablename__ = 'tecnico_administrativo'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    siape = db.Column(db.String(20))
    cargo = db.Column(db.String(100))
    chave_membro_equipe = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'))
    id_pcd = db.Column(db.Integer, db.ForeignKey('pcd.id'))

class Terceirizado(db.Model):
    __tablename__ = 'terceirizado'
    cpf = db.Column(db.String(11), db.ForeignKey('servidor.cpf'), primary_key=True)
    cargo = db.Column(db.String(100))
    chave_membro_equipe = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'))

class MatriculadoEm(db.Model):
    __tablename__ = 'matriculado_em'
    cpf_aluno = db.Column(db.String(11), db.ForeignKey('aluno.cpf'), primary_key=True)
    codigo_curso = db.Column(db.Integer, db.ForeignKey('curso.codigo'), primary_key=True)
    situacao = db.Column(db.String(50))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)

class PeriodoDeVinculo(db.Model):
    __tablename__ = 'periodo_de_vinculo'
    chave_membro_equipe = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'), primary_key=True)
    data_inicio = db.Column(db.Date, primary_key=True)
    data_fim = db.Column(db.Date)

class Bolsista(db.Model):
    __tablename__ = 'bolsista'
    chave = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'), primary_key=True)
    salario = db.Column(db.Float)
    carga_horaria_semanal = db.Column(db.Integer)

class BolsistaProducao(db.Model):
    __tablename__ = 'bolsista_producao'
    chave = db.Column(db.Integer, db.ForeignKey('bolsista.chave'), primary_key=True)

class BolsistaInclusao(db.Model):
    __tablename__ = 'bolsista_inclusao'
    chave = db.Column(db.Integer, db.ForeignKey('bolsista.chave'), primary_key=True)

class Relatorios(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    chave_bolsista = db.Column(db.Integer, db.ForeignKey('bolsista_inclusao.chave'))
    relatorio_semanal = db.Column(db.String(500))

class Horarios(db.Model):
    __tablename__ = 'horarios'
    id = db.Column(db.Integer, primary_key=True)
    chave_bolsista = db.Column(db.Integer, db.ForeignKey('bolsista_inclusao.chave'))
    horario_monitoria = db.Column(db.String(100))

class Estagiario(db.Model):
    __tablename__ = 'estagiario'
    chave = db.Column(db.Integer, db.ForeignKey('membro_da_equipe.chave'), primary_key=True)
    salario = db.Column(db.Float)
    carga_horaria_semanal = db.Column(db.Integer)
