
from langchain import PromptTemplate
from langchain import LLMChain
import streamlit as st


#def generate_response(template,LLM_Model,mode,std,lesson,board,subtopic):
def generate_response(template,LLM_Model,mode,std,lesson,board,subtopic):

    prompt=PromptTemplate(template=template,input_variables=['mode','std','lesson','board','subtopic'])
    chain= LLMChain(prompt=prompt,llm=LLM_Model)
    return chain.run(mode=mode,std=std,lesson=lesson,board=board,subtopic=subtopic)

template="""You are teacher for {mode} for {std} student and you have to teach him lesson {lesson} of the
    {board} science book for subtopic{subtopic}, give me motivation to learn this lesson then give introduction then explain core 
    concepts with examples"""

schema = {
            "properties" : {
                "Motivation" : {"type" : "string"},
                "clear Learning objectives" : {"type" : "string"},
                "engaging introduction" : {"type" : "string"},
                "clear concepts" : {"type" : "string"},
                "examples" : {"type" : "string"},
                "conclusion" : {"type" : "string"}
            },
            "required" : ["Motivation","clear Learning objectives","engaging introduction","clear concepts","examples","conclusion"]
            }
def add_sidebar_image(image_path, width):
    st.sidebar.image(image_path, width=width, use_column_width=False)