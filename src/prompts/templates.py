# from langchain.prompts import PromptTemplate

# mcq_prompt_template = PromptTemplate(
#     template=(
#         "Generate a {difficulty} multiple-choice question about {topic}.\n\n"
#         "Return ONLY a JSON object with these exact fields:\n"
#         "- 'question': A clear, specific question\n"
#         "- 'options': An array of exactly 4 possible answers\n"
#         "- 'correct_answer': One of the options that is the correct answer\n\n"
#         "Example format:\n"
#         "{{\n"
#         '    "question": "What is the capital of France?",\n'
#         '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
#         '    "correct_answer": "Paris"\n'
#         "}}\n\n"
#         "Your response:"
#     ),
#     input_variables=["topic", "difficulty"],
# )

# fill_blank_prompt_template = PromptTemplate(
#     template=(
#         "Generate a {difficulty} fill-in-the-blank question about {topic}.\n\n"
#         "Return ONLY a JSON object with these exact fields:\n"
#         "- 'question': A sentence with '____' marking where the blank should be\n"
#         "- 'answer': The correct word or phrase that belongs in the blank\n\n"
#         "Example format:\n"
#         "{{\n"
#         '    "question": "The capital of France is ____.",\n'
#         '    "answer": "Paris"\n'
#         "}}\n\n"
#         "Your response:"
#     ),
#     input_variables=["topic", "difficulty"],
# )


# multiple_answer_prompt_template = PromptTemplate(
#     template=(
#         "Generate a {difficulty} multiple-answer multiple-choice question about {topic}.\n\n"
#         "Return ONLY a JSON object with these exact fields:\n"
#         "- 'question': A clear, specific question\n"
#         "- 'options': An array of 4 or more possible answers\n"
#         "- 'correct_answers': An array containing 1 or more correct answers from the options\n\n"
#         "Example format:\n"
#         "{{\n"
#         '    "question": "Which of the following are programming languages?",\n'
#         '    "options": ["Python", "HTML", "JavaScript", "Photoshop"],\n'
#         '    "correct_answers": ["Python", "JavaScript"]\n'
#         "}}\n\n"
#         "Your response:"
#     ),
#     input_variables=["topic", "difficulty"],
# )

# chat_prompt_template = PromptTemplate(
#     template=(
#         "You are a helpful study assistant. Provide answers that are short, precise, and no longer than 2-3 sentences. "
#         "Avoid unnecessary elaboration or excessive detail in your responses."
#     )
# )


from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    input_variables=["topic", "difficulty"],
    template=(
        "You are an expert quiz generator.\n\n"
        "Generate a {difficulty} multiple-choice question "
        "based ONLY on the following study material.\n\n"
        "Study material:\n"
        "{topic}\n\n"
        "Rules:\n"
        "- Do not introduce new concepts beyond the study material\n"
        "- Focus on conceptual understanding\n"
        "- Ensure exactly ONE correct answer\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question\n"
        "- 'options': An array of exactly 4 possible answers\n"
        "- 'correct_answer': One of the options that is the correct answer\n\n"
        "Example format:\n"
        "{{\n"
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        "}}\n\n"
        "Your response:"
    ),
)


fill_blank_prompt_template = PromptTemplate(
    input_variables=["topic", "difficulty"],
    template=(
        "You are an expert quiz generator.\n\n"
        "Generate a {difficulty} fill-in-the-blank question "
        "based ONLY on the following study material.\n\n"
        "Study material:\n"
        "{topic}\n\n"
        "Rules:\n"
        "- Use '____' for the blank\n"
        "- Do not introduce new facts\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A sentence with '____' marking where the blank should be\n"
        "- 'answer': The correct word or phrase that belongs in the blank\n\n"
        "Example format:\n"
        "{{\n"
        '    "question": "The capital of France is ____.",\n'
        '    "answer": "Paris"\n'
        "}}\n\n"
        "Your response:"
    ),
)

multiple_answer_prompt_template = PromptTemplate(
    input_variables=["topic", "difficulty"],
    template=(
        "You are an expert quiz generator.\n\n"
        "Generate a {difficulty} multiple-answer question "
        "based ONLY on the following study material.\n\n"
        "Study material:\n"
        "{topic}\n\n"
        "Rules:\n"
        "- There may be one or more correct answers\n"
        "- All correct answers must come from the options\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question\n"
        "- 'options': An array of 4 or more possible answers\n"
        "- 'correct_answers': An array containing 1 or more correct answers from the options\n\n"
        "Example format:\n"
        "{{\n"
        '    "question": "Which of the following are programming languages?",\n'
        '    "options": ["Python", "HTML", "JavaScript", "Photoshop"],\n'
        '    "correct_answers": ["Python", "JavaScript"]\n'
        "}}\n\n"
        "Your response:"
    ),
)

chat_prompt_template = PromptTemplate(
    template=(
        "You are a helpful study assistant. Provide answers that are short, precise, and no longer than 2-3 sentences. "
        "Avoid unnecessary elaboration or excessive detail in your responses."
    )
)
