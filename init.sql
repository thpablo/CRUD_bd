-- Modifiquei nomes de tabelas para ficar igual do modelo relacional,
-- Substitui { }  por ( ) em algumas criacoes de tabelas
-- Adicionei CONSTRAINTS ID_NOME_TABELA para as chaves primarias compostas sempre com o nome da tabela separado por '_
-- Consertei alguns nomes de atributos que estavam diferentes do modelo relacional e referencias a chaves estrangeiras
-- Modifiquei AUTO_INCREMENT (MYSQL) PARA GENERATED ALWAYS AS IDENTITY (POSTGRES)
-- Coloquei relacao departamentosetor antes de servidor
-- Algumas outras observacoes coloquei em comentarios no codigo do lado dos atributos


-- Telas individuais para diferentes entidades -  crio Pessoa e finaliza. Depois quando vou cadastrar o servidor eu busco as pessoas cadastradas anteriormente. mesma coisa pro aluno


-- Entidade Pessoa
CREATE TABLE Pessoa (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL
);

-- Atributo Telefones Multivalorado de Pessoa
CREATE TABLE ContatoTelefones (
    CPF VARCHAR(11) NOT NULL,
    Telefone VARCHAR(20) NOT NULL,
    CONSTRAINT ID_CONTATO_TELEFONES PRIMARY KEY (CPF, Telefone),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON DELETE CASCADE
);

-- Atributo Emails Multivalorado de Pessoa
CREATE TABLE ContatoEmails (
    CPF VARCHAR(11) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    CONSTRAINT ID_CONTATO_EMAILS PRIMARY KEY (CPF, Email),
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON DELETE CASCADE
);

-- Entidade PessoaLGBT
CREATE TABLE PessoaLGBT (
    CPF VARCHAR(11) PRIMARY KEY,
    NomeSocial VARCHAR(255) NOT NULL,
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON DELETE CASCADE
);

-- Entidade DepartamentoSetor
CREATE TABLE DepartamentoSetor(
	CODIGO INT PRIMARY KEY,
	Nome VARCHAR(60) NOT NULL,
	Localizacao VARCHAR(100),
	Telefone VARCHAR(20),
	Email VARCHAR (100)
);


-- Entidade Servidor
CREATE TABLE Servidor (
    CPF VARCHAR(11) PRIMARY KEY,
    TipoDeContrato VARCHAR(100) NOT NULL,
    CodigoDepartamentoSetor INT NOT NULL,
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON DELETE RESTRICT,
    FOREIGN KEY (CodigoDepartamentoSetor) REFERENCES DepartamentoSetor(CODIGO) ON DELETE RESTRICT

    -- trigger para buscar o CPF Da pessoa em Servidor e verificar se ela é PCD.
    -- se for, vai pegar o ID_PCD do PCD e colocar na tabela Aluno
);

-- Entidade PCD
CREATE TABLE PCD (
	ID_PCD INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);


-- Entidade Docente
CREATE TABLE Docente (
    CPF VARCHAR(11) PRIMARY KEY,
    SIAPE VARCHAR(8) NOT NULL UNIQUE,
    ID_PCD INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF) ON DELETE RESTRICT,
    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT
);

-- Entidade Membro da Equipe
CREATE TABLE MembroDaEquipe(
    ID_MEMBRO INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    RegimeDeTrabalho VARCHAR(100) NOT NULL,
    ID_COORDENADOR INT,
    FOREIGN KEY (ID_COORDENADOR) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT
);

-- Entidade Cargo
CREATE TABLE Cargo (
	ID_CARGO INT PRIMARY KEY, 
	Nome VARCHAR(60) NOT NULL
);

-- Entidade Técnico Administrativo
CREATE TABLE TecnicoAdministrativo(
    CPF VARCHAR(11) PRIMARY KEY,
    SIAPE VARCHAR(8) NOT NULL UNIQUE,
    ID_MEMBRO INT,
    ID_PCD INT,
    ID_CARGO INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MEMBRO) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT,
    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT,
    FOREIGN KEY (ID_CARGO) REFERENCES CARGO(ID_CARGO) ON DELETE RESTRICT
);

-- Entidade Terceirizado
CREATE TABLE Terceirizado(
    CPF VARCHAR(11) PRIMARY KEY,
    ID_MEMBRO INT,
    ID_CARGO INT,
    FOREIGN KEY (CPF) REFERENCES Servidor(CPF) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MEMBRO) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT,
    FOREIGN KEY (ID_CARGO) REFERENCES Cargo(ID_CARGO) ON DELETE RESTRICT
);

-- Entidade Aluno
CREATE TABLE Aluno (
    CPF VARCHAR(11) PRIMARY KEY,
    Matricula VARCHAR(9) NOT NULL,
    ID_MEMBRO INT,
    ID_PCD INT,
    FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MEMBRO) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT,
    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT

    -- trigger para buscar o CPF Da pessoa em Servidor e verificar se ela é PCD.
    -- se for, vai pegar o ID_PCD do PCD e colocar na tabela Aluno
);

-- Atributo Período de Vínculo Multivalorado de Membro da Equipe
CREATE TABLE PeriodoDeVinculoPCD(
    ID_PERIODO_DE_VINCULO_PCD INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    DataDeInicio DATE NOT NULL,
    DataDeFim DATE,
    ID_PCD INT NOT NULL,
    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT
);

CREATE TABLE PeriodoDeVinculoMembro(
    ID_PERIODO_DE_VINCULO_MEMBRO INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    DataDeInicio DATE NOT NULL,
    DataDeFim DATE,
    ID_MEMBRO INT NOT NULL,
    FOREIGN KEY (ID_MEMBRO) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT
);

-- Entidade Bolsista
CREATE TABLE Bolsista(
    ID_BOLSISTA INT PRIMARY KEY,
    Salario MONEY NOT NULL,
    CargaHoraria INT,
    FOREIGN KEY (ID_BOLSISTA) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT
    -- CHECK (Salario > 0) 
);

-- Entidade Bolsista de Produção
CREATE TABLE BolsistaProducao(
    ID_BOLSISTA INT PRIMARY KEY,
    FOREIGN KEY (ID_BOLSISTA) REFERENCES Bolsista(ID_BOLSISTA) ON DELETE RESTRICT
);

-- Entidade Bolsista de Inclusão
CREATE TABLE BolsistaInclusao(
    ID_BOLSISTA INT PRIMARY KEY NOT NULL,
    FOREIGN KEY (ID_BOLSISTA) REFERENCES Bolsista(ID_BOLSISTA) ON DELETE RESTRICT
);

-- Atributo Relatórios Multivalorado do Bolsista de Inclusão
CREATE TABLE Relatorios(
    ID_BOLSISTA INT NOT NULL,
    DataReferente DATE NOT NULL,
    Relatorios_Semanais VARCHAR(1000),
    FOREIGN KEY (ID_BOLSISTA) REFERENCES BolsistaInclusao(ID_BOLSISTA) ON DELETE RESTRICT,
    CONSTRAINT ID_RELATORIOS PRIMARY KEY (ID_BOLSISTA, DataReferente) -- AQUI NAO ESTA RELATORIOS SEMANAIS COMO CHAVE COMPOSTA, MAS NO DIAGRAMA RELACIONAL ESTÁ
);

-- Atributo Horários Multivalorado do Bolsista de Inclusão
CREATE TABLE Horarios(
    ID_BOLSISTA INT NOT NULL,  -- ALTEREI O NOME DO ATRIBUTO PARA CONDIZER QUE O ID VEM DE BOLSISTA INCLUSAO
    Horarios_Monitoria DATE NOT NULL,
    CONSTRAINT ID_HORARIOS PRIMARY KEY (ID_BOLSISTA, Horarios_Monitoria), -- COLOQUEI OS DOIS ATRIBUTOS COMO CHAVE IGUAL NO MODELO RELACIONAL
    FOREIGN KEY (ID_BOLSISTA) REFERENCES BolsistaInclusao(ID_BOLSISTA) ON DELETE RESTRICT
);

-- Entidade Estagiário
CREATE TABLE Estagiario(
	ID_ESTAGIARIO INT PRIMARY KEY NOT NULL,
	Salario MONEY NOT NULL,
	CargaHoraria INT, 
	FOREIGN KEY (ID_ESTAGIARIO) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT 
);

-- Entidade Deficiência
CREATE TABLE Deficiencia(
    ID_DEFICIENCIA INT PRIMARY KEY,
    Categoria VARCHAR(50) NOT NULL
);

-- Entidade Ação
CREATE TABLE Acao(
    ID_ACAO INT PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Descricao VARCHAR(500)
);

-- ################ NÃO REVISADO ################

-- Entidade Categoria Tecnologia (MOVI PARA ANTES DE TECNOLOGIA PORQUE ELA TEM REFERENCIA EM TECNOLOGIA)
CREATE TABLE CategoriaTecnologia(
    ID_CATEGORIA INT PRIMARY KEY,
    Tipo_Categoria VARCHAR(50) NOT NULL
);


-- Entidade Tecnologia
CREATE TABLE Tecnologia(
    ID_TECNOLOGIA INT PRIMARY KEY,
    Modelo VARCHAR(50) NOT NULL,
    N_Serie INT NOT NULL,
    Localizacao VARCHAR(100),
    ID_Categoria INT NOT NULL,

    FOREIGN KEY (ID_Categoria) REFERENCES CategoriaTecnologia(ID_CATEGORIA) ON DELETE RESTRICT
);


CREATE TABLE TecnologiaEmprestavel(
    ID_TECNOLOGIA INT PRIMARY KEY,
    STATUS BOOLEAN NOT NULL,
    FOREIGN KEY (ID_TECNOLOGIA) REFERENCES Tecnologia(ID_TECNOLOGIA) ON DELETE RESTRICT
    -- CHECK (STATUS IN ('Disponível', 'Indisponível')) - NAO SEI SE ISSO FUNCIONA
);


-- Entidade Categoria Material
CREATE TABLE CategoriaMaterial(
    ID_CATEGORIA INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    TipoMaterial VARCHAR(100) NOT NULL
);

-- Entidade Material Acessível
CREATE TABLE MaterialAcessivel(
    ID_MATERIAL INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Titulo VARCHAR(255) NOT NULL,
    Formato VARCHAR(100) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    Localizacao VARCHAR(255) NOT NULL,
    ID_CATEGORIA INT NOT NULL,
    ID_BOLSISTA INT,
    FOREIGN KEY (ID_CATEGORIA) REFERENCES CategoriaMaterial(ID_CATEGORIA) ON DELETE RESTRICT,
    FOREIGN KEY (ID_BOLSISTA) REFERENCES BolsistaProducao(ID_BOLSISTA) ON DELETE RESTRICT
);

-- Entidade Curso
CREATE TABLE Curso (
	CODIGO INT PRIMARY KEY, 
	Nome VARCHAR(50) NOT NULL, 
    Modalidade VARCHAR(20) NOT NULL,
    NivelDeFormacao VARCHAR(20) NOT NULL
); 

-- Atributo Funções Multivalorado de Cargo
CREATE TABLE TabelaFuncoes(
	ID_CARGO INT NOT NULL,
    Funcao VARCHAR(255), 
    CONSTRAINT ID_TABELA_FUNCOES PRIMARY KEY (ID_CARGO, Funcao), -- MODIFIQUEI NOME AQUI POIS JA EXISTIA UM ID_PERIODO ANTERIOR
    FOREIGN KEY (ID_CARGO) REFERENCES Cargo(ID_CARGO) ON DELETE RESTRICT  
);

-- Relacionamento Matriculado Em
CREATE TABLE MatriculadoEm (
	CPF VARCHAR(11) NOT NULL,
	Codigo INT NOT NULL, 
	Situacao VARCHAR (50),
	DataInicio DATE,
	DataFim DATE, 
    CONSTRAINT ID_MATRICULADO_EM PRIMARY KEY (CPF, Codigo),
	FOREIGN KEY (CPF) REFERENCES Aluno(CPF) ON DELETE RESTRICT,
	FOREIGN KEY (Codigo) REFERENCES Curso(Codigo) ON DELETE RESTRICT
);

-- Relacionamento Empréstimo Material
CREATE TABLE EmprestimoMaterial (
    ID_PCD INT,
    ID_MATERIAL INT,
    DataEmprestimo DATE,
    DataDevolucao DATE,
    DevolucaoEstimada DATE,

    CONSTRAINT ID_EMPRESTIMO_MATERIAL PRIMARY KEY (ID_PCD, ID_MATERIAL), -- Verificar no modelo relacional e diagrama quais sao as chaves daqui

    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MATERIAL) REFERENCES TecnologiaEmprestavel(ID_TECNOLOGIA) ON DELETE RESTRICT
);


-- Relacionamento Material Disponibilizado
CREATE TABLE MaterialDisponibilizado(
    ID_PCD INT NOT NULL,
    ID_MATERIAL INT NOT NULL,
    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MATERIAL) REFERENCES MaterialAcessivel(ID_MATERIAL),
    CONSTRAINT ID_MATERIAL_DISPONIBILIZADO PRIMARY KEY (ID_PCD, ID_MATERIAL)
);

-- Entidade Deficiência
CREATE TABLE DadosDeficienciaPCD (
    ID_PCD INT NOT NULL,
    ID_DEFICIENCIA INT NOT NULL,
    Grau VARCHAR(100),
    Observacoes TEXT,

    CONSTRAINT ID_DADOS_DEFICIENCIA_PCD PRIMARY KEY (ID_PCD, ID_DEFICIENCIA),

    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT,
    FOREIGN KEY (ID_DEFICIENCIA) REFERENCES Deficiencia(ID_DEFICIENCIA) ON DELETE RESTRICT
);

-- Relacionamento Presta Assistência
CREATE TABLE PrestaAssistencia (
    ID_PCD INT NOT NULL,
    ID_ACAO INT NOT NULL,
    ID_MEMBRO_CAIN INT NOT NULL,
    DataInicio DATE NOT NULL,
    DataFim DATE,

    CONSTRAINT ID_PRESTA_ASSISTENCIA PRIMARY KEY (ID_PCD, ID_ACAO, ID_MEMBRO_CAIN, DataInicio),

    FOREIGN KEY (ID_PCD) REFERENCES PCD(ID_PCD) ON DELETE RESTRICT,
    FOREIGN KEY (ID_ACAO) REFERENCES Acao(ID_ACAO) ON DELETE RESTRICT,
    FOREIGN KEY (ID_MEMBRO_CAIN) REFERENCES MembroDaEquipe(ID_MEMBRO) ON DELETE RESTRICT
);
