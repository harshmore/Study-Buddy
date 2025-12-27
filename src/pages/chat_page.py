import os
import streamlit as st
from src.config.settings import settings
from src.utils.helper_functions import rerun
from src.chat.chat_engine import ChatEngine
from src.prompts.templates import chat_prompt_template
from src.pages.state import reset_quiz_state


def render_chat_page():
    st.sidebar.header("💬 chat")

    chat_model = st.sidebar.selectbox(
        "Chat Model", settings.MODELS, index=len(settings.MODELS) - 1
    )

    if st.sidebar.button("➕ New Chat"):
        chat_id = f"chat_{len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[chat_id] = {
            "model": chat_model,
            "messages": [{"role": "system", "content": chat_prompt_template.template}],
        }
        st.session_state.active_chat_id = chat_id
        rerun()

    if not st.session_state.chat_sessions:
        st.info("Create a chat to start studying.")
        return

    if st.session_state.chat_sessions:
        st.session_state.active_chat_id = st.sidebar.selectbox(
            "Select Chat",
            list(st.session_state.chat_sessions.keys()),
            index=(
                list(st.session_state.chat_sessions.keys()).index(
                    st.session_state.active_chat_id
                )
                if st.session_state.active_chat_id
                else 0
            ),
        )

    chat = st.session_state.chat_sessions[st.session_state.active_chat_id]

    st.header("🧠 Study Conversation")

    for msg in chat["messages"]:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask a question...")

    if user_input:
        chat["messages"].append({"role": "user", "content": user_input})
        engine = ChatEngine(chat["model"])
        response = engine.respond(chat["messages"])
        chat["messages"].append({"role": "assistant", "content": response})
        rerun()

    if st.session_state.quiz_manager.has_meaningful_chat(chat["messages"]):
        if st.button("📝 Create Quiz from this Conversation"):
            reset_quiz_state()
            st.session_state.quiz_source = "chat"
            st.session_state.quiz_context = (
                st.session_state.quiz_manager.chat_to_context(chat["messages"])
            )
            st.session_state.page = "quiz"
            rerun()
    else:
        st.info("💡 Start a conversation to generate a quiz from it.")
