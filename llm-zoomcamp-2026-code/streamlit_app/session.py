"""Session-state helpers shared across Streamlit pages."""

import streamlit as st


def initialize() -> None:
    st.session_state.setdefault(
        "messages",
        [
            {
                "role": "assistant",
                "content": "Hi! I’m your document assistant. Ask me anything about the content you’ve indexed.",
            }
        ],
    )
    st.session_state.setdefault("feedback", {})


def clear_history() -> None:
    st.session_state.messages = [
        {"role": "assistant", "content": "New chat started. What would you like to explore?"}
    ]
    st.session_state.feedback = {}
