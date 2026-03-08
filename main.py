import streamlit as st

st.title("My First Streamlit App")

st.write("Hello from Replit")

number = st.slider("Select a number", 0, 100, 50)

st.write("Selected:", number)
