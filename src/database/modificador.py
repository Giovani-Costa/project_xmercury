import uuid



import database.models
import database.personagens
from database.connect_postgres import PostgresDB
from database.constantes import KEYSPACE


def pegar_modificador(
    conexao: PostgresDB, id: uuid.UUID | str
) -> database.models.Party:
    comando = f"SELECT * FROM modificadores WHERE id_modificador='{id}';"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        resultado = cursor.fetchone()

    return database.models.Modificador(**resultado)
