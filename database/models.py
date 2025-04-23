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
    alcance: Optional[str]
    duracao: Optional[str]
    ataque: Optional[str]
    acerto: Optional[str]
    erro: Optional[str]
    efeito: Optional[str]
    especial: Optional[str]
    gatilho: Optional[str]
    alvo: Optional[str]
    carga: Optional[str]
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
    preco: int
    volume: int


class ItemDeInventario(BaseModel):
    item: Item
    quantidade: int


class Pericia(BaseModel):
    nome: str
    descricao: str
    e_vantagem: bool
    e_soma: bool
    somar: Optional[list[str]]


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
    # pericias: Optional[list[Pericia]]
    talentos: Optional[list[Talento]]
    passivas: Optional[list[Passiva]]
    skills: Optional[list[Skill]]
    atributos: Optional[Atributos]
    pontos_de_sombra: Optional[int]
    resistencia: Optional[list[str]]
    vulnerabilidade: Optional[list[str]]
    imunidade: Optional[list[str]]
    inventario: list[ItemDeInventario]
    condicoes: Optional[list[str]]
    saldo: Optional[int]
    imagem: Optional[str]
    usuario: Optional[str]
