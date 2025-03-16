import random
from typing import Optional

import discord
from discord import FFmpegPCMAudio, Interaction, app_commands
from discord.ext.commands import Bot

import database.item
import database.models
import database.passivas_talentos
import database.personagens
import database.skill
from constante import ADMS, KEYSPACE
from database.connect_database import criar_session
from ficha import PaginaFicha
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
        app_commands.Choice(name="Adam EOP", value="adam"),
        app_commands.Choice(name="Chrollo EOP", value="chrollo"),
        app_commands.Choice(name="Gunther EOP", value="gunther"),
        app_commands.Choice(name="Julius EOP", value="julius"),
        app_commands.Choice(name="Vincenzo EOP", value="vincenzo"),
    ]
)
@xmercury.tree.command(name="efeito_sonoro", description="O bot reproduz sons na call")
async def efeito_sonoro(interaction: Interaction, sfx: app_commands.Choice[str]):
    try:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            await interaction.response.send_message(
                "<:march:1302059770785824861>", ephemeral=True
            )
            sound_effect = f"eop_sfx\{sfx.value}.mp3"
            voice = interaction.guild.voice_client
            source = discord.FFmpegPCMAudio(sound_effect)
            audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
            player = voice.play(audio_com_volume)

    except discord.ClientException:
        sound_effect = f"eop_sfx\{sfx.value}.mp3"
        voice = interaction.guild.voice_client
        source = discord.FFmpegPCMAudio(sound_effect)
        audio_com_volume = discord.PCMVolumeTransformer(source, volume=0.1)
        player = voice.play(audio_com_volume)


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
    interaction: Interaction, nome: str, descricao: str, preco: int, volume: int
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
async def dado(interaction: Interaction, numero: int, dados: Optional[int]):
    def girar_dado(numero) -> int:
        resultado = random.randint(1, numero)
        return resultado

    if dados is None:
        resultado = girar_dado(numero)
        embed = discord.Embed(
            title=f"D{numero}",
            description="",
            colour=discord.Colour.from_str("#226089"),
        )
        embed.add_field(
            name=f":game_die:  CAIU NO **{resultado}**  :game_die:",
            value=f"",
        )
        if numero > 1_000:
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

    else:
        resultados = []
        for _ in range(dados):
            resultado_dado = girar_dado(numero)
            resultados.append(resultado_dado)
        resultado = sum(resultados)

        embed = discord.Embed(
            title=f"{len(resultados)}D{numero}",
            description=f"({'+'.join(map(str, resultados))})",
            colour=discord.Colour.from_str("#226089"),
        )
        embed.add_field(
            name=f":game_die:  O TOTAL É **{resultado}**  :game_die:",
            value=f"",
        )
        if numero > 1_000:
            await interaction.response.send_message(
                "https://tenor.com/view/miguel-o'hara-spider-man-spider-verse-miles-morales-meme-gif-2617586733573544579"
            )
        else:
            await interaction.response.send_message(embed=embed)


@xmercury.tree.command(
    name="ficha",
    description="Mostra a ficha do usuário",
)
async def ficha(interaction: Interaction, personagem: Optional[str]):
    await interaction.response.defer()
    if personagem is not None:
        personagem_id = session.execute(
            f"SELECT id FROM {KEYSPACE}.personagens WHERE nome = '{personagem}' ALLOW FILTERING;"
        ).one()
        if personagem_id is None:
            personagem_id = session.execute(
                f"SELECT id FROM {KEYSPACE}.personagens WHERE nickname = '{personagem}' ALLOW FILTERING;"
            ).one()
        personagem_id = str(personagem_id)
        uuid = personagem_id.replace("Row(id=UUID('", "").replace("'))", "")
    else:
        personagem_id = session.execute(
            f"SELECT id FROM {KEYSPACE}.personagens WHERE usuario = '{interaction.user.id}' ALLOW FILTERING;"
        ).one()
        personagem_id = str(personagem_id)
        uuid = personagem_id.replace("Row(id=UUID('", "").replace("'))", "")
    personagem = database.personagens.pegar_personagem(session, uuid)
    view = PaginaFicha(personagem)
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
    name="unmute",
    description="Desmuta todos os participantes de uma call",
)
async def unmute(interaction: Interaction):
    author = interaction.user
    canal = author.voice.channel
    if author.id in ADMS:
        for membro in canal.members:
            try:
                await membro.edit(mute=False, deafen=False)
            except discord.Forbidden:
                await interaction.response.send_message(
                    f"Não tenho permissão para mutar {membro.mention}."
                )
        await interaction.response.send_message(
            f"Todos os membros do canal **{canal.name}** foram desmutados!",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "Você não tem permissão para usar esse comando", ephemeral=True
        )


xmercury.run(token)
