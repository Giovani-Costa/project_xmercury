import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constante import KEYSPACE


def criar_passiva_talento(
    session: Session,
    tipo: str,
    nome: str,
    descricao: str,
    modificador_execucao: Optional[str],
    modificador_nome: Optional[str],
    modificador_descricao: Optional[str],
    modificador_gasto: Optional[int],
    modificador_gasto_tipo: Optional[str],
) -> uuid.UUID:
    id = uuid.uuid4()

    if modificador_nome is None:
        modificador_nome = "None"

    if modificador_descricao is None:
        modificador_descricao = "None"

    if modificador_gasto is None:
        modificador_gasto = 0

    if modificador_gasto_tipo is None:
        modificador_gasto_tipo = "None"

    if modificador_execucao is None:
        modificador_execucao = "None"

    passiva_talento_novo = f"""INSERT INTO {KEYSPACE}.{tipo} (id, nome, descricao, modificador_execucao, modificador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)
VALUES (uuid(), '{nome}', '{descricao}', '{modificador_execucao}', '{modificador_nome}', '{modificador_descricao}', {modificador_gasto}, '{modificador_gasto_tipo}');"""
    session.execute(passiva_talento_novo)
    return id


def pegar_passivas(session: Session, id: uuid.UUID) -> database.models.Passiva:
    comando = f"SELECT * FROM {KEYSPACE}.passivas WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Passiva(**kwargs)


def pegar_talentos(session: Session, id: uuid.UUID) -> database.models.Talento:
    comando = f"SELECT * FROM {KEYSPACE}.talentos WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Talento(**kwargs)
