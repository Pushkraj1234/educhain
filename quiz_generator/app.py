import streamlit as st
from page6 import app
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

app()