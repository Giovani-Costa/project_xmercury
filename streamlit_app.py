import streamlit as st

from database.connect_database import criar_session

st.set_page_config(
    page_title="Escudo de Mestre",
    page_icon="🎲",
)
st.title("Escudo de Mestre")

if "db_session" not in st.session_state:
    session = criar_session()
    st.session_state["db_session"] = session
    st.success("Sessão Criada")

create_page = st.Page("escudo_de_mestre\\create_page.py", title="Create", icon="🎷")
read_page = st.Page("escudo_de_mestre\\read_page.py", title="Read", icon="🏮")
update_page = st.Page("escudo_de_mestre\\update_page.py", title="Update", icon="🎴")
delete_page = st.Page("escudo_de_mestre\\delete_page.py", title="Delete", icon="🍃")

pg = st.navigation([create_page, read_page, update_page, delete_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
