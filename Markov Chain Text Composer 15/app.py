import streamlit as st
import random
import numpy as np

# Page Config
st.set_page_config(page_title="Markov Chain Text Composer", layout="centered")

# --- Header ---
st.title("🎼 Markov Chain Text Composer")
st.markdown("Create AI-style text based on your own input using **Markov Chain Algorithm** 🔗")

# --- Toggle Instructions ---
if st.toggle("📘 Show Instructions", value=True):
    st.markdown("""
    ### 📜 How It Works:
    - Paste any text (lyrics, poems, quotes, stories etc.)
    - Markov Chain will learn the pattern between words.
    - It will **auto-compose** a new paragraph in the same style!

    ---
    ### ✨ Try Examples:
    - Song lyrics
    - Your favorite quotes
    - Dialogues from movies or dramas
    """)

st.divider()

# --- Text Input Area ---
st.subheader("📝 Paste Your Text (Training Data)")
user_input = st.text_area("Enter text to train the Markov model:", height=250)

# --- Word-Level Markov Chain Builder ---
def build_markov_chain(text):
    words = text.split()
    chain = {}
    for current_word, next_word in zip(words[:-1], words[1:]):
        if current_word in chain:
            chain[current_word].append(next_word)
        else:
            chain[current_word] = [next_word]
    return chain

# --- Text Generator ---
def generate_text(chain, length=100):
    if not chain:
        return "❌ Error: Chain is empty."
    word = random.choice(list(chain.keys()))
    result = [word]
    for _ in range(length - 1):
        next_words = chain.get(word, [])
        if not next_words:
            break
        word = random.choice(next_words)
        result.append(word)
    return " ".join(result)

# --- Word Limit Selector ---
length = st.slider("📏 Output Text Length (words)", 20, 300, 100)

# --- Compose Button ---
if st.button("🎶 Compose New Text"):
    if user_input.strip() == "":
        st.warning("⚠️ Please paste some text to begin.")
    else:
        chain = build_markov_chain(user_input)
        result = generate_text(chain, length)
        st.subheader("✨ Composed Text:")
        st.success(result)
