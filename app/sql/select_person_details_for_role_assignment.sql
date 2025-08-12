SELECT
    p.cpf,
    p.nome,
    -- Check if the person is an Aluno
    a.cpf IS NOT NULL AS is_aluno,
    -- Check if the person is a Servidor
    s.cpf IS NOT NULL AS is_servidor,
    -- Determine the type of Servidor
    CASE
        WHEN d.cpf IS NOT NULL THEN 'Docente'
        WHEN ta.cpf IS NOT NULL THEN 'Técnico Administrativo'
        WHEN tz.cpf IS NOT NULL THEN 'Terceirizado'
        ELSE NULL
    END AS servidor_tipo,
    -- Check if the person is a member of the CAIN team
    (a.id_membro IS NOT NULL OR ta.id_membro IS NOT NULL OR tz.id_membro IS NOT NULL) AS is_membro_cain
FROM
    Pessoa p
LEFT JOIN Aluno a ON p.cpf = a.cpf
LEFT JOIN Servidor s ON p.cpf = s.cpf
LEFT JOIN Docente d ON s.cpf = d.cpf
LEFT JOIN TecnicoAdministrativo ta ON s.cpf = ta.cpf
LEFT JOIN Terceirizado tz ON s.cpf = tz.cpf
WHERE
    p.cpf = :cpf;
