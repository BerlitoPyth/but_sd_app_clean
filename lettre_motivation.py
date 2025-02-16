import streamlit as st
import time
from PIL import Image
import random
import sys
import json  # Ajout de l'import manquant
import pandas as pd  # Ajout de l'import pour DataFrame
from pathlib import Path

# Ajout du chemin absolu au PYTHONPATH
file_path = Path(__file__).resolve()
project_root = file_path.parent
sys.path.append(str(project_root))

# Modification des chemins pour les assets et data
ASSETS_PATH = project_root / ".assets"
DATA_PATH = project_root / ".data"

# S'assurer que les dossiers existent
ASSETS_PATH.mkdir(exist_ok=True)
DATA_PATH.mkdir(exist_ok=True)

# Import des composants après l'ajout du chemin
try:
    from components.theme import toggle_theme  # Import direct de la fonction
    from components.quiz import display_quiz   # Import direct de la fonction
    from components.presentation import display_presentation
    from components.floating_chat import add_floating_chat_to_app
    from components.projet_gaming import display_project_concept
    from components.matrix_animation import display_matrix_animation
    from components.admission_prediction import display_prediction_interface  # Un seul composant Parcoursup
    print("Imports des composants réussis")
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)

# Import du contenu
from content.lettre_motivation_content import get_lettre_motivation_content, get_note_importante

# Au début du fichier, après les imports
if 'animation_shown' not in st.session_state:
    st.session_state.animation_shown = False

if 'intro_shown' not in st.session_state:
    st.session_state.intro_shown = False

def scroll_to_section(title_id):
    js = f'''
    <script>
        function scrollToTitle() {{
            const title = document.getElementById("{title_id}");
            if (title) {{
                title.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}
        // Exécuter après un court délai pour s'assurer que le DOM est chargé
        setTimeout(scrollToTitle, 100);
    </script>
    '''
    st.markdown(js, unsafe_allow_html=True)

def write_text_slowly(text):
    """Fonction pour l'effet machine à écrire"""
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(f"### {text[:i]}▌")
        time.sleep(0.03)
    placeholder.markdown(f"### {text}")

def load_css():
    """Charge les fichiers CSS"""
    css_files = ['main.css', 'layout.css', 'typography.css', 'components.css', 'sidebar.css']
    for css_file in css_files:
        css_path = Path(project_root) / "styles" / css_file
        try:
            css_content = css_path.read_text()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Erreur lors du chargement de {css_file}: {e}")

def get_image_base64(image_path):
    """Convert image to base64 string with path handling"""
    import base64
    try:
        image_full_path = ASSETS_PATH / Path(image_path).name
        with open(image_full_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        print(f"Erreur de chargement image: {e}")
        return ""

def main():
    # Configuration de la page en premier
    st.set_page_config(
        page_title="Candidature BUT Science des Données",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={} # Pour éviter le menu qui cause des problèmes
    )
    
    load_css()
    
    # Gestion des états sans rerun
    if not st.session_state.get('animation_shown'):
        display_matrix_animation()
        st.session_state.animation_shown = True
        with st.spinner('Chargement...'):
            time.sleep(2)
            st.rerun()  # Changé de st.experimental_rerun() à st.rerun()
        return

    # Le reste du code principal (sidebar, contenu, etc.)
    with st.sidebar:
        col1, col2 = st.columns([4, 1])
        with col2:
            toggle_theme()
        
        st.title("🎯 Navigation")
        
        # Menu de navigation
        selection = st.radio(
            "",
            ["🏠 Accueil",
             "✨ Quiz",
             "🔧 Projet",
             "👤 Présentation",
             "📊 Data Parcoursup"]
        )
        st.session_state.selection = selection
        
        # Lettre de recommandation directement après le menu
        st.markdown("### 📄 Lettre de recommandation")
        try:
            if "lettre_agrandie" not in st.session_state:
                st.session_state.lettre_agrandie = False
            
            lettre = Image.open(".assets/lettre_recommandation.jpg")
            st.image(lettre, width=200, caption="Lettre de recommandation")
            if st.button("📄 Voir en plein écran"):
                st.session_state.lettre_agrandie = True
        except Exception as e:
            print(f"Erreur lors du chargement de la lettre: {str(e)}")
            st.error("Lettre de recommandation non disponible")
        
        # Formations en dernier
        st.success("""
        ### 📚 Formations
        - DAEU B (en cours)
        - Python for Everybody
        - Python Data Structures
        - Using Python to Access Web Data
        - École 42 - La Piscine
        - École Nationale des Scaphandriers
        - Expérience professionnelle
        """)

    # Affichage plein écran de la lettre si demandé
    if st.session_state.get('lettre_agrandie', False):
        # Création d'une overlay pour l'image en plein écran
        overlay_container = st.container()
        with overlay_container:
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                try:
                    lettre = Image.open(".assets/lettre_recommandation.jpg")
                    st.image(lettre, use_container_width=True)
                    if st.button("❌ Fermer", key="close_fullscreen"):
                        st.session_state.lettre_agrandie = False
                        st.rerun()  # Changé de st.experimental_rerun() à st.rerun()
                except Exception as e:
                    st.error("Impossible d'afficher la lettre en plein écran")
                    print(f"Erreur: {e}")

    # Contenu principal basé sur la sélection
    if selection == "🏠 Accueil":
        # Style mise à jour
        st.markdown("""
            <style>
            .header-content {
                display: flex;
                align-items: center;
                gap: 2rem;
                padding: 1rem 2rem;
                width: 100%;
            }
            
            .photo-container {
                flex-shrink: 0;
                width: 150px;  /* Augmenté de 100px à 150px */
                height: 150px; /* Augmenté de 100px à 150px */
            }
            
            .photo-container img {
                width: 150px;  /* Augmenté de 100px à 150px */
                height: 150px; /* Augmenté de 100px à 150px */
                object-fit: cover;
            }
            
            .text-content {
                flex-grow: 1;
            }
            
            .title-text {
                font-size: 2em !important;
                margin: 0 !important;
                line-height: 1.1;
                color: inherit;
                font-weight: bold;
            }
            
            .subtitle-text {
                font-size: 1.3em !important;
                margin: 0.2rem 0 !important;
                color: inherit;
                font-weight: 500;
            }
            
            .motto-text {
                font-style: italic;
                font-size: 1em;
                margin: 0.2rem 0 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Header avec nouvelle structure
        header_html = f"""
            <div class="page-header">
                <div class="header-content">
                    <div class="photo-container">
                        <img src="data:image/jpg;base64,{get_image_base64(".assets/photo.jpg")}" 
                             width="150" style="transform: rotate(0deg);">  <!-- Augmenté à 150 -->
                    </div>
                    <div class="text-content">
                        <h1 class="title-text">Candidature BUT Science des Données</h1>
                        <h2 class="subtitle-text">Adrien BERLIAT</h2>
                        <p class="motto-text">De la profondeur des océans à la profondeur des données... 🌊➡️📊</p>
                    </div>
                </div>
            </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)

        # Contenu avec marges
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        
        # Points clés
        st.markdown('<div class="points-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            #### Points Clés
            - 📊 Goût pour les mathématiques
            - 🤝 Expérience du travail d'équipe
            - 💡 Autodidacte
            - 🚀 Motivation à toute épreuve
            """)
        with col2:
            st.info("""
            #### Formation Actuelle
            - 📚 DAEU B en cours
            - 💻 Certifications Python
            - 🔍 École 42 - La Piscine
            - 🌟 Excellents résultats en sciences
            """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Chat
        add_floating_chat_to_app()
        
        st.markdown("---")
        
        # Lettre de motivation
        st.markdown("""
            <h2 style="display: flex; align-items: center; gap: 0.5rem;">
                📜 Ma Lettre de Motivation
            </h2>
        """, unsafe_allow_html=True)
        
        st.markdown(get_lettre_motivation_content())
        st.markdown(get_note_importante(), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Fermeture du content-section

    elif selection == "👤 Présentation":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0;
                padding: 0;
                color: inherit;
            ">Qui suis-je ?</h1>
        """, unsafe_allow_html=True)
        display_presentation(show_title=False)  # Nouveau paramètre pour éviter le doublon

        st.markdown("---")
        
    elif selection == "🔧 Projet":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0 0 1.5rem 0;
                color: inherit;
            ">🎮 Concept PC Gaming adapté aux réels besoins du client</h1>
        """, unsafe_allow_html=True)
        display_project_concept(show_title=False)  # Nouveau paramètre pour éviter le doublon
        
    elif selection == "✨ Quiz":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0 0 1.5rem 0;
                color: inherit;
            ">Découvrez si nous matchons ! ❤️</h1>
        """, unsafe_allow_html=True)
        display_quiz()
        
    elif selection == "📊 Data Parcoursup":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0;
                padding: 0;
                color: inherit;
            ">📊 Analyse des données Parcoursup 2024 - BUT Science des données</h1>
        """, unsafe_allow_html=True)
        
        # Chargement des données Parcoursup
        data_path = DATA_PATH / "parcoursup.json"
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            df = pd.DataFrame(data['results'])
        
        # Utiliser la nouvelle fonction à la place de l'ancienne
        display_prediction_interface(df, show_title=False)
    
    # Footer
    st.markdown("---")
    st.markdown("*Application interactive créée pour accompagner ma candidature au BUT Science des Données*")

if __name__ == "__main__":
    main()