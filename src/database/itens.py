import uuid
from typing import Optional



import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_ITEM


def criar_item(
    conexao: PostgresDB,
    nome: str,
    descricao: str,
    preco: int,
    volume: int,
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    if nome is None:
        nome = "NULL"
    else:
        nome = "'" + nome + "'"
    if descricao is None:
        descricao = "NULL"
    else:
        descricao = "'" + descricao + "'"
    if preco is None:
        preco = "NULL"
    if volume is None:
        volume = "NULL"
    
    item_novo = f"""{INSERT_ITEM}
VALUES ('{id}', {nome}, {descricao}, {preco}, {volume});"""
    with conexao.get_cursor() as cursor:
        cursor.execute(item_novo)
        print(f"{item_novo}\n")
    return id


def pegar_item(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Item:
    comando = f"SELECT * FROM itens WHERE id_item='{id}';"
    row = None

    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        row = cursor.fetchone()
    return database.models.Item(**row) if row else None


def pegar_todos_os_itens(conexao: PostgresDB) -> list[database.models.Item]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT * FROM itens;")
        return [database.models.Item(**r) for r in cursor.fetchall()]
    
