from database import db
import streamlit as st

title = "Resident Survey"

st.set_page_config(
    page_title=title,
    page_icon="🤔",
)

st.title(title)

st.text("Please answer the following questions about your commute.")

live = st.text_input("Where do you live?")
work = st.text_input("Where do you work?")
would_use = st.checkbox("I would use a public transit option if it was available.")

if st.button("Submit"):
    print(f"Lives in {live}, works in {work}, would use transit: {would_use}")
    user_collection = db["people"]
    user_collection.insert_one({
        "live": live,
        "work": work,
        "would_use": would_use
    })
