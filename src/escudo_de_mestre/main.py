import streamlit as st
from dotenv import load_dotenv
import os

from database.connect_postgres import PostgresDB

load_dotenv()
postgres_db = PostgresDB(
    os.getenv("POSTGRES_DB"),
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_PORT"),
)
st.set_page_config(
    page_title="Escudo de Mestre",
    page_icon="🎲",
)
st.title("Escudo de Mestre")

if "db_session" not in st.session_state:
    conexao = PostgresDB(
        os.getenv("POSTGRES_DB"),
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
    )
    st.session_state["db_session"] = conexao
    st.success("Sessão Criada")

create_page = st.Page(
    "/code/src/escudo_de_mestre/pages/create.py", title="Create", icon="🎷"
)
read_page = st.Page("/code/src/escudo_de_mestre/pages/read.py", title="Read", icon="🏮")
update_page = st.Page(
    "/code/src/escudo_de_mestre/pages/update.py", title="Update", icon="🎴"
)
delete_page = st.Page(
    "/code/src/escudo_de_mestre/pages/delete.py", title="Delete", icon="🍃"
)

pg = st.navigation([create_page, read_page, update_page, delete_page])
st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")
pg.run()
