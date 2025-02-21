import streamlit as st
import random
import time

def display_matrix_animation():
    """Animation style Matrix en plein écran avec effet de pluie amélioré"""
    # Créer un conteneur vide avec une div de masquage
    loading_container = st.empty()
    loading_container.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: black;
            z-index: 99999;
        "></div>
    """, unsafe_allow_html=True)
    
    # Attendre un court instant pour s'assurer que le CSS est chargé
    time.sleep(0.1)
    
    st.markdown("""
        <style>
        /* Garder uniquement une animation pour le changement binaire */
        @keyframes binary-flicker {
            0% { content: "1"; }
            33% { content: "0"; }
            66% { content: "1"; }
            100% { content: "0"; }
        }

        @keyframes rain-fall {
            from { transform: translateY(-100%); }
            to { transform: translateY(100vh); }
        }

        /* Combine les effets de lueur en une seule animation */
        @keyframes glow {
            from {
                text-shadow: 0 0 2px #0f0;
                opacity: 0.4;
            }
            to {
                text-shadow: 0 0 3px #0f0;
                opacity: 0.6;
            }
        }

        /* Modifier les animations pour les caractères qui tombent */
        @keyframes binary-change {
            0%, 100% { content: "1"; }
            50% { content: "0"; }
        }

        .rain-char {
            display: block;
            text-align: center;
            color: #00FF41;
            opacity: 0.8;
            text-shadow: 0 0 2px #0f0;
            transition: transform 0.3s ease;
            font-family: 'Share Tech Mono', monospace;
        }

        /* Ajouter une animation d'apparition progressive */
        @keyframes fade-in-out {
            0% { opacity: 0; }
            50% { opacity: 0.8; }
            100% { opacity: 0; }
        }

        .matrix-animation {
            font-family: 'Courier New', monospace;
            background-color: rgba(0, 0, 0, 0.95);
            color: #0f0;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            overflow: hidden;
            will-change: opacity;
        }
        
        .matrix-rain {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
        }
        
        .rain-column {
            position: absolute;
            width: 1.5em;  /* Augmenté pour les caractères japonais */
            color: #0f0;
            font-size: 1.2em;
            text-shadow: 0 0 2px #0f0;
            white-space: pre;
            opacity: 0.5;
            font-family: 'Share Tech Mono', monospace;
            animation: rain-fall 8s linear infinite;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            will-change: transform;
        }

        .rain-char {
            animation: 
                binary-change 1s steps(1) infinite,
                fade-in-out 4s ease-in-out infinite;
            transition: all 0.3s ease;
        }

        /* Supprimer l'animation glow redondante du message-container */
        .message-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10000;
            text-align: center;
        }
        
        .message-text {
            font-size: 2em;
            text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
            animation: messageAppear 0.5s ease-out forwards, glow-pulse 2s infinite;
            background: linear-gradient(90deg, #ffffff 0%, #00FF41 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            opacity: 0;
            font-weight: 800;
            letter-spacing: 1.2px;
        }

        @keyframes messageAppear {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .loading-bar-container {
            position: fixed;
            bottom: 35%;  /* Changed from 25% to 35% */
            left: 50%;
            transform: translateX(-50%);
            width: 400px;
            height: 6px;
            background: rgba(0, 255, 0, 0.1);
            border-radius: 3px;
            overflow: hidden;
            z-index: 10001;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }
        
        @keyframes loading {
            0% { 
                width: 0%;
                opacity: 0.8;
            }
            5% {
                opacity: 1;
            }
            95% {
                opacity: 1;
            }
            100% { 
                width: 100%;
                opacity: 0.8;
            }
        }

        .loading-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, 
                #00FF41, 
                #32CD32);
            background-size: 200% 100%;
            animation: 
                loading 9s ease-in-out forwards,
                gradient-shift 2s linear infinite;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 0; }
            50% { background-position: -100% 0; }
            100% { background-position: -200% 0; }
        }

        .disclaimer-box {
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid transparent;
            border-radius: 5px;
            padding: 15px;
            color: #fff;
            font-size: 1.2em;  /* Increased from 1em */
            font-family: 'Share Tech Mono', 'Courier New', monospace;
            z-index: 10002;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
            backdrop-filter: blur(5px);
            animation: glow-border 4s infinite;
        }

        .typing-text {
            display: block;
            overflow: hidden;
            white-space: nowrap;
            width: 0;
            opacity: 1;
            margin-bottom: 0.5em;
        }

        .typing-text.part1 {
            border-right: 3px solid #ffffff;
            animation: 
                typing 1.5s steps(40) 1s forwards,         /* Réduit de 2s à 1.5s */
                blink-caret 0.75s step-end infinite 1s,
                hide-caret 0s linear 3s forwards;          /* Ajusté à 3s */
        }

        .typing-text.part2 {
            border-right: 3px solid #ffffff;
            animation: 
                typing 1.5s steps(40) 3.5s forwards,       /* Réduit de 2s à 1.5s */
                blink-caret 0.75s step-end infinite 3.5s,
                hide-caret 0s linear 5.5s forwards;        /* Ajusté à 5.5s */
        }

        .typing-text.part3 {
            border-right: 3px solid #ffffff;
            animation: 
                typing 1.5s steps(40) 6s forwards,         /* Réduit de 2s à 1.5s */
                blink-caret 0.75s step-end infinite 6s,
                hide-caret 0s linear 8s forwards;          /* Ajusté à 8s */
        }

        /* Ajouter cette nouvelle animation pour cacher le curseur */
        @keyframes hide-caret {
            to {
                border-right-color: transparent;
            }
        }

        /* Les autres keyframes restent identiques */
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: #ffffff; }
        }

        /* Nouvelles animations et styles */
        @keyframes glow-pulse {
            0%, 100% { text-shadow: 0 0 5px #0f0, 0 0 10px #0f0; }
            50% { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
        }

        .matrix-animation::before {
            display: none;
        }

        @keyframes glow-border {
            0%, 100% { border-color: #00FF41; }
            50% { border-color: #98FB98; }
        }

        .tech-stack-container {
            position: fixed;
            bottom: 30%;  /* Déplacé sous la barre de chargement */
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            text-align: center;
            z-index: 10001;
            font-family: 'Share Tech Mono', monospace;
        }

        .tech-item {
            display: inline-block;
            margin: 0 10px;
            color: #ffffff;  /* Changé en blanc */
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            opacity: 0;
            animation: techAppear 0.5s ease-out forwards;
        }

        @keyframes techAppear {
            from { 
                opacity: 0;
                transform: translateY(20px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
    """, unsafe_allow_html=True)

    def create_binary_rain():
        """Version optimisée de la pluie matricielle avec symboles japonais"""
        # Mélange de chiffres et caractères japonais simples
        characters = "10あめアメ天雨"  # Nombres + symboles japonais pour 'pluie' et 'ciel'
        lines = []
        num_columns = 20  # Réduit pour performance
        
        for i in range(num_columns):
            # Création de la colonne avec rotation
            column = ''.join([
                f'''<span class="rain-char" style="
                    transform: rotate({random.choice([-30, 0, 30])}deg);
                    animation-delay: {random.uniform(0, 2)}s;
                ">{random.choice(characters)}</span>'''
                for _ in range(15)  # Moins de caractères par colonne
            ])
            
            left_position = (i * (100 / num_columns))
            speed = random.uniform(6, 10)
            
            lines.append(f'''
            <div class="rain-column" style="
                left: {left_position}%; 
                animation: rain-fall {speed}s linear infinite;
                animation-delay: -{random.uniform(0, 3)}s;
            ">{column}</div>
            ''')
        return ''.join(lines)

    # Créer la pluie une seule fois au début
    initial_rain = create_binary_rain()
    
    # Modifier la fonction create_matrix_animation pour utiliser la pluie existante
    def create_matrix_animation(progress_text, rain_content, tech_index=0):
        technologies = [
            "Streamlit", "Pandas", "Numpy", "Plotly", 
            "PIL", "Pathlib", "JSON", "Random", "Time"
        ]
        
        tech_items = "".join([
            f'<span class="tech-item" style="animation-delay: {i * 0.1}s">{tech}</span>'
            for i, tech in enumerate(technologies[:tech_index])
        ])
        
        return f"""
            <div class="matrix-animation">
                <div class="matrix-rain">{rain_content}</div>
                <div class="disclaimer-box">
                    <div class="typing-text part1" style="color: white;">Composition du projet<span style="color: #00FF41;">:</span> <strong>16 fichiers Python, 5 CSS, 11 autres</strong></div>
                    <div class="typing-text part2" style="color: white;">Nombre total de lignes de code<span style="color: #00FF41;">:</span> <strong>> 3 100</strong></div>
                    <div class="typing-text part3" style="color: white;">Temps de travail estimé<span style="color: #00FF41;">:</span> <strong>Erreur 404</strong></div>
                </div>
                <div class="tech-stack-container">
                    {tech_items}
                </div>
                <div class="message-container">
                    <div class="message-text">{progress_text}</div>
                </div>
                <div class="loading-bar-container">
                    <div class="loading-bar" style="animation: loading 9s ease-in-out forwards, gradient-shift 1.5s linear infinite;"></div>
                </div>
            </div>
        """

    # Messages et délais
    messages = [
        "Initialisation de la Matrice...",
        "Chargement des données...",
        "Configuration des paramètres...",
        "Activation des protocoles...",
        "Bienvenue dans la Matrice"
    ]
    
    delays = [2.0, 1.75, 1.75, 1.75, 1.75]  # Total: 9s
    tech_count = [2, 4, 6, 7, 9]  # Ajusté pour le nombre réel de technologies
    
    # Utiliser la même pluie pour tous les messages
    for message, delay, tech_index in zip(messages, delays, tech_count):
        loading_container.markdown(
            create_matrix_animation(message, initial_rain, tech_index),
            unsafe_allow_html=True
        )
        time.sleep(delay)

    time.sleep(0.5)  # Court délai final
    loading_container.empty()