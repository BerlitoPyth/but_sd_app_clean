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
            font-size: 2em;
            letter-spacing: 4px;
            margin-bottom: 1em;
            text-shadow: 0 0 10px #0f0;
        }
        
        .message-text {
            font-size: 1.5em;
            color: #fff;
            text-shadow: 0 0 10px #0f0;
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

    # Création de l'animation
    for i in range(3):  # 3 vagues de colonnes
        rain_columns = ''.join([create_rain_column(j) for j in range(50)])  # 50 colonnes par vague
        
        loading_container.markdown(f"""
            <div class="matrix-animation">
                <div class="matrix-rain">{rain_columns}</div>
                <div class="message-container">
                    <div class="binary-stream">{"".join(random.choice("01") for _ in range(20))}</div>
                    <div class="message-text">{"Initialisation de la Matrice..." if i < 2 else "Bienvenue dans la Matrice 🚀"}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)

    time.sleep(1.5)
    loading_container.empty()