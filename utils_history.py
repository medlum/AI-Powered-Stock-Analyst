import streamlit as st
from sys_message import system_analysis_message, system_news_message

def initialize_session_state():
    """Initialize session state variables if they do not exist."""
    if 'news_history' not in st.session_state:
        st.session_state.news_history = []
    if 'msg_history' not in st.session_state:
        st.session_state.msg_history = []

def initialize_chat_history():
    """Set up system messages for news summarization and stock analysis."""
    st.session_state.news_history.append({"role": "system", "content": system_news_message})
    st.session_state.msg_history.append({"role": "system", "content": system_analysis_message})

