import uuid
from typing import Optional



import database.constantes
import database.item
import database.models
import database.passivas_talentos
import database.pericias
import database.skills
from database.connect_postgres import PostgresDB


def criar_personagem(
    conexao: PostgresDB,
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
    pe_atual: Optional[int],
    hp: int,
    hp_atual: Optional[int],
    hp_tipo: Optional[str],
    reducao_de_dano: Optional[int],
    bonus_de_proficiencia: Optional[int],
    pericias: Optional[list[uuid.UUID]],
    pontos_de_sombra: Optional[int],
    protecao_forca: int,
    bonus_forca: int,
    protecao_destreza: int,
    bonus_destreza: int,
    protecao_contituicao: int,
    bonus_contituicao: int,
    protecao_inteligencia: int,
    bonus_inteligencia: int,
    protecao_sabedoria: int,
    bonus_sabedoria: int,
    protecao_carisma: int,
    bonus_carisma: int,
    volume_atual: Optional[int],
    limete_de_volumes: Optional[int],
    resistencia: Optional[str],
    vulnerabilidade: Optional[str],
    imunidade: Optional[str],
    saldo: int,
    imagem: Optional[str],
    tokenn: Optional[str],
    usuario: Optional[int],
    id_party: Optional[str],
    id: Optional[str] = None,
) -> uuid.UUID:
    if id is None:
        id = uuid.uuid4()
    else:
        id = uuid.UUID(id)
    personagem_novo = f"""{database.constantes.INSERT_PERSONAGEM}
    VALUES ('{id}', '{nome}', '{nickname}', {level}, '{legacy}', '{classe}', '{path}', '{heritage}', '{melancholy}', {catarse}, {pe}, {pe_atual}, {hp}, {hp_atual}, '{hp_tipo}', {reducao_de_dano}, {bonus_de_proficiencia}, ARRAY['{"', '".join(pericias)}']::UUID[], {pontos_de_sombra}, {protecao_forca}, {bonus_forca}, {protecao_destreza}, {bonus_destreza}, {protecao_contituicao}, {bonus_contituicao}, {protecao_inteligencia}, {bonus_inteligencia}, {protecao_sabedoria}, {bonus_sabedoria}, {protecao_carisma}, {bonus_carisma}, {volume_atual}, {limete_de_volumes}, '{resistencia}', '{vulnerabilidade}', '{imunidade}', {saldo}, '{imagem}', '{tokenn}', '{usuario}', '{id_party}');"""
    with conexao.get_cursor() as cursor:
        cursor.execute(f"{personagem_novo}\n")
    return id


def pegar_personagem_com_id(
    conexao: PostgresDB, id: uuid.UUID | str
) -> database.models.Personagem:
    with conexao.get_cursor() as cursor:
        cursor.execute(f"SELECT * FROM personagens WHERE id_personagem='{id}';")
        resultado_personagem = cursor.fetchone()

        cursor.execute(f"SELECT id_skill FROM skills WHERE id_personagem='{id}'")
        resultado_skills = cursor.fetchall()

        cursor.execute(f"SELECT id_passiva FROM passivas WHERE id_personagem='{id}'")
        resultado_passivas = cursor.fetchall()

        cursor.execute(f"SELECT id_talento FROM talentos WHERE id_personagem='{id}'")
        resultado_talentos = cursor.fetchall()

        cursor.execute(f"SELECT * FROM itens_personagens WHERE id_personagem='{id}'")
        resultado_itens_personagens = cursor.fetchall()

        # cursor.execute(f"SELECT * FROM pericias_personagens WHERE id_personagem='{id}'")
        # resultado_pericias_personagens = cursor.fetchall()

    kwargs = {}
    for k in [
        "id_personagem",
        "nome",
        "nickname",
        "level",
        "legacy",
        "classe",
        "path",
        "heritage",
        "melancholy",
        "catarse",
        "pe",
        "pe_atual",
        "hp",
        "hp_atual",
        "hp_tipo",
        "reducao_de_dano",
        "bonus_de_proficiencia",
        "pontos_de_sombra",
        "resistencia",
        "vulnerabilidade",
        "imunidade",
        "volume_atual",
        "limite_de_volume",
        "saldo",
        "imagem",
        "tokenn",
        "usuario",
    ]:
        kwargs[k] = resultado_personagem[k]

    kwargs["atributos"] = {
        "forca": {
            "protection": resultado_personagem["protecao_forca"],
            "bonus": resultado_personagem["bonus_forca"],
        },
        "destreza": {
            "protection": resultado_personagem["protecao_destreza"],
            "bonus": resultado_personagem["bonus_destreza"],
        },
        "constituicao": {
            "protection": resultado_personagem["protecao_constituicao"],
            "bonus": resultado_personagem["bonus_constituicao"],
        },
        "inteligencia": {
            "protection": resultado_personagem["protecao_inteligencia"],
            "bonus": resultado_personagem["bonus_inteligencia"],
        },
        "sabedoria": {
            "protection": resultado_personagem["protecao_sabedoria"],
            "bonus": resultado_personagem["bonus_sabedoria"],
        },
        "carisma": {
            "protection": resultado_personagem["protecao_carisma"],
            "bonus": resultado_personagem["bonus_carisma"],
        },
    }
    skills_true = []
    for s in resultado_skills:
        skills_true.append(
            database.skills.pegar_skill(conexao, s["id_skill"]).model_dump()
        )
    kwargs["skills"] = skills_true

    passivas_true = []
    for p in resultado_passivas:
        passivas_true.append(
            database.passivas_talentos.pegar_passiva(
                conexao, p["id_passiva"]
            ).model_dump()
        )
    kwargs["passivas"] = passivas_true

    talentos_true = []
    for t in resultado_talentos:
        talentos_true.append(
            database.passivas_talentos.pegar_talento(
                conexao, t["id_talento"]
            ).model_dump()
        )
    kwargs["talentos"] = talentos_true

    itens_true = []
    for i in resultado_itens_personagens:
        item = database.item.pegar_item(conexao, i["id_item"]).model_dump()
        itens_true.append(
            database.models.ItemDeInventario(
                item=item, quantidade=i["quantidade"]
            ).model_dump()
        )
    kwargs["inventario"] = itens_true

    pericias_true = []
    for p in resultado_personagem["pericias"][1:-1].split(","):
        pericias_true.append(database.pericias.pegar_pericia(conexao, p).model_dump())
    kwargs["pericias"] = pericias_true

    return database.models.Personagem(**kwargs)

def pegar_todos_os_personagens(conexao: PostgresDB) -> list[database.models.Personagem]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT id_personagem FROM personagens ORDER BY nome;")
        return [pegar_personagem_com_id(conexao, r["id_personagem"]) for r in cursor.fetchall()]
    
def pegar_todos_os_id_dos_personagens(conexao: PostgresDB) -> list[uuid.UUID]:
    with conexao.get_cursor() as cursor:
        cursor.execute("SELECT id_personagem FROM personagens ORDER BY nome;")
        return [r["id_personagem"] for r in cursor.fetchall()]

def pegar_id_por_nome_ou_nick(conexao: PostgresDB, personagem: str):
    with conexao.get_cursor() as cursor:
        cursor.execute(
            f"SELECT id_personagem FROM personagens WHERE nome = '{personagem}';"
        )
        resultado = cursor.fetchone()
        if resultado is None:
            cursor.execute(
                f"SELECT id_personagem FROM personagens WHERE nickname = '{personagem}';"
            )
            resultado = cursor.fetchone()
    id_personagem = resultado["id_personagem"]
    return id_personagem


def pegar_id_por_user_id(conexao: PostgresDB, user_id: int):
    with conexao.get_cursor() as cursor:
        cursor.execute(
            f"SELECT id_personagem FROM personagens WHERE usuario = '{user_id}';"
        )
        resultado = cursor.fetchone()
    id_personagem = resultado["id_personagem"]
    return id_personagem
