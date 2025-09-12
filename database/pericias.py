import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constantes import INSERT_PERICIA, KEYSPACE


def criar_pericia(
    session: Session,
    nome: str,
    descricao: str,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    pericia_nova = f"""{INSERT_PERICIA}
VALUES ({id}, '{nome}', '{descricao}');"""
    session.execute(pericia_nova)
    print(f"{pericia_nova}\n")
    return id


def pegar_pericia(session: Session, id: uuid.UUID | str) -> database.models.Pericia:
    comando = f"SELECT * FROM {KEYSPACE}.pericias WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Pericia(**kwargs)


def pegar_todas_as_pericias(session: Session) -> list[database.models.Pericia]:
    comando = f"SELECT * FROM {KEYSPACE}.pericias;"
    resultado = session.execute(comando)
    lista_pericias = []
    for r in resultado:
        kwargs = {k: getattr(r, k) for k in resultado.column_names}
        lista_pericias.append(database.models.Pericia(**kwargs))
        lista_pericias.sort(key=lambda p: p.nome.lower())
    return lista_pericias
