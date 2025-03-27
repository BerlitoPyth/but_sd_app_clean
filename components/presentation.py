import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

def display_presentation(show_title=True):
    """Affiche la présentation avec photo"""
    try:
        # Get absolute path to image
        image_path = Path(__file__).parent.parent.resolve() / ".assets" / "profile.jpg"
        
        # Create columns for content and photo
        col1, col2 = st.columns([2, 1])
        
        # Display title and introduction text in first column
        with col1:
            st.markdown("""
                <h1 style='
                    color: white;
                    font-size: 2.5rem;
                    margin-top: 1rem;
                    margin-bottom: 1.5rem;
                    background: linear-gradient(90deg, #fff, #00FF41);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    display: inline;
                '>👋 Découvrez mon parcours</h1>
            """, unsafe_allow_html=True)

            # Texte d'introduction dans la même colonne que le titre
            st.markdown("""
                <div style='
                    background: linear-gradient(135deg, rgba(28, 31, 38, 0.8), rgba(40, 44, 52, 0.8));
                    border: 1px solid rgba(0, 255, 65, 0.3);
                    border-radius: 16px;
                    padding: 1.8rem;
                    margin-bottom: 1.5rem;
                    color: #e2e8f0;
                    line-height: 1.8;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                    backdrop-filter: blur(5px);
                '>
                    <p style='margin-bottom: 1rem; font-size: 1.1rem;'>
                        Passionné par la <span style='color: #00FF41; font-weight: 600;'>Data Science</span> et la programmation,
                        j'ai un parcours atypique qui m'a permis de développer une forte capacité d'<span style='color: #00FF41; font-weight: 600;'>adaptation</span> et de <span style='color: #00FF41; font-weight: 600;'>résolution de problèmes</span>.
                    </p>
                    <p style='font-size: 1.1rem;'>
                        Mon expérience de <span style='color: #00FF41; font-weight: 600;'>scaphandrier professionnel</span> m'a appris la rigueur et la gestion du stress,
                        tandis que mes projets personnels démontrent ma capacité à mener un projet de bout en bout avec <span style='color: #00FF41; font-weight: 600;'>créativité</span> et <span style='color: #00FF41; font-weight: 600;'>autonomie</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Display image in second column directly, without container
        with col2:            
            st.image(
                str(image_path),
                width=220,
                use_container_width=False
            )

    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {str(e)}")
        print(f"Full error details: {e}")

    presentation_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body {
                background-color: #0e1117;
                color: #fff;
                font-family: system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 0;
            }

            .profile-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem 0;
            }

            .section-title-container {
                margin: 2rem 0 3rem 0;
                text-align: center;
                position: relative;
            }

            .section-title {
                font-size: 2rem;
                font-weight: 700;
                background: linear-gradient(90deg, #ffffff, #00FF41);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                position: relative;
                display: inline-block;
                margin: 0;
            }

            .section-title::after {
                content: "";
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 3px;
                background: linear-gradient(90deg, #ffffff, #00FF41);
                border-radius: 3px;
            }

            .cards-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2rem;
                margin-top: 2rem;
            }

            @media (max-width: 1200px) {
                .cards-container {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 768px) {
                .cards-container {
                    grid-template-columns: 1fr;
                }
            }

            .card {
                background: linear-gradient(135deg, rgba(28, 31, 38, 0.8), rgba(40, 44, 52, 0.8));
                border-radius: 16px;
                overflow: hidden;
                transition: all 0.3s ease;
                position: relative;
                border: 1px solid rgba(0, 255, 65, 0.1);
                min-height: 250px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                backdrop-filter: blur(5px);
            }

            .card:hover {
                transform: translateY(-8px);
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
                border-color: rgba(0, 255, 65, 0.3);
            }

            .card-header {
                padding: 1.5rem;
                display: flex;
                align-items: center;
                gap: 1rem;
                background: linear-gradient(90deg, rgba(0, 255, 65, 0.1), transparent);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .card-icon {
                width: 2.5rem;
                height: 2.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 12px;
                background: linear-gradient(135deg, rgba(0, 255, 65, 0.2), rgba(0, 255, 65, 0.05));
                font-size: 1.2rem;
                color: #00FF41;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

            .card-title {
                font-size: 1.4rem;
                font-weight: 600;
                color: #fff;
                margin: 0;
            }

            .card-body {
                padding: 1.5rem;
                flex-grow: 1;
            }

            .card-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            .card-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 1rem;
                color: #d1d5db;
                transition: all 0.2s ease;
            }

            .card-item:last-child {
                margin-bottom: 0;
            }

            .card-item:hover {
                color: #fff;
                transform: translateX(4px);
            }

            .card-item-icon {
                color: #00FF41;
                margin-right: 0.75rem;
                margin-top: 0.25rem;
                font-size: 0.7rem;
            }

            .card-item-text {
                line-height: 1.5;
            }

            .badge {
                position: absolute;
                top: -10px;
                right: -10px;
                background: linear-gradient(135deg, #00FF41, #15b330);
                color: #111;
                padding: 0.35rem 0.8rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                transform: rotate(5deg);
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .animate-fade {
                opacity: 0;
                animation: fadeIn 0.5s ease-out forwards;
            }
        </style>
    </head>
    <body>
        <div id="profile-root"></div>
        <script type="text/babel">
            const sections = [
                {
                    icon: "fas fa-user",
                    title: "À propos de moi",
                    items: [
                        "25 ans, originaire du Sud de la France (Saint-Cyprien-66)",
                        "Passionné de technologie et d'innovation",
                        "Amateur de musique classique, particulièrement le piano",
                        "Sportif et ancien champion de pentathlon",
                        "Autodidacte passionné"
                    ]
                },
                {
                    icon: "fas fa-star",
                    title: "Centres d'intérêt",
                    items: [
                        "Exploration de Paris et de sa scène culturelle",
                        "Concerts de musique classique",
                        "Veille technologique",
                        "Sport et bien-être",
                        "Apprentissage constant"
                    ]
                },
                {
                    icon: "fas fa-graduation-cap",
                    title: "Formation en cours",
                    items: [
                        "DAEU B - Équivalent Bac Scientifique",
                        "Spécialisation en Mathématiques",
                        "Excellent niveau académique",
                        "Formations certifiantes en Python",
                        "Veille technologique dans le domaine de la Data Science"
                    ],
                    badge: "En cours"
                },
                {
                    icon: "fas fa-briefcase",
                    title: "Expérience Pro",
                    items: [
                        "Plongeur Scaphandrier en Travaux Publics",
                        "Gestion de projets techniques",
                        "Travail en équipe et sous pression",
                        "Analyse des risques et des besoins",
                        "Communication avec l'équipe et les clients",
                        "Création de solutions numériques"
                    ]
                },
                {
                    icon: "fas fa-award",
                    title: "Points Forts",
                    items: [
                        "Capacité d'adaptation exceptionnelle",
                        "Résolution créative des problèmes",
                        "Rigueur et précision dans le travail",
                        "Détermination et persévérance",
                        "Esprit d'équipe et communication"
                    ]
                },
                {
                    icon: "fas fa-rocket",
                    title: "Ambition",
                    items: [
                        "Me préparer à un Master ou une école d'ingénieur",
                        "Évoluer professionnellement dans un domaine innovant",
                        "Apprendre à utiliser la Data pour concrétiser des projets",
                        "Combiner mathématiques et programmation",
                        "Relever de nouveaux défis stimulants"
                    ]
                }
            ];

            const Card = ({ icon, title, items, badge, delay }) => (
                <div 
                    className="card animate-fade" 
                    style={{ animationDelay: `${delay}s` }}
                >
                    <div className="card-header">
                        <div className="card-icon"><i className={icon}></i></div>
                        <h3 className="card-title">{title}</h3>
                        {badge && <span className="badge">{badge}</span>}
                    </div>
                    <div className="card-body">
                        <ul className="card-list">
                            {items.map((item, i) => (
                                <li key={i} className="card-item">
                                    <span className="card-item-icon">
                                        <i className="fas fa-chevron-right"></i>
                                    </span>
                                    <span className="card-item-text">{item}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            );

            const Profile = () => (
                <div className="profile-container">
                    <div className="section-title-container">
                        <h2 className="section-title animate-fade" style={{ animationDelay: "0.1s" }}>
                            Mes compétences & expériences
                        </h2>
                    </div>
                    
                    <div className="cards-container">
                        {sections.map((section, index) => (
                            <Card 
                                key={index} 
                                {...section} 
                                delay={(index % 3) * 0.1 + 0.2}
                            />
                        ))}
                    </div>
                </div>
            );

            ReactDOM.render(<Profile />, document.getElementById('profile-root'));
        </script>
    </body>
    </html>
    """
    
    # Pour éviter les marges par défaut de Streamlit
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hauteur augmentée pour afficher toutes les cartes complètement
    components.html(presentation_html, height=1300, scrolling=False)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    display_presentation()
