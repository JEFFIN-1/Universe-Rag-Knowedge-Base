import base64
import html

import streamlit as st
import streamlit.components.v1 as components

from components.source_cards import render as render_sources


def render_user_content(content: str) -> None:
    """Render a compact user bubble without treating their query as HTML."""
    st.markdown(f"<span class='user-message-text'>{html.escape(content)}</span>", unsafe_allow_html=True)


def render_messages(messages: list[dict]) -> None:
    for index, message in enumerate(messages):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                render_user_content(message["content"])
            else:
                st.markdown(message["content"])
            render_sources(message.get("sources", []))
            if message["role"] == "user":
                left, right, _ = st.columns([.7, .7, 10.6])
                with left:
                    encoded_message = base64.b64encode(message["content"].encode()).decode()
                    components.html(
                        f"""
                        <style>
                          body {{ margin: 0; background: transparent; font-family: sans-serif; }}
                          button {{ background: transparent; border: 0; color: #a8a8a8; cursor: pointer;
                            font-size: 12px; padding: 4px 0; }}
                          button:hover {{ color: #f4f4f4; }}
                        </style>
                        <button title="Copy message" aria-label="Copy message" onclick='navigator.clipboard.writeText(new TextDecoder().decode(Uint8Array.from(atob("{encoded_message}"), c => c.charCodeAt(0)))); this.innerHTML = "✓";'>
                          <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 8h10v12H8zM6 16H5V4h10v2H7v10z"/></svg>
                        </button>
                        """,
                        height=28,
                    )
                if right.button("✎", key=f"edit_{index}", help="Edit message"):
                    st.session_state.editing_message = index


def render_message_editor() -> None:
    """Provide an inline, editable version of a previous user prompt."""
    index = st.session_state.get("editing_message")
    if index is None:
        return

    message = st.session_state.messages[index]
    st.markdown("<div class='edit-label'>Edit message</div>", unsafe_allow_html=True)
    edited = st.text_area(
        "Edit message",
        value=message["content"],
        key=f"message_editor_{index}",
        label_visibility="collapsed",
    )
    save, cancel, _ = st.columns([1, 1, 8])
    if save.button("Save", key=f"save_edit_{index}"):
        message["content"] = edited.strip() or message["content"]
        st.session_state.messages = st.session_state.messages[: index + 1]
        st.session_state.pending_question = message["content"]
        del st.session_state.editing_message
        st.rerun()
    if cancel.button("Cancel", key=f"cancel_edit_{index}"):
        del st.session_state.editing_message
        st.rerun()
