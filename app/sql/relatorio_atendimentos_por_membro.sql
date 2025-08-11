-- Consulta para contar quantos atendimentos (PrestaAssistencia) cada membro da equipe realizou.
-- Esta consulta é complexa pois o nome do membro da equipe está na tabela 'pessoa',
-- e o vínculo entre 'membrodaequipe' e 'pessoa' é indireto, passando por 'aluno' ou 'tecnicoadministrativo'/'terceirizado'.
-- Usamos LEFT JOINs e COALESCE para unificar os caminhos e obter o nome corretamente.

SELECT
    m.id_membro,
    COALESCE(p_aluno.nome, p_servidor.nome) AS nome_membro,
    COUNT(pa.id_pcd) AS total_atendimentos
FROM membrodaequipe m
JOIN prestaassistencia pa ON m.id_membro = pa.id_membro_cain
LEFT JOIN aluno a ON m.id_membro = a.id_membro
LEFT JOIN pessoa p_aluno ON a.cpf = p_aluno.cpf
LEFT JOIN tecnicoadministrativo ta ON m.id_membro = ta.id_membro
LEFT JOIN terceirizado t ON m.id_membro = t.id_membro
LEFT JOIN servidor s ON ta.cpf = s.cpf OR t.cpf = s.cpf
LEFT JOIN pessoa p_servidor ON s.cpf = p_servidor.cpf
GROUP BY m.id_membro, nome_membro
ORDER BY total_atendimentos DESC;
