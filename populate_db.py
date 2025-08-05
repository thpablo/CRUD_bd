from app import db, app
from sqlalchemy import text

# SQL script to populate the database
# NOTE: This script assumes that the tables have been created by schema.sql
# and that auto-incrementing primary keys are in use for tables like PCD, Cargo, etc.
populate_script = """
INSERT INTO Pessoa (CPF, Nome) VALUES
('11111111111', 'Ana Silva'),
('22222222222', 'Bruno Costa'),
('33333333333', 'Carla Dias');

INSERT INTO ContatoTelefones (CPF, Telefones) VALUES
('11111111111', '(31) 99999-1111'),
('22222222222', '(31) 99999-2222');

INSERT INTO ContatoEmails (CPF, E_mails) VALUES
('11111111111', 'ana.silva@aluno.ufop.edu.br'),
('22222222222', 'bruno.costa@ufop.edu.br');

INSERT INTO PessoaLGBT (CPF, NomeSocial) VALUES
('33333333333', 'Carla');

INSERT INTO MembroDaEquipe (Chave, Categoria, RegimeDeTrabalho, Coordenador) VALUES
(1, 'Técnico', 'Presencial', NULL),
(2, 'Bolsista', 'Híbrido', 1);

INSERT INTO Departamento_Setor (Codigo, Nome, Localizacao, Telefone, E_mail) VALUES
('DCC', 'Departamento de Ciência da Computação', 'ICEB III', '3559-1234', 'dcc@ufop.edu.br'),
('PROACE', 'Pró-Reitoria de Assuntos Comunitários e Estudantis', 'Centro de Vivência', '3559-5678', 'proace@ufop.edu.br');

INSERT INTO Servidor (CPF, TipodeContrato, Codigo) VALUES
('22222222222', 'Efetivo', 'DCC'),
('33333333333', 'Efetivo', 'PROACE');

INSERT INTO PCD (ID) VALUES (1), (2);

INSERT INTO Cargo (ID, Nome) VALUES
(1, 'Técnico em Assuntos Educacionais'),
(2, 'Tradutor e Intérprete de Libras');

INSERT INTO Docente (CPF, SIAPE, ID) VALUES
('22222222222', '1234567', 2);

INSERT INTO TecnicoAdministrativo (CPF, SIAPE, Chave, ID, IDCargo) VALUES
('33333333333', '7654321', 1, NULL, 1);

INSERT INTO Aluno (CPF, Matricula, Chave, ID) VALUES
('11111111111', '18.1.1234', NULL, 1),
('33333333333', '19.2.5678', 2, NULL);

INSERT INTO PeriodoDeVinculo (Chave, DataDeInicio, DataDeFim) VALUES
(1, '2020-01-15', NULL),
(2, '2023-03-01', '2024-03-01');

INSERT INTO Bolsista (Chave, Salario, CargaHorariaSemanal) VALUES
(2, 700.00, 20);

INSERT INTO BolsistaProducao (Chave) VALUES (2);

INSERT INTO Deficiencia (ID, Categoria) VALUES
(1, 'Visual'),
(2, 'Auditiva');

INSERT INTO Acao (ID, Nome, Descricao) VALUES
(1, 'Acompanhamento Pedagógico', 'Apoio nas atividades acadêmicas.'),
(2, 'Tradução em Libras', 'Tradução para a Língua Brasileira de Sinais.');

INSERT INTO MatriculadoEm (CPF, Codigo, Situacao, DataInicio, DataFim) VALUES
('11111111111', 'BCC', 'Ativo', '2018-03-05', NULL),
('33333333333', 'PED', 'Ativo', '2019-08-01', NULL);

INSERT INTO DadosDeficiencia_PCD (IDPCD, IDDeficiencia, Grau, Observacoes) VALUES
(1, 1, 'Severo', 'Necessita de software leitor de tela.');

INSERT INTO PrestaAssistencia (IDPCD, IDAcao, IDMembroCAIN, DataInicio, DataFim) VALUES
(1, 1, 1, '2024-01-01', NULL);
"""

def populate_db():
    print("Connecting to the database to populate data...")
    with app.app_context():
        try:
            print("Executing SQL population script...")
            with db.engine.connect() as connection:
                # Split script into individual statements and execute them
                for statement in populate_script.strip().split(';'):
                    if statement.strip():
                        connection.execute(text(statement))
                connection.commit()
            print("Database populated successfully from SQL script!")
        except Exception as e:
            print(f"An error occurred during population: {e}")

if __name__ == '__main__':
    populate_db()
