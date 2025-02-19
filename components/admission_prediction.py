import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
            
def display_profil_feedback(probability):
    """Affiche les recommandations basées sur le profil avec un style amélioré"""
    try:
        probability = float(probability)
        
        if probability >= 30:
            st.markdown("""
                <div style='background: linear-gradient(90deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%); 
                     border: 1px solid rgba(76, 175, 80, 0.3); 
                     border-radius: 10px; 
                     padding: 20px; 
                     margin: 10px 0;'>
                    <h3 style='color: #4CAF50; margin-bottom: 20px; font-size: 1.5em; font-weight: bold;'>
                        ✨ Profil compétitif
                    </h3>
                    <div style='background: rgba(76, 175, 80, 0.05); 
                         border-radius: 8px; 
                         padding: 15px; 
                         margin-bottom: 20px;'>
                        <h4 style='color: #4CAF50; margin-bottom: 10px; font-size: 1.1em; font-weight: bold;'>
                            💪 Points forts
                        </h4>
                        <ul style='list-style-type: none; margin: 0; padding: 0; color: white;'>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #4CAF50'>✓</span> Votre profil correspond bien aux critères de sélection de cet IUT
                            </li>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #4CAF50'>✓</span> Vous avez de bonnes chances d'obtenir une proposition
                            </li>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #4CAF50'>✓</span> Continuez à maintenir votre niveau et préparez bien votre dossier
                            </li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: rgba(255, 167, 38, 0.1); 
                     border: 1px solid rgba(255, 167, 38, 0.3); 
                     border-radius: 10px; 
                     padding: 20px; 
                     margin: 10px 0;'>
                    <h3 style='color: #FFA726; margin-bottom: 20px; font-size: 1.5em; font-weight: bold;'>
                        ⚠️ Profil à consolider
                    </h3>
                    <div style='background: rgba(255, 167, 38, 0.05); 
                         border-radius: 8px; 
                         padding: 15px; 
                         margin-bottom: 20px;'>
                        <h4 style='color: #FFA726; margin-bottom: 10px; font-size: 1.1em; font-weight: bold;'>
                            💡 Recommandations
                        </h4>
                        <ul style='list-style-type: none; margin: 0; padding: 0; color: white;'>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #FFA726'>▹</span> Mettez en avant vos projets personnels et votre motivation
                            </li>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #FFA726'>▹</span> Considérez des IUT avec un taux de pression plus favorable
                            </li>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #FFA726'>▹</span> Soignez particulièrement votre lettre de motivation
                            </li>
                            <li style='margin-bottom: 8px;'>
                                <span style='color: #FFA726'>▹</span> Développez des compétences en programmation ou data science
                            </li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur dans display_profil_feedback: {str(e)}")

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
    """Calcule la probabilité de recevoir une proposition selon le profil"""
    # 1. Calculer le taux de base selon le type de bac
    if profile['bac_type'] == "Général":
        candidats = iut_data['nb_voe_pp_bg']
        propositions = iut_data['prop_tot_bg']
    elif profile['bac_type'] == "Technologique":
        candidats = iut_data['nb_voe_pp_bt']
        propositions = iut_data['prop_tot_bt']
    else:  # DAEU et autres
        candidats = iut_data['nb_voe_pp_at']
        propositions = iut_data['prop_tot_at']
        
    base_rate = (propositions / candidats * 100) if candidats > 0 else 0

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
        'taux_proposition': round((iut_data['prop_tot'] / iut_data['voe_tot']) * 100, 1),
        'profil_match': round(base_rate, 1),
        'mention_boost': round((mention_bonus - 1) * 100, 1),
        'boursier_boost': round((boursier_bonus - 1) * 100, 1)
    }
    
    return probability, stats

def calculate_chances(profile, data):
    
    """Calcule les chances pour tous les établissements"""
    results = []
    for _, iut in data.iterrows():
        # Base rate calculation based on bac type
        if profile['bac_type'] == "Général":
            candidats = iut['nb_voe_pp_bg']
            propositions = iut['prop_tot_bg']
        elif profile['bac_type'] == "Technologique":
            candidats = iut['nb_voe_pp_bt']
            propositions = iut['prop_tot_bt']
        else:  # DAEU et autres
            candidats = iut['nb_voe_pp_at']
            propositions = iut['prop_tot_at']
        
        base_rate = (propositions / candidats * 100) if candidats > 0 else 0

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
                <h3 style='color: #FFFFFF; margin: 0;'>Total propositions</h3>
                <p style='color: #FFFFFF; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                    {data['prop_tot'].sum():,}
                </p>
            </div>
        """, unsafe_allow_html=True)

def display_prediction_interface(data, show_title=True):
    """Interface de prédiction des chances de recevoir une proposition"""
    
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

    # Get IUT data
    iut_data = data[data['g_ea_lib_vx'] == iut_choice].iloc[0]
    
    # Calculate probability
    probability, stats = calculate_admission_probability(iut_data, profile)
    
    # Affichage résultats
    col1, col2 = st.columns(2)
    
    with col1:
        # Jauge de probabilité
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability,
            title={'text': "Probabilité de recevoir une proposition"},
            number={
                'font': {'size': 50},
                'suffix': "%"
            },
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {
                    'color': f'rgba({255-int(probability*2.55)},{int(probability*2.55)},0,0.8)'
                },
                'bgcolor': "rgba(0,0,0,0.1)",
                'steps': [],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': probability
                }
            }
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'size': 20},
            height=400,
            margin=dict(t=100, b=0)
        )
        st.plotly_chart(fig)
    
    with col2:
        st.metric("Places disponibles", stats['capacite'])
        st.metric("Places restantes", stats['places_restantes'])
        st.metric("Taux de pression", f"{stats['taux_pression']} candidats/place")
        st.metric("Taux de proposition", f"{stats['taux_proposition']}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate percentage distributions
        total_prop = iut_data['prop_tot_bg'] + iut_data['prop_tot_bt'] + iut_data['prop_tot_at']
        pct_bg = round((iut_data['prop_tot_bg'] / total_prop * 100), 1) if total_prop > 0 else 0
        pct_bt = round((iut_data['prop_tot_bt'] / total_prop * 100), 1) if total_prop > 0 else 0
        pct_at = round((iut_data['prop_tot_at'] / total_prop * 100), 1) if total_prop > 0 else 0
        
        st.markdown(f"""
        #### 📈 Statistiques de l'établissement
        - **Répartition des propositions :**
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
        - **Chances de proposition :** {stats['profil_match']}%
          * {'✅ Profil recherché' if stats['profil_match'] > 50 else '⚠️ Profil moins représenté'}
        
        - **Bonus acquis :**
          * Mention : +{stats['mention_boost']}%
          * Boursier : +{stats['boursier_boost']}%
        """)

    return iut_choice, probability  # Retourne à la fois l'IUT choisi et la probabilité
def display_conseils(sorted_df=None):
    """Affiche les conseils pour la candidature en utilisant les composants natifs Streamlit"""
    
    # Conteneur principal avec style personnalisé
    with st.container():
        # Titre principal
        st.markdown("""
            <h3 style='
                color: #FFC107;
                margin-bottom: 20px;
                font-size: 1.5em;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(255, 193, 7, 0.1);
                border-radius: 10px;
                border: 1px solid rgba(255, 193, 7, 0.3);
            '>
                💡 Conseils pour votre candidature
            </h3>
        """, unsafe_allow_html=True)
        
        # Section 1
        st.subheader("🎯 Diversifiez vos choix")
        st.markdown("""
        - Candidatez à des établissements avec différents niveaux de sélectivité
        - Ne vous limitez pas aux IUT les plus demandés
        """)
        
        # Section 2
        st.subheader("⭐ Optimisez vos chances")
        st.markdown("""
        - Préparez un dossier solide pour chaque établissement
        - Tenez compte de la mobilité géographique
        - Considérez les IUT avec moins de candidatures
        """)
        
        # Section 3
        st.subheader("🎓 Soyez stratégique")
        st.markdown("""
        - Les IUT moins demandés peuvent offrir d'excellentes opportunités
        - Tenez compte du coût de la vie dans chaque ville
        - Renseignez-vous sur les spécificités de chaque formation
        """)
        
        # Note finale (optionnelle)
        st.info("Ces conseils sont basés sur l'analyse des données Parcoursup et visent à optimiser vos chances d'admission.")

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
    
    # Statistiques globales
    st.subheader("Statistiques générales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Capacité moyenne",
            f"{int(results_df['capacite'].mean())}"
        )
    with col2:
        st.metric(
            "Candidats moyens/IUT",
            f"{int(results_df['nb_candidats'].mean())}"
        )
    with col3:
        st.metric(
            "Chance moyenne",
            f"{results_df['chances'].mean():.1f}%"
        )
    with col4:
        st.metric(
            "Taux boursiers moyen",
            f"{results_df['pct_boursiers'].mean():.1f}%"
        )
    
    # Graphique
    fig = px.bar(
        results_df,
        x='etablissement',
        y='chances',
        title='Chances de recevoir une proposition par établissement',
        labels={'chances': 'Probabilité (%)', 'etablissement': 'Établissement'},
        color='chances',
        color_continuous_scale=[[0, 'rgb(255,50,50)'], 
                          [0.5, 'rgb(255,255,50)'], 
                          [1, 'rgb(50,255,50)']],  # Rouge -> Jaune -> Vert
        hover_data={
            'ville': True,
            'region': True,
            'capacite': ':,.0f',
            'nb_candidats': ':,.0f',
            'pct_boursiers': ':.1f%'
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'size': 12},
        title_font={'size': 24},
        hoverlabel=dict(
            bgcolor="rgba(0,0,0,0.8)",  # Fond noir semi-transparent
            font=dict(color="white", size=14),  # Texte blanc
            bordercolor="white"  # Bordure blanche
        ),
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.1)',
            color='white',
            title_font={'size': 14}
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.1)',
            color='white',
            title_font={'size': 14}
        ),
        coloraxis_colorbar=dict(
            title="Probabilité (%)",
            title_font={'color': 'white'},
            tickfont={'color': 'white'}
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des résultats
    sorted_df = results_df.copy()
    sort_column = st.selectbox(
        "Trier par",
        options=['chances', 'capacite', 'nb_candidats', 'pct_boursiers'],
        format_func=lambda x: {
            'chances': 'Probabilité',
            'capacite': 'Capacité',
            'nb_candidats': 'Nombre de candidats',
            'pct_boursiers': 'Pourcentage de boursiers'
        }[x]
    )
    
    sorted_df = sorted_df.sort_values(sort_column, ascending=False)
    
    # Afficher le tableau une seule fois avec le formatage
    st.dataframe(sorted_df.style.format({
        'capacite': '{:,.0f}',
        'nb_candidats': '{:,.0f}',
        'chances': '{:.1f}%',
        'pct_boursiers': '{:.1f}%'
    }))

def main():
    """Main function for standalone testing"""
    st.set_page_config(layout="wide", page_title="Calculateur Parcoursup BUT SD") 

if __name__ == "__main__":
    main()