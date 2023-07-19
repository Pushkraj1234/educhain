import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain ,create_extraction_chain,ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(model_name='gpt-4', temperature=0.0)

memory = ConversationBufferMemory()



def respond_to_query(query):
    llm_agent = ConversationChain(
        llm=llm,
        memory=memory,
    )
    return llm_agent.run(query)

def sort_objects(obj_list):
    question = []
    options = []
    correct = []

    for obj in obj_list:

        if 'question' in obj :

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


def create_ques_ans(number_of_qn,board,classe, subject , lesson , topic,standard):
    if standard is "Basic":
        level="Remembering, Understanding"
    if standard is "Intermediate":
        level="Applying, Analyzing"
    if standard is "Advanced":
        level="Evaluating or complex numerical"
    template =f"""Prepare {number_of_qn} multiple choice questions on {{board}} board {classe} ,{subject} subject , {lesson} on {topic}
    in {level} levels of blooms taxonomy. try to make the questions on true definitons and on numerical or application also  somewhat complicated
    generate a python list which contains {number_of_qn} sublists . In each python sublist ,
    first element should be the question. Second , third and fourth elements should be the only 3 options , 
    and fifth element should be the complete correct option to the question exactly as in options .avoid unnecesary text connotations
    , extra whitespaces and also avoid newlines anywhere , terminate the lists and strings correctly"""
    prompt = PromptTemplate.from_template(template)
    gpt4_model = ChatOpenAI(model="gpt-4")
    quizzer = LLMChain(prompt = prompt, llm = gpt4_model)
    a=quizzer.run(board=board)


    llm = ChatOpenAI(model = "gpt-4")

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

def report(list):
    
    template =f"""U are provided with a list of questions {{question}} and list of coreesponding answers{list[1]} marked .
    Give a report on this and suggest if any reading or clairty is required in concepts. dont write anythign unncesary"""
    prompt = PromptTemplate.from_template(template)
    gpt4_model = ChatOpenAI(model="gpt-4")
    quizzer = LLMChain(prompt = prompt, llm = gpt4_model)
    a=quizzer.run(question=list[0])
    return a

