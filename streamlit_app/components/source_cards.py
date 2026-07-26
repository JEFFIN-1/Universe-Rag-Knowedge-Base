import streamlit as st

from utils import source_label


def render(sources: list[dict]) -> None:
    if not sources:
        return
    st.caption("Sources")
    for index, source in enumerate(sources, start=1):
        with st.expander(f"{index}. {source_label(source)}"):
            preview = source.get("text") or source.get("content") or "No preview available."
            st.write(preview[:800])
