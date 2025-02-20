import streamlit as st
from PIL import Image

def display_project_concept(show_title=True):
    """Affiche les différents projets"""
    
    if show_title:
        st.markdown("""
            <h1 style="
                margin-top: 0 !important;
                padding-top: 0 !important;
                margin-bottom: 1.5rem !important;
            ">🔧 Projets Personnels</h1>
        """, unsafe_allow_html=True)
    
    # Création des tabs
    tab1, tab2 = st.tabs(["🎮 Gaming For All", "🎲 Le Plus Proche Gagne"])
    
    with tab1:
        display_gaming_project()
        
    with tab2:
        display_board_game_project()

def display_gaming_project(show_title=True):
    """
    Affiche le concept du projet
    :param show_title: Boolean pour contrôler l'affichage du titre
    """
        
    # Genèse du projet
    st.header("💡 Genèse du Projet")
    with st.expander("Découvrir l'origine du projet", expanded=True):
        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown("""
            La hausse de popularité du gaming attire de nouveaux joueurs sur PC. En discutant avec des amis me demandant conseils pour acheter un PC, j'ai identifié plusieurs problématiques majeures
            dans le marché du PC Gaming. En effet, certains ont acheté des machines bien trop puissantes pour leurs besoins et déboursé bien plus d'argent que nécessaire,
            tandis que d'autres ont été déçus par les performances de leur ordinateur. Il y a aussi ceux qui ne sont jamais passés à l'acte se disant que les prix étaient inabordables.
                        
            C'est pourquoi j'ai décidé de créer un site web proposant des configurations de PC Gaming adaptées aux besoins réels des clients, avec des recommandations personnalisées
            et des tests de performances transparents pour répondre à ces problématiques.
                        
            - 🤔 **Complexité** : Difficulté pour les non-initiés de choisir un PC adapté à leurs besoins
            - 💰 **Budget** : Surcoût fréquent lié à des composants surdimensionnés
            - 📊 **Performances** : Manque de transparence sur les performances réelles
            - 🔍 **Conseil** : Absence d'accompagnement personnalisé
            """)
        with col2:
            try:
                image = Image.open(".assets/gaming_concept.jpg")
                st.image(image, caption="Concept PC Gaming")
            except:
                st.info("Image non disponible")

    st.header("🎯 Objectifs du Projet")
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("""
        ### 💫 Vision Globale
        - **Démocratiser** le PC Gaming
        - Rendre le gaming PC **accessible à tous**
        - Créer une **expérience d'achat sereine**
        - Offrir un **accompagnement personnalisé**
        """)
    
    with col2:
        st.markdown("""
        ### 💰 Bénéfices Clients
        - **Économies substantielles** sur les configurations
        - **Transparence totale** sur les performances
        - **Confiance** dans son achat
        - **Satisfaction** garantie grâce aux recommandations sur mesure
        """)
    
    st.markdown("""
    <div style='background-color: rgba(70, 150, 236, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #4696EC; margin: 20px 0;'>
        <h3 style='color: #4696EC; margin: 0;'>Ma Mission 🚀</h3>
        <p style='font-size: 18px; margin: 10px 0;'>
            "Permettre à chacun d'accéder au gaming PC en toute confiance, 
            sans compromis sur la qualité et avec la garantie du meilleur rapport qualité/prix"
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Solutions innovantes
    st.header("🚀 Solutions Innovantes")
    
    # Solution 1: Questionnaire intelligent
    st.subheader("📋 Questionnaire Intelligent")
    col1, col2 = st.columns([1,2])  # Changed ratio to match other sections
    with col1:
        st.markdown("""
        - Analyse détaillée des besoins
        - Récuparation de la data
        - Recommandation parfaitement adaptée
        - Interface intuitive
        - Assistant virtuel personnalisé
        - Guide pas à pas interactif
        """)  # Added two items to match other sections' content length
    with col2:
        try:
            video_file = open(".assets/demo_questionnaire.mp4", "rb")
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
        except Exception as e:
            st.info("Démo vidéo non disponible")
            print(f"Erreur: {e}")

    # Solution 2: Configurations Optimisées
    st.subheader("⚡ Configurations Optimisées")
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("""
        - 5 gammes adaptées aux différents besoins
        - Rapport qualité/prix optimisé
        - Performances garanties
        - Compatibilité des composants
        - Évolutivité des configurations
        - Comparaison intuitive des gammes
        """)
    with col2:
        try:
            video_file = open(".assets/demo_configs.mp4", "rb")
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
        except Exception as e:
            st.info("Démo vidéo non disponible")
            print(f"Erreur: {e}")

    # Solution 3: Transparence Totale
    st.subheader("📊 Transparence Totale")
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("""
        - Documentation détaillée des performances
        - Graphiques de performances
        - Vidéos des performances en jeu
        - Tests en conditions réelles
        - Explications techniques claires
        """)
    with col2:
        try:
            video_file = open(".assets/demo_performances.mp4", "rb")
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
        except Exception as e:
            st.info("Démo vidéo non disponible")
            print(f"Erreur: {e}")

    # Solution 4: Guide du Novice
    st.subheader("📚 Guide du Novice")
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("""
        - Explications simples des composants PC
        - Guide des résolutions et FPS
        - Impact des paramètres sur les performances
        - Comprendre ses besoins en Hz/FPS
        - Vocabulaire hardware simplifié
        - Conseils adaptés aux débutants
        """)
    with col2:
        try:
            video_file = open(".assets/demo_guide.mp4", "rb")
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
        except Exception as e:
            st.info("Démo vidéo non disponible")
            print(f"Erreur: {e}")
    
    # Démo du site
    st.header("🌐 Découvrir le Site")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <a href='https://gamingforall.odoo.com/' target='_blank'>
                <button style='
                    background-color: #FF4B4B;
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                '>
                    🔗 Visiter le Site
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Statistiques et résultats
    st.header("📈 Chiffres")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Performances comparées aux PC de grandes enseignes en moyenne", value="+20%", delta="20 FPS")
    with col2:
        st.metric(label="Économie Moyenne", value="210€", delta="par configuration")

def display_board_game_project():
    """Contenu du projet Le Plus Proche Gagne"""
    st.header("🎲 Le Plus Proche Gagne")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            video_file = open(".assets/gameplay_demo.mp4", "rb")
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
        except Exception as e:
            st.markdown("""
                <div style='
                    background: rgba(28, 31, 38, 0.7);
                    border: 1px solid rgba(96, 165, 250, 0.2);
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                    margin: 10px 0;
                '>
                    🎥 Démo du gameplay en cours de production
                </div>
            """, unsafe_allow_html=True)
    with st.expander("En savoir plus", expanded=True):
        st.markdown("""
        ### 💡 Genèse du Projet
        Lors d'une soirée dans un bar à jeux avec ma copine, nous avons découvert un jeu de société 
        nommé "Le Plus Proche Gagne". Nous avons adoré le concept et j'ai décidé de recréer le jeu pour animer nos soirées. Je développe une version en ligne pour jouer à distance.
        
        ### 🏅 Principe du jeu
        Un jeu de culture générale basé sur l'estimation, où le plus proche de la bonne réponse remporte la victoire !

        
        
        ### 🎯 Les 9 thèmes
        - ⚽ L'athlète        
        - 🌍 Le globe-trotteur
        - 🎬 Le fan 
        - 📚 L'érudit
        - 🃏 Le loufoque 
        - 📜 L'historien 
        - 🦁 L'observateur 
        - 👔 Le ministre 
        - 🔬 Le scientifique

        ### 📜 Déroulement
        1. Chaque joueur choisit 3 médailles pour démarrer
        2. Le joueur actif choisit un thème disponible
        3. Une question numérique est posée
        4. Tous les joueurs répondent simultanément
        5. Le plus proche remporte la médaille du thème
        6. Si déjà possédée, la médaille devient sécurisée

        ### 🏆 Victoire
        - La partie se termine quand toutes les médailles sont sécurisées
        - Le joueur avec le plus de médailles l'emporte

        ### ⚡ Avantages
        - Génération illimitée de questions grâce à l'IA
        - Mode en ligne pour jouer à distance
        - Base de données évolutive            
        """)    

    # État du développement
    st.header("📈 État d'avancement")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Questions générées", value="1500+", delta="Base évolutive")
    with col2:
        st.metric(label="Version en ligne", value="60%", delta="En développement")

if __name__ == "__main__":
    st.set_page_config(page_title="Projet PC Gaming", layout="wide")
    display_project_concept()
