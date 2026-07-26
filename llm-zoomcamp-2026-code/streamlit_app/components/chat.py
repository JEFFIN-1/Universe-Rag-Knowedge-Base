import streamlit as st

from components.source_cards import render as render_sources


def render_messages(messages: list[dict]) -> None:
    for message in messages:
        avatar = "✦" if message["role"] == "assistant" else "●"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            render_sources(message.get("sources", []))
