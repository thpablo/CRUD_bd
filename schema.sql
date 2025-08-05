-- O CPF é a chave primária desta tabela.
CREATE TABLE Pessoa (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(255)
);

-- O CPF é uma chave estrangeira que referencia a tabela Pessoa.
-- A combinação de CPF e Telefones pode ser considerada uma chave primária composta.
CREATE TABLE ContatoTelefones (
    CPF VARCHAR(11),
    Telefones VARCHAR(20),
    PRIMARY KEY (CPF, Telefones),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF)
);

-- O CPF é uma chave estrangeira que referencia a tabela Pessoa.
-- A combinação de CPF e E-mails pode ser considerada uma chave primária composta.
CREATE TABLE ContatoEmails (
    CPF VARCHAR(11),
    E_mails VARCHAR(255),
    PRIMARY KEY (CPF, E_mails),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF)
);

-- O CPF é tanto a chave primária quanto uma chave estrangeira que referencia a tabela Pessoa.
CREATE TABLE PessoaLGBT (
    CPF VARCHAR(11) PRIMARY KEY,
    NomeSocial VARCHAR(255),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF)
);

-- A Chave é a chave primária desta tabela.
CREATE TABLE MembroDaEquipe (
    Chave INT PRIMARY KEY,
    Categoria VARCHAR(255),
    RegimeDeTrabalho VARCHAR(255),
    Coordenador INT,
    FOREIGN KEY (Coordenador) REFERENCES MembroDaEquipe(Chave)
);

-- O Código é a chave primária desta tabela.
CREATE TABLE Departamento_Setor (
    Codigo VARCHAR(255) PRIMARY KEY,
    Nome VARCHAR(255),
    Localizacao VARCHAR(255),
    Telefone VARCHAR(20),
    E_mail VARCHAR(255)
);

-- O CPF é a chave primária e também uma chave estrangeira que referencia a tabela Pessoa.
-- O Código é uma chave estrangeira que referencia a tabela Departamento_Setor.
CREATE TABLE Servidor (
    CPF VARCHAR(11) PRIMARY KEY,
    TipodeContrato VARCHAR(255),
    Codigo VARCHAR(255),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF),
    FOREIGN KEY (Codigo) REFERENCES Departamento_Setor(Codigo)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE PCD (
    ID INT PRIMARY KEY
);

-- O CPF é a chave primária e também uma chave estrangeira que referencia a tabela Servidor.
-- O ID é uma chave estrangeira que referencia a tabela PCD.
CREATE TABLE Docente (
    CPF VARCHAR(11) PRIMARY KEY,
    SIAPE VARCHAR(255),
    ID INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF),
    FOREIGN KEY (ID) REFERENCES PCD(ID)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE Cargo (
    ID INT PRIMARY KEY,
    Nome VARCHAR(255)
);

-- O CPF é a chave primária e também uma chave estrangeira que referencia a tabela Servidor.
-- A Chave é uma chave estrangeira que referencia a tabela MembroDaEquipe.
-- O ID é uma chave estrangeira que referencia a tabela PCD.
-- O IDCargo é uma chave estrangeira que referencia a tabela Cargo.
CREATE TABLE TecnicoAdministrativo (
    CPF VARCHAR(11) PRIMARY KEY,
    SIAPE VARCHAR(255),
    Chave INT,
    ID INT,
    IDCargo INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF),
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave),
    FOREIGN KEY (ID) REFERENCES PCD(ID),
    FOREIGN KEY (IDCargo) REFERENCES Cargo(ID)
);

-- O CPF é a chave primária e também uma chave estrangeira que referencia a tabela Servidor.
-- A Chave é uma chave estrangeira que referencia a tabela MembroDaEquipe.
-- O ID é uma chave estrangeira que referencia a tabela Cargo.
CREATE TABLE Terceirizado (
    CPF VARCHAR(11) PRIMARY KEY,
    Chave INT,
    ID INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF),
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave),
    FOREIGN KEY (ID) REFERENCES Cargo(ID)
);

-- O CPF é a chave primária e também uma chave estrangeira que referencia a tabela Pessoa.
-- A Chave é uma chave estrangeira que referencia a tabela MembroDaEquipe.
-- O ID é uma chave estrangeira que referencia a tabela PCD.
CREATE TABLE Aluno (
    CPF VARCHAR(11) PRIMARY KEY,
    Matricula VARCHAR(255),
    Chave INT,
    ID INT,
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF),
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave),
    FOREIGN KEY (ID) REFERENCES PCD(ID)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela MembroDaEquipe.
CREATE TABLE PeriodoDeVinculo (
    Chave INT PRIMARY KEY,
    DataDeInicio DATE,
    DataDeFim DATE,
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela MembroDaEquipe.
CREATE TABLE Bolsista (
    Chave INT PRIMARY KEY,
    Salario DECIMAL(10, 2),
    CargaHorariaSemanal INT,
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela Bolsista.
CREATE TABLE BolsistaProducao (
    Chave INT PRIMARY KEY,
    FOREIGN KEY (Chave) REFERENCES Bolsista(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela Bolsista.
CREATE TABLE BolsistaInclusao (
    Chave INT PRIMARY KEY,
    FOREIGN KEY (Chave) REFERENCES Bolsista(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela BolsistaInclusao.
CREATE TABLE Relatorios (
    Chave INT PRIMARY KEY,
    RelatoriosSemanais TEXT,
    FOREIGN KEY (Chave) REFERENCES BolsistaInclusao(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela BolsistaInclusao.
CREATE TABLE Horarios (
    Chave INT PRIMARY KEY,
    HorariosDeMonitoria VARCHAR(255),
    FOREIGN KEY (Chave) REFERENCES BolsistaInclusao(Chave)
);

-- A Chave é a chave primária e também uma chave estrangeira que referencia a tabela MembroDaEquipe.
CREATE TABLE Estagiario (
    Chave INT PRIMARY KEY,
    Salario DECIMAL(10, 2),
    CargaHorariaSemanal INT,
    FOREIGN KEY (Chave) REFERENCES MembroDaEquipe(Chave)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE Deficiencia (
    ID INT PRIMARY KEY,
    Categoria VARCHAR(255)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE Acao (
    ID INT PRIMARY KEY,
    Nome VARCHAR(255),
    Descricao TEXT
);

-- O ID é a chave primária desta tabela.
CREATE TABLE CategoriaTecnologia (
    ID INT PRIMARY KEY,
    TipoCategoria VARCHAR(255)
);

-- O ID é a chave primária desta tabela.
-- IDCategoria é uma chave estrangeira que referencia a tabela CategoriaTecnologia.
CREATE TABLE Tecnologia (
    ID INT PRIMARY KEY,
    Modelo VARCHAR(255),
    Patrimonio_NSérie VARCHAR(255),
    Localizacao VARCHAR(255),
    IDCategoria INT,
    FOREIGN KEY (IDCategoria) REFERENCES CategoriaTecnologia(ID)
);

-- O ID é a chave primária e também uma chave estrangeira que referencia a tabela Tecnologia.
CREATE TABLE TecnologiaEmprestaval (
    ID INT PRIMARY KEY,
    Status VARCHAR(255),
    FOREIGN KEY (ID) REFERENCES Tecnologia(ID)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE CategoriaMaterial (
    ID INT PRIMARY KEY,
    TipoMaterial VARCHAR(255)
);

-- O ID é a chave primária desta tabela.
-- IDCategoria é uma chave estrangeira que referencia a tabela CategoriaMaterial.
-- Chave é uma chave estrangeira que referencia a tabela BolsistaProducao.
CREATE TABLE MaterialAcessivel (
    ID INT PRIMARY KEY,
    Titulo VARCHAR(255),
    Formato VARCHAR(255),
    Status VARCHAR(255),
    Localizacao VARCHAR(255),
    IDCategoria INT,
    Chave INT,
    FOREIGN KEY (IDCategoria) REFERENCES CategoriaMaterial(ID),
    FOREIGN KEY (Chave) REFERENCES BolsistaProducao(Chave)
);

-- O ID é a chave primária desta tabela.
CREATE TABLE TabelaFuncoes (
    ID INT PRIMARY KEY,
    Funcoes VARCHAR(255),
    FOREIGN KEY (ID) REFERENCES Cargo(ID)
);

-- O Código é a chave primária desta tabela.
CREATE TABLE Curso (
    Codigo VARCHAR(255) PRIMARY KEY,
    Nome VARCHAR(255),
    Modalidade VARCHAR(255),
    NivelDeFormacao VARCHAR(255)
);

-- CPF e Codigo formam a chave primária composta.
-- CPF é uma chave estrangeira que referencia a tabela Aluno.
-- Codigo é uma chave estrangeira que referencia a tabela Curso.
CREATE TABLE MatriculadoEm (
    CPF VARCHAR(11),
    Codigo VARCHAR(255),
    Situacao VARCHAR(255),
    DataInicio DATE,
    DataFim DATE,
    PRIMARY KEY (CPF, Codigo),
    FOREIGN KEY (CPF) REFERENCES Aluno(CPF),
    FOREIGN KEY (Codigo) REFERENCES Curso(Codigo)
);

-- IDPCD e IDMaterial junto com DataEmprestimo formam a chave primária composta para permitir múltiplos empréstimos da mesma pessoa e material em datas diferentes.
-- IDPCD é uma chave estrangeira que referencia a tabela PCD.
-- IDMaterial é uma chave estrangeira que referencia a tabela TecnologiaEmprestaval.
CREATE TABLE EmprestimoMaterial (
    IDPCD INT,
    IDMaterial INT,
    DataEmprestimo DATE,
    DataDevolucao DATE,
    DevolucaoEstimada DATE,
    PRIMARY KEY (IDPCD, IDMaterial, DataEmprestimo),
    FOREIGN KEY (IDPCD) REFERENCES PCD(ID),
    FOREIGN KEY (IDMaterial) REFERENCES TecnologiaEmprestaval(ID)
);

-- IDPCD e IDMaterial formam a chave primária composta.
-- IDPCD é uma chave estrangeira que referencia a tabela PCD.
-- IDMaterial é uma chave estrangeira que referencia a tabela MaterialAcessivel.
CREATE TABLE MaterialDisponibilizado (
    IDPCD INT,
    IDMaterial INT,
    PRIMARY KEY (IDPCD, IDMaterial),
    FOREIGN KEY (IDPCD) REFERENCES PCD(ID),
    FOREIGN KEY (IDMaterial) REFERENCES MaterialAcessivel(ID)
);

-- IDPCD e IDDeficiencia formam a chave primária composta.
-- IDPCD é uma chave estrangeira que referencia a tabela PCD.
-- IDDeficiencia é uma chave estrangeira que referencia a tabela Deficiencia.
CREATE TABLE DadosDeficiencia_PCD (
    IDPCD INT,
    IDDeficiencia INT,
    Grau VARCHAR(255),
    Observacoes TEXT,
    PRIMARY KEY (IDPCD, IDDeficiencia),
    FOREIGN KEY (IDPCD) REFERENCES PCD(ID),
    FOREIGN KEY (IDDeficiencia) REFERENCES Deficiencia(ID)
);

-- IDPCD, IDAcao e IDMembroCAIN junto com DataInicio formam a chave primária composta.
-- IDPCD é uma chave estrangeira que referencia a tabela PCD.
-- IDAcao é uma chave estrangeira que referencia a tabela Acao.
-- IDMembroCAIN é uma chave estrangeira que referencia a tabela MembroDaEquipe.
CREATE TABLE PrestaAssistencia (
    IDPCD INT,
    IDAcao INT,
    IDMembroCAIN INT,
    DataInicio DATE,
    DataFim DATE,
    PRIMARY KEY (IDPCD, IDAcao, IDMembroCAIN, DataInicio),
    FOREIGN KEY (IDPCD) REFERENCES PCD(ID),
    FOREIGN KEY (IDAcao) REFERENCES Acao(ID),
    FOREIGN KEY (IDMembroCAIN) REFERENCES MembroDaEquipe(Chave)
);
