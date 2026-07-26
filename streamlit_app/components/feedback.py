import streamlit as st


def render(message_id: int) -> None:
    choice = st.feedback("thumbs", key=f"feedback_{message_id}")
    if choice is not None:
        st.session_state.feedback[message_id] = choice
