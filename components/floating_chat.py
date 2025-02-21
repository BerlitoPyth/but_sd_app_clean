import streamlit as st
from openai import OpenAI

# Configuration du client OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Réponses préenregistrées dans un format plus accessible
PREDEFINED_RESPONSES = {
    "but sd": """La science des données est un domaine en pleine expansion, au cœur de l'innovation, et c'est précisément ce qui m'attire. Je suis passionné par LA mathématique et l'informatique, et j'ai toujours aimé jouer avec les chiffres. Ce qui me motive particulièrement, c'est d'apprendre à « faire parler les données ».""",
    
    "parcours": """Mon parcours est atypique : après un bac STI2D, j'ai exploré la programmation à l'École 42,
puis je suis devenu scaphandrier professionnel. Cette expérience m'a appris la rigueur et la gestion du stress.
Aujourd'hui en DAEU B, je consolide mes bases scientifiques pour me réorienter vers la science des données.""",
    
    "motivations": """Ma principale motivation est de combiner ma passion pour les mathématiques et l'informatique avec mon désir d'évolution professionnelle. Je suis fasciné par la façon dont les données peuvent nous aider à comprendre le monde et à prendre de meilleures décisions."""
}

# Contexte pour OpenAI
system_prompt = """
Tu es Adrien BERLIAT, 25 ans, en préparation d'un DAEU-B après une reprise d'étude.
Tu réponds aux questions sur ta candidature au BUT Science des Données.
Les questions proviennent de professeurs et recruteurs pour l'admission.

Profil rapide :
- Ex-plongeur scaphandrier professionnel (École Nationale des Scaphandriers)
- Expérience en programmation (École 42, certifications Python)
- Passionné de mathématiques et d'informatique depuis l'enfance
- Grande capacité d'adaptation prouvée par ta reconversion
- Expérience en gestion de projets techniques et travail en équipe
- Objectif : Intégrer le BUT SD puis poursuivre en master/école d’ingénieur pour devenir Data Analyst.

Réponds de manière **professionnelle mais sympathique**, en restant concis et humble.
Mets en avant ta motivation et ton parcours unique quand c'est pertinent.
"""

def generate_response(client, message, conversation_history):
    """Génère une réponse en fonction du message reçu."""

    # Vérifier si la question a une réponse préenregistrée
    message_lower = message.lower().strip('?').strip()  # Enlever les ? et les espaces
    
    # Mapping des questions pour les variations courantes
    question_mapping = {
        "but sd": "but sd",
        "but sd ?": "but sd",
        "parcours": "parcours",
        "parcours ?": "parcours",
        "motivations": "motivations",
        "motivations ?": "motivations"
    }

    # Vérifier si la question est dans le mapping
    if message_lower in question_mapping:
        key = question_mapping[message_lower]
        return PREDEFINED_RESPONSES[key]

    # Si pas de réponse préenregistrée, utiliser OpenAI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Utilisation de GPT-3.5 au lieu de GPT-4
            messages=messages,
            temperature=0.7,  # Ajout d'un paramètre de température pour des réponses plus rapides
            max_tokens=200    # Limite la longueur des réponses
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return "Une erreur est survenue, merci de réessayer."

def add_floating_chat_to_app():
    st.markdown("""
        <style>
        /* Hide empty label container */
        [data-testid="stWidgetLabel"] {
            display: none !important;
        }

        /* Optimize vertical spacing */
        .stTextInput > div {
            margin-top: 0.5rem !important;
        }

        .chat-message {
            padding: 0.5rem 1rem !important;
            margin: 0.5rem 0 !important;
            font-size: 1rem !important;
            line-height: 1.4 !important;
            border-radius: 8px !important;
        }
        
        .bot-message {
            background: rgba(28, 31, 38, 0.7) !important;
            border: 1px solid rgba(96, 165, 250, 0.2) !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            color: rgba(255, 255, 255, 0.9) !important;
        }

        /* Reduce button container spacing */
        .row-widget.stHorizontal {
            gap: 0.25rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* Compact input field with better styling */
        .stTextInput input {
            padding: 0.5rem 1rem !important;
            height: 2.5rem !important;
            background: rgba(28, 31, 38, 0.7) !important;
            border: 1px solid rgba(96, 165, 250, 0.2) !important;
            border-radius: 6px !important;
            color: white !important;
            font-size: 0.95rem !important;
        }

        .stTextInput input:focus {
            border-color: rgba(96, 165, 250, 0.5) !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.1) !important;
        }

        /* Style for the robot emoji */
        .bot-message .emoji {
            margin-right: 0.5rem !important;
            opacity: 0.8 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Predefined question buttons first
    col1, col2, col3 = st.columns(3)
    
    if col1.button("BUT SD ?"):
        response = PREDEFINED_RESPONSES["but sd"]
        st.session_state.messages = [{"role": "assistant", "content": response}]
        st.rerun()
    if col2.button("Parcours ?"):
        response = PREDEFINED_RESPONSES["parcours"]
        st.session_state.messages = [{"role": "assistant", "content": response}]
        st.rerun()
    if col3.button("Motivations ?"):
        response = PREDEFINED_RESPONSES["motivations"]
        st.session_state.messages = [{"role": "assistant", "content": response}]
        st.rerun()

    # Input field below buttons
    user_input = st.text_input("", key="chat_input", placeholder="Posez moi une autre question ici...")
    
    # Process user input for chatbot
    if user_input and st.session_state.get("last_input") != user_input:
        st.session_state.last_input = user_input
        response = generate_response(client, user_input, st.session_state.messages)
        if response:
            st.session_state.messages = [
                {"role": "assistant", "content": response}
            ]

    # Display bot response
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(
                f"""<div class="chat-message bot-message">
                    <span class="emoji">🤖</span>{msg['content']}
                </div>""", 
                unsafe_allow_html=True
            )