import streamlit as st
import numpy as np

# Page Config
st.set_page_config(page_title="Sudoku Solver", layout="centered")

# --- Optional: Show Instructions Toggle ---
if st.toggle("📘 Show Instructions", value=True):
    st.markdown("""
    ### 🧠 Sudoku Solver App

    This is a **Sudoku Puzzle Solver** built using the **Backtracking Algorithm** and **Streamlit**.

    ---
    ### 🕹️ How to Use:
    - Fill in your Sudoku puzzle below. Leave empty cells as `0` or blank.
    - Click **Solve Puzzle** to get the solution.
    - If the puzzle has no solution, a message will be shown.
    
    ---
    ### 💡 Tip:
    Try a real-world puzzle and watch it get solved instantly! ✨
    """)

st.divider()

# --- Sudoku Grid Input ---
st.subheader("📝 Enter Your Sudoku Puzzle")
grid = []

for i in range(9):
    cols = st.columns(9)
    row = []
    for j in range(9):
        cell_value = cols[j].text_input(f"{i},{j}", "", max_chars=1, key=f"cell_{i}_{j}")
        if cell_value.strip().isdigit():
            row.append(int(cell_value))
        else:
            row.append(0)
    grid.append(row)

# --- Backtracking Sudoku Solver Function ---
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# --- Solve Puzzle Button ---
if st.button("🧩 Solve Puzzle"):
    input_board = np.array(grid)
    board_copy = input_board.copy().tolist()

    if solve_sudoku(board_copy):
        st.success("🎉 Sudoku Solved Successfully!")
        st.subheader("✅ Solved Sudoku Grid:")
        for i in range(9):
            cols = st.columns(9)
            for j in range(9):
                cols[j].markdown(f"<div style='background-color:#e0f7fa; padding:5px; text-align:center; font-size:18px; border-radius:6px'>{board_copy[i][j]}</div>", unsafe_allow_html=True)
    else:
        st.error("❌ This Sudoku puzzle has no valid solution.")

