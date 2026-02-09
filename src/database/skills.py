import uuid
from typing import Optional



import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_SKILL
from database.modificador import pegar_modificador


def criar_skill(
    conexao: PostgresDB,
    nome: str,
    custo: int,
    execucao: str,
    descritores: Optional[str],
    alcance: Optional[str],
    duracao: Optional[str],
    ataque: Optional[str],
    acerto: Optional[str],
    erro: Optional[str],
    efeito: Optional[str],
    especial: Optional[str],
    gatilho: Optional[str],
    alvo: Optional[str],
    carga: Optional[str],
    id_personagem: Optional[str],
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    skill_nova = f"""{INSERT_SKILL}
VALUES ('{id}', '{nome}', {custo}, '{execucao}', '{descritores}', '{alcance}', '{duracao}', '{ataque}', '{acerto}', '{erro}', '{efeito}', '{especial}', '{gatilho}', '{alvo}', '{carga}', '{id_personagem}');"""
    print(skill_nova)
    with conexao.get_cursor() as cursor:
        cursor.execute(skill_nova)
    return id


def pegar_skill(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Skill:
    resultado_skill = None
    resultados = {}

    with conexao.get_cursor() as cursor:
        cursor.execute(f"SELECT * FROM skills WHERE id_skill='{id}';")
        resultado_skill = cursor.fetchone()
        resultados = dict(resultado_skill)
        del resultados["id_personagem"]

        cursor.execute(
            f"SELECT id_modificador FROM modificadores_skills WHERE id_skill='{id}'"
        )
        resultado_modificador_skill = cursor.fetchall()

        resultados["modificadores"] = []
        for m in resultado_modificador_skill:
            resultados["modificadores"].append(
                pegar_modificador(conexao, m["id_modificador"])
            )

    return database.models.Skill(**resultados) if resultados else None


def pegar_todas_as_skills(conexao: PostgresDB) -> list[database.models.Skill]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT id_skill FROM skills ORDER BY nome;")
        return [pegar_skill(conexao, r["id_skill"]) for r in cursor.fetchall()]
