import os
import streamlit as st
from dotenv import load_dotenv
from src.config.settings import settings
from src.utils.helper_functions import *
from src.generator.question_generator import QuestionGenerator
from src.chat.chat_engine import ChatEngine
from src.prompts.templates import chat_prompt_template

load_dotenv()


def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "quiz"

    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_source" not in st.session_state:
        st.session_state.quiz_source = "topic"  # topic | chat

    if "quiz_context" not in st.session_state:
        st.session_state.quiz_context = None

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None

    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False


def render_sidebar_navigation():
    st.sidebar.header("Navigation")

    page = st.sidebar.radio(
        "Go to",
        ["Quiz", "Chat"],
        index=0 if st.session_state.page == "quiz" else 1,
    )

    st.session_state.page = page.lower()
    st.sidebar.markdown("---")


def render_quiz_page():
    st.header("📝 Quiz Generator")
    st.sidebar.subheader("Quiz Settings")

    quiz_mode = st.sidebar.radio(
        "Quiz Source",
        ["Topic", "Chat Conversation"],
        index=0 if st.session_state.quiz_source == "topic" else 1,
    )

    st.session_state.quiz_source = (
        "chat" if quiz_mode == "Chat Conversation" else "topic"
    )

    question_type = st.sidebar.selectbox(
        "Select question type",
        ["Single Choice", "Multiple Choice", "Fill in the Blank"],
        index=0,
    )

    if st.session_state.quiz_source == "topic":
        topic = st.sidebar.text_input("Enter topic")

    difficulty = st.sidebar.selectbox(
        "Difficulty level", ["Easy", "Medium", "Hard"], index=1
    )

    num_questions = st.sidebar.number_input(
        "Number of questions", min_value=1, max_value=10, value=5
    )

    llm = st.sidebar.selectbox("Model", settings.MODELS, index=len(settings.MODELS) - 1)

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_generated = False
        st.session_state.quiz_submitted = False

        for k in ("user_answers", "submitted"):
            st.session_state.pop(k, None)

        context = (
            st.session_state.quiz_context
            if st.session_state.quiz_source == "chat"
            else topic
        )
        if not context:
            st.warning("Please provide a topic or select a chat.")
            return

        generator = QuestionGenerator(llm)
        success = st.session_state.quiz_manager.generate_questions(
            generator=generator,
            topic=context,
            question_type=question_type,
            difficulty=difficulty,
            num_questions=num_questions,
        )

        st.session_state.quiz_generated = success
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("📋 Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("📊 Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            st.write(f"Score: {score_percentage}%")

            for _, result in results_df.iterrows():
                question_num = result["question_number"]
                if result["is_correct"]:
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")

                st.markdown("------------")

        if st.button("Save Results"):
            saved_file = st.session_state.quiz_manager.save_to_csv()

            if saved_file:
                with open(saved_file, "rb") as f:
                    st.download_button(
                        label="Downlaod Results",
                        data=f.read(),
                        file_name=os.path.basename(saved_file),
                        mime="text/csv",
                    )
            else:
                st.warning("No results avialble")


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
            st.session_state.quiz_source = "chat"
            st.session_state.quiz_context = (
                st.session_state.quiz_manager.chat_to_context(chat["messages"])
            )
            st.session_state.page = "quiz"
            rerun()
    else:
        st.info("💡 Start a conversation to generate a quiz from it.")


# -------------------------
# MAIN
# -------------------------
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
