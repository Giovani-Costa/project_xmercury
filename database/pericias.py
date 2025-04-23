import uuid

from cassandra.cluster import Session

import database.models
from constante import KEYSPACE


def pegar_pericia(session: Session, id: uuid.UUID) -> database.models.Pericia:
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
    return lista_pericias
