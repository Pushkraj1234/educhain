import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, create_extraction_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.0)
memory = ConversationBufferMemory()


def sort_objects(obj_list):
    question = []
    options = []
    correct = []

    for obj in obj_list:
        # Add each value to the appropriate list, if the key exists in the dictionary and the value is not already in
        # the list
        if 'question' in obj:
            question.append(obj['question'])
        for i in range(3):
            option_list = []
            if 'option1' in obj:
                list.append(obj['option1'])
            if 'option2' in obj:
                list.append(obj['option2'])
            if 'option3' in obj:
                list.append(obj['option3'])
        options.append(option_list)
        if 'correct answer' in obj:
            correct.append(obj['correct answer'])

    return [question, options, correct]


def create_ques_ans(m, board, classe, subject, lesson, topic):
    template = f"""Prepare {m} multiple choice questions on {{board}} board {classe} ,{subject} subject , {lesson} on {topic}.
    try to make the questions on true definitions and on numerical or application also  somewhat complicated
    generate a python list which contains {m} sublist . In each python sublist , first element should be the 
    question. Second , third and fourth elements should be the only 3 options , and fifth element should be the 
    complete correct option to the question exactly as in options .avoid unnecessary text connotations , 
    extra whitespaces and also avoid newlines anywhere , terminate the lists and strings correctly """
    prompt = PromptTemplate.from_template(template)
    gpt3_model = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)
    quizzer = LLMChain(prompt=prompt, llm=gpt3_model)
    a = quizzer.run(board=board)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    schema = {
        "properties": {
            "question": {"type": "string"},
            "option1": {"type": "string"},
            "option2": {"type": "string"},
            "option3": {"type": "string"},
            "correct answer": {"type": "string"}
        },
        "required": ["question", "options", "correct_answer"]
    }
    chain = create_extraction_chain(schema, llm)
    response = chain.run(a)

    return sort_objects(response)


# print(create_ques_ans(3, "CBSE", "10", "science", "metals and non metals", "metals"))
