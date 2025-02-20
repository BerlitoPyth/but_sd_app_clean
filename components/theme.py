import streamlit as st
import sys
from pathlib import Path

# Ajout du chemin absolu au PYTHONPATH
file_path = Path(__file__).resolve()
project_root = file_path.parent.parent
sys.path.append(str(project_root))

__all__ = ['apply_dark_theme']

def apply_dark_theme():
    """Applique le thème sombre à l'application Streamlit."""
    THEME = {
        "bg_color": "#0e1117",
        "text_color": "white",
        "sidebar_bg": "#1a1d23",
        "input_bg": "#25282e",
        "border_color": "white"
    }
    
    css = f"""
    <style>
    /* Styles de base */
    body, .stApp {{
        background-color: {THEME["bg_color"]};
        color: {THEME["text_color"]};
    }}
    
    /* Sidebar et navigation */
    .stSidebar, .stSidebarContent {{
        background-color: {THEME["sidebar_bg"]} !important;
        color: {THEME["text_color"]} !important;
        padding-top: 0 !important;
    }}
    
    /* Menu de navigation */
    div[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNav"] > ul,
    div[data-testid="stSidebarNav"] section {{
        background-color: {THEME["bg_color"]} !important;
    }}

    /* Radio buttons styling */
    .stRadio {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}

    .stRadio > div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}

    .stRadio > div[role="radiogroup"] > label {{
        background-color: {THEME["sidebar_bg"]} !important;
        color: {THEME["text_color"]} !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        height: 38px !important;
        padding: 0 12px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
        width: calc(100% - 24px) !important;  /* Adjust for padding */
        box-sizing: border-box !important;
        min-width: 200px !important;
    }}

    .stRadio > div[role="radiogroup"] > label > div {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .stRadio > div[role="radiogroup"] > label p {{
        margin: 0 !important;
        padding: 0 !important;
        font-size: 0.9rem !important;
        line-height: 1.2 !important;
    }}

    .stRadio > div[role="radiogroup"] > label:hover {{
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(4px);
        background-color: rgba(255, 255, 255, 0.05) !important;
    }}

    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {{
        border-color: rgba(255, 255, 255, 0.4) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }}

    /* Icônes et éléments interactifs */
    button[title="View fullscreen"],
    .modebar-btn,
    button svg {{
        color: {THEME["text_color"]} !important;
        fill: {THEME["text_color"]} !important;
    }}

    /* Chat et suggestions */
    .message-suggestions button,
    [data-testid="stChatMessageSuggestionsButton"] button {{
        background-color: {THEME["sidebar_bg"]} !important;
        color: {THEME["text_color"]} !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
    }}

    /* Espacement sidebar */
    section[data-testid="stSidebar"] .block-container {{
        padding: 1rem !important;
    }}

    /* Ajustement des marges pour le titre de navigation */
    .sidebar .stMarkdown h1 {{
        margin-bottom: 1rem !important;
    }}

    /* Custom Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        padding: 0.5rem 0;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: {THEME["sidebar_bg"]} !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 0 20px;
        font-size: 1.1em;
        font-weight: 500;
        color: {THEME["text_color"]};
        transition: all 0.2s ease;
        min-width: 200px;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        background-color: rgba(255, 255, 255, 0.05) !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        font-weight: 600;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}

    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Dark Theme Demo", layout="wide")
    apply_dark_theme()
    st.title("Démonstration du thème sombre")