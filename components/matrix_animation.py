import streamlit as st
import random
import time

def display_matrix_animation():
    """Animation style Matrix en plein écran"""
    loading_container = st.empty()
    
    # Style CSS Matrix
    st.markdown("""
        <style>
        @keyframes matrix-rain {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        
        @keyframes glow {
            0% { text-shadow: 0 0 5px #0f0; }
            50% { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
            100% { text-shadow: 0 0 5px #0f0; }
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
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        
        .binary-stream {
            font-size: 16px;
            letter-spacing: 4px;
            animation: glow 2s infinite;
            opacity: 0.8;
            position: relative;
            z-index: 2;
        }
        
        .message-text {
            font-size: 24px;
            margin: 20px 0;
            color: #fff;
            text-shadow: 0 0 10px #0f0;
            animation: glow 1.5s infinite;
            position: relative;
            z-index: 2;
        }
        
        .matrix-rain {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            opacity: 0.3;
            pointer-events: none;
            z-index: 1;
        }
        
        .rain-column {
            animation: matrix-rain 2s linear infinite;
            animation-delay: var(--delay);
        }
        </style>
    """, unsafe_allow_html=True)

    matrix_chars = "01"
    rain_columns = 50
    
    for i in range(50):
        binary = ''.join(random.choice(matrix_chars) for _ in range(40))
        rain_html = ''.join([
            f'<div class="rain-column" style="--delay: {random.random() * 2}s">{binary}</div>'
            for _ in range(rain_columns)
        ])
        
        loading_container.markdown(f"""
            <div class="matrix-animation">
                <div class="matrix-rain">{rain_html}</div>
                <div class="binary-stream">{binary[:int(i/50*len(binary))]}▌</div>
                <div class="message-text">📊 Initialisation de la Matrice...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)
    
    time.sleep(0.5)
    
    loading_container.markdown(f"""
        <div class="matrix-animation">
            <div class="matrix-rain">{rain_html}</div>
            <div class="binary-stream">{binary}</div>
            <div class="message-text">🚀 Bienvenue dans la Matrice. Merci pour le temps que vous m'accordez.</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.5)
    loading_container.empty()