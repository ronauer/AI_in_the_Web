from openai import OpenAI
import streamlit as st
# import numpy as py
import random
import time
# import os
from difflib import SequenceMatcher

def normalize_text(text):
    return text.strip().lower() # removes whitespace and converts to lowercase

def reset_game():
    st.session_state["is_clicked"] = False
    st.session_state["word"] = None
    st.session_state["amount_of_guessing"] = 1
    st.session_state["letter_index"] = 0
    st.session_state["my_message"] = "There is no hint available yet. You have to guess first!"
    st.session_state["prompt_count"] = 0
    st.session_state.messages = []

def save_stats(gave_up=False):
    st.session_state["guessing_list"].append(st.session_state["amount_of_guessing"])
    st.session_state["gave_up_list"].append(gave_up)
    st.session_state["number_of_games"] += 1
    st.session_state["number_list"].append(st.session_state["number_of_games"])
    st.session_state["prompt_list"].append(st.session_state["prompt_count"])
    st.session_state["is_played"] = True

# setting openAI API key from /secrets.toml file
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=st.secrets["LLM_API_KEY"],
)

st.header("The ultimate Guessing Game: \n")


# list of words for different levels
WORDS_Easy = ("cat", "dog", "chair", "fish", "tree", "book", "star", "moon", "cake", "house")
WORDS_Middle = ("elephant", "telescope", "waterfall", "lighthouse", "dolphin", "volcano", "bicycle", "pyramid", "astronaut")
WORDS_Hard = ("xylophone", "wizard", "labyrinth", "phoenix", "alchemist", "chameleon", "sphinx", "eclipse", "algorithm")
#word list of word lists
WORDS_all = [list(WORDS_Easy), list(WORDS_Middle), list(WORDS_Hard)]

# creates states for later

# statistics states
if "number_of_games" not in st.session_state:
    st.session_state["number_of_games"] = 0 

if "number_list" not in st.session_state:
    st.session_state["number_list"] = [] # list needed for statistics

if "guessing_stats" not in st.session_state:
    st.session_state["guessing_stats"] = 1   # equal one because only count of wrong guesses

if "guessing_list" not in st.session_state:
    st.session_state["guessing_list"] = []  # list needed for statistics

if "prompt_count" not in st.session_state:
    st.session_state["prompt_count"] = 0  # count of prompts for statistics, each prompt is counted as hint

if "prompt_list" not in st.session_state:
    st.session_state["prompt_list"] = []  # list needed for statistics

if "gave_up_list" not in st.session_state:
    st.session_state["gave_up_list"] = [] # 

if "guess_qualities" not in st.session_state:
    st.session_state["guess_qualities"] = []  

# game states
if "amount_of_guessing" not in st.session_state:
    st.session_state["amount_of_guessing"] = 1

if "letter_index" not in st.session_state:
    st.session_state["letter_index"] = 0

if "is_clicked" not in st.session_state:  
    st.session_state["is_clicked"] = False

if "word" not in st.session_state:  
    st.session_state["word"] = None

#info
if "my_message" not in st.session_state:
   st.session_state["my_message"] = "There is no hint available yet. You have to guess first!"


# different buttons to choose your level
if st.button("Level EASY") == True:
    st.session_state["button_value"] = 0
    st.session_state["is_clicked"] = True
elif st.button("Level MIDDLE") == True:
    st.session_state["button_value"] = 1
    st.session_state["is_clicked"] = True
elif st.button("Level HARD") == True:
    st.session_state["button_value"] = 2
    st.session_state["is_clicked"] = True


# hides buttons after one level is chosen
def hide_buttons():
        st.markdown(
            """
            <style>
            button[data-testid="stBaseButton-secondary"] {
                display: none;  
            }
            </style>
            """,  # nochmal angucken # Select all buttons with the secondary button test ID   /* Hide the selected buttons from the user interface */
            unsafe_allow_html = True,  # Allow Streamlit to render HTML and CSS instead of displaying them as plain text
        )


lenght_word = None


# chooses a random word from the level, saves word in session state, 
if st.session_state["is_clicked"] == True: # gets activated if one of the level buttons is clicked
    st.session_state["word"] = random.choice(WORDS_all[st.session_state["button_value"]])  # for each user-session, it doesn't reload the whole time#
    st.info("New word generated!")
    st.session_state["is_clicked"] = False # buttons come back 
    st.session_state.messages = []


if st.session_state["word"] is not None:
    lenght_word = len(st.session_state["word"])
    st.info(f"The word has {lenght_word} letters.")
    hide_buttons()
    if st.button("Give up!", type="primary"):
        st.error(f"You gave up! The word was: {st.session_state['word']}")
        time.sleep(2)  # wait for 4 seconds before restarting

        save_stats(gave_up=True)
        reset_game()
        st.rerun()  # restarts the game after giving up

with st.form("word_form"):
    guess = st.text_input("Guess the word!", max_chars = lenght_word)
    submitted = st.form_submit_button("Submit")

st.info(st.session_state["my_message"])  # prints hint if available
feedback_box = st.empty()  # creates an empty box for feedback

if submitted:
    if st.session_state["word"] is None:
        st.info("You have to select your level first!")
    else:
        clean_guess = normalize_text(guess)  # normalizes the input

        if not clean_guess.isalpha() and clean_guess != "42":
            st.warning("Invalid input!")
        else: 
            st.write(f"You submitted: {clean_guess}")
            # Run your calculation or other action here.
            if clean_guess == st.session_state['word'] or clean_guess == "42":  # win if word or 42
                st.success("Yeah! You did it")
                st.balloons()
                time.sleep(1.4)  # wait for 1.4 seconds before restarting
                st.session_state["guess_qualities"].append(1.0) # perfect guess, so similarity is 100%

                st.session_state["guessing_stats"] = st.session_state["amount_of_guessing"]  
                st.info(f"Your number of guesses {st.session_state["guessing_stats"]}")

                save_stats(gave_up=False)
                reset_game() 
                st.rerun() #stars again after a win, so that the user can choose a new level

            else:
                feedback_box.error("Oh no. The word is wrong.")  
                st.session_state["amount_of_guessing"] += 1   # amount of guesses increases

                quality = SequenceMatcher(None, clean_guess, st.session_state['word']).ratio()  # calculates the similarity between the guess and the word
                st.info(f"Your guess is {quality*100:.2f}% similar to the word.")  # prints the similarity in percent
                st.session_state["guess_qualities"].append(quality)  # saves the similarity in a list for statistics
                word = st.session_state['word']  # safe word which is needed to guess

                if st.session_state['amount_of_guessing']%3==0 and st.session_state['amount_of_guessing']//3 < len(word):   # after 3 guesses: hint
                    first_letters = ""
                    for letter in range (0, st.session_state['letter_index'] + 1,1):
                        first_letters = first_letters + word[letter]

                    st.session_state["my_message"]  =  (f"The {st.session_state['letter_index'] + 1}. letter is: "
                                        f"{word[st.session_state['letter_index']]} \n"
                                        f"Here is the whole word {first_letters}")
                    st.session_state["letter_index"] += 1 

                elif st.session_state['amount_of_guessing']//3  >= len(word):  # before whole word is printed, stop and lose
                    feedback_box.error(f"##### Game over! The word was: {word}")
                    time.sleep(2) 

                    save_stats(gave_up=True)
                    reset_game()
                    st.rerun()


#    except (ValueError, NameError, TypeError):  # catches errors if an user submits a number or a special character
#        st.info("You have to select your level first!")

st.subheader("Ask AI for hints!")
st.caption("You can simply ask AI for hints or yes/no questions. Each question will reduce 15 points.")

# setting a default llm
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


# initialising test chat's history without overwriting
if "messages" not in st.session_state:
    st.session_state.messages = []

# displaying chat messages from history 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# accepting user input
if prompt := st.chat_input("What is your question?"):
    # initialising chat and displaying prompt
    with st.chat_message("user"):
        st.markdown(prompt)
    # adding prompt to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.session_state["prompt_count"] += 1 # counts the number of prompts for statistics

    secret_word = st.session_state["word"]  # gets the word to guess from the session state

    if secret_word is not None:
        system_instruction = {
            "role": "system",
            "content": (
                f"This is a guessing game. The secret word is '{secret_word}'."
                f"First and most important rule ever: Never reveal {secret_word} to the user. Only provide hints to help the user guess the word. Even if guessed correctly, do not reveal the word directly."
                "Each hint as to become less abstract and more specific. So the first hint should be as abstract as possible (even though the user specific ask for a specific hint)."
                "Only use one sentence each time you provide a hint. Do not give the user the answer."
                "If the user asks a question only answer with yes or no. If yes or no do not work say you can only answer to yes or no questions."
                "If user asks for the word, do not give it to them. Instead say that you cannot give the word."
                "If user guesses a specific word, (true or not) tell him to submit it above."
            )
        } # instructions how the bot should behave when giving hints
    else: 
        system_instruction = {
            "role" : "system",
            "content" : "No secret word has been set yet."
        }



    # fetching response from openAI
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
        model="Ornith-1.5-35B-A3B",
        max_tokens=1000,
        messages=[system_instruction] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
        )
        response = st.write_stream(stream)

    # adding response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})