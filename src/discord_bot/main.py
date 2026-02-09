import asyncio
import json
import os
import random
import sys
import time
from collections import deque
from time import sleep
from typing import Optional

import discord
from dado import TipoDadoResultado, girar_dados, girar_dados_str
from discord import FFmpegPCMAudio, Interaction, app_commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from ficha import PaginaFicha
from redis import Redis
from skills import PaginaSkills

import database.condicoes
import database.descritores
import database.item
import database.models
import database.party
import database.passivas_talentos
import database.pericias
import database.personagens
import database.skills
from database.connect_postgres import PostgresDB

# from map.map import criar_mapa

load_dotenv()
xmercury = Bot(command_prefix="!", intents=discord.Intents.all())
postgres_db = PostgresDB(
    os.getenv("POSTGRES_DB"),
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_PORT"),
)
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)
ADMS = [766039963736866828, 1119222124368896020, 921158705075077150, 813254664241414144]
MARCH = "<:march:1302059770785824861>"
token = os.getenv("DISCORD_TOKEN")
KEYSPACE = os.getenv("KEYSPACE")
redis_client.set("estado_nd", 10)
redis_client.set("turno", 0)

som_atual = None
musicas = os.listdir("/code/assets/songs")
random.shuffle(musicas)

for m in musicas:
    redis_client.rpush("queue", f"/code/assets/songs/{m}")


@xmercury.event
async def on_ready():
    await xmercury.tree.sync()
    await xmercury.change_presence(
        status=discord.Status.idle,
    )
    print("XMercury se apresentando para o serviço @v@")


@app_commands.choices(
    sfx=[
        app_commands.Choice(name="Echo of Pomona: Smashing Impact", value="eop_adam"),
        app_commands.Choice(name="Echo of Pomona: The Cage", value="eop_chrollo"),
        app_commands.Choice(name="Echo of Pomona: Blood Rain", value="eop_gunther"),
        app_commands.Choice(
            name="Echo of Pomona: The Rising of the Shadows", value="eop_julius"
        ),
        app_commands.Choice(
            name="Echo of Pomona: Energy Concentracion", value="eop_vincenzo"
        ),
        app_commands.Choice(
            name="Echo of Pomona: Entei no Gekirin ", value="eop_tsuko"
        ),
        app_commands.Choice(name='"Erga-se Fenrir..."', value="theme_fenrir"),
        app_commands.Choice(name='"Quer descobrir como uma pesadelo se torna real?"', value="theme_demitre"),
        app_commands.Choice(name='"Quer descobrir como uma pesadelo se torna real?" - Instrumental', value="theme_demitre_instrumental"),
    ]
)
@xmercury.tree.command(
    name="efeito_sonoro",
    description="O bot entra na call e solta alguns sons para melhorar a gameplay do RPG",
)
async def efeito_sonoro(interaction: Interaction, sfx: app_commands.Choice[str]):
    # try:
    #     if interaction.user.voice:
    #         channel = interaction.user.voice.channel
    #         voice = await channel.connect()
    #         await interaction.response.send_message(MARCH, ephemeral=True)
    #         sound_effect = f"/code/assets/sfx/{sfx.value}.mp3"
    #         voice = interaction.guild.voice_client
    #         source = discord.FFmpegPCMAudio(sound_effect)
    #         audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.3)
    #         player = voice.play(audio_com_volume)

    # except discord.ClientException:
    #     sound_effect = f"/code/assets/sfx/{sfx.value}.mp3"
    #     voice = interaction.guild.voice_client
    #     await interaction.response.send_message(MARCH, ephemeral=True)
    #     source = discord.FFmpegPCMAudio(sound_effect)
    #     audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
    #     player = voice.play(audio_com_volume)
    if not interaction.user.voice:
        await interaction.response.send_message(
            "Você precisa estar em uma call.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(MARCH, ephemeral=True)

    channel = interaction.user.voice.channel
    voice = interaction.guild.voice_client

    if not voice:
        voice = await channel.connect()

    while voice.is_playing():
        await asyncio.sleep(0.05)

    sound_path = f"/code/assets/sfx/{sfx.value}.mp3"

    source = discord.FFmpegOpusAudio(sound_path)
    voice.play(source)

@app_commands.choices(
    vantagem=[
        app_commands.Choice(name="Vantagem", value="vantagem"),
        app_commands.Choice(name="Desvantagem", value="desvantagem"),
    ]
)
@xmercury.tree.command(
    name="d",
    description="Gira um dado com quantidade de lados determinada pelo usuário",
)
async def dado(
    interaction: Interaction,
    numero: int,
    dados: Optional[int] = 1,
    vantagem: Optional[app_commands.Choice[str]] = None,
    bonus: Optional[int] = 0,
):
    if vantagem is not None:
        vantagem = vantagem.value
    dado = girar_dados(numero, dados, vantagem, bonus)
    embed = discord.Embed(
        title=dado.titulo,
        description=dado.mensagem,
        colour=discord.Colour.from_str("#226089"),
    )
    if dado.gif is not None:
        await interaction.response.send_message(dado.gif)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message(embed=embed)


@app_commands.choices(
    personagem=[
        app_commands.Choice(
            name="Shin NovaChrollo", value="30180fc6-30ba-4f65-a520-53e63bc4ec65"
        ),
        app_commands.Choice(
            name="Julius Wick", value="69fa11c2-ca6a-44b7-93c2-b744d0e98554"
        ),
        app_commands.Choice(
            name="Hyller Wick", value="a38675f6-b1d5-427b-b5a6-dbb46eefee16"
        ),
        app_commands.Choice(
            name="Adam Andrews", value="1c773acd-295b-436d-b792-8011e739e527"
        ),
        app_commands.Choice(
            name="Max", value="e3c79d34-cfb3-418f-b382-32b12fe2dafa"
        ),
        app_commands.Choice(
            name="Gunther Nosferata", value="e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8"
        ),
        app_commands.Choice(
            name="Vincenzo LeBlanc", value="a69e5fee-70c8-47d2-b8f8-6364f08b87d0"
        ),
        app_commands.Choice(
            name="Tsuko Hangetsu", value="7eac7b56-f4d4-4177-89d6-748da17b531c"
        ),
        app_commands.Choice(
            name="Zênite", value="3328a565-9f71-48f1-a0ef-dbdc403e8640"
        ),
        app_commands.Choice(name="Fenrir", value="73939ac9-83ac-481e-a855-ca02380ba48f"),
        app_commands.Choice(name="Ashborn", value="0add69b7-771e-4580-a11b-bf1a75d35aa9"),
    ]
)
@xmercury.tree.command(
    name="ficha",
    description="Mostra a ficha do usuário",
)
async def ficha(
    interaction: Interaction, personagem: Optional[app_commands.Choice[str]]
):
    await interaction.response.defer(ephemeral=True)
    if personagem is None:
        p_id = str(
            database.personagens.pegar_id_por_user_id(postgres_db, interaction.user.id)
        )
    else:
        p_id = personagem.value
    print(p_id)
    personagem = database.personagens.pegar_personagem_com_id(postgres_db, p_id)
    print(personagem)
    view = PaginaFicha(personagem)
    embed = view.criar_ficha()
    view.send(interaction)
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)


@app_commands.choices(
    audio=[
        app_commands.Choice(name="Desativar áudio", value="False"),
        app_commands.Choice(name="Não desativar áudio", value="True"),
    ]
)
@xmercury.tree.command(
    name="mute",
    description="Muta todos os participantes de uma call",
)
async def mute(
    interaction: Interaction,
    execao: Optional[discord.Member],
    audio: Optional[app_commands.Choice[str]],
):
    author = interaction.user
    if author.id in ADMS:
        if not author.voice or not author.voice.channel:
            await interaction.response.send_message(
                "Você precisa estar em um canal de voz para usar este comando."
            )
            return
        audio = None or bool(audio)
        canal = author.voice.channel
        if execao is not None:
            execao = execao.id
            for membro in canal.members:
                if (
                    membro.bot == False
                    and execao != membro.id
                    and membro.id != 766039963736866828
                ):
                    try:
                        await membro.edit(mute=True, deafen=audio)
                    except discord.Forbidden:
                        await interaction.response.send_message(
                            f"Não tenho permissão para mutar {membro.mention}."
                        )
            await interaction.response.send_message(
                f"Todos os membros do canal **{canal.name}** foram mutados!",
                ephemeral=True,
            )
        else:
            for membro in canal.members:
                if membro.bot == False and membro.id != 766039963736866828:
                    try:
                        await membro.edit(mute=True, deafen=audio)
                    except discord.Forbidden:
                        await interaction.response.send_message(
                            f"Não tenho permissão para mutar {membro.mention}."
                        )
            await interaction.response.send_message(
                f"Todos os membros do canal **{canal.name}** foram mutados!",
                ephemeral=True,
            )
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando", ephemeral=True
        )


# @xmercury.tree.command(
#     name="mapa",
#     description="Desmuta todos os participantes de uma call",
# )
# async def mapa(interaction: Interaction):
#     buffer = criar_mapa(
#         "map/mapa.png",
#         [
#             ("map/tokens/chrollo_token.png", (28, 0)),
#             ("map/tokens/julius_token.png", (0, 0)),
#             ("map/tokens/gunther_token.png", ((29 * 9), (29 * 10))),
#         ],
#     )
#     await interaction.response.send_message(
#         file=discord.File(buffer, filename="mapa.png")
#     )


@xmercury.tree.command(
    name="pericias",
    description="Mostra todas as perícias do sistema",
)
async def pericias(interaction: Interaction):
    pericias = database.pericias.pegar_todas_as_pericias(postgres_db)
    print(pericias)
    embed = discord.Embed(
        title="Perícias",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    for p in pericias:
        embed.add_field(
            name=p.nome,
            value=p.descricao,
            inline=False,
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@xmercury.tree.command(
    name="condicoes",
    description="Mostra todas as condições do sistema",
)
async def condicoes(interaction: Interaction):
    condicoes = database.condicoes.pegar_todas_as_condicoes(postgres_db)

    embed = discord.Embed(
        title="Condições",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    for c in condicoes:
        embed.add_field(
            name=c.nome,
            value=c.descricao,
            inline=False,
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@xmercury.tree.command(
    name="descritor",
    description="Mostra todas as condições do sistema",
)
async def descritor(interaction: Interaction):
    descritores = database.descritores.pegar_todos_os_descritores(postgres_db)

    embed = discord.Embed(
        title="Condições",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    for d in descritores:
        embed.add_field(
            name=d.nome,
            value=d.descricao,
            inline=False,
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.choices(
    pericia=[
        app_commands.Choice(name=p.nome, value=str(p.id_pericia))
        for p in database.pericias.pegar_todas_as_pericias(postgres_db)
        if p.e_soma or p.e_vantagem
    ]
)
@xmercury.tree.command(
    name="girar_pericias",
    description="Gira um teste de uma perícia",
)
async def girar_pericias(interaction: Interaction, pericia: app_commands.Choice[str]):
    await interaction.response.defer()
    p_id = database.personagens.pegar_id_por_user_id(postgres_db, interaction.user.id)
    personagem = database.personagens.pegar_personagem_com_id(postgres_db, p_id)
    p = database.pericias.pegar_pericia(postgres_db, pericia.value)
    if p in personagem.pericias:
        if p.e_vantagem and p.e_soma:
            possiveis_bonus = []
            for k in p.somar:
                if k == "bonus_de_proficiencia":
                    possiveis_bonus.append(personagem.bonus_de_proficiencia)
                else:
                    atributos = personagem.atributos
                    atributo = getattr(atributos, k)
                    possiveis_bonus.append(atributo.bonus)
            dado = girar_dados(20, 1, "vantagem", max(possiveis_bonus))

        elif p.e_vantagem:
            dado = girar_dados(20, 1, "vantagem", 0)

        elif p.e_soma:
            possiveis_bonus = []
            for k in p.somar:
                if k == "bonus_de_proficiencia":
                    possiveis_bonus.append(personagem.bonus_de_proficiencia)
                else:
                    atributos = personagem.atributos
                    atributo = getattr(atributos, k)
                    possiveis_bonus.append(atributo.bonus)

            dado = girar_dados(20, 1, None, max(possiveis_bonus))
        else:
            raise RuntimeError("Todos as perícias deveriam ser vantagem ou soma")
    else:
        dado = girar_dados(20, 1, None, 0)

    embed = discord.Embed(
        title=dado.titulo,
        description=dado.mensagem,
        colour=discord.Colour.from_str("#226089"),
    )
    if dado.gif is not None:
        await interaction.followup.send(dado.gif)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(embed=embed)


@xmercury.tree.command(
    name="party",
    description="Mostra as principais informações da equipe atual",
)
async def party(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    party = database.party.pegar_party(
        postgres_db, "8a87e68e-cd9d-46e5-953a-35942487ef1b"
    )
    embed = discord.Embed(
        title="Party",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    barra_completa = 10
    barra_cheia = round(
        (party.personagens_jogaveis[-1].hp_atual / party.personagens_jogaveis[-1].hp)
        * barra_completa
    )
    barra_vazia = barra_completa - barra_cheia
    for p in party.personagens_jogaveis[:-1]:
        embed.add_field(
            name=f"{p.tokenn} {p.nickname} ­PE: {p.pe_atual}",
            value=f"{'█' * barra_cheia}{'░' * barra_vazia} ­ ­ ­ ­ ­ ­{p.hp_atual}/{p.hp}\n ­",
            inline=False,
        )
    embed.add_field(
        name=f"{party.personagens_jogaveis[-1].tokenn} {party.personagens_jogaveis[-1].nickname} ­ ­ ­ ­PE: {party.personagens_jogaveis[-1].pe_atual}",
        value=f"{'█' * barra_cheia}{'░' * barra_vazia} {party.personagens_jogaveis[-1].hp_atual}/{party.personagens_jogaveis[-1].hp}",
        inline=False,
    )

    await interaction.followup.send(embed=embed, ephemeral=True)


@app_commands.choices(
    vantagem=[
        app_commands.Choice(name="Vantagem", value="vantagem"),
        app_commands.Choice(name="Desvantagem", value="desvantagem"),
    ],
    personagem=[
        app_commands.Choice(
            name="Shin NovaChrollo", value="30180fc6-30ba-4f65-a520-53e63bc4ec65"
        ),
        app_commands.Choice(
            name="Julius Wick", value="69fa11c2-ca6a-44b7-93c2-b744d0e98554"
        ),
        app_commands.Choice(
            name="Adam Andrews", value="1c773acd-295b-436d-b792-8011e739e527"
        ),
        app_commands.Choice(
            name="Gunther Nosferata", value="e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8"
        ),
        app_commands.Choice(
            name="Vincenzo LeBlanc", value="a69e5fee-70c8-47d2-b8f8-6364f08b87d0"
        ),
        app_commands.Choice(
            name="Tsuko Hangetsu", value="7eac7b56-f4d4-4177-89d6-748da17b531c"
        ),
        app_commands.Choice(
            name="Zênite", value="3328a565-9f71-48f1-a0ef-dbdc403e8640"
        ),
        app_commands.Choice(name="Fenrir", value="a"),
        app_commands.Choice(name="Ashborn", value="a"),
    ],
)
@xmercury.tree.command(
    name="skills",
    description="Mostra as principais informações da equipe atual",
)
async def skills(
    interaction: Interaction,
    personagem: Optional[app_commands.Choice[str]],
    vantagem: Optional[app_commands.Choice[str]] = None,
):
    await interaction.response.defer(ephemeral=True)
    if personagem is None:
        p_id = str(
            database.personagens.pegar_id_por_user_id(postgres_db, interaction.user.id)
        )
    else:
        p_id = personagem.value

    p = database.personagens.pegar_personagem_com_id(postgres_db, p_id)
    view = PaginaSkills(p, len(p.skills))
    embed = view.criar_pagina_skill()
    view.send(interaction)
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    # skills_filtradas = [s for s in personagem.skills if s.ataque is not None]

    # await interaction.response.defer()

    # if vantagem is not None:
    #     vantagem = vantagem.value

    # if numero is None:
    #     skills_string = ""
    #     for i, s in enumerate(skills_filtradas):
    #         skills_string += f"{i + 1} - {s.nome}\n"

    #     embed_skills = discord.Embed(
    #         title="Suas skills",
    #         description=skills_string,
    #         colour=discord.Colour.from_str("#226089"),
    #     )
    #     await interaction.followup.send(embed=embed_skills)

    # else:
    #     skill_selecionada = skills_filtradas[numero]

    #     dado = girar_dados_str(skill_selecionada.ataque.split("vs")[0], vantagem)
    #     mensagem_adicional = ""
    #     estado_nd = int(redis_client.get("estado_nd"))

    #     if (
    #         dado.valor_total >= estado_nd
    #         or dado.tipo == TipoDadoResultado.ACERTO_CRITICO
    #     ):
    #         mensagem_adicional = "\n**Acertou o ataque!**"
    #     else:
    #         mensagem_adicional = "\n**Errou o ataque!**"

    #     embed = discord.Embed(
    #         title=dado.titulo,
    #         description=dado.mensagem + mensagem_adicional,
    #         colour=discord.Colour.from_str("#226089"),
    #     )
    #     if dado.gif is not None:
    #         embed.set_image(url=dado.gif)

    #     await interaction.followup.send(embed=embed)


@xmercury.tree.command(
    name="nd",
    description="Injeta uma dificuldade para um teste futuro",
)
async def nd(
    interaction: Interaction,
    nd: int,
):
    redis_client.set("estado_nd", nd)
    await interaction.response.send_message("MARCH")


async def tocar_proximo(interaction: discord.Interaction):
    global som_atual, musica_inicio
    queue = redis_client.lrange("queue", 0, -1)
    if len(queue) == 0:
        random.shuffle(musicas)

        for m in musicas:
            redis_client.rpush("queue", f"/code/assets/songs/{m}")

    musica_atual = redis_client.lpop("queue")
    som_atual = f"/code/assets/songs/{musica_atual}"

    voice = interaction.guild.voice_client
    source = discord.FFmpegPCMAudio(musica_atual)
    audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
    voice.play(
        audio_com_volume,
        after=lambda _: asyncio.run_coroutine_threadsafe(
            tocar_proximo(interaction), xmercury.loop
        ),
    )
    musica_inicio = time.time()


@xmercury.tree.command(
    name="playlist",
    description="Inicia a playlist de batalha do RPG em ordem aleatória na call",
)
async def playlist(interaction: Interaction, start: Optional[str]):
    if start is not None:
        redis_client.rpush(start)

    try:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            await interaction.response.send_message(MARCH, ephemeral=True)
            if not voice.is_playing():
                await tocar_proximo(interaction)

    except discord.ClientException:
        channel = interaction.user.voice.channel
        voice = await channel.connect()
        await interaction.response.send_message(MARCH, ephemeral=True)
        if not voice.is_playing():
            await tocar_proximo(interaction)


@xmercury.tree.command(
    name="girar_iniciativa",
    description="girar_iniciativa",
)
async def girar_iniciativa(
    interaction: Interaction,
):
    redis_client.set("turno", 0)
    # girar iniciativas
    await interaction.response.send_message(MARCH)


@xmercury.tree.command(
    name="encerrar_turno",
    description="encerrar_turno",
)
async def encerrar_turno(
    interaction: Interaction,
):
    redis_client.incr("turno")
    await interaction.response.send_message(MARCH)


@xmercury.tree.command(
    name="iniciativa",
    description="iniciativa",
)
async def iniciativa(
    interaction: Interaction,
):
    turno = int(redis_client.get("turno"))
    with open("battle.json", "r") as f:
        batalha = json.load(f)

    batalha = batalha["batalha"]
    batalha = sorted(batalha, reverse=True, key=lambda item: item["iniciativa"])
    embed = discord.Embed(
        title="Iniciativas",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    for i, p in enumerate(batalha):
        if turno % len(batalha) == i:
            embed.add_field(
                name=f':arrow_forward:  {p["id"]}', value=p["iniciativa"], inline=False
            )
        else:
            embed.add_field(name=p["id"], value=p["iniciativa"], inline=False)

    await interaction.response.send_message(embed=embed)


xmercury.run(token)
