import streamlit as st
import time
from PIL import Image
import random
import sys
from pathlib import Path

# Ajout du chemin absolu au PYTHONPATH
file_path = Path(__file__).resolve()
project_root = file_path.parent
sys.path.append(str(project_root))

# Import des composants après l'ajout du chemin
try:

    from components.theme import toggle_theme  # Import direct de la fonction
    from components.quiz import display_quiz   # Import direct de la fonction
    from components.presentation import display_presentation
    from components.floating_chat import add_floating_chat_to_app
    from components.projet_gaming import display_project_concept
    from components.matrix_animation import display_matrix_animation
    from components.intro_tree import display_intro_tree
    try:
        from components.parcoursup_analysis import display_parcoursup_analysis
    except ImportError:
        def display_parcoursup_analysis():
            st.error("Module d'analyse Parcoursup non disponible")
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

def main():
    st.set_page_config(
        page_title="Candidature BUT Science des Données",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()
    
    # Nouvelle logique de séquence
    if not st.session_state.get('intro_shown'):
        display_intro_tree()
        return
        
    if not st.session_state.get('animation_shown'):
        display_matrix_animation()
        st.session_state.animation_shown = True
        st.rerun()
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

        # Disclaimer après la lettre
        st.info("""
        ⚠️ **Disclaimer:**
        Cette application a été entièrement conçue et développée par mes soins. 
        Aucun template n'a été utilisé.
        
        Les idées, le design et le code sont originaux, réalisés avec l'assistance d'outils d'IA comme GitHub Copilot et Claude.""")
        
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
                        st.rerun()
                except Exception as e:
                    st.error("Impossible d'afficher la lettre en plein écran")
                    print(f"Erreur: {e}")

    # Contenu principal basé sur la sélection
    if selection == "🏠 Accueil":
        # Création d'un container pour le titre et la photo
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
                <div style="margin: 0;">
                    <h1 style="
                        font-size: 2.5em;
                        margin: 0 0 0.5rem 0;
                        color: inherit;
                    ">Candidature BUT Science des Données</h1>
                    <h2 style="
                        font-size: 1.5em;
                        margin: 0 0 1rem 0;
                        color: inherit;
                    ">Adrien BERLIAT</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Effet machine à écrire
            if 'title_written' not in st.session_state:
                write_text_slowly("De la profondeur des océans à la profondeur des données... 🌊➡️📊")
                st.session_state.title_written = True
            else:
                st.markdown("""
                    <h3 style="
                        font-style: italic;
                        color: inherit;
                        font-size: 1.2em;
                        margin: 0 0 2rem 0;
                    ">De la profondeur des océans à la profondeur des données... 🌊➡️📊</h3>
                """, unsafe_allow_html=True)

        with col2:
            try:
                image = Image.open(".assets/photo.jpg")
                image_rotated = image.rotate(-90, expand=True)
                st.image(image_rotated, width=200)
            except Exception as e:
                st.info("📸 Photo non disponible")
                print(f"Erreur: {e}")
        
        st.markdown("---")
        
        # Reste du contenu
        add_floating_chat_to_app()
        
        # Points clés
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            ### ✨ Points Clés
            - 📊 Goût pour les mathématiques
            - 🤝 Expérience du travail d'équipe
            - 💡 Autodidacte
            - 🚀 Motivation à toute épreuve
            """)
        with col2:
            st.info("""
            ### 🎓 Formation Actuelle
            - 📚 DAEU B en cours
            - 💻 Certifications Python
            - 🔍 École 42 - La Piscine
            - 🌟 Excellents résultats en sciences
            """)
            
        st.markdown("---")
        
        # Titre de la lettre de motivation avec icône
        st.markdown("""
            <h2 style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin: 1rem 0;
                line-height: 1.2;
            ">
                📜 Ma Lettre de Motivation
            </h2>
        """, unsafe_allow_html=True)
        
        # Contenu de la lettre et note
        st.markdown(get_lettre_motivation_content())
        st.markdown(get_note_importante(), unsafe_allow_html=True)

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
        display_parcoursup_analysis(show_title=False)  # Ajout du paramètre pour éviter le doublon
    
    # Footer
    st.markdown("---")
    st.markdown("*Application interactive créée pour accompagner ma candidature au BUT Science des Données*")

if __name__ == "__main__":
    main()