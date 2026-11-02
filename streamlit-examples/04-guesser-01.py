import streamlit as st

st.header("Hello, world!")

guess = st.number_input(label='Guess a number', min_value=1, max_value=100)

if guess == 42:
    st.success("Yeah! You did it")
