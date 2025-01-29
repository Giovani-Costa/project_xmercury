import uuid
from typing import Optional

from cassandra.cluster import Session

import database.models
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
    VALUES ({id}, '{nome}', '{nickname}', {level}, '{path}','{classe}', '{legacy}', '{heritage}', '{melancholy}', {catarse}, {pe}, {hp}, {reducao_de_dano}, {bonus_de_proficiencia}, {talentos}, {passivas}, {skills}, {forca}, {dexterity}, {contituicao}, {inteligencia}, {sabedoria}, {carisma}, {pontos_de_sombra}, {resistencia}, {vulnerabilidade}, {imunidade}, {inventario_itens}, {inventario_numero}, {condicoes}, {saldo}, '{imagem}', '{usuario}');"""
    print(personagem_novo)
    session.execute(personagem_novo)
    return id


def pegar_personagem(session: Session, id: uuid.UUID) -> database.models.Personagem:
    comando = f"SELECT * FROM {KEYSPACE}.personagens WHERE id={id};"
    resultado = session.execute(comando)
    primeiro_resultado = resultado.one()
    kwargs = {k: getattr(primeiro_resultado, k) for k in resultado.column_names}
    return database.models.Item(**kwargs)
