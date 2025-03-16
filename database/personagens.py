import uuid
from typing import Optional

from cassandra.cluster import Session

import database.item
import database.models
import database.passivas_talentos
import database.skill
from constante import KEYSPACE


def criar_personagem(
    session: Session,
    nome: str,
    nickname: Optional[str],
    level: Optional[int],
    legacy: Optional[str],
    classe: Optional[str],
    path: Optional[str],
    heritage: Optional[str],
    melancholy: Optional[str],
    catarse: Optional[int],
    pe: Optional[int],
    hp: int,
    reducao_de_dano: Optional[int],
    bonus_de_proficiencia: Optional[int],
    talentos: Optional[uuid.UUID],
    passivas: Optional[uuid.UUID],
    skills: Optional[uuid.UUID],
    forca: list[int],
    dexterity: list[int],
    contituicao: list[int],
    inteligencia: list[int],
    sabedoria: list[int],
    carisma: list[int],
    pontos_de_sombra: Optional[int],
    resistencia: Optional[str],
    vulnerabilidade: Optional[str],
    imunidade: Optional[str],
    inventario_itens: Optional[list[uuid.UUID]],
    inventario_numero: Optional[list[int]],
    condicoes: Optional[list[str]],
    saldo: int,
    imagem: Optional[str],
    usuario: Optional[int],
) -> uuid.UUID:
    id = uuid.uuid4()
    personagem_novo = f"""INSERT INTO {KEYSPACE}.personagens (id, nome, nickname, level, path, classe, legacy, heritage, melancholy, catarse, pe, hp, reducao_de_dano, bonus_de_proficiencia, talentos, passivas, skills, forca, dexterity, constituicao, inteligencia, sabedoria, carisma, pontos_de_sombra, resistencia, vulnerabilidade, imunidade, inventario_itens, inventario_numero, condicoes, saldo, imagem, usuario)
    VALUES ({id}, '{nome}', '{nickname}', {level}, '{path}', '{classe}', '{legacy}', '{heritage}', '{melancholy}', {catarse}, {pe}, {hp}, {reducao_de_dano}, {bonus_de_proficiencia}, {talentos}, {passivas}, {skills}, {forca}, {dexterity}, {contituicao}, {inteligencia}, {sabedoria}, {carisma}, {pontos_de_sombra}, {resistencia}, {vulnerabilidade}, {imunidade}, {inventario_itens}, {inventario_numero}, {condicoes}, {saldo}, '{imagem}', '{usuario}');"""
    print(personagem_novo)
    session.execute(f"{personagem_novo}\n")
    return id


def pegar_personagem(session: Session, id: uuid.UUID) -> database.models.Personagem:
    comando = f"SELECT * FROM {KEYSPACE}.personagens WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}

    forca = kwargs.pop("forca")
    dexterity = kwargs.pop("dexterity")
    constituicao = kwargs.pop("constituicao")
    inteligencia = kwargs.pop("inteligencia")
    sabedoria = kwargs.pop("sabedoria")
    carisma = kwargs.pop("carisma")
    kwargs["atributos"] = {
        "forca": {"protection": forca[0], "bonus": forca[1]},
        "destreza": {"protection": dexterity[0], "bonus": dexterity[1]},
        "constituicao": {"protection": constituicao[0], "bonus": constituicao[1]},
        "inteligencia": {"protection": inteligencia[0], "bonus": inteligencia[1]},
        "sabedoria": {"protection": sabedoria[0], "bonus": sabedoria[1]},
        "carisma": {"protection": carisma[0], "bonus": carisma[1]},
    }
    skills_true = []
    for s in kwargs["skills"]:
        skills_true.append(database.skill.pegar_skills(session, s).model_dump())

    kwargs["skills"] = skills_true

    passivas_true = []
    for p in kwargs["passivas"]:
        passivas_true.append(
            database.passivas_talentos.pegar_passivas(session, p).model_dump()
        )
    kwargs["passivas"] = passivas_true

    talentos_true = []
    for t in kwargs["talentos"]:
        talentos_true.append(
            database.passivas_talentos.pegar_talentos(session, t).model_dump()
        )
    kwargs["talentos"] = talentos_true

    itens = kwargs.pop("inventario_itens")
    numeros = kwargs.pop("inventario_numero")
    itens_true = []
    for i, n in zip(itens, numeros):
        item = database.item.pegar_item(session, i).model_dump()
        itens_true.append(
            database.models.ItemDeInventario(item=item, quantidade=n).model_dump()
        )
    kwargs["inventario"] = itens_true
    return database.models.Personagem(**kwargs)
