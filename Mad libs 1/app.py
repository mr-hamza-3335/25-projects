# Mad Libs Streamlit App

import streamlit as st

# Streamlit app ka title
st.title("Mad Libs Generator")

# User se input lena
adjective = st.text_input("Ek adjective daaliye (e.g., funny, silly): ")
noun = st.text_input("Ek noun daaliye (e.g., dog, car): ")
verb = st.text_input("Ek verb daaliye (e.g., run, dance): ")
place = st.text_input("Ek place daaliye (e.g., park, school): ")
animal = st.text_input("Ek animal daaliye (e.g., cat, elephant): ")

# Button dabane par story generate karna
if st.button("Generate Story"):
    story = f"Ek baar ki baat hai, ek {adjective} {noun} tha jo roz {verb} karta tha. Ek din woh {place} gaya aur wahan ek {animal} se mila. Dono dost ban gaye aur khush rehne lage."
    st.write(story)  # Story ko display karna