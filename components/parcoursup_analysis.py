import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_parcoursup_data():
    """Charger les données Parcoursup"""
    try:
        # Remplacer par le chemin de votre fichier de données
        df = pd.read_csv(".data/parcoursup_2024.csv")
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return None

def display_parcoursup_analysis():
    """Afficher l'analyse des données Parcoursup"""
    st.title("📊 Analyse des données Parcoursup 2024")
    
    # Chargement des données
    df = load_parcoursup_data()
    if df is None:
        return
    
    # Filtres et sélections
    st.sidebar.markdown("### 🔍 Filtres")
    formation_type = st.sidebar.multiselect(
        "Type de formation",
        df['type_formation'].unique()
    )
    
    # Statistiques générales
    st.header("📈 Statistiques générales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Nombre total de candidatures",
            df['nb_candidatures'].sum()
        )
    
    with col2:
        st.metric(
            "Taux d'admission moyen",
            f"{(df['taux_admission'].mean()):.2f}%"
        )
    
    with col3:
        st.metric(
            "Nombre de formations",
            len(df)
        )
    
    # Visualisations
    st.header("📊 Visualisations")
    
    # Graphique 1: Distribution des candidatures par type de formation
    fig1 = px.histogram(
        df,
        x='type_formation',
        y='nb_candidatures',
        title='Distribution des candidatures par type de formation',
        labels={'type_formation': 'Type de formation', 'nb_candidatures': 'Nombre de candidatures'}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Graphique 2: Taux d'admission par région
    fig2 = px.box(
        df,
        x='region',
        y='taux_admission',
        title='Taux d\'admission par région',
        labels={'region': 'Région', 'taux_admission': 'Taux d\'admission (%)'}
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Analyse prédictive
    st.header("🔮 Analyse prédictive")
    st.write("""
    Basé sur les données historiques, nous pouvons estimer les tendances 
    pour les admissions en BUT Science des Données...
    """)
    
    # Ajouter d'autres visualisations et analyses selon vos besoins
