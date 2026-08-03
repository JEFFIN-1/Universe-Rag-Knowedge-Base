"""Session-state helpers shared across Streamlit pages."""

import streamlit as st


def initialize() -> None:
    st.session_state.setdefault(
        "messages",
        [
            {
                "role": "assistant",
                "content": "Welcome to Universe Origins History. Ask about the history of the universe from different scientific and cultural perspectives.",
            }
        ],
    )
    st.session_state.setdefault("feedback", {})
    st.session_state.setdefault("editing_message", None)
    st.session_state.setdefault("pending_question", None)


def clear_history() -> None:
    st.session_state.messages = [
        {"role": "assistant", "content": "New chat started. What would you like to explore about universe origins?"}
    ]
    st.session_state.feedback = {}
    st.session_state.editing_message = None
    st.session_state.pending_question = None
