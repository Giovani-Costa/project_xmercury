import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
from constantes import KEYSPACE


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
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)

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
VALUES ({id}, '{nome}', '{descricao}', '{modificador_execucao}', '{modificador_nome}', '{modificador_descricao}', {modificador_gasto}, '{modificador_gasto_tipo}');"""
    session.execute(passiva_talento_novo)
    print(f"{passiva_talento_novo}\n")
    return id


def pegar_passivas(session: Session, id: uuid.UUID | str) -> database.models.Passiva:
    comando = f"SELECT * FROM {KEYSPACE}.passivas WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Passiva(**kwargs)


def pegar_talentos(session: Session, id: uuid.UUID | str) -> database.models.Talento:
    comando = f"SELECT * FROM {KEYSPACE}.talentos WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Talento(**kwargs)


def pegar_todas_as_passivas(session: Session) -> list[database.models.Passiva]:
    comando = f"SELECT * FROM {KEYSPACE}.passivas;"
    resultado = session.execute(comando)
    lista_passivas = []
    for r in resultado:
        kwargs = {k: getattr(r, k) for k in resultado.column_names}
        lista_passivas.append(database.models.Passiva(**kwargs))
        lista_passivas.sort(key=lambda p: p.nome.lower())
    return lista_passivas


def pegar_todos_os_talentos(session: Session) -> list[database.models.Talento]:
    comando = f"SELECT * FROM {KEYSPACE}.talentos;"
    resultado = session.execute(comando)
    lista_talentos = []
    for r in resultado:
        kwargs = {k: getattr(r, k) for k in resultado.column_names}
        lista_talentos.append(database.models.Talento(**kwargs))
        lista_talentos.sort(key=lambda p: p.nome.lower())
    return lista_talentos
