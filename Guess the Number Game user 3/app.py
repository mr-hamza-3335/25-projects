# Guess the Number Game (User) - Streamlit Version (Improved)

import streamlit as st
import random

def computer_guess_number():
    # Set page title and icon
    st.set_page_config(page_title="Guess the Number Game", page_icon="🎮")

    # Custom CSS for mobile responsiveness and better UI
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
        .stRadio > div {
            flex-direction: row !important;
            gap: 10px;
        }
        .stSuccess {
            color: green;
            font-size: 20px;
        }
        .stWarning {
            color: orange;
            font-size: 20px;
        }
        .stError {
            color: red;
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎮 Guess the Number Game (User Version)")
    st.write("Apne dimag mein 1 se 100 ke beech mein ek number choose karo. Computer use guess karega.")

    # Initialize session state
    if 'low' not in st.session_state:
        st.session_state.low = 1
        st.session_state.high = 100
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.computer_guess = None

    # Display remaining attempts
    max_attempts = 7
    remaining_attempts = max_attempts - st.session_state.attempts
    st.write(f"Remaining attempts: {remaining_attempts}")

    # Computer ka guess
    if not st.session_state.game_over:
        if st.session_state.low != st.session_state.high:
            st.session_state.computer_guess = random.randint(st.session_state.low, st.session_state.high)
        else:
            st.session_state.computer_guess = st.session_state.low

        st.write(f"Computer ka guess hai: **{st.session_state.computer_guess}**")

    # User se feedback lena
    feedback = st.radio(
        "Kya computer ka guess sahi hai?",
        options=("Bada: 'b'", "Chhota: 's'", "Sahi: 'c'"),
        index=None,
    )

    if st.button("Submit Feedback"):
        st.session_state.attempts += 1

        if feedback == "Bada: 'b'":
            st.session_state.high = st.session_state.computer_guess - 1
            st.warning("Computer ka guess bada hai. Dobara try karo!")
        elif feedback == "Chhota: 's'":
            st.session_state.low = st.session_state.computer_guess + 1
            st.warning("Computer ka guess chhota hai. Dobara try karo!")
        elif feedback == "Sahi: 'c'":
            st.success(f"Badhai ho! 🎉 Computer ne sahi number {st.session_state.computer_guess} guess kiya hai!")
            st.write(f"Computer ne total {st.session_state.attempts} attempts liye.")
            st.session_state.game_over = True
        else:
            st.error("Invalid input! Sirf 'b', 's', ya 'c' daaliye.")

        # Game over condition
        if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
            st.error(f"Game over! 😔 Sahi number tha: {st.session_state.computer_guess}.")
            st.session_state.game_over = True

    # Play again button
    if st.session_state.game_over:
        if st.button("Play Again 🔄"):
            st.session_state.clear()  # Reset the game

# Run the game
computer_guess_number()