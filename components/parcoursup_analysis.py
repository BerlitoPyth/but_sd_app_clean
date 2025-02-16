import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
from components.admission_prediction import display_prediction_interface

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
    """Charger et transformer les données Parcoursup depuis le fichier JSON"""
    try:  # Correction : remplacement de { par :
        # Charger le fichier JSON
        data_path = Path(__file__).parent.parent / ".data" / "parcoursup.json"
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Créer un DataFrame à partir des résultats JSON
        df = pd.DataFrame(data['results'])
        
        # Créer DataFrame avec les colonnes nécessaires
        df_clean = pd.DataFrame()
        df_clean['etablissement'] = df['g_ea_lib_vx']
        df_clean['region'] = df['region_etab_aff']
        df_clean['ville'] = df['ville_etab']
        df_clean['formation'] = df['lib_for_voe_ins']
        df_clean['capacite'] = df['capa_fin']
        df_clean['nb_candidats'] = df['voe_tot']
        df_clean['nb_admis'] = df['acc_tot']
        df_clean['nb_candidates'] = df['voe_tot_f']
        df_clean['taux_acces'] = df['taux_acces_ens']
        df_clean['pct_neo_bac'] = df['pct_neobac']
        df_clean['pct_femmes'] = (df_clean['nb_candidates'] / df_clean['nb_candidats'] * 100).round(1)
        df_clean['taux_pression'] = (df_clean['nb_candidats'] / df_clean['capacite']).round(1)
        
        return df_clean
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        print("Erreur détaillée:", e)
        return None

def display_parcoursup_analysis(show_title=True):
    """
    Affiche l'analyse des données Parcoursup
    :param show_title: Boolean pour contrôler l'affichage du titre
    """
    # Ne pas afficher le titre si show_title est False
    if show_title:
        st.markdown("""
            <h1 style="
                margin-top: 0 !important;
                padding-top: 0 !important;
                margin-bottom: 1.5rem !important;
            ">📊 Analyse des données Parcoursup 2024 - BUT Science des données</h1>
        """, unsafe_allow_html=True)
    
    # Chargement des données
    df = load_parcoursup_data()
    if df is None:
        return

    # Configuration des couleurs avec un meilleur contraste
    colors = {
        'primary': '#1976D2',      # Bleu principal plus foncé
        'secondary': '#2E7D32',    # Vert plus foncé
        'accent': '#F57C00',       # Orange plus foncé
        'card1_bg': '#1565C0',     # Bleu foncé pour le fond
        'card2_bg': '#2E7D32',     # Vert foncé pour le fond
        'card3_bg': '#EF6C00',     # Orange foncé pour le fond
        'card1_text': '#FFFFFF',   # Texte blanc
        'card2_text': '#FFFFFF',   # Texte blanc
        'card3_text': '#FFFFFF'    # Texte blanc
    }

    # Statistiques globales dans des cartes colorées
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div style='background-color: {colors['card1_bg']}; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
                <h3 style='color: {colors['card1_text']}; margin: 0;'>Capacité totale</h3>
                <p style='color: {colors['card1_text']}; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {df['capacite'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='background-color: {colors['card2_bg']}; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
                <h3 style='color: {colors['card2_text']}; margin: 0;'>Total candidatures</h3>
                <p style='color: {colors['card2_text']}; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {df['nb_candidats'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style='background-color: {colors['card3_bg']}; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
                <h3 style='color: {colors['card3_text']}; margin: 0;'>Total admis</h3>
                <p style='color: {colors['card3_text']}; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {df['nb_admis'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Graphique de comparaison avec texte noir
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['etablissement'],
        y=df['nb_candidats'],
        name='Candidatures',
        marker_color=colors['primary']
    ))
    
    fig.add_trace(go.Bar(
        x=df['etablissement'],
        y=df['capacite'],
        name='Capacité',
        marker_color=colors['secondary']
    ))
    
    fig.add_trace(go.Bar(
        x=df['etablissement'],
        y=df['nb_admis'],
        name='Admis',
        marker_color=colors['accent']
    ))
    
    fig.update_layout(
        barmode='group',
        title={
            'text': 'Comparaison par établissement',
            'font': {'color': 'black', 'size': 16}
        },
        xaxis_tickangle=-45,
        height=600,
        margin=dict(b=100),
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0.02)',
        font=dict(
            color='black',
            size=12
        ),
        legend=dict(
            font=dict(color='black'),
            title=dict(font=dict(color='black'))
        ),
        xaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Tableau détaillé modifié
    st.header("📋 Détails par établissement")
    
    # Formater le tableau avec établissement
    formatted_df = df[[
        'etablissement',
        'ville',
        'region',
        'capacite',
        'nb_candidats',
        'nb_admis',
        'taux_pression',
        'taux_acces',
        'pct_femmes'
    ]].sort_values('nb_candidats', ascending=False)
    
    st.dataframe(
        formatted_df.style.format({
            'capacite': '{:,.0f}',
            'nb_candidats': '{:,.0f}',
            'nb_admis': '{:,.0f}',
            'taux_pression': '{:.1f}',
            'taux_acces': '{:.1f}%',
            'pct_femmes': '{:.1f}%'
        }),
        use_container_width=True
    )

    # Carte des établissements avec zoom ajusté
    st.header("🗺️ Répartition géographique")
    
    # Extraire les coordonnées des établissements depuis le JSON
    locations_df = pd.DataFrame()
    with open(Path(__file__).parent.parent / ".data" / "parcoursup.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        locations = []
        for item in data['results']:
            if 'g_olocalisation_des_formations' in item:
                locations.append({
                    'etablissement': item['g_ea_lib_vx'],
                    'lat': item['g_olocalisation_des_formations']['lat'],
                    'lon': item['g_olocalisation_des_formations']['lon'],
                    'capacite': item['capa_fin']
                })
        locations_df = pd.DataFrame(locations)
    
    if not locations_df.empty:
        fig = px.scatter_mapbox(
            locations_df,
            lat='lat',
            lon='lon',
            hover_name='etablissement',
            size='capacite',
            color_discrete_sequence=[colors['primary']],
            zoom=4.5,  # Zoom ajusté pour voir toute la France
            center={"lat": 46.8, "lon": 2.2},
            mapbox_style='carto-positron'
        )
        fig.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                bearing=0,
                pitch=0
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    # Ajout de la nouvelle section de prédiction
    st.markdown("---")
    st.header("🎯 Prédiction d'admission")
    
    # Ajout d'un expander pour les explications
    with st.expander("ℹ️ Comment fonctionne la prédiction ?"):
        st.markdown("""
        Le calcul des chances d'admission est basé sur 3 facteurs principaux pondérés :

        1. **Profil du candidat (40%)**
        - Correspondance avec les profils historiquement admis
        - Répartition typique : ~70% Bac général, ~20% Bac technologique, ~10% Autres

        2. **Places disponibles (30%)**
        - Nombre de places encore disponibles
        - Ratio par rapport à la capacité totale
        - Taux de pression (nombre de candidats par place)

        3. **Taux d'accès historique (30%)**
        - Statistiques réelles d'admission de l'établissement
        - Taux de conversion candidature → admission

        *Note : Ces statistiques sont basées sur les données officielles Parcoursup 2024*
        """)
    
    # Affichage de l'interface de prédiction
    display_prediction_interface(df)
