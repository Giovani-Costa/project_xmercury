import uuid

import streamlit as st

from database import condicoes, descritores, item, passivas_talentos, skills
from database import pericias as pericia
from database import personagens
from database import descritores

st.set_page_config(
    page_title="Create Page",
    page_icon="🎷",
)
st.write("Create")
lista_personagens = personagens.pegar_todos_os_personagens(st.session_state["db_session"])
mapa_nome_id_personagem = {p.nome: p.id_personagem for p in lista_personagens}


def atualizar_uuid_skill():
    st.session_state.uuid_skill = str(uuid.uuid4())


def atualizar_uuid_passiva_talento():
    st.session_state.uuid_passiva_talento = str(uuid.uuid4())


def atualizar_uuid_item():
    st.session_state.uuid_passiva_talento = str(uuid.uuid4())


def atualizar_uuid_pericia():
    st.session_state.uuid_pericia = str(uuid.uuid4())


def atualizar_uuid_condicao():
    st.session_state.uuid_condicao = str(uuid.uuid4())


def atualizar_uuid_descritor():
    st.session_state.uuid_descritor = str(uuid.uuid4())


def atualizar_uuid_personagens():
    st.session_state.uuid_personagem = str(uuid.uuid4())


with st.expander("Mandar Skill"):
    skill_esquerda, skill_direita = st.columns(2)
    with skill_esquerda:
        skill_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_skill",
            value=None,
        )
    with skill_direita:
        st.button("Gerara UUID aleatório", on_click=atualizar_uuid_skill)

    skill_nome = st.text_input("Nome da skill")
    skill_custo = st.number_input("Custo da skill", step=1)
    skill_execucao = st.selectbox(
        "Execução", ["Ação", "Ação Bônus", "Ação Livre", "Reação", "Ultimate"]
    )
    skill_descritores = st.multiselect(
        "Descritores", [d.nome for d in descritores.pegar_todos_os_descritores(st.session_state["db_session"])]
    )
    skill_alcance = st.text_input("Alcance da skill", value=None)
    skill_duracao = st.text_input("Duração da skill", value=None)
    skill_ataque = st.text_input("Ataque da skill", value=None)
    skill_acerto = st.text_input("Acerto da skill", value=None)
    skill_erro = st.text_input("Erro da skill", value=None)
    skill_efeito = st.text_input("Efeito da efeito", value=None)
    skill_especial = st.text_input("Especial da skill", value=None)
    skill_gatilho = st.text_input("Gatilho da skill", value=None)
    skill_alvo = st.text_input("Alvo da skill", value=None)
    skill_carga = st.text_input("Carga da skill", value=None)
    skill_personagem = st.selectbox("Personagem da Skill", [p.nome for p in lista_personagens])
    if st.button("Mandar Skill"):
        uuid_criado = skills.criar_skill(
            st.session_state["db_session"],
            skill_nome,
            skill_custo,
            skill_execucao,
            ', '.join(skill_descritores),
            skill_alcance,
            skill_duracao,
            skill_ataque,
            skill_acerto,
            skill_erro,
            skill_efeito,
            skill_especial,
            skill_gatilho,
            skill_alvo,
            skill_carga,
            mapa_nome_id_personagem[skill_personagem],
            skill_uuid,
        )
        st.success(
            f'''session.execute(\n\t\tf"""{{INSERT_SKILL}}\nVALUES ({skill_uuid}, '{skill_nome}', {skill_custo}, '{skill_execucao}', '{','.join(skill_descritores)}', '{skill_alcance}', '{skill_duracao}', '{skill_ataque}', '{skill_acerto}', '{skill_erro}', '{skill_efeito}', '{skill_especial}', '{skill_gatilho}', '{skill_alvo}', '{skill_carga}, '{mapa_nome_id_personagem[skill_personagem]}');""");"""\n\t)'''
        )

with st.expander("Mandar Passiva/Talento"):
    pt_esquerda, pt_direita = st.columns(2)
    with pt_esquerda:
        pt_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_passiva_talento",
        )
    with pt_direita:
        st.button("Gerar UUID aleatório", on_click=atualizar_uuid_passiva_talento)
    pt = st.selectbox("Tabela", ["Talentos", "Passivas"])
    pt_nome = st.text_input("Nome da Passiva/Talento")
    pt_descricao = st.text_area("Descrição da Passiva/Talento")
    pt_personagem = st.selectbox("Personagem da Passiva/Talento", [p.nome for p in lista_personagens])
    if st.button("Mandar Passiva/Talento"):
        uuid_criado = passivas_talentos.criar_passiva_talento(
            st.session_state["db_session"],
            pt,
            pt_nome,
            pt_descricao,
            mapa_nome_id_personagem[pt_personagem],
            pt_uuid,
        )
        st.success(
            f'''session.execute(\n\t\tf"""{{INSERT_{pt.upper()}}}\nVALUES ({uuid_criado}, '{pt_nome}', '{pt_descricao}', '{mapa_nome_id_personagem[pt_personagem]}');"""\n\t)'''
        )

with st.expander("Mandar Item"):
    item_esquerda, item_direita = st.columns(2)
    with item_esquerda:
        item_uuid = st.text_input(
            "UUID", label_visibility="collapsed", placeholder="UUID", key="uuid_item"
        )
    with item_direita:
        st.button("Gerar UUID Aleatório para Item", on_click=atualizar_uuid_item)

    item_nome = st.text_input("Nome do item")
    item_descricao = st.text_area("Descrição")
    item_volume = st.number_input("Volume", step=1)
    item_preco = st.number_input("Preço", step=1)
    if st.button("Mandar Item"):
        uuid_criado = item.criar_item(
            st.session_state["db_session"],
            item_nome,
            item_descricao,
            item_volume,
            item_preco,
            item_uuid,
        )
        st.success(
            f'''session.execute(\n\t\tf"""{{INSERT_ITEM}}\nVALUES ({uuid_criado}, '{item_nome}', '{item_descricao}', {item_preco}, {item_volume});"""\n\t)'''
        )

with st.expander("Mandar Perícia"):
    pericia_esquerda, pericia_direita = st.columns(2)
    with pericia_esquerda:
        pericia_uuid = st.text_input(
            "UUID", label_visibility="collapsed", placeholder="UUID", key="uuid_pericia"
        )
    with pericia_direita:
        st.button("Gerar UUID Aleatório para Perícia", on_click=atualizar_uuid_pericia)

    pericia_nome = st.text_input("Nome do Perícia")
    pericia_descricao = st.text_area("Descrição da Perícia")
    if st.button("Mandar Perícia"):
        uuid_criado = pericia.pegar_pericia(
            st.session_state["db_session"],
            pericia_nome,
            pericia_descricao,
        )
        st.success(
            f'''session.execute(\n\t\tf"""{{INSERT_PERICIA}}\nVALUES ({uuid_criado}, '{pericia_nome}', '{pericia_descricao}');"""\n\t)'''
        )

with st.expander("Mandar Condição"):
    condicao_esquerda, condicao_direita = st.columns(2)
    with condicao_esquerda:
        condicao_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_condicao",
        )
    with condicao_direita:
        st.button(
            "Gerar UUID Aleatório para Condição", on_click=atualizar_uuid_condicao
        )

    pericia_nome = st.text_input("Nome do Condição")
    pericia_descricao = st.text_area("Descrição da Condição")
    if st.button("Mandar Condição"):
        uuid_criado = condicoes.criar_condicao(
            st.session_state["db_session"],
            pericia_nome,
            pericia_descricao,
        )
        st.html(
            f'''session.execute(\n\t\tf"""{{INSERT_CONDIÇÃO}}\nVALUES ({uuid_criado}, '{pericia_nome}', '{pericia_descricao}');"""\n\t)'''
        )

with st.expander("Mandar Descritor"):
    descritor_esquerda, descritor_direita = st.columns(2)
    with descritor_esquerda:
        descritor_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_descritor",
        )
    with descritor_direita:
        st.button(
            "Gerar UUID Aleatório para Descritor", on_click=atualizar_uuid_descritor
        )

    descritor_nome = st.text_input("Nome do Descritor")
    descritor_tipo = st.selectbox(
        "Tipo de Descritor",
        [
            "Descritor de Dano",
            "Descritor de Origem",
            "Descritor de Categoria",
            "Descritor de Equipamento",
            "Descritor Diverso",
        ],
    )
    descritor_descricao = st.text_area("Descrição da Descritor")
    if st.button("Mandar Descritor"):
        uuid_criado = descritores.criar_descritor(
            st.session_state["db_session"],
            pericia_nome,
            descritor_tipo,
            descritor_descricao,
        )
        st.success(
            f'''session.execute(\n\t\tf"""{{INSERT_DESCRITOR}}\nVALUES ({uuid_criado}, '{descritor_nome}', '{descritor_tipo}', '{descritor_descricao}');"""\n\t)'''
        )

with st.expander("Mandar Personagem"):
    lista_skills = skills.pegar_todas_as_skills(st.session_state["db_session"])
    mapa_skills_id = {s.nome: s.id_skill for s in lista_skills}

    lista_passivas = passivas_talentos.pegar_todas_as_passivas(
        st.session_state["db_session"]
    )
    mapa_passivas_id = {p.nome: p.id_passiva for p in lista_passivas}

    lista_talentos = passivas_talentos.pegar_todos_os_talentos(
        st.session_state["db_session"]
    )
    mapa_talentos_id = {t.nome: t.id_talento for t in lista_talentos}

    lista_pericias = pericia.pegar_todas_as_pericias(st.session_state["db_session"])
    mapa_pericias_id = {p.nome: p.id_pericia for p in lista_pericias}

    personagem_esquerda, personagem_direita = st.columns(2)
    with personagem_esquerda:
        personagem_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_personagem",
        )

    with personagem_direita:
        st.button(
            "Gerar UUID Aleatório para Personagem",
            on_click=atualizar_uuid_personagens,
        )

    personagem_nome = st.text_input("Nome do Personagem")
    personagem_nickname = st.text_input("Nickname do Personagem")
    personagem_level = st.number_input("Level do Personagem", step=1)
    personagem_legacy = st.text_input("Legacy do Personagem")
    personagem_classe = st.text_input("Classe do Personagem")
    personagem_heritage = st.text_input("Heritage do Personagem")
    personagem_melancholu = st.text_area("Melancolia do Personagem")
    personagem_pe = st.number_input("PE do Personagem", step=1)
    personagem_hp = st.number_input("HP do Personagem", step=1)
    personagem_reducao_de_dano = st.number_input(
        "Redução de Dano do Personagem", step=1
    )
    personagem_bonus_de_proficiencia = st.number_input(
        "Bônus de Proficiência do Personagem", step=1
    )
    skills = st.multiselect("Skills", list(mapa_skills_id.keys()))
    passivas = st.multiselect("Passivas", list(mapa_passivas_id.keys()))
    talentos = st.multiselect("Talentos", list(mapa_talentos_id.keys()))
    pericias = st.multiselect("Pericias", list(mapa_pericias_id.keys()))

    coluna_forca_esqueda, coluna_forca_direita = st.columns(2)
    with coluna_forca_esqueda:
        personagem_forca_protecao = st.number_input("Força Proteção", step=1, value=10)
    with coluna_forca_direita:
        personagem_forca_bonus = st.number_input("Força Bônus", step=1)
    
    coluna_destreza_esqueda, coluna_destreza_direita = st.columns(2)
    with coluna_destreza_esqueda:
        personagem_destreza_protecao = st.number_input("Destreza Proteção", step=1, value=10)
    with coluna_destreza_direita:
        personagem_destreza_bonus = st.number_input("Destreza Bônus", step=1)
    
    coluna_constituicao_esqueda, coluna_constituicao_direita = st.columns(2)
    with coluna_constituicao_esqueda:   
        personagem_constituicao_protecao = st.number_input("Constituição Proteção", step=1, value=10)
    with coluna_constituicao_direita:
        personagem_constituicao_bonus = st.number_input("Constituição Bônus", step=1)
    
    coluna_inteligencia_esqueda, coluna_inteligencia_direita = st.columns(2)
    with coluna_inteligencia_esqueda:
        personagem_inteligencia_protecao = st.number_input("Inteligência Proteção", step=1, value=10)
    with coluna_inteligencia_direita:
        personagem_inteligencia_bonus = st.number_input("Inteligência Bônus", step=1)
    
    coluna_sabedoria_esqueda, coluna_sabedoria_direita = st.columns(2)
    with coluna_sabedoria_esqueda:
        personagem_sabedoria_protecao = st.number_input("Sabedoria Proteção", step=1, value=10)
    with coluna_sabedoria_direita:
        personagem_sabedoria_bonus = st.number_input("Sabedoria Bônus", step=1)
    
    coluna_carisma_esqueda, coluna_carisma_direita = st.columns(2)
    with coluna_carisma_esqueda:        
        personagem_carisma_protecao = st.number_input("Carisma Proteção", step=1, value=10)
    with coluna_carisma_direita:
        personagem_carisma_bonus = st.number_input("Carisma Bônus", step=1)

    personagem_pontos_de_sombra = st.number_input(
        "Pontos de Sombra do Personagem", step=1, max_value=5
    )

    skills_id = [str(mapa_skills_id[s]) for s in skills]
    passivas_id = [str(mapa_passivas_id[p]) for p in passivas]
    talentos_id = [str(mapa_talentos_id[t]) for t in talentos]
    pericias_id = [str(mapa_pericias_id[p]) for p in pericias]
