import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constantes import KEYSPACE


def criar_skill(
    session: Session,
    nome: str,
    custo: int,
    execucao: str,
    descritores: Optional[str],
    alcance: Optional[str],
    duracao: Optional[str],
    ataque: Optional[str],
    acerto: Optional[str],
    erro: Optional[str],
    efeito: Optional[str],
    especial: Optional[str],
    gatilho: Optional[str],
    alvo: Optional[str],
    carga: Optional[str],
    modificador_execucao: Optional[str],
    modificador_nome: Optional[str],
    modificador_descricao: Optional[str],
    modificador_gasto: Optional[str],
    modificador_gasto_tipo: Optional[str],
) -> uuid.UUID:
    id = uuid.uuid4()
    skill_nova = f"""INSERT INTO {KEYSPACE}.skills (id, nome, custo, execucao, descritores, alcance, duracao, ataque, acerto, erro, efeito, especial, gatilho, alvo, carga, modificador_execucao, modificador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)
VALUES ({id}, '{nome}', {custo}, '{execucao}', '{descritores}', '{alcance}', '{duracao}', '{ataque}', '{acerto}', '{erro}', '{efeito}', '{especial}', '{gatilho}', '{alvo}', '{carga}', '{modificador_execucao}', '{modificador_nome}', '{modificador_descricao}', {modificador_gasto}, '{modificador_gasto_tipo}');"""
    print(skill_nova)
    session.execute(skill_nova)
    return id


def pegar_skills(session: Session, id: uuid.UUID | str) -> database.models.Skill:
    comando = f"SELECT * FROM xmercury.skills WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Skill(**kwargs)
