import streamlit as st

from components.sidebar import render as render_sidebar
from utils import load_css

st.set_page_config(page_title="About | RAG Assistant", page_icon="ℹ️", layout="wide")
load_css("sidebar.css")
load_css("chat.css")
render_sidebar()
st.title("About")
st.write("A Streamlit interface for the project's retrieval-augmented generation API.")
