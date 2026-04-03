import uuid

import streamlit as st

from utils import calc_limite_peso, calc_hp
from database import condicoes, descritores, itens, passivas_talentos, skills, modificadores, party, constantes
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
    st.session_state.uuid_item = str(uuid.uuid4())


def atualizar_uuid_pericia():
    st.session_state.uuid_pericia = str(uuid.uuid4())


def atualizar_uuid_condicao():
    st.session_state.uuid_condicao = str(uuid.uuid4())


def atualizar_uuid_descritor():
    st.session_state.uuid_descritor = str(uuid.uuid4())

def atualizar_uuid_modificador():
    st.session_state.uuid_modificador = str(uuid.uuid4())


def atualizar_uuid_personagens():
    st.session_state.uuid_personagem = str(uuid.uuid4())

def atualizar_uuid_party():
    st.session_state.uuid_party = str(uuid.uuid4())


with st.expander("Criar Skill"):
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
        st.button("Gerar UUID aleatório para Skill", on_click=atualizar_uuid_skill)

    skill_nome = st.text_input("Nome da skill")
    skill_custo = st.number_input("Custo da skill", step=1, value=0)
    skill_execucao = st.selectbox(
        "Execução", ["Ação", "Ação Bônus", "Ação Livre", "Reação", "Ultimate"], index=0
    )
    skill_descritores = st.multiselect(
        "Descritores", [d.nome for d in descritores.pegar_todos_os_descritores(st.session_state["db_session"])]
    )
    skill_alcance = st.text_input("Alcance da skill")
    skill_duracao = st.text_input("Duração da skill")
    skill_ataque = st.text_input("Ataque da skill")
    skill_acerto = st.text_input("Acerto da skill")
    skill_erro = st.text_input("Erro da skill")
    skill_efeito = st.text_input("Efeito da efeito")
    skill_especial = st.text_input("Especial da skill")
    skill_gatilho = st.text_input("Gatilho da skill")
    skill_alvo = st.text_input("Alvo da skill")
    skill_carga = st.text_input("Carga da skill", value="Ilimitado.")
    skill_personagem = st.selectbox("Personagem da Skill", [p.nome for p in lista_personagens])
    if st.button("Criar Skill"):
        if skill_alcance is None or skill_alcance == "":
            alcance = 'NULL'
        else:
            alcance = f"'{skill_alcance}'"
        if skill_duracao is None or skill_duracao == "":
            duracao = 'NULL'
        else:
            duracao = f"'{skill_duracao}'"
        if skill_ataque is None or skill_ataque == "":
            ataque = 'NULL'
        else:
            ataque = f"'{skill_ataque}'"
        if skill_acerto is None or skill_acerto == "":
            acerto = 'NULL'
        else:
            acerto = f"'{skill_acerto}'"
        if skill_erro is None or skill_erro == "":
            erro = 'NULL'
        else:
            erro = f"'{skill_erro}'"
        if skill_efeito is None or skill_efeito == "":
            efeito = 'NULL'
        else:
            efeito = f"'{skill_efeito}'"
        if skill_especial is None or skill_especial == "":
            especial = 'NULL'
        else:
            especial = f"'{skill_especial}'"
        if skill_gatilho is None or skill_gatilho == "":
            gatilho = 'NULL'
        else:
            gatilho = f"'{skill_gatilho}'"
        if skill_alvo is None or skill_alvo == "":
            alvo = 'NULL'
        else:
            alvo = f"'{skill_alvo}'"
        if skill_carga is None or skill_carga == "":
            carga = 'NULL'
        else:
            carga = f"'{skill_carga}'"
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
            f"('{skill_uuid}', '{skill_nome}', {skill_custo}, '{skill_execucao}', '{', '.join(skill_descritores)}', {alcance}, {duracao}, {ataque}, {acerto}, {erro}, {efeito}, {especial}, {gatilho}, {alvo}, {carga}, '{mapa_nome_id_personagem[skill_personagem]}'),"
        )

with st.expander("Criar Passiva/Talento"):
    pt_esquerda, pt_direita = st.columns(2)
    with pt_esquerda:
        pt_uuid = st.text_input(
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_passiva_talento",
        )
    with pt_direita:
        st.button("Gerar UUID aleatório para Passiva/Talento", on_click=atualizar_uuid_passiva_talento)
    pt = st.selectbox("Tabela", ["Talentos", "Passivas"])
    pt_nome = st.text_input("Nome da Passiva/Talento")
    pt_descricao = st.text_area("Descrição da Passiva/Talento")
    pt_personagem = st.selectbox("Personagem da Passiva/Talento", [p.nome for p in lista_personagens])
    if st.button("Criar Passiva/Talento"):
        uuid_criado = passivas_talentos.criar_passiva_talento(
            st.session_state["db_session"],
            pt,
            pt_nome,
            pt_descricao,
            mapa_nome_id_personagem[pt_personagem],
            pt_uuid,
        )
        st.success(
            f"('{uuid_criado}', '{pt_nome}', '{pt_descricao}', '{mapa_nome_id_personagem[pt_personagem]}')"
        )

with st.expander("Criar Item"):
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
    if st.button("Criar Item"):
        uuid_criado = itens.criar_item(
            st.session_state["db_session"],
            item_nome,
            item_descricao,
            item_volume,
            item_preco,
            item_uuid,
        )
        st.success(
            f"('{uuid_criado}', '{item_nome}', '{item_descricao}', {item_preco}, {item_volume}),"
        )

with st.expander("Criar Perícia"):
    # Tentar automatizar isso depois
    atributos_somaticos = ["Bônus de Proficiência", "Bônus de Força", "Bônus de Constituição", "Bônus de Destreza", "Bônus de Inteligência", "Bônus de Sabedoria", "Bônus de Carisma"]
    mapa_execucao = {
        "Bônus de Proficiência": "bonus_de_proficiencia",
        "Bônus de Força": "forca",
        "Bônus de Constituição": "constituicao",
        "Bônus de Destreza": "destreza",
        "Bônus de Inteligência": "inteligencia",
        "Bônus de Sabedoria": "sabedoria",
        "Bônus de Carisma": "carisma",}
    
    pericia_esquerda, pericia_direita = st.columns(2)
    with pericia_esquerda:
        pericia_uuid = st.text_input(
            "UUID", label_visibility="collapsed", placeholder="UUID", key="uuid_pericia"
        )
    with pericia_direita:
        st.button("Gerar UUID Aleatório para Perícia", on_click=atualizar_uuid_pericia)

    pericia_nome = st.text_input("Nome do Perícia")
    pericia_descricao = st.text_area("Descrição da Perícia")
    pericia_vantagem = st.toggle('Vantagem?', value=False)
    pericia_atributo = st.toggle("Somar Atributo?", value=False)
    if pericia_atributo:
        pericia_soma = st.multiselect("Atributos somados", atributos_somaticos)
        pericia_soma = str("'" + '{"'+ '","'.join([mapa_execucao[attr] for attr in pericia_soma]) + '"}' + "'")
    else:
        pericia_soma = "NULL"

    if st.button("Criar Perícia"):
        print(pericia_soma)
        uuid_criado = pericia.criar_pericia(
            st.session_state["db_session"],
            pericia_nome,
            pericia_descricao,
            pericia_vantagem,
            pericia_atributo,
            pericia_soma
        )
        st.success(
            f"('{uuid_criado}', '{pericia_nome}', '{pericia_descricao}', {str(pericia_vantagem).lower()}, {str(pericia_atributo).lower()}, {pericia_soma}),"
        )

with st.expander("Criar Condição"):
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
    if st.button("Criar Condição"):
        uuid_criado = condicoes.criar_condicao(
            st.session_state["db_session"],
            pericia_nome,
            pericia_descricao,
        )
        st.success(
            f'''('{uuid_criado}', '{pericia_nome}', '{pericia_descricao}'),'''
        )

with st.expander("Criar Descritor"):
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
    if st.button("Criar Descritor"):
        uuid_criado = descritores.criar_descritor(
            st.session_state["db_session"],
            descritor_nome,
            descritor_tipo,
            descritor_descricao,
        )
        st.success(
            f"('{uuid_criado}', '{descritor_nome}', '{descritor_tipo}', '{descritor_descricao}'),")
        
with st.expander("Criar Modificador"):
    execucao = ["Ação", "Ação Bônus", "Ação Livre", "Reação", "Ultimate"]
    mapa_execucao = {
        "Ação": "acao",
        "Ação Bônus": "acao bonus",
        "Ação Livre": "acao livre",
        "Reação": "reacao",
        "Ultimate": "ultimate",}
    
    modificador_esquerda, modificador_direita = st.columns(2)
    with modificador_esquerda:
        modificador_uuid = st.text_input(  
            "UUID",
            label_visibility="collapsed",
            placeholder="UUID",
            key="uuid_modificador",
        )
    with modificador_direita:
        st.button(
            "Gerar UUID Aleatório para Modificador", on_click=atualizar_uuid_modificador
        )

    modificador_tipo = st.selectbox(
        "Tipo de Modificador",
        ["ADICIONA", "MUDA", "Outro..."],
    )
    if modificador_tipo == "Outro...":
        modificador_tipo = st.text_input("Outro tipo de Modificador")
    modificador_descricao = st.text_area("Descrição da Modificador")
    modificador_execucao = st.selectbox(
        "Execução", execucao, index=3
    )
    modificador_gasto = st.number_input("Gasto do Modificador", step=1)
    modificador_gasto_tipo = st.selectbox(
        "Tipo de Gasto do Modificador",
        ["PE", "PC"], index=0,
    ).lower()

    if st.button("Criar Modificador"):
        uuid_criado = modificadores.criar_modificador(
            st.session_state["db_session"],
            modificador_tipo,
            modificador_descricao,
            modificador_execucao,
            modificador_gasto,
            modificador_gasto_tipo,
            modificador_uuid,
        )
        st.success(
            f"('{uuid_criado}', '{modificador_tipo}', '{modificador_descricao}', '{mapa_execucao[modificador_execucao]}', {modificador_gasto}, '{modificador_gasto_tipo.upper()}'),")

with st.expander("Criar Personagem"):
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

    # lista_pericias = pericia.pegar_todas_as_pericias(st.session_state["db_session"])
    # mapa_pericias_id = {p.nome: p.id_pericia for p in lista_pericias}

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
    personagem_level = st.number_input("Level do Personagem", step=1, value=constantes.LEVEL)
    personagem_legacy = st.text_input("Legado do Personagem")
    personagem_heritage = st.text_input("Heritage do Personagem")
    personagem_classe = st.text_input("Classe do Personagem")
    personagem_path = st.text_input("Trilha do Personagem")
    personagem_melancolia = st.text_area("Melancolia do Personagem")
    personagem_pe = st.number_input("PE do Personagem", step=1, value=constantes.PE)
    personagem_hp = st.toggle("Calcular HP Automático?", value=True)
    personagem_hp_tipo = st.radio("Tipo de HP", options=["HP", "Carga"], index=0)
    personagem_reducao_de_dano = st.number_input(
        "Redução de Dano do Personagem", step=1, value=0
    )
    personagem_bonus_de_proficiencia = st.number_input(
        "Bônus de Proficiência do Personagem", step=1, value=constantes.BONUS_DE_PROFICIENCIA
    )
    personagem_pontos_de_sombra = st.number_input(
        "Pontos de Sombra do Personagem", step=1, max_value=5
    )
    personagem_catarse = st.number_input(
        "Pontos de Catarse do Personagem", step=1, max_value=5
    )
    personagem_resistencia = st.text_input("Resistência do Personagem")
    personagem_vulnerabilidade = st.text_input("Vulnerabilidade do Personagem")
    personagem_imunidade = st.text_input("Imunidade do Personagem")
    personagem_volume_atual = st.number_input("Volume Atual do Personagem", step=1, value=0)
    personagem_limite_de_volume = st.toggle("Limite de Volume Automático?", value=True)
    if not personagem_limite_de_volume:
        personagem_limite_de_volume = st.number_input("Limite de Volume do Personagem", step=1, value=0)
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

    if not personagem_hp:
        personagem_hp = st.number_input("HP do Personagem", step=1, value=0)
    else:
        personagem_classe_numero = 1
        if personagem_classe == "Combatente":
            personagem_classe_numero = 0
        elif personagem_classe == "Especialista":
            personagem_classe_numero = 1
        elif personagem_classe == "Ocultista":
            personagem_classe_numero = 2
        personagem_hp = calc_hp(personagem_constituicao_bonus, personagem_classe_numero, personagem_level)

    personagem_saldo = st.number_input("Saldo do Personagem", step=1, value=100)
    personagem_tokenn = st.text_input("Token do Personagem")
    personagem_imagem = st.text_input("Imagem do Personagem", placeholder="nome_da_imagem.png")
    personagem_usuario = st.text_input("Usuário do Personagem")
    personagem_party = st.selectbox("Party do Personagem", [p.nome for p in party.pegar_todas_as_parties(st.session_state["db_session"])], index=0)
    personagem_party_mapa = {p.nome: p.id_party for p in party.pegar_todas_as_parties(st.session_state["db_session"])}
    personagem_party = personagem_party_mapa[personagem_party]

    if st.button("Criar Personagem"):
        if personagem_limite_de_volume == True:
            personagem_limite_de_volume = calc_limite_peso(personagem_forca_bonus)
        if personagem_nickname is None or personagem_nickname == "":
            personagem_nickname = 'NULL'
        else:
            personagem_nickname = f"'{personagem_nickname}'"
        if personagem_legacy is None or personagem_legacy == "":
            personagem_legacy = 'NULL'     
        else:
            personagem_legacy = f"'{personagem_legacy}'"
        if personagem_classe is None or personagem_classe == "":
            personagem_classe = 'NULL' 
        else:
            personagem_classe = f"'{personagem_classe}'"                                                      
        if personagem_path is None or personagem_path == "":
            personagem_path = 'NULL'
        else:        
            personagem_path = f"'{personagem_path}'"
        if personagem_heritage is None or personagem_heritage == "":
            personagem_heritage = 'NULL'
        else:
            personagem_heritage = f"'{personagem_heritage}'"
        if personagem_melancolia is None or personagem_melancolia == "":
            personagem_melancolia = 'NULL'
        else:
            personagem_melancolia = f"'{personagem_melancolia}'"                                          
        if personagem_resistencia is None:
            personagem_resistencia = 'NULL'
        else:
            personagem_resistencia = f"'{personagem_resistencia}'"
        if personagem_vulnerabilidade is None:
            personagem_vulnerabilidade = 'NULL'
        else:
            personagem_vulnerabilidade = f"'{personagem_vulnerabilidade}'"
        if personagem_imunidade is None:
            personagem_imunidade = 'NULL'
        else:
            personagem_imunidade = f"'{personagem_imunidade}'"
        if personagem_imagem is None or personagem_imagem == "":
            personagem_imagem = 'NULL'
        else:
            personagem_imagem = f"'{personagem_imagem}'"
        if personagem_tokenn is None or personagem_tokenn == "":
            personagem_tokenn = 'NULL' 
        else:
            personagem_tokenn = f"'{personagem_tokenn}'"
        if personagem_usuario is None or personagem_usuario == "":
            personagem_usuario = 'NULL'
        else:        
            personagem_usuario = f"{personagem_usuario}"
        uuid_criado = personagens.criar_personagem(
            st.session_state["db_session"],
            personagem_nome,
            personagem_nickname,
            personagem_level,
            personagem_legacy,
            personagem_classe,
            personagem_path,
            personagem_heritage,
            personagem_melancolia,
            personagem_catarse,
            personagem_pe,
            personagem_pe,
            personagem_hp,
            personagem_hp,
            personagem_hp_tipo.lower(),
            personagem_reducao_de_dano,
            personagem_bonus_de_proficiencia,
            personagem_pontos_de_sombra,
            personagem_forca_protecao,
            personagem_forca_bonus,
            personagem_destreza_protecao,
            personagem_destreza_bonus,
            personagem_constituicao_protecao,
            personagem_constituicao_bonus,
            personagem_inteligencia_protecao,
            personagem_inteligencia_bonus,
            personagem_sabedoria_protecao,
            personagem_sabedoria_bonus,
            personagem_carisma_protecao,
            personagem_carisma_bonus,
            personagem_volume_atual,
            personagem_limite_de_volume,
            personagem_resistencia,
            personagem_vulnerabilidade,
            personagem_imunidade,
            personagem_saldo,
            personagem_imagem,
            personagem_tokenn,
            personagem_usuario,
            personagem_party,
            personagem_uuid,
        )
        st.success(
            f"('{personagem_uuid}', '{personagem_nome}', '{personagem_nickname}', {personagem_level}, {personagem_legacy}, {personagem_classe}, {personagem_path}, {personagem_heritage}, {personagem_melancolia}, {personagem_catarse}, {personagem_pe}, {personagem_pe}, {personagem_hp}, {personagem_hp}, '{personagem_hp_tipo}', {personagem_reducao_de_dano}, {personagem_bonus_de_proficiencia}, {personagem_pontos_de_sombra}, {personagem_forca_protecao}, {personagem_forca_bonus}, {personagem_destreza_protecao}, {personagem_destreza_bonus}, {personagem_constituicao_protecao}, {personagem_constituicao_bonus}, {personagem_inteligencia_protecao}, {personagem_inteligencia_bonus}, {personagem_sabedoria_protecao}, {personagem_sabedoria_bonus}, {personagem_carisma_protecao}, {personagem_carisma_bonus}, {personagem_volume_atual}, {personagem_limite_de_volume}, '{personagem_resistencia}, {personagem_vulnerabilidade}, {personagem_imunidade}, {personagem_saldo}, {personagem_imagem}, {personagem_tokenn}, {personagem_usuario}, '{ personagem_party}'),")

with st.expander("Criar Party"):
    party_esquerda, party_direita = st.columns(2)
    with party_esquerda:
        party_uuid = st.text_input(
            "UUID", label_visibility="collapsed", placeholder="UUID", key="uuid_party"
        )
    with party_direita:
        st.button("Gerar UUID Aleatório para Party", on_click=atualizar_uuid_party)

    party_nome = st.text_input("Nome da Party")
    if st.button("Criar Party"):
        uuid_criado = party.criar_party(
            st.session_state["db_session"],
            party_nome,
            party_uuid,
        )
        st.success(
            f"('{uuid_criado}', '{party_nome}'),"
        )

with st.expander("Criar Relação entre Personagem e Item"):
    personagem_item_personagem = st.selectbox("Personagem do Item", [p.nome for p in lista_personagens])
    lista_itens = itens.pegar_todos_os_itens(st.session_state["db_session"])
    mapa_itens_id = {i.nome: i.id_item for i in lista_itens}
    personagem_item_item = st.selectbox("Item", list(mapa_itens_id.keys()))
    personagem_item_quantidade = st.number_input("Quantidade do Item", step=1, value=1)
    if st.button("Criar Relação entre Personagem e Item"):
        uuid_criado = personagens.criar_relacao_personagem_item(
            st.session_state["db_session"],
            mapa_nome_id_personagem[personagem_item_personagem],
            mapa_itens_id[personagem_item_item],
            personagem_item_quantidade,
        )
        st.success(
                f"('{mapa_itens_id[personagem_item_item]}', '{mapa_nome_id_personagem[personagem_item_personagem]}'),"
            )

with st.expander("Criar Relação entre Personagem e Perícia"):
    personagem_pericia_personagem = st.selectbox("Personagem da Perícia", [p.nome for p in lista_personagens])
    lista_pericias = pericia.pegar_todas_as_pericias(st.session_state["db_session"])
    mapa_pericias_id = {p.nome: p.id_pericia for p in lista_pericias}
    personagem_pericia_pericia = st.selectbox("Perícia", list(mapa_pericias_id.keys()))
    personagem_pericia_nivel = st.number_input("Nível da Perícia", step=1, value=1)
    if st.button("Criar Relação entre Personagem e Perícia"):
        uuid_criado = personagens.criar_relacao_personagem_pericia(
            st.session_state["db_session"],
            mapa_nome_id_personagem[personagem_pericia_personagem],
            mapa_pericias_id[personagem_pericia_pericia],
            personagem_pericia_nivel,
        )
        st.success(
                f"('{mapa_pericias_id[personagem_pericia_pericia]}', '{mapa_nome_id_personagem[personagem_pericia_personagem]}'),"
            )

with st.expander("Criar Relação entre Modificador e Skill"):
    lista_modificadores = modificadores.pegar_todos_os_modificadores(st.session_state["db_session"])
    mapa_modificadores_id = {m.id_modificador: m.descricao for m in lista_modificadores}
    modificador_skill_modificador = st.selectbox("Modificador", list(mapa_modificadores_id.keys()))
    lista_skills = skills.pegar_todas_as_skills(st.session_state["db_session"])
    mapa_skills_id = {s.nome: s.id_skill for s in lista_skills}
    modificador_skill_skill = st.selectbox("Skill", list(mapa_skills_id.keys()))
    if st.button("Criar Relação entre Modificador e Skill"):
        uuid_criado = modificadores.criar_relacao_modificador_skill(
            st.session_state["db_session"],
            mapa_modificadores_id[modificador_skill_modificador],
            mapa_skills_id[modificador_skill_skill],
        )
        st.success(
                f"('{mapa_skills_id[modificador_skill_skill]}', '{mapa_modificadores_id[modificador_skill_modificador]}'),"
            )
