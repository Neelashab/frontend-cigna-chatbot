"""
Business Insurance Chat Page - Plan discovery and recommendations
"""

import streamlit as st
from client_wrapper import (
    initialize_chatbot_session,
    discover_insurance_plans,
    get_plan_recommendations,
    has_active_session,
    is_profile_complete
)

def main():
    st.title("Business Insurance Plan Discovery")
    
    # Initialize session if not already active
    if not has_active_session():
        try:
            session_id = initialize_chatbot_session()
            st.success(f"Session initialized: {session_id}")
        except Exception as e:
            st.error(f"Failed to initialize session: {e}")
            return
    
    # Navigation button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("←"):
            st.switch_page("app-pages/main_menu.py")
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    business_chat_interface()

def business_chat_interface():
    """Chat interface for business users with plan discovery and recommendations"""
    
    # Check if profile is complete
    if not is_profile_complete():
        # Profile not complete - show plan discovery chat
        st.markdown("Let me help you find the right insurance plan for your business. I'll need to gather some information about your company first.")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input for plan discovery
        if prompt := st.chat_input("Tell me about your business insurance needs..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get plan discovery response
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Processing your request..."):
                        result = discover_insurance_plans(prompt)
                    st.markdown(result["response"])
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
                
                # Check if profile is now complete
                if result["is_complete"]:
                    st.success("✅ Your business profile is now complete! Let me analyze the best insurance plans for you...")
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error processing request: {e}")
    
    else:
        # Profile is complete - show plan recommendations
        st.markdown("###  Recommended Insurance Plans")
        st.markdown("Based on your business profile, here are the recommended insurance plans:")
        
        try:
            # Get and display recommendations
            with st.spinner("Analyzing the best insurance plans for your business..."):
                recommendations = get_plan_recommendations()
            
            # Display the analysis with markdown formatting
            st.markdown("---")
            st.markdown(f"**Found {recommendations['eligible_plans_count']} eligible plans for your business**")
            st.markdown("---")
            st.markdown(recommendations["analysis"])
            
            # Option to start over
            st.markdown("---")
            if st.button("Start New Consultation"):
                # Clear session state and restart
                keys_to_clear = ["messages", "user_choice", "session_id", "profile_complete", "plan_discovery_answers"]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
                
        except Exception as e:
            st.error(f"Error getting recommendations: {e}")
            
            # Option to try again or start over
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Try Again"):
                    st.rerun()
            with col2:
                if st.button("Start Over"):
                    keys_to_clear = ["messages", "user_choice", "session_id", "profile_complete", "plan_discovery_answers"]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()

if __name__ == "__main__":
    main()