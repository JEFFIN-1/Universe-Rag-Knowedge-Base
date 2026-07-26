"""UI utility functions."""

from pathlib import Path

import streamlit as st


ROOT = Path(__file__).parent


def load_css(name: str) -> None:
    css_path = ROOT / "styles" / name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def source_label(source: dict) -> str:
    return str(source.get("title") or source.get("filename") or source.get("source") or "Document")
