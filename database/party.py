import uuid

from cassandra.cluster import Session

import database.models
import database.personagens
from constantes import KEYSPACE


def pegar_party(session: Session, id: uuid.UUID | str) -> database.models.Party:
    comando = f"SELECT * FROM {KEYSPACE}.party WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    personagens_true = []
    for p in kwargs["personagens_jogaveis"]:
        personagens_true.append(
            database.personagens.pegar_personagem_com_id(session, p).model_dump()
        )

    kwargs["personagens_jogaveis"] = personagens_true
    return database.models.Party(**kwargs)
