-- Consulta para gerar um relatório de todas as pessoas com deficiência (PCD).
-- A consulta busca o CPF e o nome da pessoa, o ID do registro PCD, e qual o papel
-- principal da pessoa (Aluno, Docente, ou Técnico).
-- A complexidade está em unificar as diferentes formas de uma pessoa ser PCD
-- (através do papel de aluno, docente ou técnico) para chegar até a tabela 'pessoa'.
-- Isso é feito com múltiplos LEFT JOINs a partir da tabela 'pcd'.

SELECT
    p.cpf,
    p.nome,
    pcd.id_pcd,
    CASE
        WHEN a.cpf IS NOT NULL THEN 'Aluno'
        WHEN d.cpf IS NOT NULL THEN 'Docente'
        WHEN t.cpf IS NOT NULL THEN 'Técnico Administrativo'
        ELSE 'Não especificado'
    END AS papel
FROM pcd
LEFT JOIN aluno a ON pcd.id_pcd = a.id_pcd
LEFT JOIN docente d ON pcd.id_pcd = d.id_pcd
LEFT JOIN tecnicoadministrativo t ON pcd.id_pcd = t.id_pcd
-- O JOIN com a tabela pessoa precisa considerar todos os caminhos possíveis
LEFT JOIN pessoa p ON p.cpf = a.cpf OR p.cpf = d.cpf OR p.cpf = t.cpf
WHERE p.cpf IS NOT NULL
ORDER BY p.nome;
