import os

import streamlit as st

from components.sidebar import render as render_sidebar

st.set_page_config(page_title="Settings | RAG Assistant", page_icon="⚙️", layout="wide")
render_sidebar()
st.title("Settings")
st.text_input("RAG API URL", value=os.getenv("RAG_API_URL", "http://localhost:8000"), disabled=True)
st.caption("Set `RAG_API_URL` in your environment to change the backend URL.")
