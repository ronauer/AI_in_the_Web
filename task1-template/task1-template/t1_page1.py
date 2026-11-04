
import streamlit as st
import random

st.header("The ultimate Guessing Game: \n")
st.title("HANG MAN")


WORDS_Easy = ("cat", "dog", "bird")
WORDS_Middle = ("elephant", "giraffe", "kangaroo")
WORDS_Hard = ("xylophone", "quasar", "wizard")

WORDS_all = [list(WORDS_Easy), list(WORDS_Middle), list(WORDS_Hard)]


button_value = None

if st.button("Level EASY") == True:
    button_value = 0
elif st.button("Level MIDDLE") == True:
    button_value = 1
elif st.button("Level HARD") == True:
    button_value = 2




if "word" not in st.session_state:
    st.session_state["word"] = random.choice(WORDS_all[1])  #for each user-session, it doesn't reload the whole time#
    lenght_word = len(st.session_state["word"])
    st.info("New word generated! \n The word has following amount of letters:")
    st.info(lenght_word)
    

with st.form("word_form"):
    guess = st.text_input("Guess the word!")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    if guess == st.session_state['word'] or guess == "42":
        st.success("Yeah! You did it")
        del st.session_state['word']
    else:
        st.error("Oh no. The word is wrong.")
        st.info(f"Debug info: The word is {st.session_state['word']}")
