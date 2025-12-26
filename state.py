import streamlit as st
from src.utils.helper_functions import QuizManager


def init_session_state():

    defaults = {
        "page": "quiz",
        "quiz_manager": QuizManager(),
        "quiz_generated": False,
        "quiz_submitted": False,
        "quiz_source": "topic",
        "quiz_context": None,
        "chat_sessions": {},
        "active_chat_id": None,
        "rerun_trigger": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
