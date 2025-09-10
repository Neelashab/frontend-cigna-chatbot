"""
Main Menu Page - User choice between Individual and Business consultation
"""

import streamlit as st
from client_wrapper import initialize_chatbot_session, has_active_session

def main():
    st.title("Hi! I am an expert on health insurance. What best describes you?")
    
    # Initialize session if not already active
    if not has_active_session():
        try:
            session_id = initialize_chatbot_session()
            st.success(f"Session initialized")
        except Exception as e:
            st.error(f"Failed to initialize session: {e}")
            return
    
    st.markdown("## I am...")
    
    # Create two columns for the options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("An individual", use_container_width=True):
            st.switch_page("app-pages/individual_chat.py")
        st.markdown("Learn more about health insurance options for yourself and your family")
    
    with col2:
        if st.button("A business owner", use_container_width=True):
            st.switch_page("app-pages/business_chat.py")
        st.markdown("Find the right insurance plans for your employees")

if __name__ == "__main__":
    main()