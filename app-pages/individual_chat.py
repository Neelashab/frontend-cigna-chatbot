"""
Individual Insurance Chat Page - RAG bot consultation
"""

import streamlit as st
from client_wrapper import chat_with_rag_bot, has_active_session, initialize_chatbot_session

def main():
    st.title("Individual Insurance Consultation")
    st.markdown("Ask me anything about health insurance options for individuals and families!")
    
    # Initialize session if not already active
    if not has_active_session():
        try:
            session_id = initialize_chatbot_session()
            st.success("Session initialized")
        except Exception as e:
            st.error(f"Failed to initialize session: {e}")
            return
    
    # Navigation button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("←"):
            st.switch_page("app-pages/main_menu.py")
    
    # Initialize chat history in session state for individual chat
    if "individual_messages" not in st.session_state:
        st.session_state.individual_messages = []
        # Add welcome message
        welcome_msg = """Hello! I'm here to help you understand your health insurance options. 

I can help you with:
- Understanding different plan types (HMO, PPO, etc.)
- Coverage details and benefits
- Cost comparisons
- Finding in-network providers
- Claims and enrollment processes

So, how can I help?"""
        st.session_state.individual_messages.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat messages
    for message in st.session_state.individual_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your health insurance options..."):
        # Add user message to chat history
        st.session_state.individual_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_rag_bot(prompt)
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.individual_messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error getting response: {e}")
    
    # Clear chat button
    if st.session_state.individual_messages and len(st.session_state.individual_messages) > 1:
        st.markdown("---")
        if st.button("Clear Chat History"):
            st.session_state.individual_messages = []
            st.rerun()

if __name__ == "__main__":
    main()