-- Consulta para obter uma lista detalhada de todos os servidores,
-- incluindo seu tipo (Docente, Técnico, etc.), departamento e outras informações.
SELECT
    p.cpf,
    p.nome,
    s.tipodecontrato,
    dep.nome AS nome_departamento,
    -- Usa CASE para determinar o papel específico e obter o SIAPE se aplicável
    CASE
        WHEN d.cpf IS NOT NULL THEN 'Docente'
        WHEN ta.cpf IS NOT NULL THEN 'Técnico Administrativo'
        WHEN tz.cpf IS NOT NULL THEN 'Terceirizado'
        ELSE 'Não especificado'
    END AS papel_especifico,
    -- Coalesce para pegar o SIAPE de qualquer uma das tabelas de servidor que o possuam
    COALESCE(d.siape, ta.siape) AS siape,
    -- Pega o nome do cargo para técnicos e terceirizados
    c.nome AS nome_cargo
FROM
    Pessoa p
JOIN Servidor s ON p.cpf = s.cpf
LEFT JOIN DepartamentoSetor dep ON s.codigodepartamentosetor = dep.codigo
LEFT JOIN Docente d ON s.cpf = d.cpf
LEFT JOIN TecnicoAdministrativo ta ON s.cpf = ta.cpf
LEFT JOIN Terceirizado tz ON s.cpf = tz.cpf
LEFT JOIN Cargo c ON ta.id_cargo = c.id_cargo OR tz.id_cargo = c.id_cargo
ORDER BY
    p.nome;
