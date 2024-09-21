# IMPORT DE BIBLIOTHEQUE NECESSAIRE 
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gdown  # Ajoutez cette ligne pour importer gdown

# PAGE STREAMLIT 
st.set_page_config(page_title="Tableau de Bord Professionnel", page_icon=":bar_chart:", layout="wide")

# Charger les données
@st.cache_data
def load_data():
    # URL pour télécharger le fichier depuis Google Drive
    url = 'https://drive.google.com/uc?export=download&id=1jw_6cmV_jOSR-1HnfKNAlj-i-1Ni3ujz'
    gdown.download(url, 'donnes.csv', quiet=False)  # Télécharger le fichier
    return pd.read_csv("donnes.csv", encoding="ISO-8859-1", low_memory=False)
df = load_data()

# Appliquer des styles CSS personnalisés
st.markdown("""<style>
    .main {
        background-color: #f5f5f5;  /* Arrière-plan clair pour les pages */
    }
    .sidebar .sidebar-content {
        background-color: #1f4e79;  /* Couleur bleue pour la barre latérale */
        color: white;
    }
    .title-header {
        color: #2c3e50;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 40px;
    }
    .author {
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
        color: #2c3e50;
    }
    .stat-box {
        background-color: #1f4e79;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# PAGE D'ACCUEIL
def page1():
    st.markdown("<div class='title-header'>Bienvenue sur notre Dashboard Professionnel</div>", unsafe_allow_html=True)

    # Afficher le nom
    st.markdown("<div class='author'>Réalisé par Coulibaly Kiyali</div>", unsafe_allow_html=True)

    # Afficher l'heure actuelle avec un meilleur design
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"<div class='author'>Il est exactement : {current_time}</div>", unsafe_allow_html=True)

    st.markdown("""<div class="stat-box">
        <h2>Introduction</h2>
        <p>Cette application vous permet d'explorer les données sur les prêts immobiliers, avec des statistiques descriptives et des visualisations interactives.</p>
    </div>""", unsafe_allow_html=True)

    # Descriptions des variables
    st.markdown("""<div class="stat-box">
        <h3>Descriptions des variables</h3>
        <ul>
            <li><strong>pm2</strong>: Prix au m² de la surface du logement</li>
            <li><strong>vtpz</strong>: Montant du prêt à taux zéro</li>
            <li><strong>vtpr</strong>: Montant de l'ensemble des prêts de l'opération</li>
            <li><strong>vtpp</strong>: Montant du prêt principal</li>
            <li><strong>txno</strong>: Taux nominal annuel du prêt</li>
            <li><strong>an</strong>: Année d'enregistrement</li>
            <li><strong>region</strong>: Région où le prêt est accordé</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Statistiques descriptives
    st.subheader('Statistiques descriptives globales des données')
    st.write(df.describe())
    
    # Statistiques annuelles
    st.markdown("<div class='stat-box'><h3>Statistiques annuelles</h3></div>", unsafe_allow_html=True)
    selected_years = st.multiselect("Sélectionnez les années à afficher", df['an'].unique())
    if selected_years:
        stats_by_an = df[df['an'].isin(selected_years)].groupby('an')[['vtpz', 'vtpr', 'vtpp', 'txno']].mean().reset_index()
        st.write(stats_by_an)

    # Statistiques régionales
    st.markdown("<div class='stat-box'><h3>Statistiques régionales</h3></div>", unsafe_allow_html=True)
    stat_region = st.multiselect("Sélectionnez les régions à afficher", df['region'].unique())
    if stat_region:
        stats_by_region = df[df['region'].isin(stat_region)].groupby('region')[['vtpz', 'vtpr', 'vtpp', 'txno']].mean().reset_index()
        st.write(stats_by_region)

    # Option de téléchargement des données
    st.markdown("<div class='stat-box'><h3>Télécharger les données</h3></div>", unsafe_allow_html=True)
    st.download_button(
        label="Télécharger les données sous forme de CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='donnees_pret.csv',
        mime='text/csv',
    )

# PAGE DES VISUALISATIONS
def page2():
    st.markdown("<div class='title-header'>Visualisations</div>", unsafe_allow_html=True)

    # Ajouter des graphiques avec filtres
    st.markdown("<div class='title-header'>Sélectionnez vos indicateurs</div>", unsafe_allow_html=True)
    selected_years = st.multiselect("Sélectionnez les années pour les graphiques", df['an'].unique())
    selected_region = st.multiselect("Sélectionnez les régions pour les graphiques", df['region'].unique())
    
    # Choisir le type de graphique à afficher
    graphique_options = [
        'Évolution des prix au m²', 
        'Évolution du taux d\'intérêt nominal', 
        'Montant moyen du prêt à taux zéro par région',
        'Montant total des prêts par région'  # Nouvelle option ajoutée
    ]
    selected_graphique = st.selectbox("Choisissez un graphique à visualiser", graphique_options)

    if selected_years:
        filtered_df = df[df['an'].isin(selected_years)]
        if selected_region:
            filtered_df = filtered_df[filtered_df['region'].isin(selected_region)]

        if selected_graphique == 'Évolution des prix au m²':
            plot_evolution_prix_m2(filtered_df)
        elif selected_graphique == 'Évolution du taux d\'intérêt nominal':
            plot_evolution_taux_interet(filtered_df)
        elif selected_graphique == 'Montant moyen du prêt à taux zéro par région':
            plot_montant_pret_zero(filtered_df)
        elif selected_graphique == 'Montant total des prêts par région':  # Nouvelle option traitée
            plot_montant_total_pret(filtered_df)

    # Afficher la matrice de corrélation sans filtre
    plot_correlation_matrix(df)  

# STYLE PROFESSIONNEL POUR LES VISUALISATIONS
def plot_evolution_prix_m2(filtered_df):
    st.subheader("Évolution des prix au m²")
    mean_pm2 = filtered_df.groupby('an')['pm2'].mean()
    fig = px.line(x=mean_pm2.index, y=mean_pm2.values, labels={'x': 'Année', 'y': 'Prix du m²'})
    fig.update_layout(template='plotly_white', title="Évolution annuelle des prix au m²", font=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)

def plot_evolution_taux_interet(filtered_df):
    st.subheader("Évolution du taux d'intérêt nominal")
    mean_tx = filtered_df.groupby('an')['txno'].mean()
    fig = px.line(x=mean_tx.index, y=mean_tx.values, labels={'x': 'Année', 'y': "Taux d'intérêt nominal"})
    fig.update_layout(template='plotly_white', title="Évolution du taux d'intérêt nominal", font=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)

def plot_montant_pret_zero(filtered_df):
    st.subheader('Montant moyen du prêt à taux zéro par région')
    mean_montant_region = filtered_df.groupby('region')['vtpz'].mean()
    fig = px.bar(x=mean_montant_region.index, y=mean_montant_region.values, text=mean_montant_region.values, 
                 labels={'x': 'Région', 'y': 'Montant moyen'}, color=mean_montant_region.index)
    fig.update_layout(title="Montant moyen du prêt à taux zéro par région", template='plotly_white', font=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)

def plot_montant_total_pret(filtered_df):
    st.subheader('Montant total des prêts par région')
    total_pret_region = filtered_df.groupby('region')['vtpr'].sum()
    fig = px.bar(x=total_pret_region.index, y=total_pret_region.values, text=total_pret_region.values, 
                 labels={'x': 'Région', 'y': 'Montant total'}, color=total_pret_region.index)
    fig.update_layout(title="Montant total des prêts par région", template='plotly_white', font=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_matrix(df):
    st.subheader("Matrice de corrélation")
    correlation_matrix = df.corr()
    fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu')
    fig.update_layout(title="Matrice de corrélation entre les variables", template='plotly_white', font=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)

# MENU DE NAVIGATION
pages = {
    "Accueil": page1,
    "Visualisations": page2,
}

# Sélectionnez la page
selected_page = st.sidebar.selectbox("Choisissez une page", options=list(pages.keys()))

# Affichez la page sélectionnée
pages[selected_page]()
