-- Consulta para obter uma lista unificada de todos os membros da equipe da CAIN.
-- Como um membro pode ser Aluno, Técnico ou Terceirizado, esta consulta
-- usa UNION para juntar os resultados de três buscas separadas.
-- Para cada tipo de membro, ela busca as informações pessoais na tabela 'pessoa'.

-- 1. Membros que são Alunos
SELECT
    p.cpf,
    p.nome,
    'Aluno' AS papel_principal,
    m.id_membro,
    m.regimedetrabalho
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
JOIN membrodaequipe m ON a.id_membro = m.id_membro

UNION

-- 2. Membros que são Técnicos Administrativos
SELECT
    p.cpf,
    p.nome,
    'Técnico Administrativo' AS papel_principal,
    m.id_membro,
    m.regimedetrabalho
FROM pessoa p
JOIN servidor s ON p.cpf = s.cpf
JOIN tecnicoadministrativo t ON s.cpf = t.cpf
JOIN membrodaequipe m ON t.id_membro = m.id_membro

UNION

-- 3. Membros que são Terceirizados
SELECT
    p.cpf,
    p.nome,
    'Terceirizado' AS papel_principal,
    m.id_membro,
    m.regimedetrabalho
FROM pessoa p
JOIN servidor s ON p.cpf = s.cpf
JOIN terceirizado t ON s.cpf = t.cpf
JOIN membrodaequipe m ON t.id_membro = m.id_membro

ORDER BY nome;
