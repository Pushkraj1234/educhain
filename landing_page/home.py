import streamlit as st
from ui_components.utilities import render_chapter
from conversational_components.utils import doubt_container


def app():
    json_file = 'json/chapters.json'
    chapter_id = 0
    render_chapter(chapter_id, json_file)
    doubt_container()

