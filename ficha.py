import discord
from discord import Interaction

from database.models import Personagem


class PaginaFicha(discord.ui.View):
    def __init__(
        self,
        personagem: Personagem,
        pagina_atual: int = 0,
        *,
        timeout: float | None = 600,
    ):
        super().__init__(timeout=timeout)
        self.pagina_atual = pagina_atual
        self.personagem = personagem

    async def send(self, interaction: Interaction):
        await interaction.followup.send(view=self, ephemeral=True)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.gray)
    async def botao_primeiro(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual = 0
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def botao_anterior(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.pagina_atual == 0:
            self.pagina_atual = 5
        else:
            self.pagina_atual += 1
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def botao_proximo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.pagina_atual == 5:
            self.pagina_atual = 0
        else:
            self.pagina_atual += 1
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.gray)
    async def botao_ultimo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual = 5
        await self.atualizar_mensagem(interaction)

    def criar_embed(self) -> discord.Embed:
        if self.pagina_atual == 0:  # Ficha
            embed = discord.Embed(
                title=f"{self.personagem.nome}",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )

            embed.set_image(
                url=f"https://raw.githubusercontent.com/Giovani-Costa/project_xmercury/refs/heads/main/characters_images/{self.personagem.imagem}"
            )
            embed.add_field(
                name="Stataus",
                value=f"FOR: {self.personagem.atributos.forca.protection}, {self.personagem.atributos.forca.bonus}    DES: {self.personagem.atributos.destreza.protection}, {self.personagem.atributos.destreza.bonus}  CON: {self.personagem.atributos.constituicao.protection}, {self.personagem.atributos.constituicao.bonus} INT: {self.personagem.atributos.inteligencia.protection}, {self.personagem.atributos.inteligencia.bonus} SAB: {self.personagem.atributos.sabedoria.protection}, {self.personagem.atributos.sabedoria.bonus}   CAR: {self.personagem.atributos.carisma.protection}, {self.personagem.atributos.carisma.bonus}",
                inline=False,
            )
            embed.add_field(
                name="Legacy:", value=f"{self.personagem.legacy}", inline=True
            )
            embed.add_field(name="Path:", value=f"{self.personagem.path}", inline=True)
            embed.add_field(
                name="Classe:", value=f"{self.personagem.classe}", inline=True
            )
            embed.add_field(
                name="Heritage:", value=f"{self.personagem.heritage}", inline=True
            )
            embed.add_field(name="HP:", value=f"{self.personagem.hp}", inline=True)
            embed.add_field(name="PE:", value=f"{self.personagem.pe}", inline=True)
            embed.add_field(
                name="Catarse:", value=f"{self.personagem.catarse}", inline=True
            )
            embed.add_field(
                name="Redução de Dano:",
                value=f"{self.personagem.reducao_de_dano}",
                inline=True,
            )
            embed.add_field(
                name="Bônus de Proficiência:",
                value=f"{self.personagem.bonus_de_proficiencia}",
                inline=True,
            )
            embed.add_field(
                name="Pontos de Sombra:",
                value=f"{self.personagem.pontos_de_sombra}",
                inline=True,
            )
            embed.add_field(
                name="Saldo:", value=f"{self.personagem.saldo} T$", inline=True
            )

            if self.personagem.resistencia is not None:
                embed.add_field(
                    name="Resistência:",
                    value=f"{', '.join(self.personagem.resistencia)}",
                    inline=True,
                )
            if self.personagem.vulnerabilidade is not None:
                embed.add_field(
                    name="Vulnerabilidade:",
                    value=f"{', '.join(self.personagem.vulnerabilidade)}",
                    inline=True,
                )
            if self.personagem.imunidade is not None:
                embed.add_field(
                    name="Imunidade:",
                    value=f"{', '.join(self.personagem.imunidade)}",
                    inline=True,
                )
            if self.personagem.condicoes is not None:
                embed.add_field(
                    name="Condição:",
                    value=f"{', '.join(self.personagem.condicoes)}",
                    inline=True,
                )

            embed.add_field(
                name="Melancolia:",
                value=f"{self.personagem.melancholy}",
                inline=False,
            )
        elif self.pagina_atual == 1:  # Perícias
            embed = discord.Embed(
                title=f"Perícias",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )
            for k in self.personagem.pericias:
                embed.add_field(
                    name=f"{k.nome}",
                    value=f"{k.descricao}",
                    inline=False,
                )

        elif self.pagina_atual == 2:  # Inventáio
            embed = discord.Embed(
                title=f"Inventário | {self.personagem.limite_de_volumes - self.personagem.volume_atual} espaços livres",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )
            for k in self.personagem.inventario:
                embed.add_field(
                    name=f"({k.quantidade}x)  {k.item.nome}\n{k.item.preco} T$  |  {k.item.volume} volume(s)",
                    value=f"{k.item.descricao}",
                    inline=False,
                )

        elif self.pagina_atual == 3:  # Talentos
            embed = discord.Embed(
                title=f"Talentos",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )
            for i in self.personagem.talentos:
                descricao = i.descricao
                if (
                    i.modificador_execucao
                    and i.modificador_nome
                    and i.modificador_descricao
                    and i.modificador_gasto
                    and i.modificador_gasto_tipo != "None"
                ):
                    if i.modificador_execucao == "acao":
                        m_execucao = "<:acao:1326585196232966225>"
                    if i.modificador_execucao == "acao bonus":
                        m_execucao = "<:acao_bonus:1326585197004722197>"
                    if i.modificador_execucao == "reacao":
                        m_execucao = "<:reacao:1326585200519544885>"
                    if i.modificador_execucao == "eop":
                        m_execucao = "<:eop:1327039605790343168>"
                    descricao = (
                        descricao
                        + f"\n{m_execucao}  +{i.modificador_gasto} {i.modificador_gasto_tipo.upper()} [{i.modificador_nome}]\n{i.modificador_descricao}"
                    )
                embed.add_field(
                    name=f"{i.nome}",
                    value=f"{descricao}",
                    inline=False,
                )

        elif self.pagina_atual == 4:  # Pasivas
            embed = discord.Embed(
                title=f"Passivas",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )
            for i in self.personagem.passivas:
                descricao = i.descricao
                if (
                    i.modificador_execucao
                    and i.modificador_nome
                    and i.modificador_descricao
                    and i.modificador_gasto
                    and i.modificador_gasto_tipo != "None"
                ):
                    if i.modificador_execucao == "acao":
                        m_execucao = "<:acao:1326585196232966225>"
                    if i.modificador_execucao == "acao bonus":
                        m_execucao = "<:acao_bonus:1326585197004722197>"
                    if i.modificador_execucao == "reacao":
                        m_execucao = "<:reacao:1326585200519544885>"
                    if i.modificador_execucao == "eop":
                        m_execucao = "<:eop:1327039605790343168>"
                    descricao = (
                        descricao
                        + f"\n{m_execucao}  +{i.modificador_gasto} {i.modificador_gasto_tipo.upper()} [{i.modificador_nome}]\n{i.modificador_descricao}"
                    )
                embed.add_field(
                    name=f"{i.nome}",
                    value=f"{descricao}",
                    inline=False,
                )

        elif self.pagina_atual == 5:  # Skills
            embed = discord.Embed(
                title=f"Skills",
                description=f"",
                colour=discord.Colour.from_str("#226089"),
            )
            for i in self.personagem.skills:
                if i.execucao == "acao":
                    execucao = "<:acao:1326585196232966225>"
                if i.execucao == "acao bonus":
                    execucao = "<:acao_bonus:1326585197004722197>"
                if i.execucao == "reacao":
                    execucao = "<:reacao:1326585200519544885>"
                if i.execucao == "eop":
                    execucao = "<:eop:1327039605790343168>"

                ficha_skill = f"**{i.descritores}**"

                if i.duracao != "None":
                    ficha_skill += f"\n**Duração:** {i.duracao}"
                if i.gatilho != "None":
                    ficha_skill += f"\n**Gatilho:** {i.gatilho}"
                if i.alvo != "None":
                    ficha_skill += f"\n**Alvo:** {i.alvo}"
                if i.ataque != "None":
                    ficha_skill += f"\n**Ataque:** {i.ataque}"
                if i.acerto != "None":
                    ficha_skill += f"\n**Acerto:** {i.acerto}"
                if i.efeito != "None":
                    ficha_skill += f"\n**Efeito:** {i.efeito}"
                if i.erro != "None":
                    ficha_skill += f"\n**Erro:** {i.erro}"
                if i.carga != "None":
                    ficha_skill += f"\n**Cargas:** {i.carga}"
                if (
                    i.modificador_execucao
                    and i.modificador_nome
                    and i.modificador_descricao
                    and i.modificador_gasto
                    and i.modificador_gasto_tipo != "None"
                ):
                    if i.modificador_execucao == "acao":
                        m_execucao = "<:acao:1326585196232966225>"
                    if i.modificador_execucao == "acao bonus":
                        m_execucao = "<:acao_bonus:1326585197004722197>"
                    if i.modificador_execucao == "reacao":
                        m_execucao = "<:reacao:1326585200519544885>"
                    if i.modificador_execucao == "eop":
                        m_execucao = "<:eop:1327039605790343168>"
                    modificador_skill = f"{m_execucao}  +{i.modificador_gasto} {i.modificador_gasto_tipo.upper()} [{i.modificador_nome}]\n{i.modificador_descricao}"
                    ficha_skill = ficha_skill + f"\n{modificador_skill}"

                embed.add_field(
                    name=f"{execucao}  {i.nome}                   PE:{i.custo}",
                    value=f"{ficha_skill}\n ­",
                    inline=False,
                )

        return embed

    async def atualizar_mensagem(self, interaction: Interaction):
        embed = self.criar_embed()
        await interaction.edit_original_response(embed=embed, view=self)
