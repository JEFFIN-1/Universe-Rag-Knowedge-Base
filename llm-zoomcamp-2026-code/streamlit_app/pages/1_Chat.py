from pathlib import Path

import streamlit as st

st.switch_page(Path(__file__).parents[1] / "app.py")
