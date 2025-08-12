SELECT cpf, nome FROM Pessoa WHERE nome ILIKE :query OR cpf LIKE :query ORDER BY nome;
