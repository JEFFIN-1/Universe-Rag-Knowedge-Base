import streamlit as st

from components.metrics import render
from components.sidebar import render as render_sidebar
from session import initialize

st.set_page_config(page_title="History | RAG Assistant", page_icon="🕘", layout="wide")
initialize(); render_sidebar()
st.title("Chat history")
render(len(st.session_state.messages))
for message in st.session_state.messages:
    st.markdown(f"**{message['role'].title()}:** {message['content']}")
