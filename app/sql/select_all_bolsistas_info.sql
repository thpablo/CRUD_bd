-- Consulta para obter uma lista detalhada de todos os bolsistas.
-- Ela junta múltiplas tabelas para mostrar informações pessoais, do curso,
-- e detalhes específicos da bolsa, como salário, carga horária e o tipo de bolsa.
-- A cláusula CASE é usada para determinar se o bolsista é de 'Inclusão' ou 'Produção'.

SELECT
    p.nome,
    p.cpf,
    a.matricula,
    c.nome AS nome_curso,
    b.salario,
    b.cargahoraria,
    CASE
        WHEN bi.id_bolsista IS NOT NULL THEN 'Inclusão'
        WHEN bp.id_bolsista IS NOT NULL THEN 'Produção'
        ELSE 'Não especificado'
    END AS tipo_bolsa
FROM pessoa p
JOIN aluno a ON p.cpf = a.cpf
JOIN membrodaequipe m ON a.id_membro = m.id_membro
JOIN bolsista b ON m.id_membro = b.id_bolsista
LEFT JOIN bolsistainclusao bi ON b.id_bolsista = bi.id_bolsista
LEFT JOIN bolsistaproducao bp ON b.id_bolsista = bp.id_bolsista
LEFT JOIN matriculadoem ma ON p.cpf = ma.cpf
LEFT JOIN curso c ON ma.codigo = c.codigo
ORDER BY p.nome;
