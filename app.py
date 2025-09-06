import streamlit as st

from main import get_motherduck_connection
from pages import mainpage

PAGES = {
    "Главная": mainpage,
}


def _get_connection_status():
    try:
        conn = get_motherduck_connection()
        return conn, "Подключено"
    except Exception as e:
        return None, f"Ошибка: {e}"


def main():
    st.set_page_config(page_title="StreamDuck", layout="wide")

    # Sidebar navigation
    st.sidebar.title("Навигация")
    page_name = st.sidebar.selectbox("Страница", list(PAGES.keys()))

    # Database connection status
    conn, status = _get_connection_status()
    if conn:
        st.sidebar.success(status)
    else:
        st.sidebar.error(status)

    # Render selected page
    page_module = PAGES[page_name]
    page_module.render(conn)


if __name__ == "__main__":
    main()
