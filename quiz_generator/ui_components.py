import json
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
from ai_components import respond_to_query


def read_image(image_path):
    return Image.open(image_path)


def render_html():
    components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)


def doubt_container(key='1'):
    if "messages{}".format(key) not in st.session_state:
        st.session_state['messages{}'.format(key)] = []
    with st.container():
        # Display chat messages from history on app rerun
        for message in st.session_state['messages{}'.format(key)]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is up?"):
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


# Define the function
def render_chapter(chapter_id, json_path):
    # Load the JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Traverse each chapter in the data
    for chapter in data['chapters']:
        # Check if the chapter's id is the id that we're looking for
        if chapter['chapterId'] == chapter_id:
            # Display the chapter title
            st.title(chapter['chapterTitle'])

            # Display each section of the chapter
            for section in chapter['sections']:
                st.header(section['sectionTitle'])
                if 'content' in section:
                    st.markdown(section['content'])
                if 'code' in section:
                    st.code(section['code'])

                # Display each subsection of the chapter
                if 'subsections' in section:
                    for subsection in section['subsections']:
                        st.subheader(subsection['subsectionTitle'])
                        if 'content' in subsection:
                            st.markdown('*' + subsection[
                                'content'] + '*')  # Wrapping the content inside asterisks will italicize the text in markdown
                        if 'image' in subsection:
                            st.image(subsection['image'])
                        if 'code' in subsection:
                            st.code(subsection['code'])
