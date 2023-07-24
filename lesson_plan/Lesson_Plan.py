#imporing required modules,functions,objects,classes:
import openai
import streamlit as st
from key import my_key
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import Syllabus as S
from Lesson_Utils import generate_response,template
from students import student
import json
import prompts
from langchain.chains import create_extraction_chain
from langchain import PromptTemplate
from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
import pickle
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings


#setting model and api key:
os.environ['OPENAI_API_KEY']=my_key

LLM_model=ChatOpenAI(temperature=0)

openai.api_key =my_key
#llm=gpt3_model = ChatOpenAI(model="gpt-3.5-turbo-0613",temperature=0)

def main():
    llm=gpt3_model = ChatOpenAI(model="gpt-3.5-turbo-0613",temperature=0)

    #Reading json file and storing its data in data variable:
    with open('Syllabus1.json') as f:
        data=json.load(f)
        boards=[] #storing all available boards in json file to list
        for board in data['boards']:
            boards.append(board['name'])
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    with open('D:\LLM_Intern\Vector_DB\CBSE-9th-Motion.pkl','rb') as f:
        chunks=pickle.load(f)
    st.session_state.db = Chroma.from_texts(chunks,embedding=embeddings)
    st.write("database generated")
    qa_chain = load_qa_chain(llm, chain_type="stuff",verbose=True)


    #creating student object
    stud=student()
    st.title("Lesson Plan Generator")
    #getting board as input from student with selectbox and setting attribute value:
    board=st.sidebar.selectbox('Select your board',boards)
    stud.set_board(board)

    #getting class data from student through selectbox:
    classes=[]
    for board in data['boards']:
        if board['name']==stud.get_board():
            for classs in board['classes']:
                classes.append(classs['name'])

    std=st.sidebar.selectbox('select your class',classes) #class selected by student is stored here in std
    stud.set_std(std) #added std attribute value

    #selecting subject to learn:
    subject_list=[]
    for board in data['boards']:
        if board['name']==stud.get_board():
            for classs in board['classes']:
                if classs['name']=='Class 7':
                    for subject in classs['subjects']:
                        subject_list.append(subject['name'])

    #showing list of available subjects in selectbox:
    subject=st.sidebar.selectbox("Select your subject",subject_list)
    stud.set_subject(subject) #added subject attribute value


    #selecting lesson to learn:
    lesson_names=[]
    for boards in data['boards']:
        if boards['name']==stud.get_board():
            for classes in boards['classes']:
                if classes['name']==stud.get_std():
                    for subject in classes['subjects']:
                        if subject['name']==stud.get_subject():
                            for lesson in subject['lessons']:
                                lesson_names.append(lesson['name'])

    #showing list of lessons in subject selected by student and setting attribute value:
    lesson=st.sidebar.selectbox("Select lesson to learn",lesson_names)
    stud.set_lesson(lesson)

    # subtopics to learn:
    subtopics_names=['All',]
    for boards in data['boards']:
        if boards['name']==stud.get_board():
            for classes in boards['classes']:
                if classes['name']==stud.get_std():
                    for subject in classes['subjects']:
                        if subject['name']==stud.get_subject():
                            for lesson in subject['lessons']:
                                if lesson['name']==stud.get_lesson():
                                    subtopics_names.extend(lesson['topics'])
    #the above code will store all the subtopics of selected lesson in list object
    #creating selectbox to choose the subtopic:
    sub_topic=st.sidebar.selectbox("select subtopic:",subtopics_names)
    stud.set_subtopic(sub_topic)

                                
    #selecting mode by default its learning mode:
    mode = st.sidebar.radio('Mode', ['Learning', 'Revision'])

    if mode=='Learning':
        st.write("Mode: Learning")
    else:
        st.write("Mode: Revision")


    #button to generate response:
    if st.button("Generate"):
        #spinner will shown while generating response
        with st.spinner(f"Generating Lesson plan for {stud.get_std()} std of {stud.get_board()} student"):
            template='''1) give engaging introduction to learn the lesson e.g. ask some questions
                        2) then give the clear learning objectives
                        3) then give the list of clear concepts
                        4) then give some real life examples explaing the concepts
                        5) then give conclusion which gives overview'''
            #prompt = PromptTemplate.from_template(template)
           # gpt3_model = ChatOpenAI(model="gpt-3.5-turbo-0613",temperature=0)
            #chain = LLMChain(prompt = prompt, llm = gpt3_model)
            #resp=chain.run(mode="Learning",std=stud.get_std(),lesson=stud.get_lesson(),board=stud.get_board(),subtopic=stud.get_subtopic())
            #using similarity search:
            matching_docs = st.session_state.db.similarity_search(template)
            answer =  qa_chain.run(input_documents=matching_docs, question=template)
            #llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-0613")
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
            chain = create_extraction_chain(schema, llm)
            response = chain.run(answer)
            st.write("content Generated")
            if 'content_items' not in st.session_state:
                st.session_state.content_items=[response[0]['Motivation'],response[0]['clear Learning objectives'],response[0]['clear concepts'],response[0]['examples'],response[0]['conclusion']]
            #st.write(response)
# Add a button to navigate to the next item
    
    if 'index' not in st.session_state:
        st.session_state.index = 0
# Add a button to navigate to the next item
    if st.button('Next'):
        if st.session_state.index < len(st.session_state.content_items) - 1:
            st.session_state.index += 1

    if st.button('Previous'):
     if st.session_state.index > 0:
        st.session_state.index -= 1
    try:
        for i in range(len(st.session_state.content_items)):
            if i == st.session_state.index:
                if i==0:
                    st.header('Motivation')
                elif i==1:
                    st.header('Learning Objective')
                elif i==2:
                    st.header('concepts')
                elif i==3:
                    st.header('Examples')
                elif i==4:
                    st.header('conclusion')
                st.write(st.session_state.content_items[i])
            #st.markdown(response)
    except:
        st.write("")
    #Chat interface:
    user_input=st.chat_input("Ask me")
    if user_input:
        with st.chat_message("user"):
                st.markdown(user_input)
    if user_input:
        try:
            content=st.session_state.content_items[st.session_state.index]
            input=f"for this \n\n {content} \n\n {user_input}"

            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content":input}
                ]
            )

            # Extract the assistant's reply
            assistant_reply = response['choices'][0]['message']['content']
            st.subheader("Bot response:")
            
            with st.chat_message("assistant"):
                st.markdown(response['choices'][0]['message']['content'])
        except:
            st.warning("Please generate lesson plan first")



#calling main function as code starts running:
if __name__=="__main__":
    main()

