import streamlit as st
from src.utils.helper_functions import rerun


def render_sidebar_navigation():
    st.sidebar.header("Navigation")

    page = st.sidebar.radio(
        "Navigate",
        ["Quiz", "Chat"],
        index=0 if st.session_state.page == "quiz" else 1,
    )
    st.session_state.page = page.lower()
    st.sidebar.markdown("---")
