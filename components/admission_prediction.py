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
    # Ajouter une gestion d'état pour éviter les recharges infinies
    if 'prediction_state' not in st.session_state:
        st.session_state.prediction_state = {}

    if show_title:
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0;
                padding: 0;
                color: inherit;
            ">📊 Analyse des données Parcoursup 2024 - BUT Science des données</h1>
        """, unsafe_allow_html=True)
    
    # Affichage des statistiques globales
    display_summary_stats(data)
    
    # Ajout des onglets
    tab1, tab2 = st.tabs(["🎯 Prédiction détaillée", "🌍 Comparaison globale"])
    
    with tab1:
        st.markdown("### 🎯 Prédiction des chances d'admission")
        
        # Sélection établissement et profil
        col1, col2 = st.columns(2)
        
        with col1:
            iut_choice = st.selectbox("Choisissez votre IUT cible", data['g_ea_lib_vx'].unique())
            bac_type = st.selectbox("Type de Bac/Diplôme", ["DAEU", "Général", "Technologique"])
        
        with col2:
            mention = st.selectbox("Mention", ["Sans mention", "AB", "B", "TB"])
        
        profile = {
            'bac_type': bac_type,
            'mention': mention,
            'boursier': st.checkbox("Je suis boursier", help="Cochez si vous êtes boursier")
        }

        # Calculate probability using new logic
        probability, stats = calculate_admission_probability(data[data['g_ea_lib_vx'] == iut_choice].iloc[0], profile)
        
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
        st.info(f"""
        **Répartition indicative dans cet IUT :**
        - Bac général : ~70%
        - Bac technologique : ~20%
        - Autres profils : ~10%
        
        **Correspondance de votre profil :**
        - Match type de bac : {stats['profil_match']}%
        - Boost mention : {stats['mention_boost']}%
        - Boost boursier : {stats['boursier_boost']}%
        """)

        # Recommandations
        if probability >= 75:
            st.success("✨ Excellentes chances ! Votre profil correspond parfaitement aux critères d'admission.")
        elif probability >= 50:
            st.info("📈 Bonnes chances d'admission. Candidature cohérente avec le profil recherché.")
        else:
            st.warning("""
            ⚠️ Admission possible mais plus difficile.
            - Préparez bien votre lettre de motivation
            - Mettez en avant vos points forts
            """)

    with tab2:
        display_global_interface(data)

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
    st.title("Calculateur d'admission BUT Science des données")
    
    with st.expander("ℹ️ Comment fonctionne le modèle de prédiction ?"):
        st.markdown("""
        ### Modèle de calcul des chances d'admission

        Le calculateur utilise un modèle basé sur les données réelles Parcoursup 2024 qui combine trois facteurs principaux :

        #### 1. Taux de base par type de Bac (facteur principal)
        - Calculé à partir des statistiques réelles de chaque IUT
        - Utilise le ratio : `nombre d'admis du même bac / nombre de candidats du même bac`
        - Prend en compte :
            * Pour Bac général : `acc_bg / nb_voe_pp_bg`
            * Pour Bac technologique : `acc_bt / nb_voe_pp_bt`
            * Pour autres profils : `acc_at / nb_voe_pp_at`

        #### 2. Bonus Mention au Bac
        Multiplicateur appliqué selon la mention :
        - Sans mention : ×1.0 (pas de bonus)
        - Assez Bien : ×1.3 (+30%)
        - Bien : ×1.6 (+60%)
        - Très Bien : ×2.0 (+100%)

        #### 3. Bonus Boursier
        - Bonus minimum de 10% pour tous les boursiers
        - Bonus supplémentaire basé sur le taux de boursiers admis dans l'IUT
        - Formule : `1 + max(0.1, taux_boursiers_iut)`

        #### Calcul final
        ```
        Chances = Taux_base × Bonus_mention × Bonus_boursier
        ```

        #### Ajustements
        - Les chances sont plafonnées à 100%
        - Un minimum de 1% est garanti si le taux de base est non nul
        - Prise en compte du taux de conversion proposition → admission

        #### Exemple
        Pour un candidat avec :
        - Bac général (taux de base 40%)
        - Mention Bien (×1.6)
        - Boursier dans un IUT avec 15% de boursiers (×1.15)
        
        Le calcul serait : `40% × 1.6 × 1.15 = 73.6%`

        #### Fiabilité
        Les prédictions sont basées sur les données réelles Parcoursup 2024 mais restent indicatives. 
        De nombreux facteurs qualitatifs (lettre de motivation, parcours spécifique, etc.) ne sont pas pris en compte.
        """)
    
    # Chargement des données
    df = load_data()
    if df is not None:
        tab1, tab2 = st.tabs(["Prédiction détaillée", "Comparaison globale"])
        
        with tab1:
            display_prediction_interface(df)
        
        with tab2:
            display_global_interface(df)

if __name__ == "__main__":
    main()
