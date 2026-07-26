import streamlit as st


def render() -> None:
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded:
        st.info(f"{uploaded.name} is ready to be sent to your ingestion workflow.")
