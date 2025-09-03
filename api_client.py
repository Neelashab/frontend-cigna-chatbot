"""
Frontend API client functions to connect to the Cigna Insurance Chatbot backend service.
"""
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import urllib.request

import streamlit as st
import requests
import os
import json
import google.auth.transport.requests
import google.oauth2.id_token

# Backend service URL from Google Cloud Secret Manager
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def get_auth_headers() -> Dict[str, str]:
    """
    Get authentication headers for API requests.
    
    Returns:
        Dict[str, str]: Headers with authorization token
        
    Raises:
        APIError: If authentication fails
    """
    try:
        # Get ID token for authentication
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, BACKEND_URL)
        
        # Prepare headers with authentication
        return {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json"
        }
    except Exception as e:
        raise APIError(f"Authentication failed: {str(e)}")


def create_session() -> str:
    """
    Create a new session with the backend service and store it in session state.
    
    Returns:
        str: The session ID
        
    Raises:
        APIError: If the session creation fails
    """
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BACKEND_URL}/session", headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        session_id = data["session_id"]
        
        # Store session ID in Streamlit session state
        st.session_state["session_id"] = session_id
        
        return session_id
        
    except requests.exceptions.RequestException as e:
        raise APIError(f"Failed to create session: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        raise APIError(f"Invalid response from backend: {str(e)}")

def get_or_create_session() -> str:
    """
    Get existing session ID from session state or create a new one.
    
    Returns:
        str: The session ID
    """
    if "session_id" not in st.session_state:
        return create_session()
    return st.session_state["session_id"]

def ask_rag_bot(user_input: str, session_id: Optional[str] = None) -> str:
    """
    Send user input to the RAG bot endpoint and collect the response.
    
    Args:
        user_input (str): The user's question or message
        session_id (str, optional): Session ID. If None, uses session from state
        
    Returns:
        str: The bot's response
        
    Raises:
        APIError: If the API call fails
    """
    if session_id is None:
        session_id = get_or_create_session()
    
    try:
        headers = get_auth_headers()
        response = requests.post(
            f"{BACKEND_URL}/chat/{session_id}",
            headers=headers,
            json={"message": user_input},
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        return data["response"]
        
    except requests.exceptions.RequestException as e:
        raise APIError(f"Failed to get RAG bot response: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        raise APIError(f"Invalid response from backend: {str(e)}")

def start_plan_discovery(user_query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the plan discovery endpoint and return the complete response.
    
    Args:
        user_query (str): The user's query for plan discovery
        session_id (str, optional): Session ID. If None, uses session from state
        
    Returns:
        Dict[str, Any]: Complete response containing:
            - response (str): Chat response
            - profile (dict): User profile information
            - is_complete (bool): Whether profile collection is complete
            
    Raises:
        APIError: If the API call fails
    """
    if session_id is None:
        session_id = get_or_create_session()
    
    try:
        headers = get_auth_headers()
        response = requests.post(
            f"{BACKEND_URL}/plan-discovery/{session_id}",
            headers=headers,
            json={"message": user_query},
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Store profile completion status in session state
        st.session_state["profile_complete"] = data.get("is_complete", False)
        st.session_state["plan_discovery_answers"] = data.get("plan_discovery_answers")
        
        return {
            "response": data["response"],
            "profile": data.get("plan_discovery_answers"),
            "is_complete": data.get("is_complete", False)
        }
        
    except requests.exceptions.RequestException as e:
        raise APIError(f"Failed to start plan discovery: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        raise APIError(f"Invalid response from backend: {str(e)}")

def analyze_plans(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the endpoint that analyzes plans given the user's profile.
    
    Args:
        session_id (str, optional): Session ID. If None, uses session from state
        
    Returns:
        Dict[str, Any]: Analysis response containing:
            - analysis (str): The plan analysis and recommendations
            - eligible_plans_count (int): Number of eligible plans found
            
    Raises:
        APIError: If the API call fails or profile is incomplete
    """
    if session_id is None:
        session_id = get_or_create_session()
    
    # Check if profile is complete before making the call
    if not st.session_state.get("profile_complete", False):
        raise APIError("Plan discovery must be completed before analyzing plans")
    
    try:
        headers = get_auth_headers()
        response = requests.post(
            f"{BACKEND_URL}/analyze-plans/{session_id}",
            headers=headers,
            timeout=90  # Analysis might take longer
        )
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "analysis": data["analysis"],
            "eligible_plans_count": data["eligible_plans_count"]
        }
        
    except requests.exceptions.RequestException as e:
        if "400" in str(e):
            raise APIError("Plan discovery is not complete. Please complete your business profile first.")
        raise APIError(f"Failed to analyze plans: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        raise APIError(f"Invalid response from backend: {str(e)}")

def get_session_info(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about the current session.
    
    Args:
        session_id (str, optional): Session ID. If None, uses session from state
        
    Returns:
        Dict[str, Any]: Session information
        
    Raises:
        APIError: If the API call fails
    """
    if session_id is None:
        session_id = get_or_create_session()
    
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BACKEND_URL}/session/{session_id}", headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise APIError(f"Failed to get session info: {str(e)}")
    except json.JSONDecodeError as e:
        raise APIError(f"Invalid response from backend: {str(e)}")

def reset_session():
    """Reset the current session by clearing session state variables."""
    keys_to_clear = ["session_id", "profile_complete", "plan_discovery_answers"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]