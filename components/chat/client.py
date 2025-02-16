import streamlit as st
from openai import OpenAI

def init_chat_client():
    """Initialize OpenAI client with API key"""
    try:
        if not hasattr(st.secrets, "OPENAI_API_KEY"):
            st.error("Clé API OpenAI manquante")
            return None
            
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
            
    except Exception as e:
        st.error(f"Erreur d'initialisation OpenAI: {str(e)}")
        return None