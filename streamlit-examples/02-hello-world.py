import streamlit as st

st.header("Hello, world!")

st.button("I am a button")

if st.button("Cheers!"):
    st.balloons()

if st.button("Don't click me!"):
    st.error("You clicked the button!")