import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

def load_data():
    """Charge les données depuis le fichier JSON avec gestion des chemins"""
    try:
        data_path = Path(__file__).resolve().parent.parent / ".data" / "parcoursup.json"
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return pd.DataFrame(data['results'])
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        print(f"Chemin tenté: {data_path}")
        return None

def calculate_admission_probability(iut_data, profile):
    """Calcule la probabilité d'admission avec la nouvelle formule unifiée"""
    # 1. Calculer le taux de base selon le type de bac
    if profile['bac_type'] == "Général":
        candidats = iut_data['nb_voe_pp_bg']
        admis = iut_data['acc_bg']
    elif profile['bac_type'] == "Technologique":
        candidats = iut_data['nb_voe_pp_bt']
        admis = iut_data['acc_bt']
    else:  # DAEU et autres
        candidats = iut_data['nb_voe_pp_at']
        admis = iut_data['acc_at']
        
    base_rate = (admis / candidats * 100) if candidats > 0 else 0

    # 2. Bonus mention
    mention_bonus = {
        'Sans mention': 1.0,
        'AB': 1.3,
        'B': 1.6,
        'TB': 2.0
    }.get(profile['mention'], 1.0)

    # 3. Bonus boursier amélioré
    boursier_rate = iut_data['pct_bours'] / 100
    boursier_bonus = 1 + max(0.1, boursier_rate) if profile['boursier'] else 1

    # 4. Score final avec ajustements
    probability = base_rate * mention_bonus * boursier_bonus
    
    # Limiter entre 0 et 100
    probability = min(100, max(0, probability))

    # Calculer les statistiques pour l'affichage
    stats = {
        'capacite': iut_data['capa_fin'],
        'places_restantes': iut_data['capa_fin'] - iut_data['acc_tot'],
        'taux_pression': round(iut_data['voe_tot'] / iut_data['capa_fin'], 1),
        'taux_admission': round((iut_data['acc_tot'] / iut_data['voe_tot']) * 100, 1),
        'profil_match': round(base_rate, 1),
        'mention_boost': round((mention_bonus - 1) * 100, 1),
        'boursier_boost': round((boursier_bonus - 1) * 100, 1)
    }
    
    return probability, stats

def calculate_chances(profile, data):
    """Calcule les chances pour tous les établissements avec la formule unifiée"""
    results = []
    for _, iut in data.iterrows():
        # Base rate calculation based on bac type
        if profile['bac_type'] == "Général":
            candidats = iut['nb_voe_pp_bg']
            admis = iut['acc_bg']
        elif profile['bac_type'] == "Technologique":
            candidats = iut['nb_voe_pp_bt']
            admis = iut['acc_bt']
        else:  # DAEU et autres
            candidats = iut['nb_voe_pp_at']
            admis = iut['acc_at']
        
        base_rate = (admis / candidats * 100) if candidats > 0 else 0

        # Mention bonus
        mention_bonus = {
            'Sans mention': 1.0,
            'AB': 1.3,
            'B': 1.6,
            'TB': 2.0
        }.get(profile['mention'], 1.0)

        # Boursier bonus
        boursier_rate = iut['pct_bours'] / 100
        boursier_bonus = 1 + max(0.1, boursier_rate) if profile['boursier'] else 1

        # Final score calculation
        score = base_rate * mention_bonus * boursier_bonus
        score = min(100, max(0, score))

        results.append({
            'etablissement': iut['g_ea_lib_vx'],
            'ville': iut['ville_etab'],
            'region': iut['region_etab_aff'],
            'capacite': iut['capa_fin'],
            'nb_candidats': iut['voe_tot'],
            'chances': round(score, 1),
            'pct_boursiers': iut['pct_bours']
        })
    
    return pd.DataFrame(results).sort_values('chances', ascending=False)

def display_summary_stats(data):
    """Affiche les statistiques globales"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div style='background-color: #1565C0; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #FFFFFF; margin: 0;'>Capacité totale</h3>
                <p style='color: #FFFFFF; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {data['capa_fin'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='background-color: #2E7D32; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #FFFFFF; margin: 0;'>Total candidatures</h3>
                <p style='color: #FFFFFF; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {data['voe_tot'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style='background-color: #EF6C00; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #FFFFFF; margin: 0;'>Total admis</h3>
                <p style='color: #FFFFFF; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {data['acc_tot'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

def display_prediction_interface(data, show_title=True):
    """Interface de prédiction des chances d'admission"""
    # Selection interface
    col1, col2 = st.columns(2)
    
    with col1:
        iut_choice = st.selectbox("Choisissez votre IUT cible", data['g_ea_lib_vx'].unique())
        bac_type = st.selectbox("Type de Bac/Diplôme", ["DAEU", "Général", "Technologique"])
    
    with col2:
        mention = st.selectbox("Mention", ["Sans mention", "AB", "B", "TB"])
        boursier = st.checkbox("Je suis boursier", help="Cochez si vous êtes boursier")

    profile = {
        'bac_type': bac_type,
        'mention': mention,
        'boursier': boursier
    }

    # Get IUT data first
    iut_data = data[data['g_ea_lib_vx'] == iut_choice].iloc[0]
    
    # Calculate probability using new logic
    probability, stats = calculate_admission_probability(iut_data, profile)
    
    # Affichage résultats
    col1, col2 = st.columns(2)
    
    with col1:
        # Jauge de probabilité
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability,
            title={'text': "Probabilité d'admission"},
            gauge={'axis': {'range': [0, 100]},
                  'bar': {'color': "darkblue"},
                  'steps': [
                      {'range': [0, 33], 'color': "lightgray"},
                      {'range': [33, 66], 'color': "gray"},
                      {'range': [66, 100], 'color': "darkgray"}
                  ]}
        ))
        st.plotly_chart(fig)
    
    with col2:
        st.metric("Places disponibles", stats['capacite'])
        st.metric("Places restantes", stats['places_restantes'])
        st.metric("Taux de pression", f"{stats['taux_pression']} candidats/place")
        st.metric("Taux d'admission", f"{stats['taux_admission']}%")
    
    # Analyse détaillée
    st.markdown("""
    <div style='background-color: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: white; margin-top: 0;'>📊 Analyse détaillée de votre candidature</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate percentage distributions
        total_admis = iut_data['acc_bg'] + iut_data['acc_bt'] + iut_data['acc_at']
        pct_bg = round((iut_data['acc_bg'] / total_admis * 100), 1) if total_admis > 0 else 0
        pct_bt = round((iut_data['acc_bt'] / total_admis * 100), 1) if total_admis > 0 else 0
        pct_at = round((iut_data['acc_at'] / total_admis * 100), 1) if total_admis > 0 else 0
        
        st.markdown(f"""
        #### 📈 Statistiques de l'établissement
        - **Répartition des admis :**
          * Bac général : {pct_bg}%
          * Bac technologique : {pct_bt}%
          * Autres profils : {pct_at}%
        
        - **Profil des candidats :**
          * Taux de boursiers : {iut_data['pct_bours']}%
          * Taux de pression : {stats['taux_pression']} candidats/place
        """)
    
    with col2:
        st.markdown(f"""
        #### 🎯 Adéquation de votre profil
        - **Match type de bac :** {stats['profil_match']}%
          * {'✅ Profil recherché' if stats['profil_match'] > 50 else '⚠️ Profil moins représenté'}
        
        - **Bonus acquis :**
          * Mention : +{stats['mention_boost']}%
          * Boursier : +{stats['boursier_boost']}%
        """)

    # Recommandations personnalisées
    st.markdown("<h3 style='color: white; margin-top: 20px;'>🎓 Conseils personnalisés</h3>", unsafe_allow_html=True)
    
    # Calcul du taux moyen d'admission pour contextualiser
    taux_admission_moyen = (iut_data['acc_tot'] / iut_data['voe_tot']) * 100
    
    if probability >= 30:  # Top 15% des candidats
        st.success(f"""
        ### ✨ Profil très compétitif (Top 15%)
        
        **Contexte de sélection :**
        - Taux d'admission moyen : {taux_admission_moyen:.1f}%
        - Formation très sélective : {iut_data['capa_fin']} places pour {iut_data['voe_tot']} candidats
        
        **Points forts de votre dossier :**
        - Votre profil correspond aux critères principaux
        - Vos chances sont supérieures à la moyenne
        
        **Actions prioritaires :**
        1. Préparez un dossier d'excellence :
           * CV détaillé de vos projets et compétences
           * Lettre de motivation ciblée pour chaque IUT
           * Portfolio de vos réalisations techniques
        
        2. Anticipez la formation :
           * Initiez-vous à Python (certifications à l'appui)
           * Renforcez vos bases en mathématiques
           * Suivez des cours en ligne de statistiques
        """)
    elif probability >= 15:  # Dans la moyenne haute
        st.info(f"""
        ### 📊 Candidature compétitive
        
        **Contexte important :**
        - Taux d'admission : {taux_admission_moyen:.1f}%
        - Places disponibles : {iut_data['capa_fin']}
        - Candidats : {iut_data['voe_tot']}
        
        **Stratégie recommandée :**
        1. Renforcez votre dossier :
           * Développez des projets personnels (programmation/data)
           * Obtenez des certifications en ligne
           * Documentez toutes vos réalisations
        
        2. Optimisez vos chances :
           * Candidatez dans plusieurs IUT
           * Adaptez votre lettre pour chaque établissement
           * Préparez-vous aux éventuels entretiens
        """)
    else:  # Chances plus faibles
        st.warning(f"""
        ### ⚠️ Contexte très sélectif
        
        **Statistiques clés :**
        - Taux d'admission : {taux_admission_moyen:.1f}%
        - {iut_data['capa_fin']} places pour {iut_data['voe_tot']} candidats
        - Taux de pression : {stats['taux_pression']} candidats/place
        
        **Plan d'action recommandé :**
        1. Développez votre profil technique :
           * Suivez des cours de programmation (Python)
           * Initiez-vous aux statistiques et à l'analyse de données
           * Créez un portfolio de projets personnels
        
        2. Stratégie de candidature :
           * Visez plusieurs IUT avec des profils différents
           * Préparez des alternatives (BTS SIO, BUT Info...)
           * Considérez une année préparatoire si nécessaire
        
        3. Maximisez vos atouts :
           * Mettez en avant votre motivation et votre potentiel
           * Démontrez votre capacité d'apprentissage
           * Valorisez toute expérience pertinente
        """)

    # Note sur la sélectivité générale
    st.info("""
    💡 **Comprendre la sélectivité :**
    - Le BUT SD est parmi les formations les plus sélectives de Parcoursup
    - Taux d'admission moyen national : 7.2%
    - Même les excellents dossiers doivent se démarquer
    - La motivation et la préparation technique sont déterminantes
    """)

    return iut_choice, probability

def display_global_interface(data):
    """Interface de comparaison globale"""
    st.subheader("Comparer tous les établissements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bac_type = st.selectbox(
            "Type de Bac",
            options=["Général", "Technologique", "DAEU"],
            key="global_bac"
        )
    
    with col2:
        mention = st.selectbox(
            "Mention au Bac",
            options=["Sans mention", "AB", "B", "TB"],
            key="global_mention"
        )
    
    with col3:
        boursier = st.checkbox("Boursier", key="global_boursier")

    profile = {
        'bac_type': bac_type,
        'mention': mention,
        'boursier': boursier
    }
    
    results_df = calculate_chances(profile, data)
    
    # Graphique
    fig = px.bar(
        results_df,
        x='etablissement',
        y='chances',
        title='Chances d\'admission par établissement',
        labels={'chances': 'Chances estimées (%)', 'etablissement': 'Établissement'},
        color='chances',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau détaillé
    st.dataframe(
        results_df.style.format({
            'capacite': '{:,.0f}',
            'nb_candidats': '{:,.0f}',
            'chances': '{:.1f}%',
            'pct_boursiers': '{:.1f}%'
        })
    )

def main():
    """Main function for standalone testing"""
    if __name__ == "__main__":
        st.set_page_config(layout="wide", page_title="Calculateur d'admission BUT SD")
        
        # Load data first
        df = load_data()
        
        if df is not None:
            # Create tabs
            tab1, tab2 = st.tabs(["🎯 Prédiction détaillée", "🌍 Comparaison globale"])
            
            with tab1:
                display_prediction_interface(df, show_title=False)
            
            with tab2:
                display_global_interface(df)

if __name__ == "__main__":
    main()
