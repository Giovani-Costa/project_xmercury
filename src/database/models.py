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


class Modificador(BaseModel):
    id_modificador: UUID
    nome: str
    descricao: str
    execucao: str
    gasto: int
    gasto_tipo: str


class Skill(BaseModel):
    id_skill: UUID
    nome: str
    custo: int
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
    modificadores: Optional[list[Modificador]]


class Talento(BaseModel):
    id_talento: UUID
    nome: str
    descricao: str


class Passiva(BaseModel):
    id_passiva: UUID
    nome: str
    descricao: str


class Item(BaseModel):
    id_item: UUID
    nome: str
    descricao: str
    preco: int
    volume: int


class ItemDeInventario(BaseModel):
    item: Item
    quantidade: int


class Pericia(BaseModel):
    id_pericia: UUID
    nome: str
    descricao: str
    e_vantagem: bool
    e_soma: bool
    somar: Optional[list[str]] = None
    

class PericiaPersonagem(BaseModel):
    personagem_pericia: Pericia
    nivel: int


class Condicao(BaseModel):
    id_condicao: UUID
    nome: str
    descricao: str


class Descritor(BaseModel):
    id_descritor: UUID
    nome: str
    tipo: str
    descricao: str


class Personagem(BaseModel):
    id_personagem: UUID
    nome: str
    nickname: Optional[str]
    level: int
    legacy: Optional[str]
    classe: Optional[str]
    path: Optional[str]
    heritage: Optional[str]
    melancholy: Optional[str]
    catarse: Optional[int]
    pe: Optional[int]
    pe_atual: Optional[int]
    hp: int
    hp_atual: int
    hp_tipo: str
    reducao_de_dano: Optional[int]
    bonus_de_proficiencia: Optional[int]
    pericias: Optional[list[Pericia]]
    talentos: Optional[list[Talento]]
    passivas: Optional[list[Passiva]]
    skills: Optional[list[Skill]]
    atributos: Optional[Atributos]
    pontos_de_sombra: Optional[int]
    resistencia: Optional[str]
    vulnerabilidade: Optional[str]
    imunidade: Optional[str]
    inventario: list[ItemDeInventario]
    volume_atual: Optional[int]
    limite_de_volume: Optional[int]
    # condicoes: Optional[str]
    saldo: Optional[int]
    imagem: Optional[str]
    tokenn: Optional[str]
    usuario: Optional[str]


class Party(BaseModel):
    id_party: UUID
    personagens_jogaveis: list[Personagem]
