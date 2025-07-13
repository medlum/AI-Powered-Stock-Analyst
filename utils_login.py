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





# custom CSS for buttons
btn_css = """
<style>
    .stButton > button {
        background-color: #85b0c9; /* Yellow background */
        color: #fafcfc; /*text background*/
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 18px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #fafcfc;
        background-color: #4ea6d9; /* Slightly darker yellow on hover */
    }
</style>
"""