import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

#imporing necessary packages packages from langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3:fireworks-ai", 
    openai_api_base="https://router.huggingface.co/v1",
    openai_api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    temperature=0
)

X = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    }
}
Y = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "review": "Review of the quality of the mcq"
}

prompt_mcq_generator=PromptTemplate.from_template("""Content: {Text} .You are an english expert. Given the content you have to generate {Number} MCQ's for the student with the difficulty of {Difficulty}. The response should be of the format X.\
                                                  Return the result strictly in json format (not Python dict, not Markdown, no explanations)\
                                                  format of json\
                                                  {X}""")

prompt_mcq_evaluater=PromptTemplate.from_template("""Quiz: {Quiz} .You are an Mcq evaluater expert. Given the mcq your role is to review the mcq and Provide a review of less than 50 words and then correct the MCQ's if the difficulty is not on par with {Difficulty}.\
                                                  And provide the final result of the format Y. Make sure that the number of questions is {Number} and the review is given in the review section.\
                                                  Return the result strictly in JSON format (not Python dict, not Markdown, no explanations)\
                                                  format of JSON:\
                                                  {Y}""")
mcq_generator=LLMChain(llm=llm,prompt=prompt_mcq_generator,output_key="Quiz")
mcq_evaluater=LLMChain(llm=llm,prompt=prompt_mcq_evaluater,output_key="Review")

chain=SequentialChain(chains=[mcq_generator,mcq_evaluater],input_variables=["Text","Difficulty","Number","X","Y"],output_variables=["Quiz","Review"])