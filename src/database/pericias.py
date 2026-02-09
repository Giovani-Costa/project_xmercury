import uuid
from typing import Optional

import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_PERICIA


def criar_pericia(
    conexao: PostgresDB,
    nome: str,
    descricao: str,
    e_vantagem: bool,
    e_soma: bool,
    somar: list[str],
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    pericia_nova = f"""{INSERT_PERICIA}
VALUES ('{id}', '{nome}', '{descricao}', {str(e_vantagem).lower()}, {str(e_soma).lower()}, {somar});"""
    with conexao.get_cursor() as cursor:
        cursor.execute(pericia_nova)
        print(f"{pericia_nova}\n")
    return id


def pegar_pericia(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Pericia:
    with conexao.get_cursor() as cursor:
        cursor.execute(f"SELECT * FROM pericias WHERE id_pericia='{id}';")
        resultado = cursor.fetchone()
    return database.models.Pericia(**dict(resultado))


def pegar_todas_as_pericias(db: PostgresDB) -> list[database.models.Pericia]:
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM pericias ORDER BY nome;")
        return [database.models.Pericia(**r) for r in cursor.fetchall()]

