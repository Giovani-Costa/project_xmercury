import uuid
from typing import Optional



import database.models
from database.connect_postgres import PostgresDB
from database.constantes import KEYSPACE


def criar_passiva_talento(
    conexao: PostgresDB,
    tipo: str,
    nome: str,
    descricao: str,
    id_personagem: uuid.UUID,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)

    passiva_talento_novo = f"""INSERT INTO {tipo} (id_{tipo[:-1]}, nome, descricao, id_personagem)
VALUES ('{id}', '{nome}', '{descricao}', '{id_personagem}');"""
    with conexao.get_cursor() as cursor:
        cursor.execute(passiva_talento_novo)
    print(f"{passiva_talento_novo}\n")
    return id


def pegar_passiva(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Passiva:
    comando = f"SELECT * FROM passivas WHERE id_passiva='{id}';"
    row = None

    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        row = cursor.fetchone()
        del row["id_personagem"]
    return database.models.Passiva(**row) if row else None


def pegar_talento(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Talento:
    comando = f"SELECT * FROM talentos WHERE id_talento='{id}';"
    row = None

    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        row = cursor.fetchone()
        del row["id_personagem"]
    return database.models.Talento(**row) if row else None

def pegar_todas_as_passivas(conexao: PostgresDB) -> list[database.models.Passiva]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT id_passiva FROM passivas ORDER BY nome;")
        return [pegar_passiva(conexao, r["id_passiva"]) for r in cursor.fetchall()]


def pegar_todos_os_talentos(conexao: PostgresDB) -> list[database.models.Talento]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT id_talento FROM talentos ORDER BY nome;")
        return [pegar_talento(conexao, r["id_talento"]) for r in cursor.fetchall()]
