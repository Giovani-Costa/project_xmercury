import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constantes import INSERT_DESCRITOR, KEYSPACE


def criar_descritor(
    session: Session,
    nome: str,
    tipo: str,
    descricao: str,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    descritor_novo = f"""{INSERT_DESCRITOR}
VALUES ({id}, '{nome}', '{tipo}', '{descricao}');"""
    session.execute(descritor_novo)
    print(f"{descritor_novo}\n")
    return id


def pegar_descritor(session: Session, id: uuid.UUID | str) -> database.models.Descritor:
    comando = f"SELECT * FROM {KEYSPACE}.condicoes WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Descritor(**kwargs)


def pegar_todas_os_descritor(session: Session) -> list[database.models.Descritor]:
    comando = f"SELECT * FROM {KEYSPACE}.descritor;"
    resultado = session.execute(comando)
    lista_descritor = []
    for d in resultado:
        kwargs = {k: getattr(d, k) for k in resultado.column_names}
        lista_descritor.append(database.models.Descritor(**kwargs))
        lista_descritor.sort(key=lambda p: p.nome.lower())
    return lista_descritor
