import streamlit as st


def render(conn):
    """Render the main dashboard page."""
    st.title("StreamDuck Dashboard")
    st.write("Это базовая главная страница для будущего дашборда.")
    if conn is not None:
        st.success("Соединение с БД активно")
    else:
        st.warning("Нет подключения к БД")
