import streamlit as st
from pathlib import Path
import base64
from PIL import Image

def display_data_explorer_project():
    """Affiche la présentation des projets professionnels avec un système d'onglets"""
    
    st.markdown("""
        <h1 style='margin-bottom: 1.5rem;'>💼 Mes Projets Professionnels</h1>
    """, unsafe_allow_html=True)
    
    # Onglets principaux pour les projets
    project_tabs = st.tabs(["📊 Explorateur de Données", "🌐 InnovaWeb"])
    
    # Premier onglet : Explorateur de Données
    with project_tabs[0]:
        display_data_explorer()
    
    # Deuxième onglet : InnovaWeb
    with project_tabs[1]:
        display_innovaweb()

def display_data_explorer():
    """Affiche la présentation du projet Explorateur de Données"""
    
    st.markdown("""
        <h2 style='margin-bottom: 1rem;'>📊 Explorateur de Données</h2>
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

def display_innovaweb():
    """Affiche la présentation du projet InnovaWeb - création de sites web"""
    
    st.markdown("""
        <h2 style='margin-bottom: 1rem;'>🌐 InnovaWeb</h2>
        <p class="subtitle">Création de sites web professionnels pour PME</p>
    """, unsafe_allow_html=True)
    
    # Bouton "Visiter le site"
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <a href='https://innovaweb.fr' target='_blank'>
                <button style='
                    background-color: #4696EC;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                '>
                    🔗 Visiter le site
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Genèse du projet
    st.header("💡 Genèse du Projet")
    with st.expander("Découvrir l'origine du projet", expanded=True):
        # Modification du ratio des colonnes pour doubler la taille de la vidéo
        col1, col2 = st.columns([1,1.5])
        with col1:
            st.markdown("""
            En échangeant avec des PME, j'ai identifié un besoin : des sites web 
            professionnels à prix accessibles.
            
            J'ai créé InnovaWeb pour offrir aux petites structures des sites
            optimisés pour convertir les visiteurs en clients.
                        
            - 🔍 **Accessibilité** : Prix abordables
            - 🚀 **Performance** : SEO optimisé
            """)
        with col2:
            try:
                # Utiliser le fichier vidéo innovaweb_home.mp4
                video_path = Path(".assets/innovaweb_home.mp4")
                if video_path.exists():
                    st.video(str(video_path))
                else:
                    st.info("📽️ Vidéo de démonstration non disponible")
            except Exception as e:
                st.warning(f"Impossible de charger la vidéo: {e}")
    
    # NOUVELLE SECTION: Solutions proposées
    st.header("💼 Solutions")
    col1, col2 = st.columns([1, 1.8])  # Ratio modifié pour agrandir l'image
    
    with col1:
        st.markdown("""
        Dans ce projet entrepreneurial, j'ai développé quatre domaines d'expertise :
        
        **🔹 Développement Web**
        - Sites vitrines et e-commerce sur mesure
        - Intégration de réservation et paiement
        
        **🔹 Responsive Design**
        - Adaptation à tous les appareils
        - Expérience utilisateur optimale
        
        **🔹 Design UI/UX**
        - Interfaces modernes et intuitives
        - Optimisation des taux de conversion
        
        **🔹 Performance Web**
        - Optimisation technique
        - SEO et accessibilité
        """)
    
    with col2:
        try:
            # Afficher une image des solutions
            image_path = Path(".assets/innovaweb_solutions.jpg")
            if image_path.exists():
                img = Image.open(image_path)
                st.image(img, caption="Expertise technique", use_container_width=True)
            else:
                st.info("📸 Image non disponible")
        except Exception as e:
            st.warning(f"Impossible de charger l'image: {e}")
    
    # NOUVELLE SECTION: Processus
    st.header("⚙️ Processus")
    col1, col2 = st.columns([1, 1.8])  # Ratio modifié pour agrandir la vidéo
    
    with col1:
        st.markdown("""
        **Méthode en 4 étapes :**
        
        **1️⃣ Écoute & Découverte**
        Analyse des besoins et objectifs du client.
        
        **2️⃣ Proposition & Maquettes**
        Élaboration de concepts visuels.
        
        **3️⃣ Développement & Tests**
        Création du site optimisé.
        
        **4️⃣ Livraison & Formation**
        Formation du client à l'utilisation.
        """)
    
    with col2:
        try:
            # Afficher une vidéo du processus
            video_path = Path(".assets/innovaweb_processus.mp4")
            if video_path.exists():
                st.video(str(video_path))
            else:
                st.info("📽️ Vidéo non disponible")
        except Exception as e:
            st.warning(f"Impossible de charger la vidéo: {e}")
    
    # NOUVELLE SECTION: Avant-Après
    st.header("🔄 Transformations")
    col1, col2 = st.columns([1, 1.8])  # Ratio modifié pour agrandir la vidéo
    
    with col1:
        st.markdown("""
        Les transformations web améliorent :
        
        **🔹 Image de marque**
        - Design moderne et professionnel
        - Cohérence visuelle
        
        **🔹 Performance**
        - Chargement rapide
        - Optimisation pour mobile
        
        **🔹 Conversion**
        - Parcours utilisateur simplifié
        - Appels à l'action efficaces
        """)
    
    with col2:
        try:
            # Afficher une vidéo des transformations
            video_path = Path(".assets/avant_apres.mp4")
            if video_path.exists():
                st.video(str(video_path))
            else:
                st.info("📽️ Vidéo non disponible")
        except Exception as e:
            st.warning(f"Impossible de charger la vidéo: {e}")
    
    # NOUVELLE SECTION: Chatbot Intelligent
    st.header("🤖 Chatbot IA")
    col1, col2 = st.columns([1, 1.8])  # Ratio modifié pour agrandir la vidéo
    
    with col1:
        st.markdown("""
        Le chatbot IA améliore l'expérience sur le site web :
        
        - **Assistant 24/7** : Réponses instantanées
        - **Qualification** : Capture de leads
        - **Multilangue** : Communication globale
        - **Évolutif** : Apprentissage continu
        """)
    
    with col2:
        try:
            # Afficher une vidéo du chatbot
            video_path = Path(".assets/innovaweb_chatbot.mp4")
            if video_path.exists():
                st.video(str(video_path))
            else:
                st.info("📽️ Vidéo non disponible")
        except Exception as e:
            st.warning(f"Impossible de charger la vidéo: {e}")
    