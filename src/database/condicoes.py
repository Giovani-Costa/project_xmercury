import uuid
from typing import Optional

import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_CONDICAO


def criar_condicao(
    conexao: PostgresDB,
    nome: str,
    descricao: str,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    condicao_novo = f"""{INSERT_CONDICAO}
VALUES ('{id}', '{nome}', '{descricao}');"""
    with conexao.get_cursor() as cursor:
        cursor.execute(condicao_novo)
        print(f"{condicao_novo}\n")
    return id


def pegar_condicao(
    conexao: PostgresDB, condicao_id: uuid.UUID
) -> database.models.Condicao | None:
    row = None
    with conexao.get_cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM condicoes WHERE id_condicao = '{condicao_id}';",
        )
        row = cursor.fetchone()
    return database.models.Condicao(**row) if row else None


def pegar_todas_as_condicoes(conexao: PostgresDB) -> list[database.models.Condicao]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT * FROM condicoes ORDER BY nome;")
        return [database.models.Condicao(**r) for r in cursor.fetchall()]
