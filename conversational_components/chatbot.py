import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.0)
memory = ConversationBufferMemory()


def respond_to_query(query):
    llm_agent = ConversationChain(
        llm=llm,
        memory=memory,
    )
    return llm_agent.run(query)