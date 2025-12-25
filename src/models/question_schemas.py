from typing import List
from pydantic import BaseModel,Field,field_validator

class MCQQuestion(BaseModel):

    question : str = Field(description="The question text")
    options: List[str] = Field(description="List of 4 options")
    correct_answer: str = Field(description="The correct answer from the options")

    @field_validator('question', mode='before')
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get('description' , str(v))
        return str(v)

class FillBlankQuestion(BaseModel):

    question: str = Field(description="The question text with '____' for the blank")

    answer : str = Field(description="The correct word or phrase for the blank")

    @field_validator('question' , mode='before')
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get('description' , str(v))
        return str(v)

class MultipleAnswerQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[str] = Field(min_items=4, description="List of answer options (4 or more)")
    correct_answers: List[str] = Field(description="List of correct answers from the options")

    @field_validator('question', mode='before')
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)