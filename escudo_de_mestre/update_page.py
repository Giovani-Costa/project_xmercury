import streamlit as st

from constantes import KEYSPACE

st.set_page_config(
    page_title="Update Page",
    page_icon="🎴",
)
with st.expander("CQL"):
    mapa_personagem_id = {
        personagem.nickname: personagem.id
        for personagem in st.session_state["equipe"].personagens_jogaveis
    }
    personagem = st.selectbox("Personagem", list(mapa_personagem_id.keys()))
    operacao = st.selectbox("Operação", ["Adicionar", "Subtrair", "Definir"])
    valor = st.number_input("Valor", step=1, min_value=1)
    mapa_coluna = {
        "HP": "hp_atual",
        "PE": "pe_atual",
    }
    coluna = st.selectbox("Coluna", ["HP", "PE"])

    if st.button("Executar"):
        valor_atual_coluna = str(
            st.session_state["db_session"]
            .execute(
                f"SELECT {mapa_coluna[coluna]} FROM {KEYSPACE}.personagens WHERE id = {mapa_personagem_id[personagem]};"
            )
            .one()
        )
        valor_coluna = int(
            valor_atual_coluna.replace(f"Row({mapa_coluna[coluna]}=", "").replace(
                ")", ""
            )
        )
        if operacao.lower() == "subtrair":
            st.session_state["db_session"].execute(
                f"UPDATE {KEYSPACE}.personagens SET {mapa_coluna[coluna]} = {valor_coluna - int(valor)} WHERE id = {mapa_personagem_id[personagem]}"
            )
        elif operacao.lower() == "somar":
            st.session_state["db_session"].execute(
                f"UPDATE {KEYSPACE}.personagens SET {mapa_coluna[coluna]} = {valor_coluna + int(valor)} WHERE id = {mapa_personagem_id[personagem]}"
            )
        elif operacao.lower() == "definir":
            st.session_state["db_session"].execute(
                f"UPDATE {KEYSPACE}.personagens SET {mapa_coluna[coluna]} = {int(valor)} WHERE id = {mapa_personagem_id[personagem]}"
            )
