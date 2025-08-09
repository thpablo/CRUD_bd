-- Consulta para listar todos os materiais acessíveis que foram produzidos,
-- mostrando o nome do material, sua categoria, o status atual e, mais importante,
-- o nome do bolsista de produção que o criou.
-- Esta consulta demonstra uma longa cadeia de JOINs para conectar o material acessível
-- até a tabela de pessoas, passando por categoriadematerial, bolsistaproducao,
-- bolsista, membrodaequipe e aluno.

SELECT
    ma.titulo AS material,
    cm.tipomaterial AS categoria_material,
    p.nome AS nome_bolsista,
    ma.status
FROM materialacessivel ma
JOIN categoriamaterial cm ON ma.id_categoria = cm.id_categoria
JOIN bolsistaproducao bp ON ma.id_bolsista = bp.id_bolsista
JOIN bolsista b ON bp.id_bolsista = b.id_bolsista
JOIN membrodaequipe m ON b.id_bolsista = m.id_membro
JOIN aluno a ON m.id_membro = a.id_membro
JOIN pessoa p ON a.cpf = p.cpf
ORDER BY p.nome, ma.titulo;
