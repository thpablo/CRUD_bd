SELECT DISTINCT
    p.Nome AS NomeAluno,
    p.CPF,
    c.Nome AS NomeCurso,
    -- Use a CASE statement to determine the type of scholar providing assistance
    CASE
        WHEN bi.ID_BOLSISTA IS NOT NULL THEN 'Inclusão'
        WHEN bp.ID_BOLSISTA IS NOT NULL THEN 'Produção'
        ELSE 'Outro' -- Should not happen based on the JOIN logic but good practice
    END AS TipoBolsista
FROM
    Aluno a
-- Join with Pessoa to get student's name
JOIN
    Pessoa p ON a.CPF = p.CPF
-- Join with MatriculadoEm and Curso to filter by course
JOIN
    MatriculadoEm me ON a.CPF = me.CPF
JOIN
    Curso c ON me.Codigo = c.CODIGO
-- Join with PrestaAssistencia to find students who received assistance
JOIN
    PrestaAssistencia pa ON a.ID_PCD = pa.ID_PCD
-- Join through MembroDaEquipe and Bolsista to identify the scholar
JOIN
    MembroDaEquipe m ON pa.ID_MEMBRO_CAIN = m.ID_MEMBRO
JOIN
    Bolsista b ON m.ID_MEMBRO = b.ID_BOLSISTA
-- Left Join with the specific scholar type tables to determine the type
LEFT JOIN
    BolsistaInclusao bi ON b.ID_BOLSISTA = bi.ID_BOLSISTA
LEFT JOIN
    BolsistaProducao bp ON b.ID_BOLSISTA = bp.ID_BOLSISTA
WHERE
    -- Ensure the student is a PCD
    a.ID_PCD IS NOT NULL
    -- Filter by the selected course code
    AND c.CODIGO = :codigo_curso
    -- Filter by the selected scholar type
    AND (
        (:tipo_bolsista = 'inclusao' AND bi.ID_BOLSISTA IS NOT NULL)
        OR
        (:tipo_bolsista = 'producao' AND bp.ID_BOLSISTA IS NOT NULL)
    )
ORDER BY
    p.Nome;
