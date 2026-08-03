import streamlit as st

from api import is_healthy
from session import clear_history


def render() -> int:
    with st.sidebar:
        st.caption("Your private document assistant")
        if st.button("＋  New chat", use_container_width=True, type="secondary"):
            clear_history()
            st.rerun()
        st.markdown("<p class='side-label'>WORKSPACE</p>", unsafe_allow_html=True)
        st.page_link("app.py", label="Chat", use_container_width=True)
        st.page_link("pages/2_History.py", label="History", use_container_width=True)
        st.page_link("pages/3_Documents.py", label="Documents", use_container_width=True)
        st.page_link("pages/4_Settings.py", label="Settings", use_container_width=True)
        st.page_link("pages/5_About.py", label="About", use_container_width=True)
        limit = st.slider("Source depth", 1, 10, 5, help="How many document chunks to search")
        st.divider()
        connected = is_healthy()
        state = "Connected" if connected else "Offline demo"
        dot = "online" if connected else "offline"
        st.markdown(f"<div class='connection'><i class='{dot}'></i>{state}</div>", unsafe_allow_html=True)
        st.caption("API: `RAG_API_URL`")
    return limit
