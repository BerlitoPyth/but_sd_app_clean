import streamlit as st
import random
import time

def display_matrix_animation():
    """Animation style Matrix en plein écran avec effet de pluie amélioré"""
    loading_container = st.empty()
    
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
            from { transform: translateY(-100%) translateZ(0); }
            to { transform: translateY(100vh) translateZ(0); }
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

        .rain-char {
            display: block;
            text-align: center;
            animation: binary-flicker 0.5s steps(2) infinite;
        }

        /* Supprimer l'animation glow redondante de .rain-char */
        .matrix-animation {
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: #0f0;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            overflow: hidden;
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
            width: 1em;
            color: #0f0;
            font-size: 1.2em;
            text-shadow: 0 0 2px #0f0;
            white-space: pre;
            opacity: 0.5;
            font-family: monospace;
            animation: rain-fall 10s linear infinite;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            will-change: transform;
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
            color: #ffffff;
            text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
            animation: messageAppear 0.5s ease-out forwards;
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
                #00FF41 0%, 
                #00AA30 50%, 
                #00FF41 100%);
            background-size: 200% 100%;
            animation: 
                loading 9s ease-in-out forwards,  /* Updated duration */
                gradient-shift 1.5s linear infinite;
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
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00FF41;
            border-radius: 5px;
            padding: 15px;
            color: #fff;
            font-size: 1em;
            z-index: 10002;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
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
        </style>
    """, unsafe_allow_html=True)

    def create_binary_rain():
        lines = []
        num_columns = 20
        for i in range(num_columns):
            # Génération des caractères avec délais différents
            column = ''.join([
                f'<span class="rain-char">{random.choice("10")}</span>'
                for _ in range(20)
            ])
            
            left_position = (i * (100 / num_columns))
            lines.append(f'''
            <div class="rain-column" style="
                left: {left_position}%; 
                animation-delay: -{random.uniform(0, 10)}s;
                animation-duration: 10s;
            ">{column}</div>
            ''')
        return ''.join(lines)

    # Créer la pluie une seule fois au début
    initial_rain = create_binary_rain()
    
    # Modifier la fonction create_matrix_animation pour utiliser la pluie existante
    def create_matrix_animation(progress_text, rain_content):
        return f"""
            <div class="matrix-animation">
                <div class="matrix-rain">{rain_content}</div>
                <div class="disclaimer-box">
                    <div class="typing-text part1" style="color: white;">Composition du projet : 16 fichiers Python, 5 CSS, 11 autres.</div>
                    <div class="typing-text part2" style="color: white;">Nombre total de lignes de code : +3 078.</div>
                    <div class="typing-text part3" style="color: white;">Temps de travail estimé : Donnée non disponible.</div>
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
    
    # Utiliser la même pluie pour tous les messages
    for message, delay in zip(messages, delays):
        loading_container.markdown(
            create_matrix_animation(message, initial_rain),
            unsafe_allow_html=True
        )
        time.sleep(delay)

    time.sleep(0.5)  # Court délai final
    loading_container.empty()