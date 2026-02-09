import random
import re
from enum import Enum, auto
from typing import Optional

import discord
from discord import Interaction, app_commands
from discord.ext.commands import Bot
from pydantic import BaseModel

import database.personagens



class TipoDadoResultado(Enum):
    NORMAL = auto()
    ERRO = auto()
    ACERTO_CRITICO = auto()
    ERRO_CRITICO = auto()


class DadoResultado(BaseModel):
    titulo: str
    mensagem: str
    valor_total: Optional[int]
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
    if numero > 1000 or dados > 200:
        return DadoResultado(
            titulo="Número muito grande",
            mensagem="Número muito grande",
            valor_total=None,
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
            gif = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDlwMThuZ2RlNWp6YTl5NXprMXQzZHVkM2djYTFzMzl3bDljZ256MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ba4V3kNdU6SAoV89EL/giphy.gif"
        elif r == 1:
            tipo = TipoDadoResultado.ERRO_CRITICO
            gif = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzdvN3VreWF6bnU1bHQ0bGNmZWx3aG41bHE2aDUxNTV4czdhNmI1dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/978LBlZgPzjWC6mFjJ/giphy.gif"

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
        valor_total=resultado,
        gif=gif,
        tipo=tipo,
    )


def girar_dados_str(string: str, vantagem: Optional[str]) -> DadoResultado:
    regex = r"(\d+)d(\d+)(.*)"
    match = re.match(regex, string)

    if match:
        dados = int(match.group(1))
        numero = int(match.group(2))
        bonus = eval(match.group(3))

        return girar_dados(numero, dados, vantagem, bonus)
    else:
        return DadoResultado(
            titulo="Erro no banco de dados",
            mensagem="Erro no banco de dados",
            valor_total=None,
            tipo=TipoDadoResultado.ERRO,
            gif="https://tenor.com/view/helpies-gif-3682755414895971819",
        )
