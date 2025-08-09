-- Consulta para gerar um relatório de recursos de acessibilidade (tecnologias).
-- Ela agrupa as tecnologias por sua categoria, conta o total de itens em cada uma,
-- e também conta quantos desses itens estão disponíveis para empréstimo.
-- Usa LEFT JOIN para incluir todas as tecnologias, mesmo as não emprestáveis,
-- e uma expressão CASE dentro de uma função de agregação (SUM) para a contagem condicional.

SELECT
    ct.tipocategoria,
    COUNT(t.id_tecnologia) AS total_de_itens,
    SUM(CASE WHEN te.status = true THEN 1 ELSE 0 END) AS disponiveis_para_emprestimo
FROM categoriatecnologia ct
JOIN tecnologia t ON ct.id_categoria = t.id_categoria
LEFT JOIN tecnologiaemprestavel te ON t.id_tecnologia = te.id_tecnologia
GROUP BY ct.tipocategoria
ORDER BY ct.tipocategoria;
