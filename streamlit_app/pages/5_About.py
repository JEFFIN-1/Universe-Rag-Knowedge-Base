import streamlit as st

from components.sidebar import render as render_sidebar

st.set_page_config(page_title="About | RAG Assistant", page_icon="ℹ️", layout="wide")
render_sidebar()
st.title("About")
st.write("A Streamlit interface for the project's retrieval-augmented generation API.")
