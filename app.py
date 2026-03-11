# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Tableau de bord Achats", page_icon="📦", layout="wide")

@st.cache_data(show_spinner=False)
def load_excel(path: str) -> dict:
    # Lecture de toutes les feuilles en DataFrame
    xls = pd.read_excel(path, sheet_name=None, engine='openpyxl')
    # Nettoyage léger: enlever lignes vides et normaliser les noms de colonnes
    cleaned = {}
    for sheet, df in xls.items():
        df = df.copy()
        # Supprimer colonnes totalement vides
        df = df.dropna(axis=1, how='all')
        # Supprimer lignes totalement vides
        df = df.dropna(axis=0, how='all')
        # Normaliser en chaînes & strip
        df.columns = [str(c).strip() for c in df.columns]
        for c in df.columns:
            if df[c].dtype == object:
                df[c] = df[c].astype(str).str.strip()
        cleaned[sheet] = df
    return cleaned

@st.cache_data(show_spinner=False)
def concat_sites(data_by_sheet: dict) -> pd.DataFrame:
    frames = []
    for site, df in data_by_sheet.items():
        df2 = df.copy()
        df2['Site'] = site
        frames.append(df2)
    if frames:
        df_all = pd.concat(frames, ignore_index=True)
    else:
        df_all = pd.DataFrame()
    return df_all

@st.cache_data(show_spinner=False)
def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtré')
    return output.getvalue()

DATA_PATH = 'data/AGENT ACHATS.xlsx'

st.title('📦 Tableau de bord – Service Achats')
st.caption("Source: fichier Excel partagé par l'équipe Achats")

try:
    data_by_sheet = load_excel(DATA_PATH)
except FileNotFoundError:
    st.error("❌ Fichier non trouvé. Placez votre Excel sous **data/AGENT ACHATS.xlsx** dans le projet.")
    st.stop()

if not data_by_sheet:
    st.warning("Le fichier ne contient pas de données lisibles.")
    st.stop()

# Concaténer toutes les feuilles (ex: 'ASMENT TEMARA', 'SAFI')
df_all = concat_sites(data_by_sheet)

# Harmoniser quelques colonnes clés attendues
# On essaie de repérer les colonnes par proximité de nom
COL_MAP_CANDIDATES = {
    'code_da': ['CODE DA', 'Code DA', 'Code_DA', 'DA', 'Code'],
    'poste': ['Poste', 'POSTE'],
    'article': ['Article', 'Code article', 'Code'],
    'designation': ['Désignation', 'Designation', 'DESIGNATION'],
    'quantite': ['Quantité', 'Qte', 'Qté', 'QTY'],
    'unite': ['Unite', 'Unité', 'UNITÉ', 'U.M', 'UM'],
    'status': ['Status', 'STATUT', 'Etat', 'État'],
    'code_doc': ['CODE DOC', 'Code doc', 'Doc', 'Référence']
}

col_found = {}
cols = list(df_all.columns)
for k, cand in COL_MAP_CANDIDATES.items():
    for c in cand:
        if c in cols:
            col_found[k] = c
            break

# Ajouter colonnes manquantes si besoin
for k in COL_MAP_CANDIDATES.keys():
    if k not in col_found:
        df_all[k] = None

# Renommer pour unifier
rename_map = {v: k for k, v in col_found.items()}
df_all = df_all.rename(columns=rename_map)

# Convertir quantité en numérique
if 'quantite' in df_all.columns:
    df_all['quantite'] = pd.to_numeric(df_all['quantite'], errors='coerce')

# Barre latérale: filtres
st.sidebar.header('🔎 Filtres')
site_options = sorted(df_all['Site'].dropna().unique().tolist())
site = st.sidebar.multiselect('Site', site_options, default=site_options)

status_options = sorted([s for s in df_all.get('status', pd.Series(dtype=str)).dropna().unique().tolist()])
status = st.sidebar.multiselect('Statut', status_options, default=status_options)

unite_options = sorted([u for u in df_all.get('unite', pd.Series(dtype=str)).dropna().unique().tolist()])
unites = st.sidebar.multiselect('Unité', unite_options)

search = st.sidebar.text_input('Recherche (Code DA / Article / Désignation)')

# Appliquer filtres
filtered = df_all.copy()
if site:
    filtered = filtered[filtered['Site'].isin(site)]
if status:
    filtered = filtered[filtered['status'].isin(status)]
if unites:
    filtered = filtered[filtered['unite'].isin(unites)]
if search:
    s = search.lower()
    mask = (
        filtered.get('code_da', pd.Series('', index=filtered.index)).astype(str).str.lower().str.contains(s, na=False)
        | filtered.get('article', pd.Series('', index=filtered.index)).astype(str).str.lower().str.contains(s, na=False)
        | filtered.get('designation', pd.Series('', index=filtered.index)).astype(str).str.lower().str.contains(s, na=False)
    )
    filtered = filtered[mask]

# KPIs
c1, c2, c3, c4 = st.columns(4)
nb_lignes = len(filtered)
nb_articles = filtered['article'].nunique() if 'article' in filtered else None
sum_qte = filtered['quantite'].sum(min_count=1)
nb_da = filtered['code_da'].nunique() if 'code_da' in filtered else None

c1.metric('Lignes', f"{nb_lignes:,}".replace(',', ' '))
c2.metric('Articles uniques', f"{nb_articles:,}".replace(',', ' ') if nb_articles is not None else '-')
c3.metric('Quantité totale', f"{sum_qte:,.2f}".replace(',', ' ') if pd.notna(sum_qte) else '-')
c4.metric('Codes DA uniques', f"{nb_da:,}".replace(',', ' ') if nb_da is not None else '-')

st.markdown('---')

# Graphiques
colA, colB = st.columns(2)
if 'status' in filtered and filtered['status'].notna().any():
    status_count = (
        filtered.groupby('status', dropna=True)
        .size()
        .reset_index(name='Lignes')
        .sort_values('Lignes', ascending=False)
    )
    fig_status = px.bar(status_count, x='status', y='Lignes', color='status', title='Répartition par statut')
    colA.plotly_chart(fig_status, use_container_width=True)

if 'article' in filtered and 'quantite' in filtered:
    top_articles = (
        filtered.groupby('article', dropna=True)['quantite']
        .sum()
        .reset_index()
        .sort_values('quantite', ascending=False)
        .head(10)
    )
    fig_top = px.bar(top_articles, x='article', y='quantite', title='Top 10 articles par quantité')
    colB.plotly_chart(fig_top, use_container_width=True)

st.markdown('---')

# Tableau
st.subheader('📃 Détails des lignes filtrées')
st.dataframe(filtered, use_container_width=True, hide_index=True)

# Téléchargement
col_dl1, col_dl2 = st.columns(2)
with col_dl1:
    st.download_button(
        label='📥 Télécharger (CSV)',
        data=filtered.to_csv(index=False).encode('utf-8'),
        file_name='achats_filtre.csv',
        mime='text/csv'
    )
with col_dl2:
    st.download_button(
        label='📥 Télécharger (Excel)',
        data=to_excel_bytes(filtered),
        file_name='achats_filtre.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

st.sidebar.markdown('---')
st.sidebar.info('💡 Astuce: utilisez la barre de recherche pour filtrer rapidement sur Code DA, Article ou Désignation.')
