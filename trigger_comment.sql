-- Trigger para tabela tecnicoadministrativo
CREATE TRIGGER check_member_id_tecnicoadministrativo
    BEFORE INSERT OR UPDATE OF id_membro ON tecnicoadministrativo
    FOR EACH ROW
    WHEN (NEW.id_membro_equipe IS NOT NULL)
    EXECUTE FUNCTION checar_id_membro();

-- Trigger para tabela terceirizado
CREATE TRIGGER check_member_id_terceirizado
    BEFORE INSERT OR UPDATE OF id_membroON terceirizado
    FOR EACH ROW
    WHEN (NEW.id_membro_equipe IS NOT NULL)
    EXECUTE FUNCTION checar_id_membro();

-- Trigger para tabela aluno
CREATE TRIGGER check_member_id_aluno
    BEFORE INSERT OR UPDATE OF id_membro ON aluno
    FOR EACH ROW
    WHEN (NEW.id_membro_equipe IS NOT NULL)
    EXECUTE FUNCTION checar_id_membro();
