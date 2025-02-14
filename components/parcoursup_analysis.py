import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def load_parcoursup_data():
    """Charger les données Parcoursup"""
    try:
        data_path = Path(__file__).parent.parent / ".data" / "parcoursup_2024.csv"
        df = pd.read_csv(data_path, encoding='utf-8', sep=';')
        
        # Renommer les colonnes pour plus de clarté
        df = df.rename(columns={
            'Filière de formation': 'formation',
            'Etablissement': 'etablissement',
            'Région de l\'établissement': 'region',
            'Capacité de l\'établissement par formation': 'capacite',
            'Effectif total des candidats pour une formation': 'nb_candidatures',
            'Effectif total des candidats ayant accepté la proposition de l\'établissement (admis)': 'admis',
            'Taux d\'accès': 'taux_admission'
        })
        
        # Créer une colonne type_formation en extrayant le type depuis la formation
        df['type_formation'] = df['formation'].apply(lambda x: x.split(' - ')[0] if ' - ' in x else x.split(' ')[0])
        
        print("Colonnes disponibles:", df.columns.tolist())
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        print(f"Chemin tenté : {data_path}")
        print(f"Erreur complète : {str(e)}")
        return None

def display_parcoursup_analysis():
    """Afficher l'analyse des données Parcoursup"""
    st.title("📊 Analyse des données Parcoursup 2024")
    
    # Chargement des données
    df = load_parcoursup_data()
    if df is None:
        return
    
    # Filtres
    st.sidebar.markdown("### 🔍 Filtres")
    formation_type = st.sidebar.multiselect(
        "Type de formation",
        sorted(df['type_formation'].unique())
    )
    
    # Filtrer les données si des types de formation sont sélectionnés
    if formation_type:
        df_filtered = df[df['type_formation'].isin(formation_type)]
    else:
        df_filtered = df
    
    # Statistiques générales
    st.header("📈 Statistiques générales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Nombre total de candidatures",
            f"{df_filtered['nb_candidatures'].sum():,}"
        )
    
    with col2:
        taux_moyen = df_filtered['taux_admission'].mean()
        st.metric(
            "Taux d'admission moyen",
            f"{taux_moyen:.1f}%"
        )
    
    with col3:
        st.metric(
            "Nombre de formations",
            len(df_filtered)
        )
    
    # Visualisations
    st.header("📊 Visualisations")
    
    # Graphique 1: Distribution des candidatures par type de formation
    fig1 = px.bar(
        df_filtered.groupby('type_formation')['nb_candidatures'].sum().reset_index(),
        x='type_formation',
        y='nb_candidatures',
        title='Distribution des candidatures par type de formation',
        labels={'type_formation': 'Type de formation', 'nb_candidatures': 'Nombre de candidatures'}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Graphique 2: Taux d'admission par région
    fig2 = px.box(
        df_filtered,
        x='region',
        y='taux_admission',
        title='Taux d\'admission par région',
        labels={'region': 'Région', 'taux_admission': 'Taux d\'admission (%)'}
    )
    fig2.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Top 10 des formations les plus demandées
    st.header("🏆 Top 10 des formations les plus demandées")
    top_10 = df_filtered.nlargest(10, 'nb_candidatures')[['formation', 'etablissement', 'nb_candidatures', 'taux_admission']]
    st.dataframe(top_10)
    
    # Analyse prédictive
    st.header("🔮 Analyse prédictive")
    st.write("""
    Basé sur les données historiques, nous pouvons estimer les tendances 
    pour les admissions en BUT Science des Données...
    """)
    
    # Ajouter d'autres visualisations et analyses selon vos besoins
