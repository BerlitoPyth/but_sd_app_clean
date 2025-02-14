import streamlit as st
from pathlib import Path

def display_intro_tree():
    # Chargement du CSS spécifique pour le bouton Matrix
    with open(Path(__file__).parent.parent / "styles" / "matrix_button.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # CSS initial et configuration dans une balise style
    st.markdown("""<style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="block-container"] { padding-top: 0rem; padding-bottom: 0rem; }
        .intro-main { margin: -4rem auto 0; padding: 1rem; max-width: 1200px; }
        .intro-title { margin-top: 0 !important; padding-top: 0 !important; }
    </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="intro-main">', unsafe_allow_html=True)
    
    # Colonnes principales avec alignement ajusté
    title_col, info_col = st.columns([3, 1])
    
    # Titre et info-box sur la même ligne
    with title_col:
        st.markdown('<h1 class="intro-title">🎯 Sommaire</h1>', unsafe_allow_html=True)
        
        # Sous-colonnes pour le contenu
        content_cols = st.columns(3)
        with content_cols[0]:
            st.markdown("""
                <div class="menu-section">
                    <h3>🏠 Menu Principal</h3>
                    <div class="menu-item">📝 Lettre motivation</div>
                    <div class="menu-item">🤖 Assistant chat</div>
                </div>
                <div class="menu-section" style="margin-top: 1.5rem;">
                    <h3>👤 Présentation</h3>
                    <div class="menu-item">👤 En savoir plus sur moi</div>
                    <div class="menu-item">💡 Mes compétences</div>
                </div>
            """, unsafe_allow_html=True)
            
        with content_cols[1]:
            st.markdown("""
                <div class="menu-section">
                    <h3>🔧 Projet</h3>
                    <div class="menu-item">🎮 Projet innovant</div>
                    <div class="menu-item">📊 Analyse des données</div>
                </div>
                <div class="menu-section" style="margin-top: 1.5rem;">
                    <h3>✨ Quiz</h3>
                    <div class="menu-item">🎯 Test de compatibilité</div>
                    <div class="menu-item">📈 Match profil</div>
                </div>
            """, unsafe_allow_html=True)

        with content_cols[2]:
            st.markdown("""
                <div class="menu-section">
                    <h3>📊 Data Parcoursup</h3>
                    <div class="menu-item">📈 Analyse données 2024</div>
                    <div class="menu-item">🎓 Statistiques</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="matrix-button-container">', unsafe_allow_html=True)
            if st.button("ENTRER DANS LA MATRICE", key="intro_tree_matrix_button", type="primary"):
                st.session_state.intro_shown = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Info box alignée avec le titre
    with info_col:
        st.markdown("""
            <div class="info-box">
                <h3>💡 Guide</h3>
                <div class="info-item">🎯 Navigation</div>
                <div class="info-item">🌓 Thème</div>
                <div class="info-item">💬 Chat-bot</div>
                <div class="info-item">📝 Lettre de recommandation</div>
                <h3 style="margin-top: 1rem;">⚠️ Disclaimer</h3>
                <p class="info-disclaimer">
                    Cette application a été entièrement conçue et développée par mes soins. 
                    Aucun template n'a été utilisé. Les idées, le design et le code sont originaux, 
                    réalisés avec l'assistance d'outils d'IA comme GitHub Copilot et Claude.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)