-- Consulta para obter uma lista detalhada de todos os alunos.
-- Junta as tabelas pessoa, aluno, e curso (via matriculadoem)
-- para mostrar o nome, CPF, matrícula e o nome do curso de cada aluno.

SELECT
    p.cpf,
    p.nome,
    a.matricula,
    c.nome AS nome_curso
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
LEFT JOIN matriculadoem m ON a.cpf = m.cpf
LEFT JOIN curso c ON m.codigo = c.codigo
ORDER BY p.nome;
