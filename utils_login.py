import streamlit as st

# credentials 
VALID_USERS = {
    "andy": "cosmo",
    "admin": "adminpass"
}

# Dialog function for login
@st.dialog("Login")
def login_dialog():
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if user in VALID_USERS and VALID_USERS[user] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Invalid username or password")





