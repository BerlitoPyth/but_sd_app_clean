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
                    font-size: 2rem;
                    margin-top: 1rem;
                    margin-bottom: 1.5rem;
                '>👋 Découvrez-en plus sur moi !</h1>
            """, unsafe_allow_html=True)

            # Texte d'introduction dans la même colonne que le titre
            st.markdown("""
                <div style='
                    background: rgba(96, 165, 250, 0.1);
                    border: 1px solid rgba(96, 165, 250, 0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;
                    color: #cbd5e1;
                    line-height: 1.6;
                '>
                    <p style='margin-bottom: 1rem;'>
                        Je suis passionné par la Data Science et la programmation,
                         avec un fort attrait pour l'analyse et la résolution de problèmes. 
                        Curieux et rigoureux, j’aime explorer de nouvelles technologies et développer des projets concrets.
                    </p>
                    <p>
                        Je pense que mes réalisations démontrent ma capacité à mener un projet de bout en bout,
                        de l'analyse des besoins à la mise en production, en passant par le développement et le design.
                </div>
            """, unsafe_allow_html=True)
        
        # Display image in second column
        with col2:
            st.image(
                str(image_path),
                width=200,
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
        <style>
            body {
                background-color: #0e1117;
                color: #fff;
                font-family: system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 1rem;
            }

            .profile-container {
                max-width: 1000px;
                margin: 0;
                padding: 0;
            }

            .profile-header {
                display: none;
            }

            .section-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 2rem;
                margin-top: 0;
                padding-top: 0;
            }

            @media (max-width: 1200px) {
                .section-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 768px) {
                .section-grid {
                    grid-template-columns: 1fr;
                }
            }

            .section {
                background-color: #1a1d23;
                border-radius: 12px;
                padding: 1.5rem;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: 1px solid rgba(255, 255, 255, 0.1);
                min-height: 250px;
                display: flex;
                flex-direction: column;
            }

            .section:hover {
                transform: translateY(-4px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                border-color: rgba(96, 165, 250, 0.4);
            }

            .section-header {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
                padding-bottom: 0.75rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .icon {
                width: 1.75rem;
                height: 1.75rem;
                padding: 0.375rem;
                border-radius: 8px;
                background: rgba(96, 165, 250, 0.1);
            }

            .section-title {
                font-size: 1.25rem;
                font-weight: 600;
                color: #fff;
                margin: 0;
            }

            .content-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            .content-item {
                display: flex;
                align-items: center;
                padding: 0.5rem 0;
                color: #cbd5e1;
                transition: all 0.2s ease;
            }

            .content-item::before {
                content: "▹";
                color: #60a5fa;
                margin-right: 0.75rem;
            }

            .content-item:hover {
                color: #fff;
                transform: translateX(4px);
            }

            .badge {
                background: rgba(96, 165, 250, 0.1);
                color: #60a5fa;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                margin-left: auto;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .animate-slide {
                animation: slideIn 0.5s ease-out forwards;
            }

            .profile-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 2rem;
                gap: 2rem;
            }

            .profile-image {
                width: 200px;
                height: 200px;
                border-radius: 12px;
                object-fit: cover;
                border: 2px solid rgba(96, 165, 250, 0.3);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }

            .profile-image:hover {
                transform: scale(1.02);
                border-color: rgba(96, 165, 250, 0.6);
            }
        </style>
    </head>
    <body>
        <div id="profile-root"></div>
        <script type="text/babel">
            const sections = [
                {
                    icon: "👤",
                    title: "À propos de moi",
                    items: [
                        "25 ans, originaire du Sud de la France (Saint-Cyprien-66)",
                        "Passionné de technologie et d'innovation",
                        "Amateur de musique classique, particulièrement le piano",
                        "Sportif et ancien champion de pentathlon"
                    ]
                },
                {
                    icon: "🌟",
                    title: "Centres d'intérêt",
                    items: [
                        "Exploration de Paris et de sa scène culturelle",
                        "Concerts de musique classique",
                        "Veille technologique",
                        "Sport et bien-être"
                    ]
                },
                {
                    icon: "📚",
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
                    icon: "💼",
                    title: "Expérience Professionnelle",
                    items: [
                        "Plongeur Scaphandrier en Travaux Publics",
                        "Gestion de projets techniques",
                        "Travail en équipe et sous pression",
                        "Analyse des risques et des besoins",
                        "Communication avec l'équipe et les clients"
                    ]
                },
                {
                    icon: "🎯",
                    title: "Points Forts",
                    items: [
                        "Capacité d'adaptation",
                        "Résolution des problèmes",
                        "Rigueur et précision dans le travail",
                        "Détermination et persévérance",
                        "Esprit d'équipe"
                    ]
                },
                {
                    icon: "🚀",
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

            const Section = ({ icon, title, items, badge, delay }) => (
                <div 
                    className="section animate-slide" 
                    style={{ animationDelay: `${delay}s` }}
                >
                    <div className="section-header">
                        <span className="icon">{icon}</span>
                        <h3 className="section-title">{title}</h3>
                        {badge && <span className="badge">{badge}</span>}
                    </div>
                    <ul className="content-list">
                        {items.map((item, i) => (
                            <li key={i} className="content-item">
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
            );

            const Profile = () => (
                <div className="profile-container">
                    <div className="section-grid">
                        {sections.map((section, index) => (
                            <Section 
                                key={index} 
                                {...section} 
                                delay={index * 0.1}
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
    
    # Modifiez la dernière ligne de la fonction display_presentation
    components.html(presentation_html, height=1200, scrolling=False)  # Increased height from 900 to 1200

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    display_presentation()
