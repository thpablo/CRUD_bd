-- Consulta para gerar um relatório de todas as pessoas com deficiência (PCD).
-- A consulta une os resultados de três buscas separadas (para Alunos, Docentes e Técnicos)
-- para garantir que todos os caminhos de vínculo entre uma Pessoa e um registro PCD sejam cobertos.

-- 1. Busca Alunos que são PCD
SELECT p.cpf, p.nome, pcd.id_pcd, 'Aluno' AS papel
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
JOIN pcd ON a.id_pcd = pcd.id_pcd

UNION

-- 2. Busca Docentes que são PCD
SELECT p.cpf, p.nome, pcd.id_pcd, 'Docente' AS papel
FROM pessoa p
JOIN servidor s ON p.cpf = s.cpf
JOIN docente d ON s.cpf = d.cpf
JOIN pcd ON d.id_pcd = pcd.id_pcd

UNION

-- 3. Busca Técnicos Administrativos que são PCD
SELECT p.cpf, p.nome, pcd.id_pcd, 'Técnico Administrativo' AS papel
FROM pessoa p
JOIN servidor s ON p.cpf = s.cpf
JOIN tecnicoadministrativo t ON s.cpf = t.cpf
JOIN pcd ON t.id_pcd = pcd.id_pcd

ORDER BY nome;
