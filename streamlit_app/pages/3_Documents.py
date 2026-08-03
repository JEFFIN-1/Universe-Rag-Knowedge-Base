import streamlit as st

from components.sidebar import render as render_sidebar
from components.uploader import render as render_uploader
from utils import load_css

st.set_page_config(page_title="Documents | RAG Assistant", page_icon="📄", layout="wide")
load_css("sidebar.css")
load_css("chat.css")
render_sidebar()
st.title("Documents")
render_uploader()
st.caption("Connect this uploader to your ingestion endpoint when it is available.")
