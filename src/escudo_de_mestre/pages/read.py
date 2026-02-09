import pandas as pd
import streamlit as st

from database import party

st.set_page_config(
    page_title="Read Page",
    page_icon="🏮",
)

with st.expander("Party"):
    if "equipe" not in st.session_state:
        equipe = party.pegar_party(
            st.session_state["db_session"], "8a87e68e-cd9d-46e5-953a-35942487ef1b"
        )
        st.session_state["equipe"] = equipe
    if st.button("Refresh"):
        st.session_state["equipe"] = party.pegar_party(
            st.session_state["db_session"], "8a87e68e-cd9d-46e5-953a-35942487ef1b"
        )

    equipe_df = pd.DataFrame(
        [
            {
                "nickname": personagem.nickname,
                "hp": personagem.hp,
                "hp_atual": personagem.hp_atual,
                "pe": personagem.pe,
                "pe_atual": personagem.pe_atual,
            }
            for personagem in st.session_state["equipe"].personagens_jogaveis
        ]
    )

    st.dataframe(equipe_df, hide_index=True)
