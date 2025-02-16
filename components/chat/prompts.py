SYSTEM_PROMPT = """
Tu es Adrien BERLIAT, 25ans actuellement en préparation d'un DAEU-B...
# ...existing prompt content...
"""

def get_messages(user_message, conversation_history):
    """Prepare messages for the API call"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        *[{"role": msg["role"], "content": msg["content"]} for msg in conversation_history],
        {"role": "user", "content": user_message}
    ]
