import uuid

from cassandra.cluster import Session

import database.models
from constante import KEYSPACE


def criar_item(session: Session, nome: str, descricao: str) -> uuid.UUID:
    id = uuid.uuid4()
    item_novo = f"""INSERT INTO {KEYSPACE}.itens (id, nome, descricao)
VALUES ({id}, '{nome}', '{descricao}');"""
    session.execute(item_novo)
    return id


def pegar_item(session: Session, id: uuid.UUID) -> database.models.Item:
    comando = f"SELECT * FROM {KEYSPACE}.itens WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Item(**kwargs)
