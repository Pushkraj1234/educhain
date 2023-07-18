import os
import streamlit as st
from ui_components.utilities import render_chapter
from landing_page import home
from lesson_plan import Lesson_Plan
from quiz_generator import page6


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


PAGES = {
    "How to use your AI notes?": [home, '1'],
    "Test your knowledge": [Lesson_Plan, '2'],
    "Quick revision using Flash Cards": [page6, '3']
}

st.sidebar.title('AI-Powered Notes')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection][0]


with st.container():
    page.app()

st.divider()

