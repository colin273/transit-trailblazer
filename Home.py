import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

with open("./README.md", "r") as fp:
    st.markdown(fp.read())
