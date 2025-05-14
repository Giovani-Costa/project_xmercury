import random
from enum import Enum, auto
from typing import Optional

import discord
from discord import Interaction, app_commands
from discord.ext.commands import Bot
from pydantic import BaseModel

import database.personagens
from constante import KEYSPACE
from database.connect_database import criar_session


class TipoDadoResultado(Enum):
    NORMAL = auto()
    ERRO = auto()
    ACERTO_CRITICO = auto()
    ERRO_CRITICO = auto()


class DadoResultado(BaseModel):
    titulo: str
    mensagem: str
    tipo: TipoDadoResultado
    gif: Optional[str] = None


def _girar_dado(numero: int, vantagem: Optional[str]) -> tuple[int, str]:
    if vantagem == "vantagem":
        dado_1 = random.randint(1, numero)
        dado_2 = random.randint(1, numero)
        if dado_1 > dado_2:
            return dado_1, f"[**{dado_1}** | {dado_2}]"
        else:
            return dado_2, f"[{dado_1} | **{dado_2}**]"
    elif vantagem == "desvantagem":
        dado_1 = random.randint(1, numero)
        dado_2 = random.randint(1, numero)
        if dado_1 > dado_2:
            return dado_2, f"[{dado_1} | **{dado_2}**]"
        else:
            return dado_1, f"[**{dado_1}** | {dado_2}]"
    else:
        valor = random.randint(1, numero)
        return valor, str(valor)


def girar_dados(
    numero: int,
    dados: int,
    vantagem: Optional[str],
    bonus: int,
) -> DadoResultado:
    if numero > 1000 or dados > 30:
        return DadoResultado(
            titulo="Número muito grabde",
            mensagem="Número muito grabde",
            tipo=TipoDadoResultado.ERRO,
            gif="https://tenor.com/view/miguel-o'hara-spider-man-spider-verse-miles-morales-meme-gif-2617586733573544579",
        )
    resultados = []
    resultados_str = []
    for _ in range(dados):
        r, r_str = _girar_dado(numero, vantagem)
        resultados.append(r)
        resultados_str.append(r_str)

    resultado = sum(resultados) + bonus
    gif = None
    tipo = TipoDadoResultado.NORMAL
    if dados == 1 and numero == 20:
        if r == numero:
            tipo = TipoDadoResultado.ACERTO_CRITICO
            gif = "https://tenor.com/view/jujutsu-kaisen-kokusen-black-flash-yuji-itadori-gif-10077922593003290467"
        elif r == 1:
            tipo = TipoDadoResultado.ERRO_CRITICO
            gif = "https://tenor.com/view/dnd-nat1-going-to-bed-dungeons-and-dragons-natural1-gif-26298479"

    titulo = f"{dados}d{numero}"
    if bonus != 0:
        titulo += f" + {bonus}"

    if dados == 1 and bonus == 0:
        mensagem = f"**:game_die:  CAIU NO {resultado}  :game_die:**"
    else:
        mensagem = f"**:game_die:  O TOTAL É {resultado}  :game_die:**\n({' + '.join(resultados_str)})"
        if bonus != 0:
            mensagem += f" + {bonus}"

    return DadoResultado(
        titulo=titulo,
        mensagem=mensagem,
        gif=gif,
        tipo=tipo,
    )
