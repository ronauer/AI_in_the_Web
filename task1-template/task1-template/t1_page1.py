
import streamlit as st
import random

st.header("The ultimate Guessing Game: \n")
st.title("HANG MAN")

WORDS = ("python", "ice", "chocolate")

# create a new random number if we don't have one yet
if "word" not in st.session_state:
    st.session_state["word"] = random.choice(WORDS)  #for each user-session, it doesn't reload the whole time#
    lenght_word = len(st.session_state["word"])
    st.info("New word generated! \n The word has following amount of letters:")
    st.info(lenght_word)
    

with st.form("word_form"):
    guess = st.text_input("Guess the word!")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    if guess == st.session_state['word']:
        st.success("Yeah! You did it")
        del st.session_state['word']
    else:
        st.error("Oh no. The word is wrong.")
        st.info(f"Debug info: The word is {st.session_state['word']}")
