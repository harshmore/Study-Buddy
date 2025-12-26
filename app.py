import streamlit as st
from dotenv import load_dotenv
from state import init_session_state
from navigation import render_sidebar_navigation
from src.pages.quiz_page import render_quiz_page
from src.pages.chat_page import render_chat_page

load_dotenv()


def main():
    st.set_page_config(page_title="Study Buddy AI", page_icon="🎧🎧")
    st.title("Study Buddy AI")

    init_session_state()
    render_sidebar_navigation()

    if st.session_state.page == "quiz":
        render_quiz_page()
    else:
        render_chat_page()

    if st.session_state.get("rerun_trigger"):
        st.session_state["rerun_trigger"] = False
        st.rerun()


if __name__ == "__main__":
    main()
