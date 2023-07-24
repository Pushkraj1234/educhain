import streamlit as st
import csv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def main():
    st.title("Flashcards")
    
    if 'template' not in st.session_state:
        st.session_state.template = ''
    if 'topic' not in st.session_state:
        st.session_state.topic = ''
    if 'input_taken' not in st.session_state:
        st.session_state.input_taken = False
    if 'generate' not in st.session_state:
        st.session_state.generate = False
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    if 'card_index' not in st.session_state:
        st.session_state.card_index = 0
    if 'flashcard' not in st.session_state:
        st.session_state.flashcard = ''
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = []
    if 'remembered' not in st.session_state:
        st.session_state.remembered = 0
    if 'total_cards' not in st.session_state:
        st.session_state.total_cards = 5
        
    def generate():
        st.session_state.generate = True        
    if st.session_state.generate == False:
        topic = st.text_input("Enter the topic for flashcards")
        st.session_state.topic = topic
        content_template = "Give me 5 summary points on {topic}.Follow format: start new point from next line. don't leave a line in between "
        template = content_template
        st.session_state.template = template
        st.button("Generate Flashcards", on_click=generate)
    
    if st.session_state.generate:
        st.subheader(st.session_state.topic)

    if st.session_state.generate and st.session_state.generated == False:
        topic = st.session_state.topic
        content_prompt = PromptTemplate(template=st.session_state.template, input_variables=['topic'])
        gpt3_model = ChatOpenAI(temperature=0.5)
        discourse_writer = LLMChain(prompt=content_prompt, llm=gpt3_model)
        posts = discourse_writer.run(topic=topic)
        lines = posts.strip().split('\n')
        if len(lines) == 5:
            st.session_state.generated = True
            st.session_state.flashcards = lines
            st.session_state.flashcard = lines[0]
            # st.write(lines)
    
    if st.session_state.generated and st.session_state.card_index < st.session_state.total_cards:
        def next():
            st.session_state.flashcard = st.session_state.flashcards[st.session_state.card_index]
        def yes():
            st.session_state.remembered += 1
            st.session_state.card_index += 1
            if st.session_state.card_index < st.session_state.total_cards:
                next()
        def no():
            st.session_state.card_index += 1
            if st.session_state.card_index < st.session_state.total_cards:
                next()
        st.write(st.session_state.flashcard)
        st.write("Remebered it?")
        st.button("Yes", on_click=yes)
        st.button("No", on_click=no)
    if st.session_state.generated and st.session_state.card_index >= st.session_state.total_cards:
        st.write("Flashcards completed")
        res = f"You remembered {st.session_state.remembered} out of {st.session_state.total_cards} cards"
        st.write(res)
        

if __name__ == '__main__':
    main()