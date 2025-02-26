import streamlit as st
from pathlib import Path
import base64
from PIL import Image

def display_data_explorer_project():
    """Affiche la présentation du projet Explorateur de Données"""
    
    st.markdown("""
        <h1 style='margin-bottom: 1.5rem;'>📊 Explorateur de Données</h1>
        <p class="subtitle">Une application interactive d'analyse exploratoire de données</p>
    """, unsafe_allow_html=True)
    
    # Présentation du projet
    st.markdown("""
        ## 🎯 Objectif du projet
        
        J'ai conçu cet outil pour faciliter l'analyse exploratoire 
        de données à partir de fichiers CSV et JSON. Elle offre une interface utilisateur intuitive permettant 
        aux utilisateurs, même sans compétences avancées en programmation, d'explorer et de transformer efficacement leurs données.
        
        Cette application vise à simplifier le processus d'exploration et de prétraitement des données, 
        étapes essentielles dans tout projet d'analyse ou de machine learning, en offrant des outils 
        visuels et interactifs accessibles via une interface web.
                
        Jeu de données utilisé : [**"Titanic"**](https://www.kaggle.com/c/titanic/data)

    """)
    
    # Afficher l'image principale
    try:
        image_path = Path(".assets/data_explorer_home.jpg")
        if image_path.exists():
            img = Image.open(image_path)
            # Utilisation du paramètre use_container_width au lieu de use_column_width
            st.image(img, caption="Interface principale de l'Explorateur de Données", use_container_width=True)
        else:
            st.info("📸 Aperçu de l'application non disponible")
    except Exception as e:
        st.warning(f"Impossible de charger l'image: {e}")
    
    # Principales fonctionnalités
    st.markdown("## 🎬 Principales fonctionnalités")
    
    # Onglets pour les vidéos de démo - Ordre modifié
    tabs = st.tabs(["Chargement des données", "Gestion des valeurs manquantes", "Visualisations", 
                   "Transformation des variables", "Analyses statistiques"])
    
    # Mise à jour de l'ordre des vidéos
    video_files = {
        0: ".assets/data_tool_import.mp4",
        1: ".assets/data_tool_valeurs.mp4",
        2: ".assets/data_tool_visualisation.mp4",
        3: ".assets/data_tool_transform.mp4",
        4: ".assets/data_tool_stats.mp4"
    }
    
    with tabs[0]:
        st.markdown("### 1. Chargement et prévisualisation des données")
        st.markdown("""
            - Importation de fichiers aux formats CSV ou JSON
            - Détection automatique de l'encodage des fichiers
            - Aperçu configurable (tête, queue, échantillon)
            - Informations sur la structure du dataset
        """)
        # Afficher la vidéo si elle existe
        video_path = Path(video_files[0])
        if video_path.exists():
            st.video(video_path)
        else:
            st.info("Vidéo de démonstration non disponible")
    
    with tabs[1]:
        st.markdown("### 2. Gestion des valeurs manquantes")
        st.markdown("""
            - Détection et visualisation des patterns de données manquantes
            - Différentes stratégies de traitement (moyenne, médiane, mode, suppression)
            - Application immédiate des transformations avec prévisualisation
            - Validation et export des données nettoyées
        """)
        # Afficher la vidéo si elle existe
        video_path = Path(video_files[1])
        if video_path.exists():
            st.video(video_path)
        else:
            st.info("Vidéo de démonstration non disponible")
    
    with tabs[2]:
        st.markdown("### 3. Visualisations interactives")
        st.markdown("""
            - Génération automatique d'histogrammes pour toutes les variables numériques
            - Création de matrices de corrélation avec code couleur
            - Visualisation des valeurs manquantes et leur distribution
            - Graphiques personnalisables et exportables
        """)
        # Afficher la vidéo si elle existe
        video_path = Path(video_files[2])
        if video_path.exists():
            st.video(video_path)
        else:
            st.info("Vidéo de démonstration non disponible")
    
    with tabs[3]:
        st.markdown("### 4. Transformation des variables")
        st.markdown("""
            - Encodage des variables catégorielles (binaire, one-hot, ordinal)
            - Conversion de variables textuelles en variables numériques
            - Normalisation des données (min-max, z-score)
            - Prévisualisation des résultats
        """)
        # Afficher la vidéo si elle existe
        video_path = Path(video_files[3])
        if video_path.exists():
            st.video(video_path)
        else:
            st.info("Vidéo de démonstration non disponible")
    
    with tabs[4]:
        st.markdown("### 5. Analyses statistiques descriptives")
        st.markdown("""
            - Calcul automatique des statistiques de base (moyenne, médiane, écart-type)
            - Affichage détaillé des distributions pour variables numériques et catégorielles
            - Visualisation par colonnes avec des box plots et des histogrammes
            - Identification des tendances et anomalies
        """)
        # Afficher la vidéo si elle existe
        video_path = Path(video_files[4])
        if video_path.exists():
            st.video(video_path)
        else:
            st.info("Vidéo de démonstration non disponible")
    
    # Technologies utilisées
    st.markdown("""
        ## 🛠️ Technologies utilisées
        
        Cette application s'appuie sur plusieurs technologies modernes en science des données :
    """)
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    with tech_col1:
        st.info("### Streamlit\nFramework Python pour applications web interactives")
    with tech_col2:
        st.info("### Pandas\nManipulation et analyse des données")
    with tech_col3:
        st.info("### Plotly\nVisualisations interactives avancées")
    with tech_col4:
        st.info("### NumPy\nCalculs numériques")
    