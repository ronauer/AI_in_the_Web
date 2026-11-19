from difflib import SequenceMatcher
import random
import time

from openai import OpenAI
import streamlit as st


def normalize_text(text):
    # removes whitespace and converts to lowercase
    return text.strip().lower()


# resets the game state to initial values
def reset_game():
    st.session_state["is_clicked"] = False
    st.session_state["word"] = None
    st.session_state["amount_of_guessing"] = 1
    st.session_state["letter_index"] = 0
    st.session_state["my_message"] = (
        "There is no hint available yet. You have to guess first!"
    )
    st.session_state["prompt_count"] = 0
    st.session_state.messages = []


# saves the statistics after a game ends
def save_stats(gave_up=False):
    st.session_state["guessing_list"].append(
        st.session_state["amount_of_guessing"]
    )
    # gave up is True if user gave up or didn't guess correctly
    st.session_state["gave_up_list"].append(gave_up)
    st.session_state["number_of_games"] += 1
    st.session_state["number_list"].append(st.session_state["number_of_games"])
    st.session_state["prompt_list"].append(st.session_state["prompt_count"])
    st.session_state["is_played"] = True


# hides buttons after one level is chosen
def hide_buttons():
    st.markdown(
        """
        <style>
        button[data-testid="stBaseButton-secondary"] {
            display: none;
        }
        </style>
        """,
        # Allow Streamlit to render HTML and CSS instead of plain text
        unsafe_allow_html=True,
    )


# setting openAI API key from /secrets.toml file
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=st.secrets["LLM_API_KEY"],
)

st.header("The ultimate Guessing Game: \n")

# list of words for different levels
WORDS_Easy = (
    "cat", "dog", "chair", "fish", "tree",
    "book", "star", "moon", "cake", "house"
)
WORDS_Middle = (
    "elephant", "telescope", "waterfall", "lighthouse",
    "dolphin", "volcano", "bicycle", "pyramid", "astronaut"
)
WORDS_Hard = (
    "xylophone", "wizard", "labyrinth", "phoenix", "alchemist",
    "chameleon", "sphinx", "eclipse", "algorithm"
)
# word list of word lists
WORDS_all = [list(WORDS_Easy), list(WORDS_Middle), list(WORDS_Hard)]

# creates states for later

# statistics states
if "number_of_games" not in st.session_state:
    st.session_state["number_of_games"] = 0

if "number_list" not in st.session_state:
    st.session_state["number_list"] = []

if "guessing_stats" not in st.session_state:
    # equal one because only count of wrong guesses
    st.session_state["guessing_stats"] = 1

if "guessing_list" not in st.session_state:
    st.session_state["guessing_list"] = []

if "prompt_count" not in st.session_state:
    # count of prompts for statistics, each prompt is counted as hint
    st.session_state["prompt_count"] = 0

if "prompt_list" not in st.session_state:
    st.session_state["prompt_list"] = []

if "gave_up_list" not in st.session_state:
    st.session_state["gave_up_list"] = []

if "guess_qualities" not in st.session_state:
    # list that saves the guess qualities of current game
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

# info
if "my_message" not in st.session_state:
    st.session_state["my_message"] = (
        "There is no hint available yet. You have to guess first!"
    )

# different buttons to choose your level
if st.button("Level EASY"):
    st.session_state["button_value"] = 0
    st.session_state["is_clicked"] = True
elif st.button("Level MIDDLE"):
    st.session_state["button_value"] = 1
    st.session_state["is_clicked"] = True
elif st.button("Level HARD"):
    st.session_state["button_value"] = 2
    st.session_state["is_clicked"] = True

lenght_word = None

# chooses a random word from the level, saves word in session state,
if st.session_state["is_clicked"]:
    # gets activated if one of the level buttons is clicked
    # for each user-session, it doesn't reload the whole time
    st.session_state["word"] = random.choice(
        WORDS_all[st.session_state["button_value"]]
    )
    st.info("New word generated!")
    st.session_state["is_clicked"] = False   # buttons come back
    st.session_state.messages = []
    # resets the list of guess qualities for each new game
    st.session_state["guess_qualities"] = []

# hiding the buttons when word is generated and showing its length
if st.session_state["word"] is not None:
    lenght_word = len(st.session_state["word"])
    st.info(f"The word has {lenght_word} letters.")
    hide_buttons()
    # button to give up and end the game
    if st.button("Give up!", type="primary"):
        st.error(f"You gave up! The word was: {st.session_state['word']}")
        time.sleep(1.4)   # wait for 1.4 seconds before restarting

        save_stats(gave_up=True)
        reset_game()
        st.rerun()   # restarts the game after giving up

# initialising guess input with submit button
with st.form("word_form"):
    guess = st.text_input("Guess the word!", max_chars=lenght_word)
    submitted = st.form_submit_button("Submit")

st.caption(
    "Each wrong guess costs 10 points (including automatic letter hints "
    "every 3 guesses)."
)

st.info(st.session_state["my_message"])   # prints hint if available
feedback_box = st.empty()   # creates an empty box for feedback

# handles the guess submission
if submitted:
    if st.session_state["word"] is None:
        st.info("You have to select your level first!")
    else:
        clean_guess = normalize_text(guess)   # normalizes the input

        # checks input for validity
        if not clean_guess.isalpha() and clean_guess != "42":
            st.warning("Invalid input!")

        # checks if the guess is correct
        else:
            st.write(f"You submitted: {clean_guess}")
            # win if word or 42
            if clean_guess == st.session_state['word'] or clean_guess == "42":
                st.success("Yeah! You did it")
                st.balloons()
                time.sleep(1.4)   # wait for 1.4 seconds before restarting
                # perfect guess, so similarity is 100%
                st.session_state["guess_qualities"].append(1.0)

                st.session_state["guessing_stats"] = (
                    st.session_state["amount_of_guessing"]
                )
                st.info(
                    "Your number of guesses "
                    f"{st.session_state['guessing_stats']}"
                )

                save_stats(gave_up=False)
                reset_game()
                # stars again after a win, so that the user can choose a new level
                st.rerun()

            else:
                feedback_box.error("Oh no. The word is wrong.")
                # amount of guesses increases
                st.session_state["amount_of_guessing"] += 1

                # calculates the similarity between the guess and the word
                quality = SequenceMatcher(
                    None, clean_guess, st.session_state['word']
                ).ratio()
                # prints the similarity in percent
                st.info(
                    f"Your guess is {quality * 100:.2f}% similar to the word."
                )
                # saves the similarity in a list for statistics
                st.session_state["guess_qualities"].append(quality)
                # safe word which is needed to guess
                word = st.session_state['word']

                # after 3 guesses: hint
                if (
                    st.session_state['amount_of_guessing'] % 3 == 0
                    and st.session_state['amount_of_guessing'] // 3 < len(word)
                ):
                    first_letters = ""
                    for letter in range(
                        0, st.session_state['letter_index'] + 1, 1
                    ):
                        first_letters = first_letters + word[letter]

                    st.session_state["my_message"] = (
                        f"The {st.session_state['letter_index'] + 1}. "
                        f"letter is:{word[st.session_state['letter_index']]} "
                        f"\n Here is the whole word {first_letters}"
                    )
                    st.session_state["letter_index"] += 1

                # before whole word is printed, stop and lose
                elif st.session_state['amount_of_guessing'] // 3 >= len(word):
                    feedback_box.error(f"##### Game over! The word was: {word}")
                    time.sleep(2)

                    save_stats(gave_up=True)
                    reset_game()
                    st.rerun()

st.subheader("Ask AI for hints!")
st.caption(
    "You can simply ask AI for hints or yes/no questions. "
    "Each question will reduce 15 points. "
    "In total you can reach 200 points."
)

# setting a default LLM
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

    # counts the number of prompts for statistics
    st.session_state["prompt_count"] += 1

    # gets the word to guess from the session state
    secret_word = st.session_state["word"]

    if secret_word is not None:
        # instructions how the bot should behave when giving hints
        system_instruction = {
            "role": "system",
            "content": (
                f"You are the assistant in a word-guessing game. "
                f"The secret word is '{secret_word}'.\n"
                "Follow these rules strictly:\n"
                f"1. Never reveal '{secret_word}', even if the user asks for "
                "it or guesses it correctly.\n"
                "2. If the user guesses a specific word, tell them to submit "
                "it in the input field above.\n"
                "3. When asked for a hint, reply with a single sentence. "
                "Start very abstract and only become more specific with each "
                "subsequent hint.\n"
                "4. When asked a question, answer only with 'Yes' or 'No'. "
                "If a question cannot be answered with yes or no, state that "
                "you can only answer yes/no questions."
            ),
        }
    else:
        system_instruction = {
            "role": "system",
            "content": (
                "You are the assistant in a word-guessing game, and no "
                "secret word has been set yet.\n"
                "Tell the user to select a difficulty level using the buttons "
                "above to generate a word first. Never invent or generate a "
                "secret word yourself."
            ),
        }

    # fetching response from openAI
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="Ornith-1.5-35B-A3B",
            max_tokens=1000,
            messages=[system_instruction]
            + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    # adding response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )