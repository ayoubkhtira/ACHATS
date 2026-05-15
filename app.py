import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

# ============================================================
# CONFIGURATION PAGE
# ============================================================

st.set_page_config(
    page_title="Dashboard Achats",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS MODERNE
# ============================================================

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .app-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 28px 32px;
        border-radius: 22px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.18);
    }

    .app-header h1 {
        font-size: 34px;
        margin-bottom: 8px;
        font-weight: 800;
    }

    .app-header p {
        font-size: 15px;
        color: #dbeafe;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 8px 22px rgba(15, 23, 42, 0.06);
        border: 1px solid #e5e7eb;
    }

    .metric-card {
        background-color: white;
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0px 8px 22px rgba(15, 23, 42, 0.06);
        border-left: 5px solid #2563eb;
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 27px;
        color: #0f172a;
        font-weight: 850;
        margin-bottom: 2px;
    }

    .metric-help {
        font-size: 12px;
        color: #94a3b8;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 14px;
        padding: 12px 20px;
        border: 1px solid #e5e7eb;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }

    div[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    div[data-testid="stSidebar"] * {
        color: white;
    }

    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stMultiSelect label,
    div[data-testid="stSidebar"] .stDateInput label,
    div[data-testid="stSidebar"] .stFileUploader label {
        color: white !important;
        font-weight: 700;
    }

    .small-note {
        font-size: 13px;
        color: #64748b;
    }

    .success-box {
        background-color: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #065f46;
        padding: 14px 18px;
        border-radius: 14px;
        font-weight: 600;
    }

    .warning-box {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
        padding: 14px 18px;
        border-radius: 14px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

@st.cache_data(show_spinner=False)
def load_excel(file):
    return pd.ExcelFile(file)


@st.cache_data(show_spinner=False)
def read_sheet(file, sheet_name):
    return pd.read_excel(file, sheet_name=sheet_name)


def normalize_columns(df):
    """
    Nettoyage simple des noms de colonnes.
    """
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\t", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )
    return df


def find_column(df, possible_names):
    """
    Trouve une colonne même si le nom varie légèrement.
    """
    cols = list(df.columns)
    cols_clean = {c.lower().strip(): c for c in cols}

    for name in possible_names:
        key = name.lower().strip()
        if key in cols_clean:
            return cols_clean[key]

    for c in cols:
        c_low = c.lower().strip()
        for name in possible_names:
            if name.lower().strip() in c_low:
                return c

    return None


def convert_dates(df, date_columns):
    df = df.copy()
    for col in date_columns:
        if col and col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def convert_numeric(df, numeric_columns):
    df = df.copy()
    for col in numeric_columns:
        if col and col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace(" ", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}".replace(",", " ")


def format_amount(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.2f}".replace(",", " ")


def metric_card(label, value, help_text="", color="#2563eb"):
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color:{color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def download_excel_button(df, filename, label):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Données filtrées")

    st.download_button(
        label=label,
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def safe_group_count(df, group_col, count_col=None, top_n=15):
    if group_col is None or group_col not in df.columns:
        return pd.DataFrame()

    if count_col and count_col in df.columns:
        result = (
            df.groupby(group_col, dropna=False)[count_col]
            .nunique()
            .reset_index(name="Nombre")
            .sort_values("Nombre", ascending=False)
            .head(top_n)
        )
    else:
        result = (
            df[group_col]
            .fillna("Non renseigné")
            .value_counts()
            .reset_index()
        )
        result.columns = [group_col, "Nombre"]
        result = result.head(top_n)

    return result


def safe_group_sum(df, group_col, value_col, top_n=15):
    if group_col is None or value_col is None:
        return pd.DataFrame()

    if group_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby(group_col, dropna=False)[value_col]
        .sum()
        .reset_index(name="Total")
        .sort_values("Total", ascending=False)
        .head(top_n)
    )

    return result


def apply_common_filters(df, filters):
    filtered = df.copy()

    for col, selected_values in filters.items():
        if col in filtered.columns and selected_values:
            filtered = filtered[filtered[col].isin(selected_values)]

    return filtered


def apply_date_filter(df, date_col, date_range):
    filtered = df.copy()

    if date_col and date_col in filtered.columns and date_range:
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered = filtered[
                (filtered[date_col].dt.date >= start_date) &
                (filtered[date_col].dt.date <= end_date)
            ]

    return filtered


def data_quality_card(df):
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_cells = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Lignes", format_number(total_rows), "Nombre total d'enregistrements", "#2563eb")
    with c2:
        metric_card("Colonnes", format_number(total_cols), "Champs disponibles", "#7c3aed")
    with c3:
        metric_card("Cellules vides", format_number(missing_cells), "Valeurs manquantes", "#f59e0b")
    with c4:
        metric_card("Doublons", format_number(duplicate_rows), "Lignes dupliquées", "#ef4444")


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="app-header">
    <h1>📦 Dashboard Achats — Demandes & Commandes</h1>
    <p>
        Application de pilotage pour analyser les demandes d'achat, les commandes, les fournisseurs,
        les articles, les divisions et les montants achats à partir d'un fichier Excel.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR UPLOAD
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    st.markdown("Chargez votre fichier Excel contenant les demandes et/ou commandes achats.")

    uploaded_file = st.file_uploader(
        "📤 Importer le fichier Excel",
        type=["xlsx", "xls"]
    )

    st.markdown("---")
    st.markdown("### Colonnes attendues")

    st.markdown("""
    **Demandes :**
    - Dem.achat
    - Poste
    - Article
    - Désignation
    - GAc
    - Créé par
    - Demandeur
    - Quantité
    - UQ
    - Date DA
    - Date lanc.

    **Commandes :**
    - Article
    - Désignation
    - Doc achat
    - Poste
    - Date doc.
    - Quantité
    - Nom du fournisseur
    - UAc
    - Prix net
    - Dev.
    - GAc
    - Div.
    """)


if uploaded_file is None:
    st.markdown("""
    <div class="warning-box">
        📌 Veuillez importer un fichier Excel pour démarrer l'analyse.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✅ Fonctionnalités prévues")
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="card">
            <h4>📄 Analyse des demandes</h4>
            <p class="small-note">
                Nombre de demandes, articles les plus demandés, analyse par demandeur, GAc et période.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="card">
            <h4>🧾 Analyse des commandes</h4>
            <p class="small-note">
                Suivi des commandes, top fournisseurs, montants, quantités et répartition par division.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="card">
            <h4>📊 Dashboard interactif</h4>
            <p class="small-note">
                Filtres dynamiques, graphiques Plotly, KPI et export des données filtrées.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# LECTURE EXCEL
# ============================================================

excel_file = load_excel(uploaded_file)
sheet_names = excel_file.sheet_names

with st.sidebar:
    st.markdown("---")
    st.markdown("## 📑 Feuilles Excel")

    demande_sheet = st.selectbox(
        "Feuille des demandes d'achat",
        options=["Aucune"] + sheet_names,
        index=1 if len(sheet_names) >= 1 else 0
    )

    commande_sheet = st.selectbox(
        "Feuille des commandes achats",
        options=["Aucune"] + sheet_names,
        index=2 if len(sheet_names) >= 2 else 0
    )


df_demandes = pd.DataFrame()
df_commandes = pd.DataFrame()

if demande_sheet != "Aucune":
    df_demandes = normalize_columns(read_sheet(uploaded_file, demande_sheet))

if commande_sheet != "Aucune":
    df_commandes = normalize_columns(read_sheet(uploaded_file, commande_sheet))


# ============================================================
# MAPPING COLONNES DEMANDES
# ============================================================

dem_col_da = find_column(df_demandes, ["Dem.achat", "Demande achat", "DA"]) if not df_demandes.empty else None
dem_col_poste = find_column(df_demandes, ["Poste"]) if not df_demandes.empty else None
dem_col_article = find_column(df_demandes, ["Article"]) if not df_demandes.empty else None
dem_col_designation = find_column(df_demandes, ["Désignation", "Designation"]) if not df_demandes.empty else None
dem_col_gac = find_column(df_demandes, ["GAc", "GAC"]) if not df_demandes.empty else None
dem_col_createur = find_column(df_demandes, ["Créé par", "Cree par", "Créateur"]) if not df_demandes.empty else None
dem_col_demandeur = find_column(df_demandes, ["Demandeur"]) if not df_demandes.empty else None
dem_col_quantite = find_column(df_demandes, ["Quantité", "Quantite"]) if not df_demandes.empty else None
dem_col_uq = find_column(df_demandes, ["UQ"]) if not df_demandes.empty else None
dem_col_date_da = find_column(df_demandes, ["Date DA", "Date demande"]) if not df_demandes.empty else None
dem_col_date_lanc = find_column(df_demandes, ["Date lanc.", "Date lanc", "Date lancement"]) if not df_demandes.empty else None
dem_col_div = find_column(df_demandes, ["Div.", "Div", "Division"]) if not df_demandes.empty else None

if not df_demandes.empty:
    df_demandes = convert_dates(df_demandes, [dem_col_date_da, dem_col_date_lanc])
    df_demandes = convert_numeric(df_demandes, [dem_col_quantite])


# ============================================================
# MAPPING COLONNES COMMANDES
# ============================================================

cmd_col_article = find_column(df_commandes, ["Article"]) if not df_commandes.empty else None
cmd_col_designation = find_column(df_commandes, ["Désignation", "Designation"]) if not df_commandes.empty else None
cmd_col_doc = find_column(df_commandes, ["Doc achat", "Document achat", "Commande"]) if not df_commandes.empty else None
cmd_col_poste = find_column(df_commandes, ["Poste"]) if not df_commandes.empty else None
cmd_col_date = find_column(df_commandes, ["Date doc.", "Date doc", "Date document"]) if not df_commandes.empty else None
cmd_col_quantite = find_column(df_commandes, ["Quantité", "Quantite"]) if not df_commandes.empty else None
cmd_col_fournisseur = find_column(df_commandes, ["Nom du fournisseur", "Fournisseur"]) if not df_commandes.empty else None
cmd_col_uac = find_column(df_commandes, ["UAc", "UAC"]) if not df_commandes.empty else None
cmd_col_prix = find_column(df_commandes, ["Prix net", "Prix"]) if not df_commandes.empty else None
cmd_col_devise = find_column(df_commandes, ["Dev.", "Devise"]) if not df_commandes.empty else None
cmd_col_gac = find_column(df_commandes, ["GAc", "GAC"]) if not df_commandes.empty else None
cmd_col_div = find_column(df_commandes, ["Div.", "Div", "Division"]) if not df_commandes.empty else None

if not df_commandes.empty:
    df_commandes = convert_dates(df_commandes, [cmd_col_date])
    df_commandes = convert_numeric(df_commandes, [cmd_col_quantite, cmd_col_prix])

    if cmd_col_quantite and cmd_col_prix:
        df_commandes["Montant estimé"] = df_commandes[cmd_col_quantite] * df_commandes[cmd_col_prix]
    elif cmd_col_prix:
        df_commandes["Montant estimé"] = df_commandes[cmd_col_prix]
    else:
        df_commandes["Montant estimé"] = 0


# ============================================================
# TABS PRINCIPAUX
# ============================================================

tab_overview, tab_demandes, tab_commandes, tab_compare, tab_data = st.tabs([
    "🏠 Vue globale",
    "📄 Demandes d'achat",
    "🧾 Commandes achats",
    "🔎 Analyse croisée",
    "🗂️ Données"
])


# ============================================================
# TAB OVERVIEW
# ============================================================

with tab_overview:
    st.markdown('<div class="section-title">🏠 Vue globale du fichier importé</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    nb_demandes = df_demandes[dem_col_da].nunique() if not df_demandes.empty and dem_col_da else len(df_demandes)
    nb_commandes = df_commandes[cmd_col_doc].nunique() if not df_commandes.empty and cmd_col_doc else len(df_commandes)
    nb_fournisseurs = df_commandes[cmd_col_fournisseur].nunique() if not df_commandes.empty and cmd_col_fournisseur else 0
    montant_total = df_commandes["Montant estimé"].sum() if not df_commandes.empty and "Montant estimé" in df_commandes.columns else 0

    with c1:
        metric_card("Demandes d'achat", format_number(nb_demandes), "Nombre de DA uniques", "#2563eb")
    with c2:
        metric_card("Commandes achats", format_number(nb_commandes), "Nombre de commandes uniques", "#16a34a")
    with c3:
        metric_card("Fournisseurs", format_number(nb_fournisseurs), "Fournisseurs distincts", "#7c3aed")
    with c4:
        metric_card("Montant commandes", format_amount(montant_total), "Quantité × Prix net", "#f97316")

    st.markdown("### 📊 Synthèse visuelle")

    col_left, col_right = st.columns(2)

    with col_left:
        if not df_demandes.empty and dem_col_gac:
            data = safe_group_count(df_demandes, dem_col_gac, dem_col_da, 10)
            fig = px.bar(
                data,
                x="Nombre",
                y=dem_col_gac,
                orientation="h",
                title="Top GAc par nombre de demandes",
                text="Nombre"
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée demande exploitable pour le graphique GAc.")

    with col_right:
        if not df_commandes.empty and cmd_col_fournisseur:
            data = safe_group_sum(df_commandes, cmd_col_fournisseur, "Montant estimé", 10)
            fig = px.bar(
                data,
                x="Total",
                y=cmd_col_fournisseur,
                orientation="h",
                title="Top fournisseurs par montant estimé",
                text="Total"
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée commande exploitable pour le graphique fournisseurs.")


# ============================================================
# TAB DEMANDES
# ============================================================

with tab_demandes:
    st.markdown('<div class="section-title">📄 Analyse des demandes d’achat</div>', unsafe_allow_html=True)

    if df_demandes.empty:
        st.warning("Aucune feuille de demandes sélectionnée ou feuille vide.")
    else:
        with st.sidebar:
            st.markdown("---")
            st.markdown("## 📄 Filtres demandes")

            dem_filters = {}

            if dem_col_gac:
                dem_filters[dem_col_gac] = st.multiselect(
                    "Filtrer par GAc",
                    sorted(df_demandes[dem_col_gac].dropna().astype(str).unique())
                )

            if dem_col_demandeur:
                dem_filters[dem_col_demandeur] = st.multiselect(
                    "Filtrer par demandeur",
                    sorted(df_demandes[dem_col_demandeur].dropna().astype(str).unique())
                )

            if dem_col_createur:
                dem_filters[dem_col_createur] = st.multiselect(
                    "Filtrer par créateur",
                    sorted(df_demandes[dem_col_createur].dropna().astype(str).unique())
                )

            if dem_col_div:
                dem_filters[dem_col_div] = st.multiselect(
                    "Filtrer par division",
                    sorted(df_demandes[dem_col_div].dropna().astype(str).unique())
                )

            dem_date_range = None
            if dem_col_date_da and dem_col_date_da in df_demandes.columns and df_demandes[dem_col_date_da].notna().any():
                min_date = df_demandes[dem_col_date_da].min().date()
                max_date = df_demandes[dem_col_date_da].max().date()
                dem_date_range = st.date_input(
                    "Période Date DA",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

        df_dem_filtered = df_demandes.copy()

        for col, values in dem_filters.items():
            if values:
                df_dem_filtered = df_dem_filtered[df_dem_filtered[col].astype(str).isin(values)]

        df_dem_filtered = apply_date_filter(df_dem_filtered, dem_col_date_da, dem_date_range)

        c1, c2, c3, c4 = st.columns(4)

        total_da = df_dem_filtered[dem_col_da].nunique() if dem_col_da else len(df_dem_filtered)
        total_lignes = len(df_dem_filtered)
        total_articles = df_dem_filtered[dem_col_article].nunique() if dem_col_article else 0
        total_quantite = df_dem_filtered[dem_col_quantite].sum() if dem_col_quantite else 0

        with c1:
            metric_card("DA uniques", format_number(total_da), "Demandes distinctes", "#2563eb")
        with c2:
            metric_card("Lignes DA", format_number(total_lignes), "Postes de demandes", "#16a34a")
        with c3:
            metric_card("Articles", format_number(total_articles), "Articles distincts", "#7c3aed")
        with c4:
            metric_card("Quantité totale", format_number(total_quantite), "Somme des quantités", "#f97316")

        st.markdown("### 📈 Analyses principales")

        g1, g2 = st.columns(2)

        with g1:
            if dem_col_div:
                data = safe_group_count(df_dem_filtered, dem_col_div, dem_col_da, 15)
                fig = px.bar(
                    data,
                    x=dem_col_div,
                    y="Nombre",
                    title="Nombre de demandes par division",
                    text="Nombre"
                )
                st.plotly_chart(fig, use_container_width=True)
            elif dem_col_gac:
                data = safe_group_count(df_dem_filtered, dem_col_gac, dem_col_da, 15)
                fig = px.bar(
                    data,
                    x=dem_col_gac,
                    y="Nombre",
                    title="Nombre de demandes par GAc",
                    text="Nombre"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Colonne Division ou GAc non disponible.")

        with g2:
            if dem_col_designation:
                data = safe_group_count(df_dem_filtered, dem_col_designation, None, 15)
                fig = px.bar(
                    data,
                    x="Nombre",
                    y=dem_col_designation,
                    orientation="h",
                    title="Top articles demandés par désignation",
                    text="Nombre"
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Colonne Désignation non disponible.")

        g3, g4 = st.columns(2)

        with g3:
            if dem_col_demandeur:
                data = safe_group_count(df_dem_filtered, dem_col_demandeur, dem_col_da, 15)
                fig = px.bar(
                    data,
                    x="Nombre",
                    y=dem_col_demandeur,
                    orientation="h",
                    title="Top demandeurs par nombre de DA",
                    text="Nombre"
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)

        with g4:
            if dem_col_date_da:
                trend = (
                    df_dem_filtered.dropna(subset=[dem_col_date_da])
                    .groupby(df_dem_filtered[dem_col_date_da].dt.to_period("M"))
                    .size()
                    .reset_index(name="Nombre")
                )
                if not trend.empty:
                    trend[dem_col_date_da] = trend[dem_col_date_da].astype(str)
                    fig = px.line(
                        trend,
                        x=dem_col_date_da,
                        y="Nombre",
                        markers=True,
                        title="Évolution mensuelle des demandes"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🧮 Qualité des données demandes")
        data_quality_card(df_dem_filtered)

        st.markdown("### 📋 Données demandes filtrées")
        st.dataframe(df_dem_filtered, use_container_width=True, height=420)
        download_excel_button(df_dem_filtered, "demandes_filtrees.xlsx", "📥 Télécharger les demandes filtrées")


# ============================================================
# TAB COMMANDES
# ============================================================

with tab_commandes:
    st.markdown('<div class="section-title">🧾 Analyse des commandes achats</div>', unsafe_allow_html=True)

    if df_commandes.empty:
        st.warning("Aucune feuille de commandes sélectionnée ou feuille vide.")
    else:
        with st.sidebar:
            st.markdown("---")
            st.markdown("## 🧾 Filtres commandes")

            cmd_filters = {}

            if cmd_col_fournisseur:
                cmd_filters[cmd_col_fournisseur] = st.multiselect(
                    "Filtrer par fournisseur",
                    sorted(df_commandes[cmd_col_fournisseur].dropna().astype(str).unique())
                )

            if cmd_col_div:
                cmd_filters[cmd_col_div] = st.multiselect(
                    "Filtrer par division commande",
                    sorted(df_commandes[cmd_col_div].dropna().astype(str).unique())
                )

            if cmd_col_gac:
                cmd_filters[cmd_col_gac] = st.multiselect(
                    "Filtrer par GAc commande",
                    sorted(df_commandes[cmd_col_gac].dropna().astype(str).unique())
                )

            if cmd_col_devise:
                cmd_filters[cmd_col_devise] = st.multiselect(
                    "Filtrer par devise",
                    sorted(df_commandes[cmd_col_devise].dropna().astype(str).unique())
                )

            cmd_date_range = None
            if cmd_col_date and cmd_col_date in df_commandes.columns and df_commandes[cmd_col_date].notna().any():
                min_date = df_commandes[cmd_col_date].min().date()
                max_date = df_commandes[cmd_col_date].max().date()
                cmd_date_range = st.date_input(
                    "Période Date document",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

        df_cmd_filtered = df_commandes.copy()

        for col, values in cmd_filters.items():
            if values:
                df_cmd_filtered = df_cmd_filtered[df_cmd_filtered[col].astype(str).isin(values)]

        df_cmd_filtered = apply_date_filter(df_cmd_filtered, cmd_col_date, cmd_date_range)

        c1, c2, c3, c4 = st.columns(4)

        total_cmd = df_cmd_filtered[cmd_col_doc].nunique() if cmd_col_doc else len(df_cmd_filtered)
        total_lignes_cmd = len(df_cmd_filtered)
        total_fournisseurs = df_cmd_filtered[cmd_col_fournisseur].nunique() if cmd_col_fournisseur else 0
        total_montant = df_cmd_filtered["Montant estimé"].sum() if "Montant estimé" in df_cmd_filtered.columns else 0

        with c1:
            metric_card("Commandes uniques", format_number(total_cmd), "Documents achats distincts", "#2563eb")
        with c2:
            metric_card("Lignes commandes", format_number(total_lignes_cmd), "Postes de commandes", "#16a34a")
        with c3:
            metric_card("Fournisseurs", format_number(total_fournisseurs), "Fournisseurs distincts", "#7c3aed")
        with c4:
            metric_card("Montant total", format_amount(total_montant), "Quantité × Prix net", "#f97316")

        st.markdown("### 📊 Analyses fournisseurs, articles et divisions")

        g1, g2 = st.columns(2)

        with g1:
            if cmd_col_fournisseur:
                data = safe_group_sum(df_cmd_filtered, cmd_col_fournisseur, "Montant estimé", 15)
                fig = px.bar(
                    data,
                    x="Total",
                    y=cmd_col_fournisseur,
                    orientation="h",
                    title="Top fournisseurs par montant estimé",
                    text="Total"
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Colonne fournisseur non disponible.")

        with g2:
            if cmd_col_designation:
                data = safe_group_sum(df_cmd_filtered, cmd_col_designation, "Montant estimé", 15)
                fig = px.bar(
                    data,
                    x="Total",
                    y=cmd_col_designation,
                    orientation="h",
                    title="Top articles par montant estimé",
                    text="Total"
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Colonne désignation non disponible.")

        g3, g4 = st.columns(2)

        with g3:
            if cmd_col_div:
                data = safe_group_sum(df_cmd_filtered, cmd_col_div, "Montant estimé", 15)
                fig = px.pie(
                    data,
                    names=cmd_col_div,
                    values="Total",
                    title="Répartition du montant par division",
                    hole=0.45
                )
                st.plotly_chart(fig, use_container_width=True)
            elif cmd_col_gac:
                data = safe_group_sum(df_cmd_filtered, cmd_col_gac, "Montant estimé", 15)
                fig = px.pie(
                    data,
                    names=cmd_col_gac,
                    values="Total",
                    title="Répartition du montant par GAc",
                    hole=0.45
                )
                st.plotly_chart(fig, use_container_width=True)

        with g4:
            if cmd_col_date:
                trend = (
                    df_cmd_filtered.dropna(subset=[cmd_col_date])
                    .groupby(df_cmd_filtered[cmd_col_date].dt.to_period("M"))["Montant estimé"]
                    .sum()
                    .reset_index(name="Montant")
                )
                if not trend.empty:
                    trend[cmd_col_date] = trend[cmd_col_date].astype(str)
                    fig = px.line(
                        trend,
                        x=cmd_col_date,
                        y="Montant",
                        markers=True,
                        title="Évolution mensuelle des montants commandes"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🏆 Classements avancés")

        c1, c2, c3 = st.columns(3)

        with c1:
            if cmd_col_fournisseur:
                top_nb_cmd = safe_group_count(df_cmd_filtered, cmd_col_fournisseur, cmd_col_doc, 10)
                st.markdown("#### Fournisseurs par nombre de commandes")
                st.dataframe(top_nb_cmd, use_container_width=True, height=330)

        with c2:
            if cmd_col_designation:
                top_qty = safe_group_sum(df_cmd_filtered, cmd_col_designation, cmd_col_quantite, 10)
                st.markdown("#### Articles par quantité")
                st.dataframe(top_qty, use_container_width=True, height=330)

        with c3:
            if cmd_col_gac:
                top_gac = safe_group_sum(df_cmd_filtered, cmd_col_gac, "Montant estimé", 10)
                st.markdown("#### GAc par montant")
                st.dataframe(top_gac, use_container_width=True, height=330)

        st.markdown("### 🧮 Qualité des données commandes")
        data_quality_card(df_cmd_filtered)

        st.markdown("### 📋 Données commandes filtrées")
        st.dataframe(df_cmd_filtered, use_container_width=True, height=420)
        download_excel_button(df_cmd_filtered, "commandes_filtrees.xlsx", "📥 Télécharger les commandes filtrées")


# ============================================================
# TAB ANALYSE CROISÉE
# ============================================================

with tab_compare:
    st.markdown('<div class="section-title">🔎 Analyse croisée demandes vs commandes</div>', unsafe_allow_html=True)

    if df_demandes.empty or df_commandes.empty:
        st.warning("L'analyse croisée nécessite les deux feuilles : demandes et commandes.")
    else:
        c1, c2, c3 = st.columns(3)

        articles_demandes = set(df_demandes[dem_col_article].dropna().astype(str)) if dem_col_article else set()
        articles_commandes = set(df_commandes[cmd_col_article].dropna().astype(str)) if cmd_col_article else set()

        articles_communs = articles_demandes.intersection(articles_commandes)
        articles_non_commandes = articles_demandes - articles_commandes

        with c1:
            metric_card("Articles demandés", format_number(len(articles_demandes)), "Articles présents dans les DA", "#2563eb")
        with c2:
            metric_card("Articles commandés", format_number(len(articles_commandes)), "Articles présents dans les commandes", "#16a34a")
        with c3:
            metric_card("Articles non commandés", format_number(len(articles_non_commandes)), "Présents en DA mais absents en commande", "#ef4444")

        st.markdown("### 📌 Couverture articles")

        coverage_df = pd.DataFrame({
            "Catégorie": ["Articles communs", "Demandés non commandés", "Commandés hors demandes"],
            "Nombre": [
                len(articles_communs),
                len(articles_non_commandes),
                len(articles_commandes - articles_demandes)
            ]
        })

        fig = px.bar(
            coverage_df,
            x="Catégorie",
            y="Nombre",
            text="Nombre",
            title="Couverture entre demandes et commandes"
        )
        st.plotly_chart(fig, use_container_width=True)

        if articles_non_commandes:
            st.markdown("### ⚠️ Articles demandés mais non commandés")
            non_cmd_df = df_demandes[df_demandes[dem_col_article].astype(str).isin(articles_non_commandes)]
            st.dataframe(non_cmd_df, use_container_width=True, height=350)
            download_excel_button(non_cmd_df, "articles_demandes_non_commandes.xlsx", "📥 Télécharger la liste")


# ============================================================
# TAB DONNÉES
# ============================================================

with tab_data:
    st.markdown('<div class="section-title">🗂️ Exploration des données brutes</div>', unsafe_allow_html=True)

    data_tab1, data_tab2 = st.tabs(["📄 Demandes", "🧾 Commandes"])

    with data_tab1:
        if df_demandes.empty:
            st.info("Aucune donnée demande disponible.")
        else:
            st.markdown("### Aperçu demandes")
            st.dataframe(df_demandes, use_container_width=True, height=500)

            st.markdown("### Colonnes détectées demandes")
            st.write(list(df_demandes.columns))

    with data_tab2:
        if df_commandes.empty:
            st.info("Aucune donnée commande disponible.")
        else:
            st.markdown("### Aperçu commandes")
            st.dataframe(df_commandes, use_container_width=True, height=500)

            st.markdown("### Colonnes détectées commandes")
            st.write(list(df_commandes.columns))
