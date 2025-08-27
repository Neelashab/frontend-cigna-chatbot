"""
Wrapper functions for the Cigna Insurance Chatbot API client.
Provides a simplified interface for frontend components.
"""

import streamlit as st
from typing import Optional, Dict, Any
from api_client import (
    create_session,
    ask_rag_bot,
    start_plan_discovery,
    analyze_plans,
    get_session_info,
    reset_session
)

def initialize_chatbot_session() -> str:
    """
    Wrapper to initialize a new chatbot session.
    
    Returns:
        str: The session ID
    """
    return create_session()

def chat_with_rag_bot(user_message: str) -> str:
    """
    Wrapper to send a message to the RAG chatbot.
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: The bot's response
    """
    return ask_rag_bot(user_message)

def discover_insurance_plans(user_query: str) -> Dict[str, Any]:
    """
    Wrapper to start the plan discovery process.
    
    Args:
        user_query (str): The user's query about their insurance needs
        
    Returns:
        Dict[str, Any]: Response containing response, profile, is_complete
    """
    return start_plan_discovery(user_query)

def get_plan_recommendations() -> Dict[str, Any]:
    """
    Wrapper to get plan analysis and recommendations.
    
    Returns:
        Dict[str, Any]: Analysis data with analysis and eligible_plans_count
    """
    return analyze_plans()

def get_current_session_status() -> Dict[str, Any]:
    """
    Wrapper to get current session information.
    
    Returns:
        Dict[str, Any]: Session information
    """
    return get_session_info()

def restart_chatbot_session():
    """
    Wrapper to reset the current session.
    """
    reset_session()

def is_profile_complete() -> bool:
    """
    Helper function to check if user profile is complete.
    
    Returns:
        bool: True if profile collection is complete
    """
    return st.session_state.get("profile_complete", False)

def get_user_profile() -> Optional[Dict[str, Any]]:
    """
    Helper function to get the current user profile.
    
    Returns:
        Optional[Dict[str, Any]]: User profile data or None
    """
    return st.session_state.get("plan_discovery_answers")

def has_active_session() -> bool:
    """
    Helper function to check if there's an active session.
    
    Returns:
        bool: True if there's an active session
    """
    return "session_id" in st.session_state