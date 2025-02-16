import streamlit as st
from .responses import get_predefined_response

def handle_user_input(client, message, conversation_history):
    """Handle user input and generate response"""
    try:
        # Check for predefined response first
        response = get_predefined_response(message)
        if response:
            return response
            
        # Use OpenAI API
        from .prompts import get_messages
        messages = get_messages(message, conversation_history)
        api_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return api_response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in handle_user_input: {str(e)}")
        return f"Désolé, une erreur est survenue: {str(e)}"
