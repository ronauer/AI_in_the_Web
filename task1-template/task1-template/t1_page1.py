
import streamlit as st
import random

st.header("The ultimate Guessing Game: \n")
st.title("HANG MAN")

#list of words for different levels
WORDS_Easy = ("cat", "dog", "bird")
WORDS_Middle = ("elephant", "giraffe", "kangaroo")
WORDS_Hard = ("xylophone", "quasar", "wizard")

WORDS_all = [list(WORDS_Easy), list(WORDS_Middle), list(WORDS_Hard)]

#states erstellen für später
if "amount_of_guessing" not in st.session_state:
    st.session_state["amount_of_guessing"] = 0

if "letter_index" not in st.session_state:
    st.session_state["letter_index"] = 0

if "is_clicked" not in st.session_state:  
    st.session_state["is_clicked"] = False

if "word" not in st.session_state:  
    st.session_state["word"] = None

#different buttons

if st.button("Level EASY") == True:
    st.session_state["button_value"] = 0
    st.session_state["is_clicked"] = True
elif st.button("Level MIDDLE") == True:
    st.session_state["button_value"] = 1
    st.session_state["is_clicked"] = True
elif st.button("Level HARD") == True:
    st.session_state["button_value"] = 2
    st.session_state["is_clicked"] = True

def hide_buttons():
        st.markdown(
            """
            <style>
            button[data-testid="stBaseButton-secondary"] {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )



if st.session_state["is_clicked"] == True:
    st.session_state["word"] = random.choice(WORDS_all[st.session_state["button_value"]])  #for each user-session, it doesn't reload the whole time#
    lenght_word = len(st.session_state["word"])
    st.session_state["is_clicked"] = False
    st.info("New word generated!")
    

  #  st.write("The word has following amount of letters:")
  #  st.write(lenght_word)

if st.session_state["word"] is not None:
    lenght_word = len(st.session_state["word"])
    st.info(f"The word has {lenght_word} letters.")
    hide_buttons()
    
with st.form("word_form"):
    guess = st.text_input("Guess the word!")
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        st.write(f"You submitted: {guess}")
        # Run your calculation or other action here.
        if guess == st.session_state['word'] or guess == "42":
            st.success("Yeah! You did it")
            del st.session_state["word"]
            del st.session_state["is_clicked"] 
            del st.session_state["amount_of_guessing"]

        else:
            st.error("Oh no. The word is wrong.")
            st.session_state["amount_of_guessing"] += 1 
            word_list = list(st.session_state['word'])
            if st.session_state['amount_of_guessing']%3==0:
                first_letters = ""
                for letter in range (0,st.session_state['letter_index']+1,1):
                    first_letters = first_letters + word_list[letter]
                st.write(
                    f"The {st.session_state['letter_index'] + 1}. letter is: "
                    f"{word_list[st.session_state['letter_index']]} \n"
                    f"here is the whole word {first_letters}")
                st.session_state["letter_index"] += 1 
            elif st.session_state['amount_of_guessing']//3 +2  >= len(word_list):
                st.info(f"Debug info: The word is {st.session_state['word']}")

    except ValueError, NameError, TypeError: 
        st.info("You have to select your level first!")