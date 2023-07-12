import streamlit as st
from ai_components1 import create_ques_ans
import json
def app():
    tab1= st.tabs(["Give a quick quiz!"])

    st.title("Let's test your knowledge!")
    st.header("Attempt this multiple choice based quiz and test your knowledge in all levels of learning!")

    f = open('Syllabus1.json')
  
    data = json.load(f)


    session_state = st.session_state
    if "quiz_data" not in session_state:
        session_state.quiz_data = None
    if "score" not in session_state:
        session_state.score = 0
    board_placeholder=st.empty()
    class_placeholder=st.empty()
    subject_placeholder = st.empty()
    lesson_placeholder = st.empty()
    topic_placeholder = st.empty()
    n_placeholder=st.empty()
    button=st.empty()

    if session_state.quiz_data is None:
        board_names = [board["name"] for board in data["boards"]]
        board = board_placeholder.selectbox("Select board",board_names)
        board_list = next((b for b in data["boards"] if b["name"] == board), None)

        class_names = [Class["name"] for Class in board_list["classes"]]
        classe = class_placeholder.selectbox("Select class",class_names)
        classe_list= next((b for b in board_list["classes"] if b["name"]==classe) , None)

        subject_names = [subject["name"] for subject in classe_list["subjects"]]
        subject = subject_placeholder.selectbox("Select subject",subject_names)
        subject_list= next((b for b in classe_list["subjects"] if b["name"]==subject) , None)

        lesson_names = [lesson["name"] for lesson in subject_list["lessons"]]
        lesson = lesson_placeholder.selectbox("Select Lesson",lesson_names)
        lesson_list= next((b for b in subject_list["lessons"] if b["name"]==lesson) , None)
        
        topic = topic_placeholder.selectbox("Select topic",lesson_list["topics"])

        n = n_placeholder.number_input("Number of posts", min_value = 1 ,max_value = 15, value = 1, step = 1)
        if button.button("Generate"):
            if n and board and classe and subject and lesson and topic :
                try:
                    session_state.quiz_data = create_ques_ans(n, board ,classe , subject , lesson , topic)
                    n_placeholder.empty()
                    board_placeholder.empty()
                    class_placeholder.empty()
                    subject_placeholder.empty()
                    lesson_placeholder.empty()
                    topic_placeholder.empty()
                except Exception as e :
                    st.error("Please select valid topic and number")
    if session_state.quiz_data:
        questions = session_state.quiz_data[0]
        options = session_state.quiz_data[1]
        answers = session_state.quiz_data[2]
    
    ans = []
    if session_state.quiz_data:
        button.empty()
        with st.form(key='quiz'):
            question_placeholders = []
            for i, quest in enumerate(questions):
                st.write(f"{i+1}. {quest}")
                question_placeholder = st.empty()
                question_placeholders.append(question_placeholder)
                options_= options[i]

                choice = st.radio("", options_, key=i)
                if choice:
                    ans.append(choice)
            if session_state.quiz_data:
                submitted = st.form_submit_button("Submit")
            else:
                submitted = False
            if submitted:
                session_state.score=0
                for i, user_input in enumerate(answers):
                    question_placeholder = question_placeholders[i]
                    if ans[i] == user_input:
                        session_state.score+=1
                        question_placeholder.write("Correct  Answer!")
                    if ans[i] != user_input:
                        question_placeholder.write(f" Wrong! , right answer is {answers[i]}")
            st.success("Test Score - " + str(session_state.score))
        if session_state.quiz_data :
            new_quiz = st.button("new quiz")
            if new_quiz:
                session_state.quiz_data = None
                session_state.score = 0
                st.experimental_rerun()
