from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Atributo(BaseModel):
    protection: int
    bonus: int


class Atributos(BaseModel):
    forca: Atributo
    destreza: Atributo
    constituicao: Atributo
    inteligencia: Atributo
    sabedoria: Atributo
    carisma: Atributo


class Skill(BaseModel):
    id: UUID
    nome: str
    custo: Optional[int]
    execucao: str
    descritores: Optional[str]
    alcance: Optional[int]
    duracao: Optional[str]
    ataque: Optional[str]
    acerto: Optional[str]
    erro: Optional[str]
    efeito: Optional[str]
    especial: Optional[str]
    gatilho: Optional[str]
    alvo: Optional[str]
    modificacoes: Optional[str]
    carga: Optional[int]
    modificador_execucao: Optional[str]
    modificador_nome: Optional[str]
    modificador_descricao: Optional[str]
    modificador_gasto: Optional[int]
    modificador_gasto_tipo: Optional[str]


class Talento(BaseModel):
    id: UUID
    nome: str
    descricao: str
    modificador_execucao: Optional[str]
    modificador_nome: Optional[str]
    modificador_descricao: Optional[str]
    modificador_gasto: Optional[int]
    modificador_gasto_tipo: Optional[str]


class Passiva(BaseModel):
    id: UUID
    nome: str
    descricao: str
    modificador_execucao: Optional[str]
    modificador_nome: Optional[str]
    modificador_descricao: Optional[str]
    modificador_gasto: Optional[int]
    modificador_gasto_tipo: Optional[str]


class Item(BaseModel):
    id: UUID
    nome: str
    descricao: str


class ItemDeInventario(BaseModel):
    item: Item
    quantidade: int


class Personagem(BaseModel):
    nome: str
    nickname: str
    level: int
    legacy: str
    classe: str
    path: str
    heritage: str
    melancholy: str
    catarse: int
    pe: int
    hp: int
    reducao_de_dano: int
    bonus_de_proficiencia: int
    talentos: list[Talento]
    passivas: list[Passiva]
    skills: list[Skill]
    atributos: Atributos
    pontos_de_sombra: Optional[int]
    resistencia: Optional[str]
    vulnerabilidade: Optional[str]
    imunidade: Optional[str]
    inventario: list[ItemDeInventario]
    condicoes: list[str]
    saldo: Optional[int]
    imagem: Optional[str]
    usuario: Optional[str]
