# Guess the Number Game (Computer) - Streamlit Version (Improved)

import streamlit as st
import random

def guess_the_number():
    # Set page title and icon
    st.set_page_config(page_title="Guess the Number Game", page_icon="🎮")

    # Custom CSS for mobile responsiveness
    st.markdown(
        """
        <style>
        .stNumberInput input {
            font-size: 18px !important;
            padding: 10px !important;
        }
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
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎮 Guess the Number Game")
    st.write("Computer ne 1 se 100 ke beech mein ek number choose kiya hai. Guess karo!")

    # Initialize session state
    if 'number_to_guess' not in st.session_state:
        st.session_state.number_to_guess = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False

    # User input with placeholder
    user_guess = st.number_input(
        "Apna guess daaliye (1 se 100): ",
        min_value=1,
        max_value=100,
        value=1,  # Default value (min_value ke equal)
        placeholder="Enter a number between 1 and 100",  # Placeholder text
    )

    # Submit button
    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        # Check user's guess
        if user_guess < st.session_state.number_to_guess:
            st.warning("Apka guess chhota hai. Dobara try karo!")
        elif user_guess > st.session_state.number_to_guess:
            st.warning("Apka guess bada hai. Dobara try karo!")
        else:
            st.success(f"Badhai ho! 🎉 Aapne sahi number {st.session_state.number_to_guess} guess kiya hai!")
            st.write(f"Aapne total {st.session_state.attempts} attempts liye.")
            st.session_state.game_over = True

        # Remaining attempts
        if not st.session_state.game_over:
            st.info(f"Aapke paas abhi {7 - st.session_state.attempts} attempts bache hain.")

        # Game over condition
        if st.session_state.attempts >= 7 and not st.session_state.game_over:
            st.error(f"Game over! 😔 Sahi number tha: {st.session_state.number_to_guess}.")
            st.session_state.game_over = True

    # Play again button
    if st.session_state.game_over:
        if st.button("Play Again 🔄"):
            st.session_state.clear()  # Reset the game

# Run the game
guess_the_number()