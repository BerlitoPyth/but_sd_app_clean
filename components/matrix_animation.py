import streamlit as st
import random
import time

def display_matrix_animation():
    """Animation style Matrix en plein écran avec effet de pluie amélioré"""
    loading_container = st.empty()
    
    st.markdown("""
        <style>
        @keyframes matrix-rain {
            0% {
                transform: translateY(-100%);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh);
                opacity: 0;
            }
        }
        
        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes character-change {
            0%, 95% { content: attr(data-value); }
            96% { content: "1"; }
            97% { content: "0"; }
            98% { content: "1"; }
            99%, 100% { content: attr(data-value); }
        }
        
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
            display: flex;
            justify-content: space-around;
        }
        
        .rain-column {
            display: flex;
            flex-direction: column;
            animation: matrix-rain linear infinite;
            position: absolute;
            top: -100%;
            color: #0f0;
            text-shadow: 0 0 5px #0f0;
            font-size: 1.2em;
            white-space: pre;
        }
        
        .rain-char {
            opacity: 0;
            animation: fade-in 0.1s forwards;
        }
        
        .rain-char::before {
            content: attr(data-value);
            animation: character-change 3s infinite;
        }
        
        .message-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10000;
            text-align: center;
            animation: glow 2s infinite;
        }
        
        .binary-stream {
            font-size: 2.2em;  /* Increased from 2em */
            letter-spacing: 6px;  /* Increased from 4px */
            margin-bottom: 1.2em;
            text-shadow: 0 0 15px #0f0;
            animation: flicker 3s infinite;
        }

        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .message-text {
            font-size: 1.8em;  /* Increased from 1.5em */
            color: #fff;
            text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.8; text-shadow: 0 0 10px #0f0; }
            50% { opacity: 1; text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
            100% { opacity: 0.8; text-shadow: 0 0 10px #0f0; }
        }

        .loading-bar-container {
            position: fixed;
            bottom: 25%;
            left: 50%;
            transform: translateX(-50%);
            width: 400px;  /* Increased from 300px */
            height: 6px;   /* Increased from 4px */
            background: rgba(0, 255, 0, 0.1);
            border-radius: 3px;
            overflow: hidden;
            z-index: 10001;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
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
                loading 8s cubic-bezier(0.1, 0.5, 0.2, 1) forwards,
                gradient-shift 2s linear infinite;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        }
        
        @keyframes loading {
            0% { width: 0%; }
            5% { width: 5%; }
            10% { width: 15%; }
            20% { width: 25%; }
            30% { width: 35%; }
            40% { width: 45%; }
            50% { width: 55%; }
            60% { width: 65%; }
            70% { width: 75%; }
            80% { width: 85%; }
            90% { width: 92%; }
            100% { width: 100%; }
        }

        @keyframes gradient-shift {
            0% { background-position: 0% 0; }
            50% { background-position: -100% 0; }
            100% { background-position: -200% 0; }
        }

        .disclaimer-box {
            position: fixed;
            top: 50%;
            right: 20px;
            width: 300px;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00FF41;
            border-radius: 5px;
            padding: 15px;
            color: #00FF41;
            font-size: 0.8em;
            z-index: 10001;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
        }
        
        .disclaimer-box h4 {
            margin: 0 0 10px 0;
            color: #00FF41;
            font-family: 'Courier New', monospace;
        }
        </style>
    """, unsafe_allow_html=True)

    def create_rain_column(index):
        chars = "10"
        length = random.randint(10, 30)
        delay = random.random() * -20
        duration = random.uniform(1.5, 4)
        left = f"{index * 2}%"
        
        chars_html = ''.join([
            f'<span class="rain-char" data-value="{random.choice(chars)}" '
            f'style="animation-delay: {i * 0.1}s">'
            f'</span>' for i in range(length)
        ])
        
        return f'<div class="rain-column" style="left: {left}; animation-duration: {duration}s; animation-delay: {delay}s">{chars_html}</div>'

    def create_matrix_animation(progress_text):
        return f"""
            <div class="matrix-animation">
                <div class="matrix-rain">{rain_columns}</div>
                <div class="message-container">
                    <div class="binary-stream">{"".join(random.choice("01") for _ in range(20))}</div>
                    <div class="message-text">{progress_text}</div>
                </div>
                <div class="loading-bar-container">
                    <div class="loading-bar"></div>
                </div>
                <div class="disclaimer-box">
                    <h4>⚠️ Disclaimer</h4>
                    <p>Cette application a été entièrement conçue et développée par mes soins.
                    Aucun template n'a été utilisé. Les idées, le design et le code sont originaux,
                    réalisés avec l'assistance d'outils d'IA.</p>
                </div>
            </div>
        """

    # Animation sequence avec temps ajustés
    messages = [
        "Initialisation de la Matrice...",
        "Chargement des données...",
        "Configuration des paramètres...",
        "Activation des protocoles...",
        "Bienvenue dans la Matrice"
    ]
    
    delays = [1.6, 1.6, 1.6, 1.6, 1.6]  # Délais uniformes pour une progression plus fluide
    
    for i, (message, delay) in enumerate(zip(messages, delays)):
        rain_columns = ''.join([create_rain_column(j) for j in range(50)])
        loading_container.markdown(
            create_matrix_animation(message),
            unsafe_allow_html=True
        )
        time.sleep(delay)

    time.sleep(0.5)  # Court délai final
    loading_container.empty()