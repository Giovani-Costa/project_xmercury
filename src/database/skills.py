import uuid
from typing import Optional



import database.models
from database.connect_postgres import PostgresDB
from database.constantes import INSERT_SKILL, INSERT_MODIFICADORES_SKILLS
from database.modificadores import pegar_modificador


def criar_skill(
    conexao: PostgresDB,
    nome: str,
    custo: int,
    execucao: str,
    descritores: Optional[str] = 'NULL',
    alcance: Optional[str] = 'NULL',
    duracao: Optional[str] = 'NULL',
    ataque: Optional[str] = 'NULL',
    acerto: Optional[str] = 'NULL',
    erro: Optional[str] = 'NULL',
    efeito: Optional[str] = 'NULL',
    especial: Optional[str] = 'NULL',
    gatilho: Optional[str] = 'NULL',
    alvo: Optional[str] = 'NULL',
    carga: Optional[str] = 'NULL',
    id_personagem: Optional[str] = 'NULL',
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
    
def criar_relacao_skill_modificador(
        conexao: PostgresDB, id_skill: uuid.UUID | str, id_modificador: uuid.UUID | str
):
    with conexao.get_cursor() as cursor:
        skill_modificador_novo = f"""{INSERT_MODIFICADORES_SKILLS}
VALUES ('{id_skill}', '{id_modificador}');"""
        cursor.execute(f"{skill_modificador_novo}\n")
    return skill_modificador_novo
