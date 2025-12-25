from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.config.settings import settings


def get_groq_llm(model):
    return ChatGroq(
        api_key=settings.GROQ_API_KEY, model=model, temperature=settings.TEMPERATURE
    )


def get_openai_llm(model):
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY, model=model, temperature=settings.TEMPERATURE
    )
