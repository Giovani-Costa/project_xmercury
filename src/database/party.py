import uuid



import database.models
import database.personagens
from database.connect_postgres import PostgresDB
from database.constantes import KEYSPACE


def pegar_party(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Party:
    comando = f"SELECT id_personagem FROM personagens WHERE id_party='{id}';"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        lista_dict_id_personagem = cursor.fetchall()

    personagens_true = []
    for p in lista_dict_id_personagem:
        personagens_true.append(
            database.personagens.pegar_personagem_com_id(
                conexao, p["id_personagem"]
            ).model_dump()
        )

    return database.models.Party(id_party=id, personagens_jogaveis=personagens_true)
