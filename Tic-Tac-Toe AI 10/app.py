import streamlit as st
import random

# Page setup
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎮 Tic Tac Toe - AI Mode</h1>", unsafe_allow_html=True)

# Game State Initialization
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None

# Winning combo checker
def get_winning_combo(board):
    combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in combos:
        if board[combo[0]] != "" and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return combo
    return []

# AI Move (Minimax)
def ai_move(board):
    def minimax(board, is_max):
        winner = check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in board:
            return 0
        scores = []
        for i in range(9):
            if board[i] == "":
                board[i] = "O" if is_max else "X"
                score = minimax(board, not is_max)
                board[i] = ""
                scores.append(score)
        return max(scores) if is_max else min(scores)

    best_score = -999
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Winner checker
def check_winner(board):
    combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in combos:
        if board[combo[0]] != "" and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return None

# Reset button
if st.button("🔄 Reset Game"):
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None

# Show winning combo
winning_combo = get_winning_combo(st.session_state.board)

# --- Draw Game Board using 3 rows x 3 cols ---
for row in range(3):
    cols = st.columns([1,1,1], gap="small")  # proper equal width cols
    for col in range(3):
        idx = row * 3 + col
        bg_color = "#fff"
        text = " "
        if st.session_state.board[idx] == "X":
            text = "❌"
            bg_color = "#FF6B6B"
        elif st.session_state.board[idx] == "O":
            text = "⭕"
            bg_color = "#4D96FF"
        if idx in winning_combo:
            bg_color = "#00C49A"

        with cols[col]:
            if st.button(text, key=idx, use_container_width=True):
                if st.session_state.board[idx] == "" and not st.session_state.winner:
                    st.session_state.board[idx] = "X"
                    if check_winner(st.session_state.board):
                        st.session_state.winner = "X"
                    elif "" in st.session_state.board:
                        move = ai_move(st.session_state.board)
                        if move is not None:
                            st.session_state.board[move] = "O"
                            if check_winner(st.session_state.board):
                                st.session_state.winner = "O"

            # Custom styling for buttons
            st.markdown(f"""
                <style>
                div[data-testid="column"] button {{
                    background-color: {bg_color};
                    height: 80px;
                    font-size: 30px;
                    font-weight: bold;
                    border-radius: 10px;
                    margin: 4px;
                    width: 100%;
                }}
                </style>
            """, unsafe_allow_html=True)

# Show result
if st.session_state.winner:
    st.success(f"🏆 Player {st.session_state.winner} Wins!")
elif "" not in st.session_state.board:
    st.info("🤝 It's a Draw!")

