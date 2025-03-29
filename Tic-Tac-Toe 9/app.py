import streamlit as st

st.set_page_config(page_title="🎮 Tic Tac Toe Pro", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>✨ Tic Tac Toe - Streamlit Edition ✨</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Play ❌ vs ⭕ — May the best player win!</h4>", unsafe_allow_html=True)

# --- Initialize session state ---
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.turn = "❌"
    st.session_state.winner = None
    st.session_state.score_x = 0
    st.session_state.score_o = 0
    st.session_state.moves = 0

# --- Winning logic ---
def check_winner(board):
    combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in combos:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

# --- Game Board UI ---
st.markdown("---")
cols = st.columns(3)
button_styles = {"❌": "background-color:#FFAAAA; font-size:35px; color:#700000;",
                 "⭕": "background-color:#AADDFF; font-size:35px; color:#003366;"}

for i in range(9):
    with cols[i % 3]:
        btn_label = st.session_state.board[i] if st.session_state.board[i] != "" else " "
        if st.session_state.board[i] == "":
            if st.button(btn_label, key=i, use_container_width=True, help=f"Click to place {st.session_state.turn}"):
                if not st.session_state.winner:
                    st.session_state.board[i] = st.session_state.turn
                    st.session_state.moves += 1
                    st.session_state.winner = check_winner(st.session_state.board)

                    if not st.session_state.winner:
                        st.session_state.turn = "⭕" if st.session_state.turn == "❌" else "❌"
        else:
            st.markdown(f"<button style='{button_styles.get(st.session_state.board[i])}' disabled>{btn_label}</button>",
                        unsafe_allow_html=True)

# --- Game Result ---
st.markdown("---")
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.info("😐 It's a Draw! No one wins.")
    else:
        st.balloons()
        st.success(f"🎉 Winner: {st.session_state.winner}")
        if st.session_state.winner == "❌":
            st.session_state.score_x += 1
        elif st.session_state.winner == "⭕":
            st.session_state.score_o += 1

# --- Show Scoreboard ---
st.markdown("---")
st.markdown(f"📊 **Scoreboard:** ❌ `{st.session_state.score_x}` | ⭕ `{st.session_state.score_o}`")
st.markdown(f"🔄 **Total Moves Played:** `{st.session_state.moves}`")

# --- Show Turn Info ---
if not st.session_state.winner:
    st.info(f"👉 **{st.session_state.turn}**'s Turn - Choose your move wisely!")

# --- Reset & New Game Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 New Round"):
        st.session_state.board = [""] * 9
        st.session_state.turn = "❌"
        st.session_state.winner = None
with col2:
    if st.button("🔃 Full Reset"):
        st.session_state.board = [""] * 9
        st.session_state.turn = "❌"
        st.session_state.winner = None
        st.session_state.score_x = 0
        st.session_state.score_o = 0
        st.session_state.moves = 0
