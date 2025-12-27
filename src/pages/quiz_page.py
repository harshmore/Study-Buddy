import os
import streamlit as st
from src.config.settings import settings
from src.utils.helper_functions import rerun
from src.pages.state import reset_quiz_state
from src.generator.question_generator import QuestionGenerator


def render_quiz_page():
    st.sidebar.subheader("Quiz Settings")

    prev_mode = st.session_state.quiz_source

    quiz_mode = st.sidebar.radio(
        "Quiz Source",
        ["Topic", "Chat Conversation"],
        index=0 if st.session_state.quiz_source == "topic" else 1,
    )

    new_mode = "chat" if quiz_mode == "Chat Conversation" else "topic"
    if new_mode != prev_mode:
        reset_quiz_state()
        st.session_state.quiz_source = new_mode

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
        # st.session_state.quiz_generated = False
        # st.session_state.quiz_submitted = False

        # for k in ("user_answers", "submitted"):
        #     st.session_state.pop(k, None)

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
