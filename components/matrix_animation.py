import streamlit as st
import time

def display_matrix_animation():
    """Version ultra-minimaliste"""
    with st.empty():
        st.markdown("""
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: black;
                color: #00FF41;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: monospace;
                font-size: 2em;
                z-index: 9999;
            ">
                Initialisation...
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)