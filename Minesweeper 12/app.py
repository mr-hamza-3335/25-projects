import streamlit as st
import random

# --- Game Settings ---
ROWS = 8
COLS = 8
NUM_MINES = 10

# --- Emoji Setup ---
MINE = "💣"
FLAG = "🚩"
EMPTY = "⬜"

# --- Initialize Game Board ---
def init_game():
    st.session_state.board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.game_over = False
    st.session_state.win = False

    # Place mines
    mine_positions = random.sample(range(ROWS * COLS), NUM_MINES)
    for pos in mine_positions:
        r, c = divmod(pos, COLS)
        st.session_state.board[r][c] = MINE

    # Calculate numbers
    for r in range(ROWS):
        for c in range(COLS):
            if st.session_state.board[r][c] != MINE:
                count = count_adjacent_mines(r, c)
                st.session_state.board[r][c] = str(count) if count > 0 else ""

def count_adjacent_mines(r, c):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if st.session_state.board[nr][nc] == MINE:
                count += 1
    return count

# --- Reveal cells ---
def reveal_cell(r, c):
    if st.session_state.game_over or st.session_state.flagged[r][c]:
        return

    if st.session_state.board[r][c] == MINE:
        st.session_state.revealed[r][c] = True
        st.session_state.game_over = True
        return

    if st.session_state.revealed[r][c]:
        return

    st.session_state.revealed[r][c] = True

    # Auto reveal empty neighbors
    if st.session_state.board[r][c] == "":
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if not st.session_state.revealed[nr][nc]:
                    reveal_cell(nr, nc)

# --- Check Win ---
def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            if st.session_state.board[r][c] != MINE and not st.session_state.revealed[r][c]:
                return False
    return True

# --- Render Game Board ---
def render_board():
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            key = f"{r}-{c}"
            btn_label = EMPTY

            if st.session_state.revealed[r][c]:
                if st.session_state.board[r][c] == MINE:
                    btn_label = MINE
                elif st.session_state.board[r][c] == "":
                    btn_label = " "
                else:
                    btn_label = st.session_state.board[r][c]
            elif st.session_state.flagged[r][c]:
                btn_label = FLAG

            if not st.session_state.revealed[r][c]:
                if cols[c].button(btn_label, key=key):
                    if st.session_state.flag_mode:
                        st.session_state.flagged[r][c] = not st.session_state.flagged[r][c]
                    else:
                        reveal_cell(r, c)

    if st.session_state.game_over:
        st.error("💥 Game Over! You hit a mine.")
    elif check_win():
        st.success("🎉 You won the game!")
        st.session_state.win = True
        st.session_state.game_over = True

# --- Start Streamlit App ---
st.set_page_config("Minesweeper Game", layout="centered")
st.title("💣 Minesweeper Game")
st.caption("Try not to hit the bombs! 🚩")

# --- Game Instructions ---
with st.expander("📘 How to Play Instructions (Click to open)", expanded=True):
    st.markdown("""
    **👨‍🏫 Instructions to Play Minesweeper Game:**
    
    - 🎯 The goal is to reveal all safe cells without hitting any **💣 mine**.
    - 🖱️ **Click a cell** to reveal it.
    - 🚩 **Toggle Flag Mode** to place/remove flags on suspected mines.
    - 💣 If you click on a mine, **Game Over**.
    - ✅ You win if all safe cells are revealed.
    
    **Tips:**
    - Use numbers to guess where mines could be.
    - Number "2" means there are 2 mines around that cell.
    - You can click "🔁 Restart Game" anytime to start over.
    """)

# --- Init game on first run
if "board" not in st.session_state:
    init_game()

# --- Flag Toggle ---
st.session_state.flag_mode = st.toggle("🚩 Flag Mode")

# --- Show board
render_board()

# --- Restart button
if st.button("🔁 Restart Game"):
    init_game()
    st.rerun()
