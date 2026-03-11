# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIG GLOBALE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tableau de bord Achats",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Tableau de bord Achats – Asment Témara\n\nConçu avec Streamlit."
    },
)

# -----------------------------------------------------------------------------
# THEME & CSS (modern / pro)
# -----------------------------------------------------------------------------
def inject_css(compact: bool = False):
    base_font_size = "14px" if compact else "15px"
    card_padding = "14px" if compact else "16px"
    header_height = "140px" if compact else "160px"

    st.markdown(
        f"""
        <style>
        :root {{
            --brand-primary: #2563eb;   /* Indigo 600 */
            --brand-primary-600: #2563eb;
            --brand-primary-700: #1d4ed8;
            --brand-cta: #0ea5e9;       /* Sky 500 */
            --text: #101828;
            --muted: #475467;
            --bg: #ffffff;
            --panel: #f8fafc;
            --border: #e5e7eb;
            --shadow: 0 8px 20px rgba(2,12,27,.08);
            --radius: 12px;
            --font-size: {base_font_size};
        }}

        html, body, [data-testid="stAppViewContainer"] {{
            background: var(--bg);
            color: var(--text);
            font-size: var(--font-size);
        }}

        /* Header hero */
        .app-hero {{
            position: relative;
            margin: 0 0 16px 0;
            padding: 24px;
            border-radius: var(--radius);
            background: radial-gradient(1000px 400px at 10% 10%, #e0e7ff 0%, transparent 70%),
                        linear-gradient(90deg, rgba(37,99,235,.08), rgba(14,165,233,.08));
            border: 1px solid var(--border);
            height: {header_height};
            display: flex; align-items: center;
            box-shadow: var(--shadow);
        }}
        .app-hero h1 {{
            margin: 0 0 6px 0;
            font-weight: 800;
            letter-spacing: -.02em;
        }}
        .app-hero p {{
            margin: 0;
            color: var(--muted);
        }}

        /* KPI cards */
        .kpi-card {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: {card_padding};
            box-shadow: var(--shadow);
        }}
        .kpi-label {{
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: .08em;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 800;
            color: var(--text);
            margin-top: 4px;
        }}

        /* Buttons */
        .btn-primary button[kind="primary"] {{
            background: var(--brand-primary);
            border-color: var(--brand-primary);
        }}
        .btn-primary button[kind="primary"]:hover {{
            background: var(--brand-primary-700);
            border-color: var(--brand-primary-700);
        }}
        .btn-ghost button {{
            background: #fff !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
        }}
        .btn-ghost button:hover {{
            border-color: var(--brand-primary) !important;
            color: var(--brand-primary) !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 12px;
        }}
        .sb-section-title {{
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: .08em;
            font-size: 12px;
            margin: 12px 0 6px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Toggle “mode compact” dans la sidebar
if "compact" not in st.session_state:
    st.session_state.compact = False
st.sidebar.toggle("Mode compact", key="compact", help="Réduit la densité d’affichage (petits écrans).")
inject_css(st.session_state.compact)

# -----------------------------------------------------------------------------
# OUTILS
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_excel(path: str) -> dict:
    xls = pd.read_excel(path, sheet_name=None, engine='openpyxl')
    cleaned = {}
    for sheet, df in xls.items():
        df = df.copy()
        df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
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
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

@st.cache_data(show_spinner=False)
def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtré')
    return output.getvalue()

# -----------------------------------------------------------------------------
# DATA
# -----------------------------------------------------------------------------
DATA_PATH = 'data/AGENT ACHATS.xlsx'

# Bandeau Hero
st.markdown(
    f"""
    <div class="app-hero">
        <div>
            <h1>📦 Tableau de bord — Service Achats</h1>
            <p>Source : fichier Excel partagé par l’équipe Achats · {datetime.now().strftime("%d/%m/%Y")}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chargement
try:
    data_by_sheet = load_excel(DATA_PATH)
except FileNotFoundError:
    st.error("❌ Fichier non trouvé. Placez votre Excel sous **data/AGENT ACHATS.xlsx** dans le projet.")
    st.stop()

if not data_by_sheet:
    st.warning("Le fichier ne contient pas de données lisibles.")
    st.stop()

df_all = concat_sites(data_by_sheet)

# Mapping colonnes
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
col_found, cols = {}, list(df_all.columns)
for k, cand in COL_MAP_CANDIDATES.items():
    for c in cand:
        if c in cols:
            col_found[k] = c
            break
for k in COL_MAP_CANDIDATES.keys():
    if k not in col_found:  # colonnes manquantes à vide
        df_all[k] = None

rename_map = {v: k for k, v in col_found.items()}
df_all = df_all.rename(columns=rename_map)

if 'quantite' in df_all.columns:
    df_all['quantite'] = pd.to_numeric(df_all['quantite'], errors='coerce')

# -----------------------------------------------------------------------------
# SIDEBAR — FILTRES
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🔎 Filtres")

site_options = sorted(df_all['Site'].dropna().unique().tolist())
status_options = sorted([s for s in df_all.get('status', pd.Series(dtype=str)).dropna().unique().tolist()])
unite_options = sorted([u for u in df_all.get('unite', pd.Series(dtype=str)).dropna().unique().tolist()])

site = st.sidebar.multiselect('Site', site_options, default=site_options, help="Filtrer par site (feuille Excel).")
status = st.sidebar.multiselect('Statut', status_options, default=status_options, help="Statut opérationnel / technique.")
unites = st.sidebar.multiselect('Unité', unite_options, help="Unité de mesure.")
search = st.sidebar.text_input('Recherche', placeholder="Code DA, Article ou Désignation…")
apply_btn = st.sidebar.button("Appliquer les filtres", type="primary", use_container_width=True)
reset_btn = st.sidebar.button("Réinitialiser", use_container_width=True)

if reset_btn:
    st.experimental_rerun()

# Application des filtres (sur click ou par défaut)
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

# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab_overview, tab_analytics, tab_data = st.tabs(["🏠 Vue d’ensemble", "📈 Analytique", "🗃️ Données"])

# -----------------------------------------------------------------------------
# TAB 1 — VUE D’ENSEMBLE
# -----------------------------------------------------------------------------
with tab_overview:
    # KPI Cards
    nb_lignes = len(filtered)
    nb_articles = filtered['article'].nunique() if 'article' in filtered else None
    sum_qte = filtered['quantite'].sum(min_count=1)
    nb_da = filtered['code_da'].nunique() if 'code_da' in filtered else None

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Lignes</div>'
                    f'<div class="kpi-value">{nb_lignes:,}'.replace(',', ' ') + '</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Articles uniques</div>'
                    f'<div class="kpi-value">{(nb_articles or 0):,}'.replace(',', ' ') + '</div></div>', unsafe_allow_html=True)
    with k3:
        qte_txt = f"{sum_qte:,.2f}".replace(',', ' ') if pd.notna(sum_qte) else '-'
        st.markdown('<div class="kpi-card"><div class="kpi-label">Quantité totale</div>'
                    f'<div class="kpi-value">{qte_txt}</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Codes DA uniques</div>'
                    f'<div class="kpi-value">{(nb_da or 0):,}'.replace(',', ' ') + '</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # Charts (theme Plotly harmonisé)
    px.defaults.template = "simple_white"
    px.defaults.color_discrete_sequence = ["#2563eb", "#0ea5e9", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"]

    colA, colB = st.columns(2)
    if 'status' in filtered and filtered['status'].notna().any():
        status_count = (
            filtered.groupby('status', dropna=True)
            .size()
            .reset_index(name='Lignes')
            .sort_values('Lignes', ascending=False)
        )
        fig_status = px.bar(
            status_count, x='status', y='Lignes', color='status',
            title='Répartition par statut', text_auto=True
        )
        fig_status.update_layout(
            margin=dict(l=10, r=10, t=60, b=10),
            xaxis_title=None, legend_title=None,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        colA.plotly_chart(fig_status, use_container_width=True)

    if 'article' in filtered and 'quantite' in filtered:
        top_n = colB.slider("Top N articles par quantité", min_value=5, max_value=30, value=10, step=1)
        top_articles = (
            filtered.groupby('article', dropna=True)['quantite']
            .sum()
            .reset_index()
            .sort_values('quantite', ascending=False)
            .head(top_n)
        )
        fig_top = px.bar(
            top_articles, x='article', y='quantite',
            title=f"Top {top_n} articles par quantité"
        )
        fig_top.update_layout(
            margin=dict(l=10, r=10, t=60, b=10),
            xaxis_title=None, yaxis_title="Quantité",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        colB.plotly_chart(fig_top, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2 — ANALYTIQUE
# -----------------------------------------------------------------------------
with tab_analytics:
    c1, c2 = st.columns(2)
    # Quantité par Site
    if 'quantite' in filtered and 'Site' in filtered:
        qty_site = (
            filtered.groupby('Site', dropna=True)['quantite']
            .sum().reset_index().sort_values('quantite', ascending=False)
        )
        fig_site = px.bar(qty_site, x='Site', y='quantite', title="Quantité totale par site")
        fig_site.update_layout(margin=dict(l=10, r=10, t=60, b=10), xaxis_title=None, yaxis_title="Quantité")
        c1.plotly_chart(fig_site, use_container_width=True)

    # Lignes par Unité
    if 'unite' in filtered:
        rows_unite = (
            filtered.groupby('unite', dropna=True).size()
            .reset_index(name='Lignes').sort_values('Lignes', ascending=False)
        )
        fig_unite = px.bar(rows_unite, x='unite', y='Lignes', title="Nombre de lignes par unité")
        fig_unite.update_layout(margin=dict(l=10, r=10, t=60, b=10), xaxis_title=None, yaxis_title="Lignes")
        c2.plotly_chart(fig_unite, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3 — DONNÉES
# -----------------------------------------------------------------------------
with tab_data:
    st.subheader("📃 Détails des lignes filtrées")

    # Configuration de colonnes (formatage)
    column_config = {}
    if 'quantite' in filtered.columns:
        column_config['quantite'] = st.column_config.NumberColumn("Quantité", format="%.2f")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )

    dl1, dl2 = st.columns(2)
    with dl1:
        st.container().markdown('<div class="btn-primary">', unsafe_allow_html=True)
        st.download_button(
            label='📥 Télécharger (CSV)',
            data=filtered.to_csv(index=False).encode('utf-8'),
            file_name='achats_filtre.csv',
            mime='text/csv',
            use_container_width=True,
            type="primary",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with dl2:
        st.container().markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        st.download_button(
            label='📥 Télécharger (Excel)',
            data=to_excel_bytes(filtered),
            file_name='achats_filtre.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FOOTER SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.info("💡 Astuce : utilisez la recherche pour filtrer sur **Code DA**, **Article** ou **Désignation**.")
