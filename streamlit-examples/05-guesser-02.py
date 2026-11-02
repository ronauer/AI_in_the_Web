import streamlit as st
import random

st.header("Hello, world!")

number = random.randint(1,100)

with st.form("number_form"):
    guess = st.number_input(
        "Enter a number",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    if guess == number:
        st.success("Yeah! You did it")
    else:
        st.error("Oh no. The number is wrong.")
        st.info(f"Debug info: The number is {number}")