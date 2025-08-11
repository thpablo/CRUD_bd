SELECT p.nome, a.matricula
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
JOIN matriculadoem m ON a.cpf = m.cpf
WHERE m.codigo = :codigo
ORDER BY p.nome;
