from typing import Optional
import uuid

import database.models
import database.personagens
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_MODIFICADOR, INSERT_MODIFICADORES_SKILLS

def criar_modificador(
    conexao: PostgresDB,
    nome: str,
    descricao: str,
    execucao: str,
    gasto: int,
    gasto_tipo: str,
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

    if execucao is None:
        execucao = "NULL"
    else:
        execucao = "'" + execucao + "'"

    if gasto_tipo is None:
        gasto_tipo = "NULL"
    else:
        gasto_tipo = "'" + gasto_tipo + "'"

    modificador_novo = f"""{INSERT_MODIFICADOR}
VALUES ('{id}', {nome}, {descricao}, {execucao}, {gasto}, {gasto_tipo});"""
    with conexao.get_cursor() as cursor:
        cursor.execute(modificador_novo)
        print(f"{modificador_novo}\n")
    return id


def pegar_modificador(
    conexao: PostgresDB, id: uuid.UUID | str
) -> database.models.Party:
    comando = f"SELECT * FROM modificadores WHERE id_modificador='{id}';"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        resultado = cursor.fetchone()

    return database.models.Modificador(**resultado)

def pegar_todos_os_modificadores(conexao: PostgresDB) -> list[database.models.Modificador]:
    comando = f"SELECT * FROM modificadores;"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        resultado = cursor.fetchall()

    lista_modificadores = []
    for r in resultado:
        lista_modificadores.append(database.models.Modificador(**dict(r)))
        lista_modificadores.sort(key=lambda p: p.nome.lower())

    return lista_modificadores

def criar_relacao_modificador_skill(
        conexao: PostgresDB, id_modificador: uuid.UUID | str, id_skill: uuid.UUID | str
):
    with conexao.get_cursor() as cursor:
        modificador_skill_novo = f"""{INSERT_MODIFICADORES_SKILLS}
VALUES ('{id_skill}', '{id_modificador}');"""
        cursor.execute(f"{modificador_skill_novo}\n")