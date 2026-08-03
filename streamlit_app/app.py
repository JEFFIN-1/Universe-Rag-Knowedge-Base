import streamlit as st

from api import ask
from components.chat import render_message_editor, render_messages, render_user_content
from components.source_cards import render as render_sources
from components.sidebar import render as render_sidebar
from session import initialize
from utils import load_css

st.set_page_config(page_title="RAG Assistant", page_icon="📚", layout="wide")
initialize()
load_css("sidebar.css")
load_css("chat.css")
limit = render_sidebar()

st.markdown("<div class='hero'><h1>Universe Origins History</h1><p>Explore how different perspectives explain the origins of the universe.</p></div>", unsafe_allow_html=True)
render_messages(st.session_state.messages)
render_message_editor()

edited_question = st.session_state.pop("pending_question", None)
question = edited_question or st.chat_input("Ask about your documents...")

if question:
    if edited_question is None:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            render_user_content(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching your documents…"):
            try:
                result = ask(question, limit)
                answer = result.get("answer") or "I couldn’t find a grounded answer."
                sources = result.get("sources", [])
            except Exception:
                answer = "The RAG API is not running yet. Start it with `uvicorn app.main:app --reload` and try again."
                sources = []
        st.markdown(answer)
        render_sources(sources)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
