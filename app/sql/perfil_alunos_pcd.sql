-- Consulta para criar um perfil dos alunos com deficiência (PCD).
-- Ela lista o nome, matrícula e curso de cada aluno que é PCD, e agrega
-- todas as suas deficiências registradas em uma única string, separada por vírgulas.
-- Esta é uma consulta avançada que usa a função de agregação `string_agg` do PostgreSQL
-- e múltiplos JOINs para conectar as tabelas pessoa, aluno, pcd, dadosdeficienciapcd,
-- deficiencia, matriculadoem e curso.

SELECT
    p.nome,
    a.matricula,
    c.nome AS nome_curso,
    string_agg(d.categoria, ', ') AS deficiencias
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
JOIN pcd ON a.id_pcd = pcd.id_pcd
JOIN dadosdeficienciapcd ddpcd ON pcd.id_pcd = ddpcd.id_pcd
JOIN deficiencia d ON ddpcd.id_deficiencia = d.id_deficiencia
LEFT JOIN matriculadoem m ON a.cpf = m.cpf
LEFT JOIN curso c ON m.codigo = c.codigo
GROUP BY p.nome, a.matricula, c.nome
ORDER BY p.nome;
