import uuid
from typing import Optional

from cassandra.cluster import Session

import database.item
import database.models
import database.passivas_talentos

# import database.pericias
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
    pericias: Optional[list[uuid.UUID]],
    bonus_de_proficiencia: Optional[int],
    talentos: Optional[list[uuid.UUID]],
    passivas: Optional[list[uuid.UUID]],
    skills: Optional[list[uuid.UUID]],
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
    personagem_novo = f"""INSERT INTO {KEYSPACE}.personagens (id, nome, nickname, level, path, classe, legacy, heritage, melancholy, catarse, pe, hp, reducao_de_dano, bonus_de_proficiencia, pericias, talentos, passivas, skills, forca, dexterity, constituicao, inteligencia, sabedoria, carisma, pontos_de_sombra, resistencia, vulnerabilidade, imunidade, inventario_itens, inventario_numero, condicoes, saldo, imagem, usuario)
    VALUES ({id}, '{nome}', '{nickname}', {level}, '{path}', '{classe}', '{legacy}', '{heritage}', '{melancholy}', {catarse}, {pe}, {hp}, {reducao_de_dano}, {bonus_de_proficiencia}, {pericias}, {talentos}, {passivas}, {skills}, {forca}, {dexterity}, {contituicao}, {inteligencia}, {sabedoria}, {carisma}, {pontos_de_sombra}, {resistencia}, {vulnerabilidade}, {imunidade}, {inventario_itens}, {inventario_numero}, {condicoes}, {saldo}, '{imagem}', '{usuario}');"""
    print(personagem_novo)
    session.execute(f"{personagem_novo}\n")
    return id


def pegar_personagem_com_id(
    session: Session, id: uuid.UUID
) -> database.models.Personagem:
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

    # pericias_true = []
    # for p in kwargs["pericias"]:
    #     pericias_true.append(database.pericias.pegar_pericia(session, p).model_dump())
    # kwargs["pericias"] = pericias_true

    return database.models.Personagem(**kwargs)


def pegar_id_por_nome_ou_nick(session, personagem):
    personagem_id = session.execute(
        f"SELECT id FROM {KEYSPACE}.personagens WHERE nome = '{personagem}' ALLOW FILTERING;"
    ).one()
    if personagem_id is None:
        personagem_id = session.execute(
            f"SELECT id FROM {KEYSPACE}.personagens WHERE nickname = '{personagem}' ALLOW FILTERING;"
        ).one()
    personagem_id = str(personagem_id)
    uuid = personagem_id.replace("Row(id=UUID('", "").replace("'))", "")
    return uuid


def pegar_id_por_user_id(session, user_id):
    personagem_id = session.execute(
        f"SELECT id FROM {KEYSPACE}.personagens WHERE usuario = '{user_id}' ALLOW FILTERING;"
    ).one()
    personagem_id = str(personagem_id)
    uuid = personagem_id.replace("Row(id=UUID('", "").replace("'))", "")
    return uuid
