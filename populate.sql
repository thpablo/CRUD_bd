-- Step 1: Populate core independent entities

-- Pessoa
INSERT INTO Pessoa (CPF, Nome) VALUES
('11111111111', 'Ana Silva'),
('22222222222', 'Bruno Costa'),
('33333333333', 'Carla Dias'),
('44444444444', 'Daniel Souza'),
('55555555555', 'Eduarda Lima'),
('66666666666', 'Fernanda Oliveira'),
('77777777777', 'Gabriel Martins'),
('88888888888', 'Helena Santos'),
('99999999999', 'Igor Pereira'),
('10101010101', 'Julia Ferreira');


-- DepartamentoSetor
INSERT INTO DepartamentoSetor (CODIGO, Nome, Localizacao, Telefone, Email) VALUES
(101, 'Departamento de Informática', 'Bloco A, Sala 101', '1111-1111', 'informatica@instituicao.com'),
(102, 'Departamento de Recursos Humanos', 'Bloco B, Sala 202', '2222-2222', 'rh@instituicao.com'),
(103, 'Setor de Acessibilidade', 'Bloco C, Sala 303', '3333-3333', 'acessibilidade@instituicao.com');

-- PCD (ID_PCD is auto-generated)
INSERT INTO PCD DEFAULT VALUES; -- ID 1
INSERT INTO PCD DEFAULT VALUES; -- ID 2
INSERT INTO PCD DEFAULT VALUES; -- ID 3

-- Cargo
INSERT INTO Cargo (ID_CARGO, Nome) VALUES
(1, 'Professor'),
(2, 'Analista de TI'),
(3, 'Secretário'),
(4, 'Recepcionista'),
(5, 'Coordenador de Curso');

-- Deficiencia
INSERT INTO Deficiencia (ID_DEFICIENCIA, Categoria) VALUES
(1, 'Visual'),
(2, 'Auditiva'),
(3, 'Física'),
(4, 'Intelectual');

-- Acao
INSERT INTO Acao (ID_ACAO, Nome, Descricao) VALUES
(1, 'Apoio Pedagógico', 'Acompanhamento de estudos e atividades acadêmicas.'),
(2, 'Suporte Técnico', 'Auxílio com tecnologias assistivas e software.'),
(3, 'Acessibilidade Física', 'Garantir acesso a todos os espaços da instituição.');

-- CategoriaTecnologia
INSERT INTO CategoriaTecnologia (ID_CATEGORIA, Tipo_Categoria) VALUES
(1, 'Hardware'),
(2, 'Software'),
(3, 'Dispositivo de Entrada');

-- CategoriaMaterial (ID_CATEGORIA is auto-generated)
INSERT INTO CategoriaMaterial (TipoMaterial) VALUES
('Apostila Digital'),          -- ID 1
('Vídeo Aula com Legendas'),   -- ID 2
('Audiolivro');                -- ID 3

-- Curso
INSERT INTO Curso (CODIGO, Nome, Modalidade, NivelDeFormacao) VALUES
(201, 'Ciência da Computação', 'Presencial', 'Graduação'),
(202, 'Administração', 'EAD', 'Graduação'),
(203, 'Mestrado em Educação', 'Presencial', 'Pós-Graduação');

-- Step 2: Populate entities dependent on Pessoa and DepartamentoSetor

-- ContatoTelefones (linking to Pessoa)
INSERT INTO ContatoTelefones (CPF, Telefone) VALUES
('11111111111', '11-98765-4321'),
('11111111111', '11-12345-6789'),
('22222222222', '21-99999-8888'),
('33333333333', '31-88888-7777');

-- ContatoEmails (linking to Pessoa)
INSERT INTO ContatoEmails (CPF, Email) VALUES
('11111111111', 'ana.silva@email.com'),
('22222222222', 'bruno.costa@email.com'),
('33333333333', 'carla.dias@email.com'),
('33333333333', 'carla.d@work.com');

-- PessoaLGBT (linking to Pessoa)
INSERT INTO PessoaLGBT (CPF, NomeSocial) VALUES
('33333333333', 'Carlota'),
('55555555555', 'Duda');

-- Servidor (linking to Pessoa and DepartamentoSetor)
-- Note: Not all Pessoas are Servidores
INSERT INTO Servidor (CPF, TipoDeContrato, CodigoDepartamento) VALUES
('11111111111', 'Efetivo', 101), -- Ana Silva, Depto de Informática
('22222222222', 'Efetivo', 102), -- Bruno Costa, RH
('44444444444', 'Temporário', 101), -- Daniel Souza, Depto de Informática
('66666666666', 'Efetivo', 103);   -- Fernanda Oliveira, Setor de Acessibilidade

-- Step 3: Populate MembroDaEquipe and related entities

-- MembroDaEquipe (ID_MEMBRO is auto-generated)
-- First, insert a coordinator (with NULL ID_COORDENADOR)
INSERT INTO MembroDaEquipe (Categoria, RegimeDeTrabalho, ID_COORDENADOR) VALUES
('Coordenador', '40h', NULL); -- ID_MEMBRO = 1

-- Now, insert other members, referencing the coordinator
INSERT INTO MembroDaEquipe (Categoria, RegimeDeTrabalho, ID_COORDENADOR) VALUES
('Bolsista', '20h', 1),      -- ID_MEMBRO = 2
('Técnico', '40h', 1),       -- ID_MEMBRO = 3
('Estagiário', '30h', 1),    -- ID_MEMBRO = 4
('Voluntário', '10h', 1);     -- ID_MEMBRO = 5

-- Step 4: Populate specialized Servidor roles

-- Docente (linking to Servidor and PCD)
-- Ana Silva (CPF '11111111111') is a Servidor. Let's make her a Docente.
-- She has a PCD ID.
INSERT INTO Docente (CPF, SIAPE, ID_PCD) VALUES
('11111111111', '12345678', 1);

-- TecnicoAdministrativo (linking to Servidor, MembroDaEquipe, PCD, Cargo)
-- Bruno Costa (CPF '22222222222') is a Servidor. Let's make him a TecnicoAdministrativo.
-- He is a member of the team (ID_MEMBRO = 3) and has a Cargo (ID_CARGO = 2, Analista de TI).
-- He does not have a PCD ID, so it will be NULL.
INSERT INTO TecnicoAdministrativo (CPF, SIAPE, ID_MEMBRO, ID_PCD, ID_CARGO) VALUES
('22222222222', '87654321', 3, NULL, 2);

-- Terceirizado (linking to Servidor, MembroDaEquipe, Cargo)
-- Daniel Souza (CPF '44444444444') is a Servidor. Let's make him a Terceirizado.
-- He is a member of the team (ID_MEMBRO = 5)
-- and has a Cargo (ID_CARGO = 4, Recepcionista).
INSERT INTO Terceirizado (CPF, ID_MEMBRO, ID_CARGO) VALUES
('44444444444', 5, 4);

-- Step 5: Populate Aluno and student-related entities

-- Aluno (linking to Pessoa, MembroDaEquipe, PCD)
-- Not all Pessoas are Alunos.
-- Carla Dias (CPF '33333333333') is an Aluno. She has a PCD ID.
INSERT INTO Aluno (CPF, Matricula, ID_MEMBRO, ID_PCD) VALUES
('33333333333', '202300001', NULL, 2);
-- Eduarda Lima (CPF '55555555555') is an Aluno.
INSERT INTO Aluno (CPF, Matricula, ID_MEMBRO, ID_PCD) VALUES
('55555555555', '202300002', NULL, NULL);
-- Gabriel Martins (CPF '77777777777') is an Aluno and also a MembroDaEquipe (Bolsista).
INSERT INTO Aluno (CPF, Matricula, ID_MEMBRO, ID_PCD) VALUES
('77777777777', '202300003', 2, NULL);


-- MatriculadoEm (linking Aluno to Curso)
-- Carla Dias is in Ciência da Computação
INSERT INTO MatriculadoEm (CPF, Codigo, Situacao, DataInicio, DataFim) VALUES
('33333333333', 201, 'Cursando', '2023-01-15', NULL);
-- Eduarda Lima is in Administração
INSERT INTO MatriculadoEm (CPF, Codigo, Situacao, DataInicio, DataFim) VALUES
('55555555555', 202, 'Cursando', '2023-01-15', NULL);
-- Gabriel Martins is also in Ciência da Computação
INSERT INTO MatriculadoEm (CPF, Codigo, Situacao, DataInicio, DataFim) VALUES
('77777777777', 201, 'Cursando', '2023-01-15', NULL);

-- Step 6: Populate Bolsista, Estagiario and related entities

-- PeriodoDeVinculo (linking to MembroDaEquipe)
-- Let's define the vinculum for the Bolsista (ID_MEMBRO = 2) and Estagiario (ID_MEMBRO = 4)
INSERT INTO PeriodoDeVinculo (ID_MEMBRO, DataDeInicio, DataDeFim) VALUES
(2, '2023-03-01', '2024-03-01'),
(4, '2023-08-01', '2024-08-01');

-- Bolsista (linking to MembroDaEquipe)
-- MembroDaEquipe with ID 2 is a 'Bolsista'
INSERT INTO Bolsista (ID_BOLSISTA, Salario, CargaHoraria) VALUES
(2, 500.00, 20);

-- BolsistaProducao (linking to Bolsista)
-- Let's say this bolsista is for production.
INSERT INTO BolsistaProducao (ID_BOLSISTA) VALUES
(2);

-- BolsistaInclusao (linking to Bolsista)
-- We need another bolsista for this. Let's create a new MembroDaEquipe and then a Bolsista.
INSERT INTO MembroDaEquipe (Categoria, RegimeDeTrabalho, ID_COORDENADOR) VALUES
('Bolsista', '15h', 1); -- ID_MEMBRO = 6
INSERT INTO Bolsista (ID_BOLSISTA, Salario, CargaHoraria) VALUES
(6, 450.00, 15);
INSERT INTO BolsistaInclusao (ID_BOLSISTA) VALUES
(6);

-- Relatorios (linking to BolsistaInclusao)
INSERT INTO Relatorios (ID_BOLSISTA, DataReferente, Relatorios_Semanais) VALUES
(6, '2023-10-01', 'Relatório de atividades da semana 1...'),
(6, '2023-10-08', 'Relatório de atividades da semana 2...');

-- Horarios (linking to BolsistaInclusao)
INSERT INTO Horarios (ID_BOLSISTA, Horarios_Monitoria) VALUES
(6, '2023-10-02'), -- Represents a date for the schedule
(6, '2023-10-04');

-- Estagiario (linking to MembroDaEquipe)
-- MembroDaEquipe with ID 4 is an 'Estagiário'
INSERT INTO Estagiario (ID_ESTAGIARIO, Salario, CargaHoraria) VALUES
(4, 800.00, 30);

-- Step 7: Populate technology and material entities

-- Tecnologia (linking to CategoriaTecnologia)
INSERT INTO Tecnologia (ID_TECNOLOGIA, Modelo, N_Serie, Localizacao, ID_Categoria) VALUES
(1, 'Notebook Dell G15', 12345, 'Sala 101', 1),
(2, 'Software Leitor de Tela NVDA', 67890, 'Online', 2),
(3, 'Teclado Braille', 11223, 'Sala 303', 3);

-- TecnologiaEmprestavel (linking to Tecnologia)
-- Let's make the Notebook and the Braille keyboard borrowable.
INSERT INTO TecnologiaEmprestavel (ID_TECNOLOGIA, STATUS) VALUES
(1, TRUE),
(3, TRUE);

-- MaterialAcessivel (linking to CategoriaMaterial and BolsistaProducao)
-- CategoriaMaterial IDs are auto-generated (1, 2, 3)
-- BolsistaProducao has ID_BOLSISTA = 2
INSERT INTO MaterialAcessivel (Titulo, Formato, Status, Localizacao, ID_CATEGORIA, ID_BOLSISTA) VALUES
('Apostila de Cálculo I', 'PDF Acessível', 'Disponível', '/materiais/calculo1.pdf', 1, 2),
('Videoaula de Python', 'MP4 com Legendas', 'Disponível', '/materiais/python.mp4', 2, 2);

-- Step 8: Populate remaining relationship tables

-- TabelaFuncoes (linking Cargo to its functions)
INSERT INTO TabelaFuncoes (ID_CARGO, Funcao) VALUES
(1, 'Lecionar aulas'),
(1, 'Orientar alunos'),
(2, 'Manter sistemas de TI'),
(2, 'Dar suporte técnico');

-- DadosDeficienciaPCD (linking PCD to Deficiencia)
-- PCD ID 1 has Visual disability
INSERT INTO DadosDeficienciaPCD (ID_PCD, ID_DEFICIENCIA, Grau, Observacoes) VALUES
(1, 1, 'Profunda', 'Necessita de leitor de tela.');
-- PCD ID 2 has Auditive disability
INSERT INTO DadosDeficienciaPCD (ID_PCD, ID_DEFICIENCIA, Grau, Observacoes) VALUES
(2, 2, 'Severa', 'Utiliza aparelho auditivo.');

-- EmprestimoMaterial (linking PCD to TecnologiaEmprestavel)
-- Note: Table name is EmprestimoMaterial, but FK is to TecnologiaEmprestavel.
-- PCD ID 1 borrows the Braille Keyboard (Tecnologia ID 3)
INSERT INTO EmprestimoMaterial (ID_PCD, ID_MATERIAL, DataEmprestimo, DevolucaoEstimada, DataDevolucao) VALUES
(1, 3, '2023-09-10', '2023-12-10', NULL);

-- MaterialDisponibilizado (linking PCD to MaterialAcessivel)
-- PCD ID 2 gets the accessible PDF of Calculus I (MaterialAcessivel ID 1)
-- MaterialAcessivel IDs are auto-generated, assuming 1 and 2.
INSERT INTO MaterialDisponibilizado (ID_PCD, ID_MATERIAL) VALUES
(2, 1);

-- PrestaAssistencia (linking PCD, Acao, and MembroDaEquipe)
-- Coordinator (Membro ID 1) provides Pedagogical Support (Acao ID 1) to PCD ID 1.
INSERT INTO PrestaAssistencia (ID_PCD, ID_ACAO, ID_MEMBRO_CAIN, DataInicio, DataFim) VALUES
(1, 1, 1, '2023-02-01', NULL);
-- Technical Member (Membro ID 3) provides Technical Support (Acao ID 2) to PCD ID 2.
INSERT INTO PrestaAssistencia (ID_PCD, ID_ACAO, ID_MEMBRO_CAIN, DataInicio, DataFim) VALUES
(2, 2, 3, '2023-03-01', '2023-06-01');
