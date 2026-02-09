import discord
from discord import Interaction

from database.models import Personagem, Skill


class PaginaSkills(discord.ui.View):
    def __init__(
        self,
        personagem: Personagem,
        skills_totais: int = 0,
        skill_atual: int = 0,
        *,
        timeout: float | None = 600,
    ):
        super().__init__(timeout=timeout)
        self.skills_totais = skills_totais
        self.personagem = personagem
        self.skill_atual = skill_atual

    def acao_emoji(self, acao: str) -> str:
        if acao == "acao":
            return "<:acao:1326585196232966225>"
        elif acao == "acao bonus":
            return "<:acao_bonus:1326585197004722197>"
        elif acao == "acao livre":
            return "<:acao_livre:1326585198892154901>"
        elif acao == "reacao":
            return "<:reacao:1326585200519544885>"
        elif acao == "eop":
            return "<:eop:1327039605790343168>"
        else:
            print(f'Erro no banco de dados: Ação "{acao}" não reconhecida.')

    async def send(self, interaction: Interaction):
        await interaction.followup.send(view=self, ephemeral=True)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.gray)
    async def botao_primeiro(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.skill_atual = 0
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def botao_anterior(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.skill_atual == 0:
            self.skill_atual = self.skills_atuais
        else:
            self.skill_atual += 1
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(emoji="⚔", style=discord.ButtonStyle.blurple)
    async def atacar(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if self.personagem.skills[self.skill_atual].ataque is not None:
            pass
        else:
            await interaction.followup.send(
                "Essa skill não é um ataque.",
                ephemeral=True,
            )
            return
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def botao_proximo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.skill_atual == self.skills_totais:
            self.skill_atual = 0
        else:
            self.skill_atual += 1
        await self.atualizar_mensagem(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.gray)
    async def botao_ultimo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.skill_atual = self.skills_totais
        await self.atualizar_mensagem(interaction)

    def criar_pagina_skill(self) -> discord.Embed:
        skill = self.personagem.skills[self.skill_atual]
        embed = discord.Embed(
            title=f"Skills",
            description="",
            colour=discord.Colour.from_str("#226089"),
        )
        if skill.nome: embed.add_field(name=f"{self.acao_emoji(skill.execucao)} {skill.nome}", value=f'**{skill.descritores}**', inline=False)
        if skill.alcance: embed.add_field(name=f'', value=f'**Alcance:** {skill.alcance}', inline=False)
        if skill.alvo :embed.add_field(name=f'', value=f'**Alvo:** {skill.alvo}', inline=False)
        if skill.duracao :embed.add_field(name=f'', value=f'**Duração:** {skill.duracao}', inline=False)
        if skill.acerto :embed.add_field(name=f'', value=f'**Acerto:** {skill.acerto}', inline=False)
        return embed

    async def atualizar_mensagem(self, interaction: Interaction):
        embed = self.criar_pagina_skill()
        await interaction.edit_original_response(embed=embed, view=self)
