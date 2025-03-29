# Countdown Timer - Streamlit Version

import streamlit as st
import time

def countdown_timer():
    st.title("⏳ Countdown Timer")
    st.write("Enter the time for the countdown in hours, minutes, and seconds.")

    # Step 1: User se input lena
    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.number_input("Hours", min_value=0, value=0)
    with col2:
        minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0)
    with col3:
        seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    # Step 2: Start button
    if st.button("Start Timer"):
        if total_seconds <= 0:
            st.error("Invalid time! Please enter a positive value.")
        else:
            # Step 3: Countdown logic
            timer_placeholder = st.empty()
            progress_placeholder = st.empty()

            while total_seconds > 0:
                # Convert total seconds into hours, minutes, and seconds
                hrs, rem = divmod(total_seconds, 3600)
                mins, secs = divmod(rem, 60)
                timer = f"{hrs:02d}:{mins:02d}:{secs:02d}"  # Format as HH:MM:SS

                # Progress bar calculation
                progress = (total_seconds / (hours * 3600 + minutes * 60 + seconds)) * 100
                progress_bar = f"Progress: [{('=' * int(progress / 5)).ljust(20)}] {progress:.2f}%"

                # Display timer and progress bar
                timer_placeholder.write(f"Time Left: **{timer}**")
                progress_placeholder.write(progress_bar)

                # Wait for 1 second
                time.sleep(1)

                # Decrease the total seconds
                total_seconds -= 1

            # Step 4: Timer complete message
            st.success("Time's up! 🎉")
            st.balloons()  # Celebrate with balloons

# Run the timer
countdown_timer()