# alternativas LIST<TEXT>

import json
import os
import time
import uuid
from random import choice

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

# from database.item import pegar_item

cloud_config = {"secure_connect_bundle": "database\\secure-connect-xmercury.zip"}

with open("database\\xmercury-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
KEYSPACE = "xmercury"

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
with cluster.connect() as session:

    # session.execute(f"DROP TABLE {KEYSPACE}.skills")
    # session.execute(f"DROP TABLE {KEYSPACE}.talentos")
    # session.execute(f"DROP TABLE {KEYSPACE}.passivas")
    session.execute(f"DROP TABLE {KEYSPACE}.personagens")
    # session.execute(f"DROP TABLE {KEYSPACE}.itens")
    # session.execute(f"DROP TABLE {KEYSPACE}.party")

    # --------------------------------------------------------------------------------------------
    # CRIAR A TABELA DE SKILLS

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.skills (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    custo INT,
    #    execucao TEXT,
    #    descritores TEXT,
    #    alcance TEXT,
    #    duracao TEXT,
    #    ataque TEXT,
    #    acerto TEXT,
    #    erro TEXT,
    #    efeito TEXT,
    #    especial TEXT,
    #    gatilho TEXT,
    #    alvo TEXT,
    #    carga TEXT,
    #    modificador_execucao TEXT,
    #    modificador_nome TEXT,
    #    modificador_descricao TEXT,
    #    modificador_gasto INT,
    #    modificador_gasto_tipo TEXT
    # );
    # """
    # )
    # print("SKILLS CRIADA")
    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PASSIVAS E TALENTOS

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.talentos (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    #    modificador_execucao TEXT,
    #    modificador_nome TEXT,
    #    modificador_descricao TEXT,
    #    modificador_gasto INT,
    #    modificador_gasto_tipo TEXT

    # );
    # """
    # )

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.passivas (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    #    modificador_execucao TEXT,
    #    modificador_nome TEXT,
    #    modificador_descricao TEXT,
    #    modificador_gasto INT,
    #    modificador_gasto_tipo TEXT

    # );
    # """
    # )
    # print("PASSIVA E TALENTOS CRIADA")

    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PERSONAGENS

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.personagens (
       id UUID PRIMARY KEY,
       nome TEXT,
       nickname TEXT,
       level INT,
       legacy TEXT,
       classe TEXT,
       path TEXT,
       heritage TEXT,
       melancholy TEXT,
       catarse INT,
       pe INT,
       hp INT,
       reducao_de_dano INT,
       bonus_de_proficiencia INT,
       talentos LIST<UUID>,
       passivas LIST<UUID>,
       skills LIST<UUID>,
       forca LIST<INT>,
       dexterity LIST<INT>,
       constituicao LIST<INT>,
       inteligencia LIST<INT>,
       sabedoria LIST<INT>,
       carisma LIST<INT>,
       pontos_de_sombra INT,
       resistencia LIST<TEXT>,
       vulnerabilidade LIST<TEXT>,
       imunidade LIST<TEXT>,
       inventario_itens LIST<UUID>,
       inventario_numero LIST<INT>,
       condicoes LIST<TEXT>,
       saldo INT,
       imagem TEXT,
       usuario TEXT
        );"""
    )
    print("PERSONAGENS CRIADA")

    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE ITENS

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.itens (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    # );
    # """
    # )
    # print("ITENS CRIADA")
    # -------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PARTY

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.party (
    #    id UUID PRIMARY KEY,
    #    personagens LIST<UUID>,
    #    iniciativas INT,
    # );
    # """
    # )
    # print("PARTY CRIADA")

    # --------------------------------------------------------------------------------------------
    # PRINTAR TODOS OS ENUNCIADOS

    # a = session.execute(
    #     f"""
    #  SELECT * FROM {KEYSPACE}.skills;
    #     """
    # )
    # print(a)

    # --------------------------------------------------------------------------------------------
    # CONTADOR DE skills

    # numero_de_questoes = session.execute(
    #     f"SELECT COUNT(*) FROM {KEYSPACE}.skills"
    # ).one()
    # print(numero_de_questoes)

    # --------------------------------------------------------------------------------------------

    # COLOCAR INFORMAÇÕES EXTRAS

    # personagem_novo = f"""INSERT INTO {KEYSPACE}.personagens (usuario) WHERE id=899ab802-ad20-46fa-9b31-005bf6ead940
    # VALUES (921158705075077150);"""
    # a = session.execute("SELECT usuario FROM xmercury.personagens;")
    # print(a)

    # --------------------------------------------------------------------------------------------

    # for arquivo in os.listdir("./imagens"):
    #     link = f"https://raw.githubusercontent.com/Giovani-Costa/project_xmercury/main/imagens/{arquivo}"
    #     numero, semetre, ano = arquivo.split("_")
    #     ano = ano[0:-4]
    #     comando = f"""UPDATE xmercury.questoes
    # SET imagem = '{link}'
    # WHERE numero = {numero} AND semestre = {semetre} AND ano = {ano}"""
    #     session.execute(comando)

    # --------------------------------------------------------------------------------------------

    # session.execute(
    #     """
    # UPDATE xmercury.passivas SET modificadores = ' Efeito: você escolhe entre usar ação de _Desengajar_ como ação livre ou fazer com que qualquer criatura que entre na sua área de ameaça ou movimente-se dentro dela até começo do seu próximo turno provoque ataque de oportunidade.' WHERE id = 23eb133f-3095-4016-8f0b-0fc61457f968;"""
    # )

    # --------------------------------------------------------------------------------------------

    # item = pegar_item(session, uuid.UUID("9cc3b95e-11cc-4eee-ae40-424e43478123"))
    # print(item)
    pass
