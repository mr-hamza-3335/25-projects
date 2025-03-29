# Hangman Game - Streamlit Version

import streamlit as st
import random

def hangman():
    # Set page title and icon
    st.set_page_config(page_title="Hangman Game", page_icon="🎮")

    # Custom CSS for better UI
    st.markdown(
        """
        <style>
        .stButton button {
            width: 100%;
            padding: 10px;
            font-size: 18px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput input {
            font-size: 18px !important;
            padding: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎮 Hangman Game")
    st.write("Guess the word by entering one letter at a time.")

    # Initialize session state
    if 'words' not in st.session_state:
        st.session_state.words = ["python", "programming", "hangman", "developer", "algorithm", "computer"]
        st.session_state.word = random.choice(st.session_state.words)
        st.session_state.guessed_letters = []
        st.session_state.attempts = 6
        st.session_state.game_over = False

    # Display the word with blanks
    display_word = ""
    for letter in st.session_state.word:
        if letter in st.session_state.guessed_letters:
            display_word += letter
        else:
            display_word += "_"
    st.write(f"Word: {display_word}")

    # Display remaining attempts
    st.write(f"Attempts left: {st.session_state.attempts}")

    # User input
    guess = st.text_input("Enter a letter:", max_chars=1, key="guess_input").lower()

    if st.button("Submit Guess"):
        if len(guess) != 1 or not guess.isalpha():
            st.error("Invalid input! Please enter a single letter.")
        elif guess in st.session_state.guessed_letters:
            st.warning("You already guessed that letter. Try again.")
        else:
            st.session_state.guessed_letters.append(guess)
            if guess not in st.session_state.word:
                st.session_state.attempts -= 1
                st.error(f"Oops! '{guess}' is not in the word. You have {st.session_state.attempts} attempts left.")
            else:
                st.success(f"Good job! '{guess}' is in the word.")

            # Check if the word has been fully guessed
            if "_" not in display_word:
                st.session_state.game_over = True
                st.success("Congratulations! You guessed the word correctly! 🎉")

            # Check if attempts are exhausted
            if st.session_state.attempts == 0:
                st.session_state.game_over = True
                st.error(f"Game over! 😔 The word was '{st.session_state.word}'. Better luck next time!")

    # Play again button
    if st.session_state.game_over:
        if st.button("Play Again 🔄"):
            st.session_state.clear()  # Reset the game

# Run the game
hangman()