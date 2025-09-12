import os
import random
from typing import Optional

import discord
from discord import FFmpegPCMAudio, Interaction, Message, app_commands
from discord.ext.commands import Bot

import database.condicoes
import database.item
import database.models
import database.party
import database.passivas_talentos
import database.pericias
import database.personagens
import database.skill
from constantes import ADMS, KEYSPACE, MARCH
from dado import TipoDadoResultado, girar_dados, girar_dados_str
from database.connect_database import criar_session
from ficha import PaginaFicha
from key import key
from map.map import criar_mapa

xmercury = Bot(command_prefix="!", intents=discord.Intents.all())
session = criar_session()
token = key.get("token")


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
            name="Echo of Pomona: Entei no Gekirin ", value="eop_tsuku"
        ),
        app_commands.Choice(name='"Erga-se Fenrir..."', value="theme_fenrir"),
    ]
)
@xmercury.tree.command(
    name="efeito_sonoro",
    description="O bot entra na call e solta alguns sons para melhorar a gameplay do RPG",
)
async def efeito_sonoro(interaction: Interaction, sfx: app_commands.Choice[str]):
    try:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            await interaction.response.send_message(MARCH, ephemeral=True)
            sound_effect = f"sfx\{sfx.value}.mp3"
            voice = interaction.guild.voice_client
            source = discord.FFmpegPCMAudio(sound_effect)
            audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
            player = voice.play(audio_com_volume)

    except discord.ClientException:
        sound_effect = f"sfx\{sfx.value}.mp3"
        voice = interaction.guild.voice_client
        await interaction.response.send_message(MARCH, ephemeral=True)
        source = discord.FFmpegPCMAudio(sound_effect)
        audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
        player = voice.play(audio_com_volume)


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
            name="Adam Andrews", value="1c773acd-295b-436d-b792-8011e739e527"
        ),
        app_commands.Choice(
            name="Gunther Nosferata", value="e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8"
        ),
        app_commands.Choice(name="Vincenzo LeBlanc", value="a"),
        app_commands.Choice(name="Zênite", value="a"),
        app_commands.Choice(name="Fenrir", value="a"),
        app_commands.Choice(name="Ashborn", value="a"),
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
            database.personagens.pegar_id_por_user_id(session, interaction.user.id)
        )
    else:
        p_id = personagem.value
    p = database.personagens.pegar_personagem_com_id(session, p_id)
    view = PaginaFicha(p)
    embed = view.criar_embed()
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


@xmercury.tree.command(
    name="mapa",
    description="Desmuta todos os participantes de uma call",
)
async def mapa(interaction: Interaction):
    buffer = criar_mapa(
        "map/mapa.png",
        [
            ("map/tokens/chrollo_token.png", (28, 0)),
            ("map/tokens/julius_token.png", (0, 0)),
            ("map/tokens/gunther_token.png", ((29 * 9), (29 * 10))),
        ],
    )
    await interaction.response.send_message(
        file=discord.File(buffer, filename="mapa.png")
    )


@xmercury.tree.command(
    name="pericias",
    description="Mostra todas as perícias do sistema",
)
async def pericias(interaction: Interaction):
    pericias = database.pericias.pegar_todas_as_pericias(session)
    dm_channel = await interaction.user.create_dm()

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

    await interaction.response.send_message(MARCH, ephemeral=True)
    await dm_channel.send(embed=embed)


@xmercury.tree.command(
    name="condicoes",
    description="Mostra todas as condições do sistema",
)
async def condicoes(interaction: Interaction):
    condicoes = database.pericias.pegar_todas_as_pericias(session)
    dm_channel = await interaction.user.create_dm()

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

    await interaction.response.send_message(MARCH, ephemeral=True)
    await dm_channel.send(embed=embed)


@app_commands.choices(
    pericia=[
        app_commands.Choice(name=p.nome, value=str(p.id))
        for p in database.pericias.pegar_todas_as_pericias(session)
        if p.e_soma or p.e_vantagem
    ]
)
@xmercury.tree.command(
    name="girar_pericias",
    description="Gira um teste de uma perícia",
)
async def girar_pericias(interaction: Interaction, pericia: app_commands.Choice[str]):
    await interaction.response.defer()
    p_id = database.personagens.pegar_id_por_user_id(session, interaction.user.id)
    personagem = database.personagens.pegar_personagem_com_id(session, p_id)
    p = database.pericias.pegar_pericia(session, pericia.value)
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
    party = database.party.pegar_party(session, "8a87e68e-cd9d-46e5-953a-35942487ef1b")
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
    ]
)
@xmercury.tree.command(
    name="skills",
    description="Mostra as principais informações da equipe atual",
)
async def skills(
    interaction: Interaction,
    vantagem: Optional[app_commands.Choice[str]] = None,
):
    await interaction.response.defer()
    if vantagem is not None:
        vantagem = vantagem.value
    p_id = str(database.personagens.pegar_id_por_user_id(session, interaction.user.id))
    personagem = database.personagens.pegar_personagem_com_id(session, p_id)

    string = ""
    for i, s in enumerate(personagem.skills):
        string += f"{i + 1} - {s.nome}\n"

    await interaction.followup.send(string)

    def e_inteiro(mensagem: Message) -> bool:
        try:
            int(mensagem.content)
            return True
        except:
            return False

    mensagem = await xmercury.wait_for("message", check=e_inteiro, timeout=15.0)
    skill_selecionada = personagem.skills[int(mensagem.content) - 1]
    dado = girar_dados_str(skill_selecionada.ataque.split("vs")[0], vantagem)
    embed = discord.Embed(
        title=dado.titulo,
        description=dado.mensagem,
        colour=discord.Colour.from_str("#226089"),
    )
    if dado.gif is not None:
        # await interaction.followup.send(dado.gif)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(embed=embed)


xmercury.run(token)
