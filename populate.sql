-- Clean up existing data to ensure a fresh start
-- The order is important to avoid foreign key constraint violations
DELETE FROM PrestaAssistencia;
DELETE FROM MaterialDisponibilizado;
DELETE FROM EmprestimoMaterial;
DELETE FROM MatriculadoEm;
DELETE FROM TabelaFuncoes;
DELETE FROM Relatorios;
DELETE FROM Horarios;
DELETE FROM BolsistaInclusao;
DELETE FROM BolsistaProducao;
DELETE FROM MaterialAcessivel;
DELETE FROM CategoriaMaterial;
DELETE FROM Bolsista;
DELETE FROM Estagiario;
DELETE FROM Docente;
DELETE FROM TecnicoAdministrativo;
DELETE FROM Terceirizado;
DELETE FROM Aluno;
DELETE FROM Servidor;
DELETE FROM PeriodoDeVinculoMembro;
DELETE FROM MembroDaEquipe;
DELETE FROM PeriodoDeVinculoPCD;
DELETE FROM DadosDeficienciaPCD;
DELETE FROM PCD;
DELETE FROM PessoaLGBT;
DELETE FROM ContatoEmails;
DELETE FROM ContatoTelefones;
DELETE FROM Pessoa;
DELETE FROM Curso;
DELETE FROM DepartamentoSetor;
DELETE FROM Cargo;
DELETE FROM Deficiencia;
DELETE FROM Acao;
DELETE FROM TecnologiaEmprestavel;
DELETE FROM Tecnologia;
DELETE FROM CategoriaTecnologia;


-- Independent entities first
-- Cursos
INSERT INTO Curso (CODIGO, Nome, Modalidade, NivelDeFormacao) VALUES
(101, 'Ciência da Computação', 'Presencial', 'Bacharelado'),
(102, 'Engenharia de Produção', 'Presencial', 'Bacharelado'),
(103, 'Letras', 'EAD', 'Licenciatura');

-- Departamentos e Setores
INSERT INTO DepartamentoSetor (CODIGO, Nome, Localizacao, Telefone, Email) VALUES
(201, 'Departamento de Computação', 'ICEB, Sala 12', '3135551000', 'decom@ufop.br'),
(202, 'Departamento de Engenharia de Produção', 'Escola de Minas, Bloco B', '3135552000', 'depro@ufop.br'),
(203, 'CAIN', 'Centro de Vivência', '3135553000', 'cain@ufop.br');

-- Cargos
INSERT INTO Cargo (ID_CARGO, Nome) VALUES
(301, 'Analista de TI'),
(302, 'Psicólogo'),
(303, 'Assistente Administrativo'),
(304, 'Serviços Gerais');

-- Funcoes dos Cargos
INSERT INTO TabelaFuncoes (ID_CARGO, Funcao) VALUES
(301, 'Desenvolvimento de Sistemas'),
(301, 'Manutenção de Redes'),
(302, 'Acompanhamento Psicológico'),
(303, 'Gestão de Documentos');

-- Deficiencias
INSERT INTO Deficiencia (ID_DEFICIENCIA, Categoria) VALUES
(401, 'Visual'),
(402, 'Auditiva'),
(403, 'Física'),
(404, 'Intelectual'),
(405, 'Transtorno do Espectro Autista');

-- Ações Assistenciais
INSERT INTO Acao (ID_ACAO, Nome, Descricao) VALUES
(501, 'Apoio Psicológico', 'Sessões de terapia e acompanhamento.'),
(502, 'Adaptação de Material', 'Produção de materiais em formatos acessíveis.'),
(503, 'Monitoria Acadêmica', 'Aulas de reforço e acompanhamento de estudos.');

-- Categorias de Tecnologia
INSERT INTO CategoriaTecnologia (ID_CATEGORIA, Tipo_Categoria) VALUES
(601, 'Leitor de Tela'),
(602, 'Impressora Braille'),
(603, 'Teclado Adaptado');

-- Tecnologias
INSERT INTO Tecnologia (ID_TECNOLOGIA, Modelo, N_Serie, Localizacao, ID_Categoria) VALUES
(701, 'JAWS Screen Reader', 112233, 'Lab. Acessibilidade 1', 601),
(702, 'Focus 40 Blue', 445566, 'Sala da CAIN', 602),
(703, 'BigKeys LX', 778899, 'Lab. Acessibilidade 2', 603),
(704, 'NVDA Screen Reader', 998877, 'Uso geral nos computadores da biblioteca', 601);

-- Tecnologias Emprestáveis
INSERT INTO TecnologiaEmprestavel (ID_TECNOLOGIA, STATUS) VALUES
(702, true), -- Impressora Braille está disponível
(703, false); -- Teclado Adaptado não está disponível

-- Pessoas (base for all roles)
INSERT INTO Pessoa (CPF, Nome) VALUES
('11122233344', 'Ana Clara Souza'),      -- Aluna, PCD, Membro da Equipe (Bolsista Inclusão)
('22233344455', 'Bruno Carvalho'),    -- Aluno
('33344455566', 'Carlos Andrade'),     -- Docente, PCD
('44455566677', 'Daniela Martins'),    -- Técnica Adm, PCD, Membro da Equipe (Coordenadora)
('55566677788', 'Eduardo Ferreira'),   -- Terceirizado, Membro da Equipe
('66677788899', 'Fernanda Lima'),      -- Aluna, Membro da Equipe (Bolsista Produção)
('77788899900', 'Gabriel Rocha');       -- Aluno, Membro da Equipe (Estagiário)

-- Contatos
INSERT INTO ContatoEmails (CPF, Email) VALUES
('11122233344', 'ana.souza@aluno.ufop.br'),
('33344455566', 'carlos.andrade@ufop.br'),
('33344455566', 'carlos.a@gmail.com'),
('44455566677', 'daniela.martins@ufop.br');

INSERT INTO ContatoTelefones (CPF, Telefone) VALUES
('11122233344', '31988887777'),
('22233344455', '31977776666'),
('44455566677', '31966665555');

-- PessoaLGBT
INSERT INTO PessoaLGBT (CPF, NomeSocial) VALUES
('11122233344', 'Analu');

-- PCD (IDs will be generated automatically, so we need to insert and assume IDs)
-- This part is tricky for a static SQL file without knowing the generated IDs.
-- A better approach for real apps would be scripting this.
-- For this populate.sql, we will have to assume the IDs start from 1.
INSERT INTO PCD DEFAULT VALUES; -- Assumed ID 1
INSERT INTO PCD DEFAULT VALUES; -- Assumed ID 2
INSERT INTO PCD DEFAULT VALUES; -- Assumed ID 3

-- Dados da Deficiencia
INSERT INTO DadosDeficienciaPCD (ID_PCD, ID_DEFICIENCIA, Grau, Observacoes) VALUES
(1, 401, 'Severo', 'Necessita de leitor de tela para todas as atividades.'),
(2, 403, 'Leve', 'Usa cadeira de rodas.'),
(3, 402, 'Intermediário', 'Usa aparelho auditivo.');

-- Membros da Equipe (IDs will be generated automatically)
-- Assuming IDs start from 1.
INSERT INTO MembroDaEquipe (RegimeDeTrabalho, Categoria, ID_COORDENADOR) VALUES
('Híbrido', 'Apoio Discente', 2),        -- Assumed ID 1 for Ana Clara
('Presencial', 'Coordenação', NULL),   -- Assumed ID 2 for Daniela Martins
('Presencial', 'Apoio Externo', 2),    -- Assumed ID 3 for Eduardo Ferreira
('Remoto', 'Produção de Material', 2), -- Assumed ID 4 for Fernanda Lima
('Híbrido', 'Desenvolvimento', 2);     -- Assumed ID 5 for Gabriel Rocha

-- Periodo de Vinculo do Membro
INSERT INTO PeriodoDeVinculoMembro (ID_MEMBRO, DataDeInicio, DataDeFim) VALUES
(1, '2023-03-01', '2024-03-01'),
(2, '2020-05-10', NULL),
(3, '2022-08-15', NULL),
(4, '2023-08-01', '2024-08-01'),
(5, '2023-09-01', '2024-09-01');

-- Servidores
INSERT INTO Servidor (CPF, TipoDeContrato, CodigoDepartamentoSetor) VALUES
('33344455566', 'Efetivo', 201), -- Carlos, Docente
('44455566677', 'Efetivo', 203), -- Daniela, Técnica
('55566677788', 'Temporário', 203); -- Eduardo, Terceirizado

-- Especialização dos Servidores
INSERT INTO Docente (CPF, SIAPE, ID_PCD) VALUES
('33344455566', '1234567', 2); -- Carlos

INSERT INTO TecnicoAdministrativo (CPF, SIAPE, ID_CARGO, ID_MEMBRO, ID_PCD) VALUES
('44455566677', '7654321', 302, 2, 3); -- Daniela

INSERT INTO Terceirizado (CPF, ID_CARGO, ID_MEMBRO) VALUES
('55566677788', 304, 3); -- Eduardo

-- Alunos
INSERT INTO Aluno (CPF, Matricula, ID_PCD, ID_MEMBRO) VALUES
('11122233344', '202210001', 1, 1), -- Ana Clara
('22233344455', '202120002', NULL, NULL), -- Bruno
('66677788899', '202310003', NULL, 4), -- Fernanda
('77788899900', '202020004', NULL, 5); -- Gabriel

-- Matricula em Curso
INSERT INTO MatriculadoEm (CPF, Codigo, Situacao, DataInicio, DataFim) VALUES
('11122233344', 103, 'Matriculado', '2022-01-15', NULL),
('22233344455', 102, 'Matriculado', '2021-07-20', NULL),
('66677788899', 101, 'Matriculado', '2023-01-18', NULL),
('77788899900', 101, 'Matriculado', '2020-07-22', NULL);

-- Alunos que são Bolsistas ou Estagiários (Membros da Equipe)
INSERT INTO Bolsista (ID_BOLSISTA, Salario, CargaHoraria) VALUES
(1, 700.00, 20), -- Ana Clara
(4, 700.00, 20); -- Fernanda

INSERT INTO Estagiario (ID_ESTAGIARIO, Salario, CargaHoraria) VALUES
(5, 1200.00, 30); -- Gabriel

-- Especialização dos Bolsistas
INSERT INTO BolsistaInclusao (ID_BOLSISTA) VALUES (1);
INSERT INTO BolsistaProducao (ID_BOLSISTA) VALUES (4);

-- Relatorios e Horarios da Bolsista de Inclusão
INSERT INTO Relatorios (ID_BOLSISTA, DataReferente, Relatorios_Semanais) VALUES
(1, '2024-01-07', 'Acompanhamento do aluno X na disciplina de Cálculo I.'),
(1, '2024-01-14', 'Auxílio na adaptação de listas de exercícios para o aluno Y.');

INSERT INTO Horarios (ID_BOLSISTA, Horarios_Monitoria) VALUES
(1, '2024-03-05'),
(1, '2024-03-07');

-- Materiais e Empréstimos
-- Categoria de Material (IDs are auto-generated)
INSERT INTO CategoriaMaterial (TipoMaterial) VALUES ('Apostila Adaptada'), ('Vídeo com Legendas'); -- Assumed IDs 1, 2

-- Material Acessível (produzido pela Bolsista de Produção Fernanda)
-- Assumed CategoriaMaterial IDs 1 and 2
INSERT INTO MaterialAcessivel (Titulo, Formato, Status, Localizacao, ID_CATEGORIA, ID_BOLSISTA) VALUES
('Apostila de Álgebra Linear em Braille', 'Braille Físico', 'Concluído', 'Acervo CAIN', 1, 4),
('Videoaula de Algoritmos com Libras', 'MP4 com Janela de Libras', 'Em Produção', 'Servidor Interno', 2, 4); -- Assumed IDs 1, 2

-- Material Disponibilizado para PCD
-- Assumed PCD ID 1 and MaterialAcessivel ID 1
INSERT INTO MaterialDisponibilizado (ID_PCD, ID_MATERIAL) VALUES
(1, 1); -- Apostila para Ana Clara

-- Empréstimo de Tecnologia Emprestável
INSERT INTO EmprestimoMaterial (ID_PCD, ID_MATERIAL, DataEmprestimo, DevolucaoEstimada) VALUES
(3, 702, '2024-02-10', '2024-03-10'); -- Daniela pegou a Impressora Braille emprestada

-- Assistência
INSERT INTO PrestaAssistencia (ID_PCD, ID_ACAO, ID_MEMBRO_CAIN, DataInicio) VALUES
(1, 503, 1, '2023-08-10'), -- Ana Clara (PCD) recebe monitoria dela mesma (Bolsista de Inclusão)
(2, 501, 2, '2022-09-01');
