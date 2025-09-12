import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constantes import KEYSPACE


def criar_item(
    session: Session,
    nome: str,
    descricao: str,
    preco: int,
    volume: int,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    item_novo = f"""INSERT INTO {KEYSPACE}.itens (id, nome, descricao, preco, volume)
VALUES ({id}, '{nome}', '{descricao}', {preco}, {volume});"""
    session.execute(item_novo)
    print(f"{item_novo}\n")
    return id


def pegar_item(session: Session, id: uuid.UUID | str) -> database.models.Item:
    comando = f"SELECT * FROM {KEYSPACE}.itens WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Item(**kwargs)
