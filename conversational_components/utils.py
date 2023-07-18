import streamlit as st
import json
from lesson_plan.Lesson_Utils import generate_response, template
from conversational_components.chatbot import respond_to_query


def chapter_list(board_name, class_name, subject_name):
    # Change this function and file name later
    json_file = 'lesson_plan/Syllabus1.json'
    with open(json_file, 'r') as f:
        data = json.load(f)

    chapters = [lesson['name'] for board in data['boards']
                if board['name'] == board_name
                for c_class in board['classes']
                if c_class['name'] == class_name
                for subject in c_class['subjects']
                if subject['name'] == subject_name
                for lesson in subject['lessons']]

    return chapters


def doubt_container(key='1'):
    if "messages{}".format(key) not in st.session_state:
        st.session_state['messages{}'.format(key)] = []
    with st.container():
        # Display chat messages from history on app rerun
        for message in st.session_state['messages{}'.format(key)]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        with st.chat_message("assistant"):
            with st.form('Form1'):
                board_name = st.selectbox("Select your Education Board", ['CBSE', 'Maharashtra Boards'], key=0)
                class_name = st.selectbox('Select your class', ['Class 6', 'Class 7', 'Class 8', 'Class 9'], key=1)
                subject_name = st.selectbox('Select the subject you want to study',
                                            ['Science', 'Mathematics', 'Social Studies', 'History'], key=2)
                if board_name and class_name and subject_name:
                    chapter_name = st.selectbox('Select the chapter you want to study',
                                                ['Matter and its Nature', 'Atoms and Molecules'], key=3)

                submitted1 = st.form_submit_button('Submit')

        if submitted1:
            with st.chat_message("user"):
                st.markdown(f'{board_name} {class_name} {subject_name} {chapter_name}')

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                query_response = generate_response(template, 'Learning', class_name, chapter_name, board_name, 'Atoms')
                # Simulate stream of response with milliseconds delay
                for chunk in query_response.split():
                    full_response += chunk + " "
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        # Accept user input
        if prompt := st.chat_input("Ask me :)"):
            # Add user message to chat history
            st.session_state['messages{}'.format(key)].append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                query_response = respond_to_query(prompt)
                # Simulate stream of response with milliseconds delay
                for chunk in query_response.split():
                    full_response += chunk + " "
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state['messages{}'.format(key)].append({"role": "assistant", "content": full_response})
