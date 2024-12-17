import random
from time import sleep
from typing import Any, Coroutine, Optional

import discord
import disnake
import disnake.utils
import pandas as pd
from discord import FFmpegPCMAudio, Interaction, app_commands
from discord.ext.commands import Bot
from disnake.ext import commands

from connect_database import criar_session
from key import key

xmercury = Bot(command_prefix="!", intents=discord.Intents.all())
session = criar_session()
CATEGORIA_ID_QUESTOES = 1273064071071137802
KEYSPACE = "xmercury"
ADMS = [766039963736866828, 1119222124368896020, 921158705075077150, 813254664241414144]
rpg_mode_bool = False

xmercury = Bot(command_prefix="!", intents=discord.Intents.all())
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
    ]
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
    modificacoes: Optional[str],
    carga: Optional[str],
):
    if interaction.user.id in ADMS:
        skill_nova = f"""INSERT INTO {KEYSPACE}.skills (id, nome, custo, execucao, descritores, alcance, duracao, ataque, acerto, erro, efeito, especial, gatilho, alvo, modificacoes, carga)
VALUES (uuid(), '{nome}', {custo}, '{execucao.value}', '{descritores}', '{alcance}', '{duracao}', '{ataque}', '{acerto}', '{erro}', '{efeito}', '{especial}', '{gatilho}', '{alvo}','{modificacoes}', '{carga}');"""
        session.execute(skill_nova)
        await interaction.response.send_message("Comando realizado!")
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
        mensagem = f"""INSERT INTO {KEYSPACE}.itens (id, nome, descricao)
VALUES (uuid(), '{nome}', '{descricao}'ß);"""
        session.execute(mensagem)
        await interaction.response.send_message("Comando realizado!")
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@app_commands.choices(
    tipo=[
        app_commands.Choice(name="Passiva", value="passivas"),
        app_commands.Choice(name="Talento", value="talentos"),
    ]
)
@xmercury.tree.command(
    name="mandar_talendo_ou_passiva",
    description="Adiciona um talento ou passiva ao banco de dados",
)
async def mandar_passiva(
    interaction: Interaction,
    tipo: app_commands.Choice[str],
    nome: str,
    descricao: str,
    modificadores: Optional[str],
    gasto: Optional[int],
):
    if interaction.user.id in ADMS:
        mensagem = f"""INSERT INTO {KEYSPACE}.{tipo.value} (id, nome, descricao, modificadores, gasto)
VALUES (uuid(), '{nome}', '{descricao}', '{str(modificadores)}', {gasto});"""
        session.execute(mensagem)
        await interaction.response.send_message("Comando realizado!")
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


@app_commands.choices(
    classe=[
        app_commands.Choice(name="Combatente", value="combatente"),
        app_commands.Choice(name="Especialista", value="especialista"),
        app_commands.Choice(name="Ocultista", value="ocultista"),
    ],
    legacy=[
        app_commands.Choice(name="Elfo", value="elfo"),
        app_commands.Choice(name="Gnomo", value="gnomo"),
        app_commands.Choice(name="Humano", value="humano"),
        app_commands.Choice(name="Orc", value="orc"),
        app_commands.Choice(name="Sanguires", value="sanguires"),
        app_commands.Choice(name="Urodelo", value="urodelo"),
        app_commands.Choice(name="Draco", value="draco"),
    ],
    path=[
        app_commands.Choice(name="Alquimista", value="alquimista"),
        app_commands.Choice(name="Assassino", value="assassino"),
        app_commands.Choice(name="Elementarista", value="elementarista"),
        app_commands.Choice(name="Guerreiro Koi", value="guerreiro_koi"),
        app_commands.Choice(name="Magitécnico", value="magitecnico"),
        app_commands.Choice(name="Malandro", value="malandro"),
        app_commands.Choice(name="Necromante", value="necromante"),
        app_commands.Choice(name="Pugilista", value="pugilista"),
    ],
)
@xmercury.tree.command(
    name="mandar_personagem",
    description="Adiciona um personagem ao banco de dados",
)
async def mandar_personagem(
    interaction: Interaction,
    nome: str,
    nickname: str,
    level: int,
    path: app_commands.Choice[str],
    classe: app_commands.Choice[str],
    legacy: app_commands.Choice[str],
    heritage: str,
    melancholy: str,
    catarse: int,
    pe_atual: int,
    pe_max: int,
    hp_atual: int,
    hp_max: int,
    talentos: str,  # LIST<UUID>
    passivas: str,  # LIST<UUID>
    skills: str,  # LIST<UUID>
    iniciativa: int,
    forca: str,  # LIST<INT>
    dexterity: str,  # LIST<INT>
    constituicao: str,  # LIST<INT>
    inteligencia: str,  # LIST<INT>
    wisdom: str,  # LIST<INT>
    carisma: str,  # LIST<INT>
    inventario_itens: str,  # LIST<UUID>
    inventario_numero: str,  # LIST<INT>
):
    if interaction.user.id in ADMS:
        skills_lista = skills.split(", ")
        for uuids in skills_lista:
            skills_id = session.execute(
                f"SELECT id FROM {KEYSPACE}.skills WHERE nome = '{uuids}' ALLOW FILTERING"
            ).one()

            print(skills_id)
            return skills_id

        mensagem = f"""INSERT INTO {KEYSPACE}.personagens (id, nome, nickname, level, classe, legacy, heritage, melancholy, catarse, pe_atual, pe_max, hp_atual, hp_max, talentos, passivas, skills, iniciativa, forca, dexterity, constituicao, inteligencia, wisdom, carisma, inventario_itens, inventarios_quantidade)
VALUES (uuid(), '{nome}', '{nickname}', {level}, '{path}','{classe}', '{legacy}', '{heritage}', '{melancholy.split(", ")}', {catarse}, {pe_atual}, {pe_max}, {hp_atual}, {hp_max}, [{talentos.split(", ")}], [{passivas.split(", ")}], [{skills.split(", ")}], {iniciativa}, [{forca.split(", ")}], [{dexterity.split(", ")}], [{constituicao.split(", ")}], [{inteligencia.split(", ")}], [{wisdom.split(", ")}], [{carisma.split(", ")}], [{inventario_itens.split(", ")}], [{inventario_numero.split(", ")}]);"""
        # session.execute(mensagem)
        await interaction.response.send_message(mensagem)
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando"
        )


class DadoView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180, numero: int, titulo: str):
        super().__init__(timeout=timeout)
        self.numero = numero
        self.titulo = titulo

    def criar_mensagem(self):
        resultado = random.randint(1, self.numero, self.titulo)
        embed = discord.Embed(
            title=f"D{self.numero}",
            description=self.titulo,
            colour=discord.Colour.from_str("#ff4040"),
        )
        embed.add_field(
            name=f":game_die:  CAIU NO **{resultado}**  :game_die:",
            value=f"",
        )
        if self.numero < 1_000_000:
            return {
                "view": self,
                "embed": embed,
            }
        else:
            return {
                "content": "https://tenor.com/view/miguel-o'hara-spider-man-spider-verse-miles-morales-meme-gif-2617586733573544579"
            }

    @discord.ui.button(emoji="🔁", style=discord.ButtonStyle.secondary)
    async def refresh(self, interaction: Interaction, button: discord.ui.Button):

        await interaction.response.send_message(**self.criar_mensagem())


@xmercury.tree.command(
    name="d",
    description="Gira um dado com quantidade de lados determinada pelo usuário",
)
async def dado(interaction: Interaction, numero: int):
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
    if numero >  1_000:
        await interaction.response.send_message(
            "https://tenor.com/view/miguel-o'hara-spider-man-spider-verse-miles-morales-meme-gif-2617586733573544579"
        )
    else:
        await interaction.response.send_message(embed=embed)


@app_commands.choices(
    bool_mode=[
        app_commands.Choice(name="True", value="True"),
        app_commands.Choice(name="False", value="False"),
    ]
)
@xmercury.tree.command(name="rpg_mode", description="Liga o modo de RPG do bot")
async def rpg_mode(interaction: Interaction, bool_mode: app_commands.Choice[str]):
    if bool_mode.value == "True":
        rpg_mode_bool = True
    elif bool_mode.value == "False":
        rpg_mode_bool = False

    chat_mesa = discord.TextChannel(1302058486577762386)
    overwrite = discord.PermissionOverwrite()
    gif_true = [
        "https://tenor.com/view/hasbula-time-rpg-gif-26890422",
        "https://tenor.com/view/poker-cards-loony-tunes-gambler-gif-8744771312165996589",
        "https://tenor.com/view/iamproudofyou-my-hero-gif-6564429772262310049",
    ]
    gif_false = [
        "https://tenor.com/view/rpg-sad-gif-27268132",
        "https://tenor.com/view/rpg-cancelado-inosuke-inosuke-hashibira-gif-20910756",
        "https://tenor.com/view/sess%C3%A3o-cancelada-galero-galero-rpg-mesa-mesa-de-rpg-gif-25594001",
    ]
    if interaction.user.id in ADMS:
        if rpg_mode_bool == False:
            gif = random.choice(gif_false)
            await interaction.response.send_message(gif, ephemeral=True)
            overwrite.view_channel = False
            overwrite.manage_channels = False
            overwrite.manage_permissions = False
            await chat_mesa.set_permissions(chat_mesa, overwrite=overwrite)

        else:
            gif = random.choice(gif_true)
            await interaction.response.send_message(gif, ephemeral=True)
            overwrite.view_channel = True
            overwrite.manage_channels = True
            overwrite.manage_permissions = True
            await chat_mesa.set_permissions(chat_mesa, overwrite=overwrite)
    else:
        await interaction.response.send_message("aaaa", ephemeral=True)

    # view = "place holder"
    # await interaction.response.send_message(**view.criar_mensagem())


xmercury.run(token)
