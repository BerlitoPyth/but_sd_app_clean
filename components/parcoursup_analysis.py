import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

def clean_and_transform_data(df):
    """Nettoyer et transformer les données"""
    # Sélectionner uniquement les colonnes utiles
    columns_to_keep = [
        'Établissement',
        'Région de l\'établissement',
        'Filière de formation',
        'Capacité de l\'établissement par formation',
        'Effectif total des candidats pour une formation',
        'Effectif total des candidats ayant accepté la proposition de l\'établissement (admis)',
        'Taux d\'accès'
    ]
    df = df[columns_to_keep]
    
    # Renommer les colonnes pour plus de clarté
    df = df.rename(columns={
        'Établissement': 'etablissement',
        'Région de l\'établissement': 'region',
        'Filière de formation': 'formation',
        'Capacité de l\'établissement par formation': 'capacite',
        'Effectif total des candidats pour une formation': 'nb_candidats',
        'Effectif total des candidats ayant accepté la proposition de l\'établissement (admis)': 'nb_admis',
        'Taux d\'accès': 'taux_acces'
    })
    
    # Extraire le type de formation (BUT, BTS, Licence, etc.)
    df['type_formation'] = df['formation'].apply(lambda x: x.split(' ')[0])
    
    # Calculer le taux de pression (nombre de candidats / capacité)
    df['taux_pression'] = df['nb_candidats'] / df['capacite']
    
    return df

def load_parcoursup_data():
    """Charger et préparer les données Parcoursup"""
    try:
        data_path = Path(__file__).parent.parent / ".data" / "parcoursup_2024.csv"
        # Lire le CSV et afficher les colonnes pour debug
        df = pd.read_csv(data_path, sep=';')
        st.write("Colonnes disponibles dans le fichier:", df.columns.tolist())
        st.write("Aperçu des données:", df.head())
        
        # Nettoyer et transformer les données
        df_cleaned = df.copy()
        
        # Simplifier les noms de colonnes
        column_mapping = {
            'Établissement': 'etablissement',
            'Région de l\'établissement': 'region',
            'Filière de formation': 'formation',
            'Capacité de l\'établissement par formation': 'capacite',
            'Effectif total des candidats pour une formation': 'nb_candidats',
            'Effectif total des candidats ayant accepté la proposition de l\'établissement (admis)': 'nb_admis',
            'Taux d\'accès': 'taux_acces'
        }
        
        # Vérifier chaque colonne avant le renommage
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df_cleaned[new_name] = df[old_name]
            else:
                st.warning(f"Colonne manquante: {old_name}")
        
        # Extraire le type de formation
        df_cleaned['type_formation'] = df_cleaned['formation'].str.split(' - ').str[0]
        df_cleaned['type_formation'] = df_cleaned['type_formation'].str.split(' ').str[0]
        
        # Convertir les colonnes numériques
        df_cleaned['capacite'] = pd.to_numeric(df_cleaned['capacite'], errors='coerce')
        df_cleaned['nb_candidats'] = pd.to_numeric(df_cleaned['nb_candidats'], errors='coerce')
        df_cleaned['nb_admis'] = pd.to_numeric(df_cleaned['nb_admis'], errors='coerce')
        df_cleaned['taux_acces'] = pd.to_numeric(df_cleaned['taux_acces'], errors='coerce')
        
        # Calculer le taux de pression
        df_cleaned['taux_pression'] = df_cleaned['nb_candidats'] / df_cleaned['capacite']
        
        return df_cleaned
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        st.write("Chemin du fichier:", data_path)
        return None

def display_parcoursup_analysis():
    """Afficher l'analyse des données Parcoursup"""
    st.title("📊 Analyse des données Parcoursup 2024")
    
    # Chargement des données
    df = load_parcoursup_data()
    if df is None:
        return

    # Filtres dans la sidebar
    st.sidebar.markdown("### 🔍 Filtres")
    
    # Filtre par type de formation
    formation_types = sorted(df['type_formation'].unique())
    selected_types = st.sidebar.multiselect(
        "Type de formation",
        formation_types,
        default=['BUT']  # Par défaut, montrer les BUT
    )
    
    # Filtre par région
    regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Région",
        regions
    )
    
    # Appliquer les filtres
    mask = pd.Series(True, index=df.index)
    if selected_types:
        mask &= df['type_formation'].isin(selected_types)
    if selected_regions:
        mask &= df['region'].isin(selected_regions)
    df_filtered = df[mask]

    # Statistiques générales
    st.header("📈 Statistiques clés")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Nombre de candidats",
            f"{df_filtered['nb_candidats'].sum():,}"
        )
    
    with col2:
        taux_acces_moy = df_filtered['taux_acces'].mean()
        st.metric(
            "Taux d'accès moyen",
            f"{taux_acces_moy:.1f}%"
        )
    
    with col3:
        taux_pression_moy = df_filtered['taux_pression'].mean()
        st.metric(
            "Taux de pression moyen",
            f"{taux_pression_moy:.1f}"
        )

    # Visualisations
    st.header("📊 Visualisations")
    
    # 1. Répartition des candidatures par type de formation
    fig1 = px.bar(
        df_filtered.groupby('type_formation').agg({
            'nb_candidats': 'sum',
            'nb_admis': 'sum'
        }).reset_index(),
        x='type_formation',
        y=['nb_candidats', 'nb_admis'],
        title='Candidatures et admissions par type de formation',
        barmode='group',
        labels={
            'type_formation': 'Type de formation',
            'value': 'Nombre d\'étudiants',
            'variable': 'Type'
        }
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2. Taux d'accès par région
    fig2 = px.box(
        df_filtered,
        x='region',
        y='taux_acces',
        title='Distribution des taux d\'accès par région',
        labels={
            'region': 'Région',
            'taux_acces': 'Taux d\'accès (%)'
        }
    )
    fig2.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 3. Top formations les plus demandées
    st.header("🏆 Formations les plus demandées")
    top_10 = df_filtered.nlargest(10, 'nb_candidats')[
        [
            'formation',
            'etablissement',
            'region',
            'nb_candidats',
            'taux_acces',
            'taux_pression'
        ]
    ].reset_index(drop=True)
    
    st.dataframe(
        top_10.style.format({
            'taux_acces': '{:.1f}%',
            'taux_pression': '{:.1f}'
        }),
        use_container_width=True
    )
