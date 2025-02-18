import streamlit as st
from openai import OpenAI

# Configuration du client OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Réponses préenregistrées dans un format plus accessible
PREDEFINED_RESPONSES = {
    "pourquoi le but sd": """La science des données est un domaine en pleine expansion, au cœur de l'innovation, et c'est précisément ce qui m'attire.
Je suis passionné par les mathématiques et l'informatique, et j'ai toujours aimé jouer avec les chiffres. Ce qui me motive particulièrement, c'est d'apprendre à « faire parler les données ».""",
    
    "quel est ton parcours": """J'ai commencé en terminale STI2D, que j'ai quittée en cours d'année, avant de passer par la piscine de l'école 42.
Après un détour par l'entrepreneuriat et un diplôme à l'École Nationale des Scaphandriers, j'ai décidé de me réorienter vers la science des données.""",
    
    "quelles sont tes motivations": """Ma principale motivation est de combiner ma passion pour les mathématiques et l'informatique avec mon désir d'évolution professionnelle.
Je suis fasciné par la façon dont les données peuvent nous aider à comprendre le monde et à prendre de meilleures décisions."""
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
        "pourquoi le but sd": "pourquoi le but sd",
        "quel est ton parcours": "quel est ton parcours",
        "quelles sont tes motivations": "quelles sont tes motivations",
        # Ajout des variations avec point d'interrogation
        "pourquoi le but sd ?": "pourquoi le but sd",
        "quel est ton parcours ?": "quel est ton parcours",
        "quelles sont tes motivations ?": "quelles sont tes motivations",
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
    """Ajoute le chat à l'application"""
    st.markdown("""
        <style>
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            font-size: 0.9rem;
        }
        
        .user-message {
            text-align: right;
            background-color: #E8F0FF;
            border: 1px solid #D0E1FF;
            color: #1F2937;
        }
        
        .bot-message {
            text-align: left;
            background-color: #F3F4F6;
            border: 1px solid #E5E7EB;
            color: #1F2937;
        }

        /* Style des boutons */
        .stButton > button {
            background-color: #F3F4F6;
            color: #1F2937;
            border: 1px solid #E5E7EB;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }

        .stButton > button:hover {
            background-color: #E5E7EB;
            border-color: #D1D5DB;
        }

        /* Style de l'input */
        .stTextInput > div > div > input {
            border-radius: 0.5rem;
            border: 1px solid #E5E7EB;
            color: #1F2937;
        }

        /* Hide empty labels only in chat input */
        .stTextInput [data-testid="stWidgetLabel"]:empty,
        .stTextInput .st-emotion-cache-aoyl2m:empty,
        .stTextInput div[data-testid="stMarkdownContainer"]:empty {
            display: none !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Keep other elements visible */
        .block-container {
            display: block !important;
        }

        /* Ensure chat components are visible */
        .chat-message,
        .stButton,
        .stTextInput {
            display: block !important;
            visibility: visible !important;
        }

        /* Style spécifique pour les boutons de questions prédéfinies */
        .stButton > button {
            background-color: #1a1d23 !important;  /* Même couleur que sidebar_bg */
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.2s ease !important;
        }

        /* Effet hover sur les boutons */
        .stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            transform: translateX(4px);
        }

        /* S'assurer que le texte des boutons reste blanc */
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: white !important;
        }

        /* Ajuster les marges des boutons pour un meilleur espacement */
        .stButton {
            margin: 0.25rem 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
        
    # Initialize session state first
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Limit messages to last question and answer (max 2 messages)
    if len(st.session_state.messages) > 2:
        st.session_state.messages = st.session_state.messages[-2:]

    # Affichage des messages existants
    for msg in st.session_state.messages:
        is_user = msg["role"] == "user"
        st.markdown(
            f"""<div class="chat-message {'user-message' if is_user else 'bot-message'}">
                {'' if is_user else '🤖 '}{msg['content']}
            </div>""", 
            unsafe_allow_html=True
        )

    # Entrée utilisateur (removed the "Vous:" label)
    user_input = st.text_input("", key="chat_input", placeholder="Posez votre question ici...")
    
    # Gestion des boutons de questions suggérées
    col1, col2, col3 = st.columns(3)
    
    button_clicked = False
    if col1.button("Pourquoi le BUT SD ?"):
        user_input = "Pourquoi le BUT SD ?"
        button_clicked = True
    if col2.button("Ton parcours ?"):
        user_input = "Quel est ton parcours ?"
        button_clicked = True
    if col3.button("Tes motivations ?"):
        user_input = "Quelles sont tes motivations ?"
        button_clicked = True

    # Traitement de l'entrée (soit par texte soit par bouton)
    if user_input and (button_clicked or st.session_state.get("last_input") != user_input):
        # Réinitialiser les messages pour ne garder que la dernière interaction
        st.session_state.messages = []
        
        # Ajouter le nouveau message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            # Obtenir la réponse
            response = generate_response(client, user_input, [])  # Plus besoin de l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state["last_input"] = user_input
            
        except Exception as e:
            st.error(f"Erreur: {str(e)}")
        
        st.rerun()