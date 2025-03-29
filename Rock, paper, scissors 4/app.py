# Rock, Paper, Scissors Game - Streamlit Version

import streamlit as st
import random

def play_game():
    st.title("🎮 Rock, Paper, Scissors Game")
    st.write("Rules: Rock beats Scissors, Scissors beats Paper, Paper beats Rock.")

    # Step 1: User se input lena
    user_choice = st.radio(
        "Apna choice daaliye:",
        options=("Rock", "Paper", "Scissors"),
        index=None,  # No option selected by default
    )

    if user_choice is not None:
        computer_choice = random.choice(["Rock", "Paper", "Scissors"])

        # Step 2: User aur computer ke choices display karna
        st.write(f"Apka choice: **{user_choice}**")
        st.write(f"Computer ka choice: **{computer_choice}**")

        # Step 3: Game ka logic
        if user_choice == computer_choice:
            st.success("It's a tie! 😐")
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Scissors" and computer_choice == "Paper") or \
             (user_choice == "Paper" and computer_choice == "Rock"):
            st.success("Badhai ho! Aap jeet gaye! 🎉")
        else:
            st.error("Oops! Aap hare. Computer jeet gaya. 😔")

    # Play again button
    if st.button("Play Again 🔄"):
        st.session_state.clear()  # Reset the game

# Run the game
play_game()