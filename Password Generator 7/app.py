import streamlit as st
import random
import string

# Function to ask user questions
def ask_questions():
    st.write("### Customize Your Password")
    questions = {
        "What is your favorite color?": "",
        "What is your birthdate? (Example: 15081990)": "",
        "What is your favorite animal?": "",
        "What is your favorite number?": ""
    }
    
    for question in questions:
        questions[question] = st.text_input(question)
    
    return questions

# Function to generate password based on rules
def generate_password(answers, length, use_letters=True, use_numbers=True, use_special_chars=True, custom_rules=None):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        return "Invalid options! Please select at least one character type."

    # Apply custom rules
    password = ""
    if custom_rules:
        if custom_rules["start_with_letter"]:
            password += random.choice(string.ascii_letters)
        if custom_rules["min_one_special"]:
            password += random.choice(string.punctuation)
        if custom_rules["min_one_number"]:
            password += random.choice(string.digits)

    # Fill the rest of the password
    remaining_length = length - len(password)
    password += ''.join(random.choice(characters) for _ in range(remaining_length))

    # Shuffle to ensure randomness
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

# Function to check password strength
def check_password_strength(password):
    strength = 0
    if len(password) >= 12:
        strength += 1
    if any(char in string.ascii_uppercase for char in password):
        strength += 1
    if any(char in string.ascii_lowercase for char in password):
        strength += 1
    if any(char in string.digits for char in password):
        strength += 1
    if any(char in string.punctuation for char in password):
        strength += 1

    if strength >= 4:
        return "Strong"
    elif strength >= 2:
        return "Medium"
    else:
        return "Weak"

# Function to display password strength visually
def display_strength_meter(strength):
    if strength == "Strong":
        st.success("🔒 Strong Password")
    elif strength == "Medium":
        st.warning("🔑 Medium Password")
    else:
        st.error("🔓 Weak Password")

# Main password generator function
def password_generator():
    st.title("🔐 Ultimate Password Generator")
    st.write("Create strong and secure passwords tailored to your needs.")

    # Step 1: Ask user questions
    answers = ask_questions()

    # Step 2: Password requirements
    st.write("### Password Requirements")
    col1, col2, col3 = st.columns(3)
    with col1:
        use_letters = st.checkbox("Include letters", value=True)
    with col2:
        use_numbers = st.checkbox("Include numbers", value=True)
    with col3:
        use_special_chars = st.checkbox("Include special characters", value=True)

    # Step 3: Custom rules
    st.write("### Custom Rules")
    custom_rules = {
        "start_with_letter": st.checkbox("Must start with a letter"),
        "min_one_special": st.checkbox("Must include at least one special character"),
        "min_one_number": st.checkbox("Must include at least one number")
    }

    # Step 4: Password length and quantity
    password_length = st.number_input("How long should the password be?", min_value=4, value=12)
    num_passwords = st.number_input("How many passwords do you want to generate?", min_value=1, value=1)

    # Step 5: Generate passwords
    if st.button("Generate Passwords"):
        passwords = []
        for i in range(num_passwords):
            password = generate_password(answers, password_length, use_letters, use_numbers, use_special_chars, custom_rules)
            strength = check_password_strength(password)
            passwords.append((password, strength))

        # Display generated passwords
        st.write("### Generated Passwords")
        for i, (password, strength) in enumerate(passwords):
            st.write(f"Password {i + 1}: **{password}**")
            display_strength_meter(strength)

        # Save passwords to session state
        if "password_history" not in st.session_state:
            st.session_state.password_history = []
        st.session_state.password_history.extend(passwords)

        # Export passwords to a file
        if st.button("Export Passwords to File"):
            password_text = "\n".join([p[0] for p in passwords])
            st.download_button(
                label="Download Passwords",
                data=password_text,
                file_name="generated_passwords.txt",
                mime="text/plain"
            )

    # Step 6: Display password history
    if "password_history" in st.session_state and st.session_state.password_history:
        st.write("### Password History")
        for i, (password, strength) in enumerate(st.session_state.password_history):
            st.write(f"Password {i + 1}: **{password}** (Strength: **{strength}**)")

# Run the password generator
password_generator()