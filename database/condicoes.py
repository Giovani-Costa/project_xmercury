import uuid

from cassandra.cluster import Session

import database.models
from constantes import KEYSPACE


def pegar_condicao(session: Session, id: uuid.UUID | str) -> database.models.Condicao:
    comando = f"SELECT * FROM {KEYSPACE}.condicoes WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Condicao(**kwargs)


def pegar_todas_as_condicoes(session: Session) -> list[database.models.Condicao]:
    comando = f"SELECT * FROM {KEYSPACE}.condicoes;"
    resultado = session.execute(comando)
    lista_condicoes = []
    for r in resultado:
        kwargs = {k: getattr(r, k) for k in resultado.column_names}
        lista_condicoes.append(database.models.Condicao(**kwargs))
        lista_condicoes.sort(key=lambda p: p.nome.lower())
    return lista_condicoes
