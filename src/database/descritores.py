import uuid
from typing import Optional

import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_CONDICAO, INSERT_DESCRITOR


def criar_descritor(
    conexao: PostgresDB,
    nome: str,
    tipo: str,
    descricao: str,
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

    if tipo is None:
        tipo = "NULL"
    else:
        tipo = "'" + tipo + "'"

    if descricao is None:
        descricao = "NULL"
    else:
        descricao = "'" + descricao + "'"
    
    descritor_novo = f"""{INSERT_DESCRITOR}
VALUES ('{id}', {nome}, {tipo}, {descricao});"""
    print(f"{descritor_novo}\n")
    with conexao.get_cursor() as cursor:
        cursor.execute(descritor_novo)
    return id


def pegar_descritor(
    conexao: PostgresDB, id: uuid.UUID | str
) -> database.models.Descritor:
    with conexao.get_cursor() as cursor:
        cursor.execute(f"SELECT * FROM descritores WHERE id_descritoo={id};")
        resultado = cursor.fetchone()
    return database.models.Descritor(**dict(resultado))


def pegar_todos_os_descritores(conexao: PostgresDB) -> list[database.models.Descritor]:
    comando = f"SELECT * FROM descritores;"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        resultado = cursor.fetchall()

    lista_descritores = []
    for r in resultado:
        lista_descritores.append(database.models.Descritor(**dict(r)))
        lista_descritores.sort(key=lambda p: p.nome.lower())

    return lista_descritores
