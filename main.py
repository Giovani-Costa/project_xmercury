import random
import re
import uuid
from collections import deque
from time import sleep
from typing import Any, Coroutine, Optional

import discord
import disnake
import disnake.utils
import pandas as pd
from discord import FFmpegPCMAudio, Interaction, app_commands
from discord.ext.commands import Bot
from disnake.ext import commands

import database.item
import database.passivas_talentos
import database.personagens
import database.skill
from constante import ADMS, KEYSPACE
from database.connect_database import criar_session
from key import key

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


@xmercury.tree.command(
    name="join", description="O bot entra no canal de voz do usuário"
)
async def join(interaction: Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        voice = await channel.connect()
        await interaction.response.send_message(
            "<:march:1302059770785824861>", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            ":x:  Não foi possível entrar no canal de voz  :x:", ephemeral=True
        )


@xmercury.tree.command(name="leave", description="O bot sai da call que está")
async def leave(interaction: Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message(
            "https://tenor.com/view/bye-bye-bye-gif-12807868928498541318",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            ":x:  Não estou em nenhum canal de voz  :x:", ephemeral=True
        )


@app_commands.choices(
    sfx=[
        app_commands.Choice(name="Julius EP", value="Julius EP"),
        app_commands.Choice(name="Hiller EP", value="Hiller EP"),
    ]
)
@xmercury.tree.command(name="efeito_sonoro", description="O bot reproduz sons na call")
async def efeito_sonoro(interaction: Interaction, sfx: app_commands.Choice[str]):
    if interaction.user.voice:
        sound_effect = f"ep_sfx\{sfx.value[:-3]}.mp3"
        voice = interaction.guild.voice_client
        source = FFmpegPCMAudio(sound_effect)
        player = voice.play(source)


@app_commands.choices(
    execucao=[
        app_commands.Choice(name="Ação", value="acao"),
        app_commands.Choice(name="Ação Bônus", value="acao bonus"),
        app_commands.Choice(name="Reação", value="reacao"),
        app_commands.Choice(name="Ação Livre", value="acao livre"),
    ],
    modificador_execucao=[
        app_commands.Choice(name="Ação", value="acao"),
        app_commands.Choice(name="Ação Bônus", value="acao_bonus"),
        app_commands.Choice(name="Reação", value="reacao"),
        app_commands.Choice(name="Ação Livre", value="acao_livre"),
    ],
    modificador_gasto_tipo=[
        app_commands.Choice(name="PE", value="pe"),
        app_commands.Choice(name="PC", value="catarse"),
    ],
)
@xmercury.tree.command(
    name="mandar_skill", description="Adiciona uma skill ao banco de dados"
)
async def mandar_skill(
    interaction: Interaction,
    nome: str,
    custo: int,
    execucao: app_commands.Choice[str],
    descritores: Optional[str],
    alcance: Optional[str],
    duracao: Optional[str],
    ataque: Optional[str],
    acerto: Optional[str],
    erro: Optional[str],
    efeito: Optional[str],
    especial: Optional[str],
    gatilho: Optional[str],
    alvo: Optional[str],
    carga: Optional[str],
    modificador_execucao: Optional[app_commands.Choice[str]],
    modificador_nome: Optional[str],
    modificador_descricao: Optional[str],
    modificador_gasto: Optional[int],
    modificador_gasto_tipo: Optional[app_commands.Choice[str]],
):
    if modificador_execucao is not None:
        modificador_execucao = modificador_execucao.value

    if modificador_gasto_tipo is not None:
        modificador_gasto_tipo = modificador_gasto_tipo.value

    if modificador_gasto is None:
        modificador_gasto = 0

    if interaction.user.id in ADMS:
        id = database.skill.criar_skill(
            session,
            nome,
            custo,
            execucao.value,
            descritores,
            alcance,
            duracao,
            ataque,
            acerto,
            erro,
            efeito,
            especial,
            gatilho,
            alvo,
            carga,
            str(modificador_execucao),
            modificador_nome,
            modificador_descricao,
            modificador_gasto,
            str(modificador_gasto_tipo),
        )
        await interaction.response.send_message(
            f":white_check_mark: SKILL CRIADA COM SUCESSO! :white_check_mark:\nO UUID de {nome} é **{id}**"
        )
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@xmercury.tree.command(
    name="mandar_item",
    description="Adiciona um item ao banco de dados",
)
async def mandar_item(
    interaction: Interaction,
    nome: str,
    descricao: str,
):
    if interaction.user.id in ADMS:
        id = database.item.criar_item(
            session,
            nome,
            descricao,
        )
        await interaction.response.send_message(
            f":white_check_mark: ITEM CRIADO COM SUCESSO! :white_check_mark:\nO UUID de {nome} é **{id}**"
        )
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@app_commands.choices(
    tipo=[
        app_commands.Choice(name="Passiva", value="passivas"),
        app_commands.Choice(name="Talento", value="talentos"),
    ],
    modificador_execucao=[
        app_commands.Choice(name="Ação", value="acao"),
        app_commands.Choice(name="Ação Bônus", value="acao_bonus"),
        app_commands.Choice(name="Reação", value="reacao"),
        app_commands.Choice(name="Ação Livre", value="acao_livre"),
    ],
    modificador_gasto_tipo=[
        app_commands.Choice(name="PE", value="pe"),
        app_commands.Choice(name="PC", value="catarse"),
    ],
)
@xmercury.tree.command(
    name="mandar_talendo_ou_passiva",
    description="Adiciona um talento ou passiva ao banco de dados",
)
async def mandar_passiva_talento(
    interaction: Interaction,
    tipo: app_commands.Choice[str],
    nome: str,
    descricao: str,
    modificador_execucao: Optional[app_commands.Choice[str]],
    modificador_nome: Optional[str],
    modificador_descricao: Optional[str],
    modificador_gasto: Optional[int],
    modificador_gasto_tipo: Optional[app_commands.Choice[str]],
):

    if interaction.user.id in ADMS:
        if modificador_execucao is not None:
            modificador_execucao = modificador_execucao.value

        if modificador_gasto_tipo is not None:
            modificador_gasto_tipo = modificador_gasto_tipo.value

        if modificador_descricao is None:
            modificador_descricao = 0

        id = database.passivas_talentos.criar_passiva_talento(
            session,
            tipo.value,
            nome,
            descricao,
            str(modificador_execucao),
            modificador_nome,
            modificador_descricao,
            modificador_gasto,
            str(modificador_gasto_tipo),
        )
        await interaction.response.send_message(
            f":white_check_mark: PASSIVA/TALENTO CRIADE COM SUCESSO! :white_check_mark:\nO UUID de {nome} é **{id}**"
        )
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@app_commands.choices(
    classe=[
        app_commands.Choice(name="Combatente", value="Combatente"),
        app_commands.Choice(name="Especialista", value="Especialista"),
        app_commands.Choice(name="Ocultista", value="Ocultista"),
    ],
    legacy=[
        app_commands.Choice(name="Anuro", value="Anuro"),
        app_commands.Choice(name="Draco", value="Draco"),
        app_commands.Choice(name="Elfe", value="Elfe"),
        app_commands.Choice(name="Gnomo", value="Gnomo"),
        app_commands.Choice(name="Humano", value="Humano"),
        app_commands.Choice(name="Orc", value="Orc"),
        app_commands.Choice(name="Sanguires", value="Sanguir"),
        app_commands.Choice(name="Tatsunoko", value="Tatsunoko"),
        app_commands.Choice(name="Tôra", value="Tôra"),
        app_commands.Choice(name="Urodelo", value="Urodelo"),
        app_commands.Choice(name="Walshie", value="Walshie"),
    ],
    path=[
        app_commands.Choice(name="Alquimista", value="Alquimista"),
        app_commands.Choice(name="Artesão de Guilda", value="Artesão de Guilda"),
        app_commands.Choice(name="Cavaleiro Tóptero", value="Cavaleiro Tóptero"),
        app_commands.Choice(name="Comamdante", value="Comandante"),
        app_commands.Choice(name="Devoto", value="Devoto"),
        app_commands.Choice(name="Elementarista", value="Elementarista"),
        app_commands.Choice(name="Guerreiro Koi", value="Guerreiro Koi"),
        app_commands.Choice(name="Herdeiro Ancestral", value="Herdeiro Ancestral"),
        app_commands.Choice(name="Magitécnico", value="Magitecnico"),
        app_commands.Choice(name="Malandro", value="Malandro"),
        app_commands.Choice(name="Mestre das Armas", value="Mestre das Armas"),
        app_commands.Choice(name="Mestre das Feras", value="Mestre das Feras"),
        app_commands.Choice(name="Necromante", value="Necromante"),
        app_commands.Choice(name="Protetor dos Ermos", value="Protetor dos Ermos"),
        app_commands.Choice(name="Pugilista", value="Pugilista"),
        app_commands.Choice(name="Vendedor Ambulante", value="Vendedor Ambulante"),
    ],
)
@xmercury.tree.command(
    name="mandar_personagem",
    description="Adiciona um personagem ao banco de dados",
)
async def mandar_personagem(
    interaction: Interaction,
    nome: str,
    nickname: Optional[str],
    level: Optional[int],
    legacy: Optional[app_commands.Choice[str]],
    classe: Optional[app_commands.Choice[str]],
    path: Optional[app_commands.Choice[str]],
    heritage: Optional[str],
    melancholy: Optional[str],
    catarse: Optional[int],
    pe: Optional[int],
    hp: int,
    reducao_de_dano: Optional[int],
    bonus_de_proficiencia: Optional[int],
    talentos: Optional[str],
    passivas: Optional[str],
    skills: Optional[str],
    status: str,
    pontos_de_sombra: Optional[int],
    resistencia: Optional[str],
    vulnerabilidade: Optional[str],
    imunidade: Optional[str],
    inventario: Optional[str],
    condicoes: Optional[str],
    saldo: Optional[int],
    usuario: Optional[discord.Member],
):

    if usuario is not None:
        usuario = usuario.id

    if classe is not None:
        classe = classe.value

    if path is not None:
        path = path.value

    if legacy is not None:
        legacy = legacy.value

    tl_final = "[]"
    ps_final = "[]"
    sk_final = "[]"
    status_splitado = status.split(" / ")
    forca_string = status_splitado[0].split(", ")
    forca = []
    for k in forca_string:
        forca.append(int(k))

    dex_string = status_splitado[1].split(", ")
    dexterity = []
    for k in dex_string:
        dexterity.append(int(k))

    con_string = status_splitado[2].split(", ")
    constituicao = []
    for k in con_string:
        constituicao.append(int(k))

    int_string = status_splitado[3].split(", ")
    inteligencia = []
    for k in int_string:
        inteligencia.append(int(k))

    wis_string = status_splitado[4].split(", ")
    sabedoria = []
    for k in wis_string:
        sabedoria.append(int(k))

    car_string = status_splitado[5].split(", ")
    carisma = []
    for k in car_string:
        carisma.append(int(k))

    skills_lista_id = []
    passivas_lista_id = []
    talentos_lista_id = []
    inventario_itens = []
    inventario_numero = [0]

    if interaction.user.id in ADMS:
        if inventario != None:
            inventario_partes = inventario.replace(",", "").split()
            for parte in inventario_partes:
                if parte.isdigit():
                    inventario_numero = []
                    inventario_numero.append(parte)
                else:
                    inventario_itens = []
                    inventario_itens.append(parte)

        if bonus_de_proficiencia is None:
            bonus_de_proficiencia = 0
        if level is None:
            level = 0
        if catarse is None:
            catarse = 0
        if pe is None:
            pe = 0
        if saldo is None:
            saldo = 0
        if pontos_de_sombra is None:
            pontos_de_sombra = 5

        if resistencia is None:
            resistencia = []
        else:
            resistencia = resistencia.split(", ")

        if vulnerabilidade is None:
            vulnerabilidade = []
        else:
            vulnerabilidade = vulnerabilidade.split(", ")

        if imunidade is None:
            imunidade = []
        else:
            imunidade = imunidade.split(", ")

        if condicoes is None:
            condicoes = []
        else:
            condicoes = condicoes.split(", ")

        if talentos is not None:
            talentos_lista = talentos.split(", ")
            for nome in talentos_lista:
                talentos_id = session.execute(
                    f"SELECT id FROM {KEYSPACE}.talentos WHERE nome = '{nome}' ALLOW FILTERING;"
                ).one()
                talentos_lista_id.append(str(talentos_id))
            tl_final = ", ".join(skills_lista_id)
            uuids = re.findall(r"UUID\('([a-f0-9\-]+)'\)", tl_final)
            tl_final = ", ".join(uuids)
            tl_final = f"[{tl_final}]"
        else:
            tl_final = "[]"

        if passivas is not None:
            passivas_lista = passivas.split(", ")
            for nome in passivas_lista:
                passivas_id = session.execute(
                    f"SELECT id FROM {KEYSPACE}.passivas WHERE nome = '{nome}' ALLOW FILTERING;"
                ).one()
                passivas_lista_id.append(str(passivas_id))
            ps_final = ", ".join(skills_lista_id)
            uuids = re.findall(r"UUID\('([a-f0-9\-]+)'\)", ps_final)
            ps_final = ", ".join(uuids)
            ps_final = f"[{ps_final}]"
        else:
            ps_final = "[]"

        if skills is not None:
            skills_lista = skills.split(", ")
            for nome in skills_lista:
                skills_id = session.execute(
                    f"SELECT id FROM {KEYSPACE}.skills WHERE nome='{nome}' ALLOW FILTERING;"
                ).one()
                skills_lista_id.append(str(skills_id))
            sk_final = ", ".join(skills_lista_id)
            uuids = re.findall(r"UUID\('([a-f0-9\-]+)'\)", sk_final)
            sk_final = ", ".join(uuids)
            sk_final = f"[{sk_final}]"
        else:
            sk_final = "[]"

        imagem = f"{nickname.lower()}.png"

        id = database.personagens.criar_personagem(
            session,
            nome,
            nickname,
            level,
            str(legacy),
            str(classe),
            str(path),
            heritage,
            melancholy,
            catarse,
            pe,
            hp,
            reducao_de_dano,
            bonus_de_proficiencia,
            tl_final,
            ps_final,
            ps_final,
            forca,
            dexterity,
            constituicao,
            inteligencia,
            sabedoria,
            carisma,
            pontos_de_sombra,
            resistencia,
            vulnerabilidade,
            imunidade,
            inventario_itens,
            inventario_numero,
            condicoes,
            saldo,
            imagem,
            str(usuario),
        )

        await interaction.response.send_message(
            f":white_check_mark: PERSONAGEM CRIADO COM SUCESSO :white_check_mark:\nO UUID de {nome} é **{id}**"
        )

    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@xmercury.tree.command(
    name="d",
    description="Gira um dado com quantidade de lados determinada pelo usuário",
)
async def dado(
    interaction: Interaction,
    numero: int,
):

    resultado = random.randint(1, numero)
    embed = discord.Embed(
        title=f"D{numero}",
        description="",
        colour=discord.Colour.from_str("#226089"),
    )
    embed.add_field(
        name=f":game_die:  CAIU NO **{resultado}**  :game_die:",
        value=f"",
    )
    if numero >= 1_000:
        await interaction.response.send_message(
            "https://tenor.com/view/miguel-o'hara-spider-man-spider-verse-miles-morales-meme-gif-2617586733573544579"
        )
    elif resultado == 1:
        await interaction.response.send_message(
            "https://tenor.com/view/dnd-nat1-going-to-bed-dungeons-and-dragons-natural1-gif-26298479"
        )
        await interaction.followup.send(embed=embed)

    elif resultado == numero:
        await interaction.response.send_message(
            "https://tenor.com/view/critical-succsess-gif-15687749433046296713"
        )
        await interaction.followup.send(embed=embed)

    else:
        await interaction.response.send_message(embed=embed)


class PaginationView(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]) -> None:
        super().__init__(timeout=30)
        self.embeds = embeds
        self.queue = deque(embeds)
        self.initial = embeds[0]
        self.len = len(embeds)
        self.current_page = 1

    @discord.ui.button(emoji="◀")
    async def previous(self, interaction: discord.Interaction, _):
        self.queue.rotate(-1)
        embed = self.queue[0]
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(emoji="▶")
    async def previous(self, interaction: discord.Interaction, _):
        self.queue.rotate(1)
        embed = self.queue[0]
        await interaction.response.edit_message(embed=embed)

    @property
    def initial(self) -> discord.Embed:
        return self._initial


@xmercury.tree.command(
    name="ficha",
    description="Mostra a ficha do usuário",
)
async def ficha(interaction: Interaction, personagem: Optional[str]):
    discord_id = interaction.user.id
    # if personagem is not None:
    #     personagem_id = session.execute(
    #         f"SELECT id FROM {KEYSPACE}.personagens WHERE nome = '{personagem}' ALLOW FILTERING;"
    #     ).one()
    #     if personagem_id is None:
    #         personagem_id = session.execute(
    #             f"SELECT id FROM {KEYSPACE}.personagens WHERE nickname = '{personagem}' ALLOW FILTERING;"
    #         ).one()
    #     personagem_id = str(personagem_id)
    #     uuid = personagem_id.replace("Row(id=UUID('", "").replace("'))", "")
    #     a = database.personagens.pegar_personagem(session, uuid)
    # print(a)

    embeds = []

    embed = discord.Embed(
        title=f"Julius Wick (Julius)                            LV4",
        description=f"",
        colour=discord.Colour.from_str("#226089"),
    )
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1304898198497656842/1333914323285708801/julius.png?ex=679aa005&is=67994e85&hm=1eed73552699b31ccfc81263f8faf7bdaa0bbc109c83ca420a2564ef940c5e9d&"
    )
    embed.add_field(name="Legacy:", value="Humano", inline=True)
    embed.add_field(name="Path:", value="Necromante", inline=True)
    embed.add_field(name="Classe:", value="Especialista", inline=True)
    embed.add_field(name="Heritage:", value="Pomona's Cycle", inline=True)
    embed.add_field(name="HP:", value="37", inline=True)
    embed.add_field(name="PE:", value="12", inline=True)
    embed.add_field(name="Catarse:", value="1", inline=True)
    embed.add_field(name="Redução: de Dano", value="2", inline=True)
    embed.add_field(name="Bônus: de Proficiência", value="2", inline=True)
    embed.add_field(name="Pontos: de Sombra", value="5", inline=True)
    embed.add_field(name="Saldo:", value="250 T$", inline=True)

    embed.add_field(
        name="Stataus",
        value="FOR: 15, +2\n CON: 15, +2\nDES: 15, +2\nINT: 15, +2\nSAB: 15, +2\nCAR: 15, +2",
        inline=False,
    )
    embed.add_field(name="Condição:", value="Nenhum", inline=True)
    embed.add_field(name="Resistência:", value="Nenhum", inline=True)
    embed.add_field(name="Vulnerabilidade:", value="Nenhum", inline=True)
    embed.add_field(name="Imunidade:", value="Nenhum", inline=True)
    embed.add_field(
        name="Melancolia:",
        value="Para você, o fim é necessário. Assim como a vida, todo ciclo tem um fim. Sua missão em vida é garantir o fim dos ciclos",
        inline=False,
    )
    embed.add_field(name="", value="", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


xmercury.run(token)
