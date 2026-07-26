import streamlit as st


def render(message_count: int, source_count: int = 0) -> None:
    first, second = st.columns(2)
    first.metric("Messages", message_count)
    second.metric("Sources used", source_count)
