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
    print("Imports des composants réussis")
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)

# Import du contenu
from content.lettre_motivation_content import get_lettre_motivation_content, get_note_importante

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
        layout="wide"
    )
    
    # Charger le CSS
    load_css()
    
    # Ajouter l'animation au début
    if 'animation_shown' not in st.session_state:
        display_matrix_animation()
        st.session_state.animation_shown = True
    
    # Afficher le toggle theme après l'animation ou directement si déjà montrée

    # Sidebar
    with st.sidebar:
        # Bouton de thème compact en haut de la sidebar
        col1, col2 = st.columns([4, 1])
        with col2:
            toggle_theme()
        
        st.title("🎯 Navigation")
        st.markdown("---")

        # Menu de navigation
        selection = st.radio(
            "",
            ["🏠 Accueil",
             "✨ Quiz",
             "🔧 Projet",
             "👤 Présentation",
             "📈 Parcours",
             "✉️ Motivation"]
        )
        st.session_state.selection = selection
        # Lettre de recommandation
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

        st.markdown("---")
        st.markdown("### 👤 À propos")
        st.info("""
        🎓 DAEU B en cours
        🤿 Ex-Plongeur Scaphandrier
        💻 Passionné de programmation
        🔢 Amateur de mathématiques
        """)

        st.markdown("---")
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
        # Conteneur principal avec titre et photo
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
                <div style="margin-bottom: 1rem;">
                    <h1 style="
                        font-size: 2em;
                        margin-bottom: 0.5rem;
                        color: inherit;
                    ">Candidature BUT Science des Données</h1>
                    <h2 style="
                        font-size: 1.5em;
                        margin-bottom: 1rem;
                        color: inherit;
                    ">Adrien BERLIAT</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Effet machine à écrire pour la citation
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
        
        # Ajouter le chat ici, après le titre et la photo
        add_floating_chat_to_app()
        
        # Points clés
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            ### ✨ Points Clés
            - 📊 Goût pour les mathématiques et l'informatique
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
        display_presentation()

        st.markdown("---")
        
    elif selection == "🔧 Projet":
        display_project_concept()
        
    elif selection == "✨ Quiz":
        title_html = """
            <div style="
                margin-top: 20px;
                margin-bottom: 30px;
                scroll-margin-top: 60px;
            ">
                <h1 id="quiz-title">Découvrez si nous matchons ! ❤️</h1>
            </div>
        """
        st.markdown(title_html, unsafe_allow_html=True)
        scroll_to_section("quiz-title")
        display_quiz()
        
    elif selection == "📈 Parcours":
        st.markdown('<h1 id="parcours-title" class="custom-title">Mon Parcours</h1>', unsafe_allow_html=True)
        scroll_to_section("parcours-title")


    elif selection == "✉️ Motivation":
        st.markdown('<h1 id="motivation-title" class="custom-title">Ma Motivation</h1>', unsafe_allow_html=True)
        scroll_to_section("motivation-title")

    # Footer
    st.markdown("---")
    st.markdown("*Application interactive créée pour accompagner ma candidature au BUT Science des Données*")

if __name__ == "__main__":
    main()