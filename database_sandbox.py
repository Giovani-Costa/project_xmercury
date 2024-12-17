# alternativas LIST<TEXT>

import json
import os
import time
from random import choice

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

cloud_config = {"secure_connect_bundle": "secure-connect-xmercury.zip"}

with open("xmercury-token.json") as f:
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
    # session.execute(f"DROP TABLE {KEYSPACE}.personagens")
    # session.execute(f"DROP TABLE {KEYSPACE}.itens")

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
    #    modificacoes TEXT,
    #    carga TEXT
    # );
    # """
    # )
    # print("SKILLS CRIADA")
    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PASSIVAS E TALENTOS

    # session.execute(
    #    f"""
    # CREATE TABLE {KEYSPACE}.talentos (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    #    modificadores TEXT
    # );
    # """
    # )

    # session.execute(
    #    f"""
    # CREATE TABLE {KEYSPACE}.passivas (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    #    modificadores TEXT,
    #    gasto INT
    # );
    # """
    # )
    # print("PASSIVA E TALENTOS CRIADA")

    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PERSONAGENS

    # session.execute(
    #     f"""
    # CREATE TABLE {KEYSPACE}.personagens (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    nickname TEXT,
    #    classe TEXT,
    #    level INT,
    #    path TEXT,
    #    legacy TEXT,
    #    heritage TEXT,
    #    melancholy TEXT,
    #    catarse INT,
    #    pe_atual INT,
    #    pe_max INT,
    #    hp_atual INT,
    #    hp_max INT,
    #    reducao_de_dano INT,
    #    talentos LIST<UUID>,
    #    passivas LIST<UUID>,
    #    skills LIST<UUID>,
    #    iniciativa INT,
    #    forca LIST<INT>,
    #    dexterity LIST<INT>,
    #    constituicao LIST<INT>,
    #    inteligencia LIST<INT>,
    #    wisdom LIST<INT>,
    #    carisma LIST<INT>,
    #    inventario_itens LIST<UUID>,
    #    inventario_numero LIST<INT>
    # );
    # """
    # )
    # print("PERSONAGENS CRIADA")

    # --------------------------------------------------------------------------------------------

    # CRIAR A TABELA DE PERSONAGENS

    # session.execute(
    #    f"""
    # CREATE TABLE {KEYSPACE}.itens (
    #    id UUID PRIMARY KEY,
    #    nome TEXT,
    #    descricao TEXT,
    # );
    # """
    # )
    # print("ITENS CRIADA")

    # --------------------------------------------------------------------------------------------
    # PRINTAR TODOS OS ENUNCIADOS

    # a = session.execute(
    #     f"""
    #  SELECT * FROM {KEYSPACE}.passivas
    #     """
    # )

    # --------------------------------------------------------------------------------------------
    # CONTADOR DE skills

    # numero_de_questoes = session.execute(
    #     f"SELECT COUNT(*) FROM {KEYSPACE}.skills"
    # ).one()
    # print(numero_de_questoes)

    # --------------------------------------------------------------------------------------------

    #

    # questoes_acertadas = session.execute(
    #     f"SELECT questoes_acertadas FROM xmercury.usuarios WHERE discord_id = '766039963736866828' ALLOW FILTERING"
    # ).one()
    # print(questoes_acertadas)

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

    pass
