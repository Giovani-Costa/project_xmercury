import uuid



import database.models
import database.personagens
import database.constantes
from database.connect_postgres import PostgresDB


def pegar_party(conexao: PostgresDB, id: uuid.UUID | str) -> database.models.Party:
    comando = f"SELECT id_personagem FROM personagens WHERE id_party='{id}';"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        lista_dict_id_personagem = cursor.fetchall()
        cursor.execute(f"SELECT nome FROM party WHERE id_party='{id}';")
        nome_party = cursor.fetchone()["nome"]
        print(f"Nome da party: {nome_party}")

    personagens_true = []
    for p in lista_dict_id_personagem:
        personagens_true.append(
            database.personagens.pegar_personagem_com_id(
                conexao, p["id_personagem"]
            ).model_dump()
        )

    return database.models.Party(id_party=id, personagens_jogaveis=personagens_true, nome=nome_party)

def pegar_todas_as_parties(conexao: PostgresDB) -> list[database.models.Party]:
    comando = f"SELECT * FROM party;"
    with conexao.get_cursor() as cursor:
        cursor.execute(comando)
        resultado = cursor.fetchall()

    lista_parties = []
    
    for r in resultado:
        data = dict(r)
        data["personagens_jogaveis"] = []
        lista_parties.append(database.models.Party(**data))
        # lista_parties.append(database.models.Party(**dict(r)))
        lista_parties.sort(key=lambda p: p.nome.lower())

    return lista_parties

def criar_party(conexao: PostgresDB, nome: str, id_party: uuid.UUID | str) -> uuid.UUID: 
    with conexao.get_cursor() as cursor:
        party_novo = f"""{database.constantes.INSERT_PARTY}
VALUES ('{id_party}', '{nome}');"""
        cursor.execute(party_novo)
        print(f"{party_novo}\n")
    return id_party