import os
import random
from typing import Optional

import discord
from discord import FFmpegPCMAudio, Interaction, app_commands
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
from dado import TipoDadoResultado, girar_dados
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
    execucao=[
        app_commands.Choice(name="Ação", value="acao"),
        app_commands.Choice(name="Ação Bônus", value="acao bonus"),
        app_commands.Choice(name="Reação", value="reacao"),
        app_commands.Choice(name="Ação Livre", value="acao livre"),
        app_commands.Choice(name="Echo of Pomona", value="eop"),
    ],
    modificador_execucao=[
        app_commands.Choice(name="Ação", value="acao"),
        app_commands.Choice(name="Ação Bônus", value="acao_bonus"),
        app_commands.Choice(name="Reação", value="reacao"),
        app_commands.Choice(name="Ação Livre", value="acao_livre"),
    ],
    modificador_gasto_tipo=[
        app_commands.Choice(name="PE", value="PE"),
        app_commands.Choice(name="PC", value="PC"),
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
    if carga is None:
        carga = "Ilimitado."

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
    preco: int,
    volume: int,
):
    if interaction.user.id in ADMS:
        id = database.item.criar_item(session, nome, descricao, preco, volume)
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
        app_commands.Choice(name="PE", value="PE"),
        app_commands.Choice(name="PC", value="PC"),
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
            f":white_check_mark: {tipo.value.upper()} CRIADE COM SUCESSO! :white_check_mark:\nO UUID de {nome} é **{id}**"
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

    def get_ids(elemento, tabela, session):
        if elemento is not None:
            lista = elemento.split(", ")
            lista_id = []
            for nome_id in lista:
                uuid_row = str(
                    session.execute(
                        f"SELECT id FROM {KEYSPACE}.{tabela} WHERE nome = '{nome_id}' ALLOW FILTERING;"
                    ).one()
                )
                uuid = uuid_row.replace("Row(id=UUID('", "").replace("'))", "")
                lista_id.append(uuid)
            return ", ".join(lista_id)
        else:
            return "[]"

    if interaction.user.id in ADMS:
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

        inventario_itens = []
        inventario_numero = []
        if inventario is not None:
            usuario = getattr(usuario, "id", None)
            classe = getattr(classe, "value", None)
            path = getattr(path, "value", None)
            legacy = getattr(legacy, "value", None)
            inventario_partes = inventario.split(" / ")

            for item_inventario in inventario_partes:
                item, numero = item_inventario.split(", ")
                item_id = get_ids(item, "itens", session)
                inventario_numero.append(int(numero))
                inventario_itens.append(item_id)
            it_final = ", ".join(inventario_itens)

            bonus_de_proficiencia = bonus_de_proficiencia or 0
            level = level or 0
            catarse = catarse or 0
            pe = pe or 0
            saldo = saldo or 0
            pontos_de_sombra = pontos_de_sombra or 5

        resistencia = resistencia.split(", ") if resistencia else []
        vulnerabilidade = vulnerabilidade.split(", ") if vulnerabilidade else []
        imunidade = imunidade.split(", ") if imunidade else []
        condicoes = condicoes.split(", ") if condicoes else []

        tl_final = get_ids(talentos, "talentos", session)
        ps_final = get_ids(passivas, "passivas", session)
        sk_final = get_ids(skills, "skills", session)

        imagem = f"{nickname.lower()}.png"

        limite_de_volume = 0
        if forca[0] == -3:
            limite_de_volume = 10
        elif forca[0] == -2:
            limite_de_volume = 12
        elif forca[0] == -1:
            limite_de_volume = 14
        elif forca[0] == 0:
            limite_de_volume = 16
        elif forca[0] == 1:
            limite_de_volume = 19
        elif forca[0] == 2:
            limite_de_volume = 22
        elif forca[0] == 3:
            limite_de_volume = 25
        elif forca[0] >= 4:
            limite_de_volume = 25 + ((forca[0] - 3) * 3)

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
            pe,
            hp,
            hp,
            reducao_de_dano,
            bonus_de_proficiencia,
            f"[{tl_final}]",
            f"[{ps_final}]",
            f"[{sk_final}]",
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
            f"[{it_final}]",
            inventario_numero,
            0,
            limite_de_volume,
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
        p_id = database.personagens.pegar_id_por_user_id(session, interaction.user.id)
        p = database.personagens.pegar_personagem_com_id(session, p_id)
    else:
        p = database.personagens.pegar_personagem_com_id(session, personagem.value)
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
    acao=[
        app_commands.Choice(name="Subtrair", value="subtrair"),
        app_commands.Choice(name="Somar", value="somar"),
        app_commands.Choice(name="Definir", value="definir"),
    ],
    coluna=[
        app_commands.Choice(name="PE", value="pe_atual"),
        app_commands.Choice(name="HP", value="hp_atual"),
        app_commands.Choice(name="PC", value="catarse"),
        app_commands.Choice(name="PS", value="pontos_de_sombra"),
        app_commands.Choice(name="Saldo", value="saldo"),
    ],
    personagem=[
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
    ],
)
@xmercury.tree.command(
    name="cql",
    description="Modifica número específicos no banco de dados",
)
async def cql(
    interaction: Interaction,
    personagem: app_commands.Choice[str],
    acao: app_commands.Choice[str],
    coluna: app_commands.Choice[str],
    valor: int,
):
    await interaction.response.defer(ephemeral=True)
    valor_atual_coluna = str(
        session.execute(
            f"SELECT {coluna.value} FROM {KEYSPACE}.personagens WHERE id = {personagem.value};"
        ).one()
    )
    valor_coluna = int(
        valor_atual_coluna.replace(f"Row({coluna.value}=", "").replace(")", "")
    )
    if acao.value == "subtrair":
        session.execute(
            f"UPDATE {KEYSPACE}.personagens SET {coluna.value} = {valor_coluna - valor} WHERE id = {personagem.value}"
        )
    elif acao.value == "somar":
        session.execute(
            f"UPDATE {KEYSPACE}.personagens SET {coluna.value} = {valor_coluna + valor} WHERE id = {personagem.value}"
        )
    elif acao.value == "definir":
        session.execute(
            f"UPDATE {KEYSPACE}.personagens SET {coluna.value} = {valor} WHERE id = {personagem.value}"
        )
    await interaction.followup.send(MARCH, ephemeral=True)


@xmercury.tree.command(
    name="w",
    description="Manda uma mensagem privada para um usuário",
)
async def w(interaction: Interaction, usuario: discord.Member, mensagem: str):
    if interaction.user.id in ADMS:
        dm = await usuario.create_dm()
        await dm.send(mensagem)
        await interaction.response.send_message(MARCH, ephemeral=True)
    else:
        await interaction.response.send_message(
            "https://tenor.com/view/brawlstars-twins-lawire-larry-larry-and-lawrie-gif-13625901646024351970",
            ephemeral=True,
        )


@xmercury.tree.command(
    name="restart_db",
    description="Reinicia o banco de dados para uma versão estável",
)
async def restart_db(interaction: Interaction):
    if interaction.user.id in ADMS:
        interaction.response.defer(ephemeral=True)
        os.system("python database\\database_prompts.py")
        await interaction.followup.send(MARCH, ephemeral=True)
    else:
        await interaction.response.send_message(
            "https://tenor.com/view/brawlstars-twins-lawire-larry-larry-and-lawrie-gif-13625901646024351970",
            ephemeral=True,
        )


xmercury.run(token)
