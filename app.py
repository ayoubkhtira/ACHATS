import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dashboard Achats",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE CSS + FLATICON
# ============================================================

st.markdown(
    """
<link rel="stylesheet" href="https://cdn-uicons.flaticon.com/2.6.0/uicons-bold-rounded/css/uicons-bold-rounded.css">
<link rel="stylesheet" href="https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css">

<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }

    .app-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 30px 34px;
        border-radius: 24px;
        margin-bottom: 26px;
        color: white;
        box-shadow: 0px 14px 34px rgba(15, 23, 42, 0.18);
    }

    .title-row {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .header-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.14);
        color: white;
        font-size: 24px;
        flex-shrink: 0;
    }

    .app-header h1 {
        font-size: 34px;
        margin-bottom: 8px;
        font-weight: 850;
        letter-spacing: -0.4px;
    }

    .app-header p {
        font-size: 15px;
        color: #dbeafe;
        margin-bottom: 0;
        line-height: 1.55;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 22px;
        font-weight: 850;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 18px;
        letter-spacing: -0.2px;
    }

    .section-title i {
        color: #2563eb;
        font-size: 21px;
    }

    .sub-section-title {
        display: flex;
        align-items: center;
        gap: 9px;
        font-size: 18px;
        font-weight: 800;
        color: #1e293b;
        margin-top: 16px;
        margin-bottom: 12px;
    }

    .sub-section-title i {
        color: #475569;
        font-size: 18px;
    }

    .card {
        background-color: white;
        padding: 22px;
        border-radius: 20px;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.06);
        border: 1px solid #e5e7eb;
        min-height: 148px;
    }

    .card h4 {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #0f172a;
        margin-bottom: 10px;
        font-size: 17px;
        font-weight: 850;
    }

    .pro-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 12px;
        background: rgba(37, 99, 235, 0.10);
        color: #2563eb;
        font-size: 17px;
        flex-shrink: 0;
    }

    .metric-card {
        background-color: white;
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0px 8px 22px rgba(15, 23, 42, 0.06);
        border-left: 5px solid #2563eb;
        min-height: 122px;
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        color: #0f172a;
        font-weight: 900;
        margin-bottom: 2px;
        letter-spacing: -0.3px;
    }

    .metric-help {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.4;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 14px;
        padding: 12px 20px;
        border: 1px solid #e5e7eb;
        font-weight: 750;
        color: #334155;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
        border-color: #1e3a8a !important;
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

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 20px;
        font-weight: 850;
        margin-bottom: 8px;
        color: white;
    }

    .sidebar-title i {
        color: #93c5fd;
        font-size: 20px;
    }

    .sidebar-note {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .small-note {
        font-size: 13px;
        color: #64748b;
        line-height: 1.55;
    }

    .warning-box {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
        padding: 15px 18px;
        border-radius: 14px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 20px;
    }

    .footer {
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #e5e7eb;
        color: #94a3b8;
        font-size: 12px;
        text-align: center;
    }
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FONCTIONS
# ============================================================

@st.cache_data(show_spinner=False)
def get_sheet_names(file_bytes):
    excel_file = pd.ExcelFile(BytesIO(file_bytes))
    return excel_file.sheet_names


@st.cache_data(show_spinner=False)
def read_sheet(file_bytes, sheet_name):
    return pd.read_excel(BytesIO(file_bytes), sheet_name=sheet_name)


def normalize_columns(df):
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
    if df.empty:
        return None

    cols = list(df.columns)
    cols_clean = {c.lower().strip(): c for c in cols}

    for name in possible_names:
        key = name.lower().strip()
        if key in cols_clean:
            return cols_clean[key]

    for col in cols:
        col_low = col.lower().strip()
        for name in possible_names:
            if name.lower().strip() in col_low:
                return col

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
                .str.replace("\u00a0", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def format_number(value):
    try:
        if pd.isna(value):
            return "0"
        return f"{value:,.0f}".replace(",", " ")
    except Exception:
        return "0"


def format_amount(value):
    try:
        if pd.isna(value):
            return "0.00"
        return f"{value:,.2f}".replace(",", " ")
    except Exception:
        return "0.00"


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


def safe_group_count(df, group_col, count_col=None, top_n=15):
    if df.empty or group_col is None or group_col not in df.columns:
        return pd.DataFrame()

    temp = df.copy()
    temp[group_col] = temp[group_col].fillna("Non renseigné").astype(str)

    if count_col and count_col in temp.columns:
        result = (
            temp.groupby(group_col, dropna=False)[count_col]
            .nunique()
            .reset_index(name="Nombre")
            .sort_values("Nombre", ascending=False)
            .head(top_n)
        )
    else:
        result = temp[group_col].value_counts().reset_index()
        result.columns = [group_col, "Nombre"]
        result = result.head(top_n)

    return result


def safe_group_sum(df, group_col, value_col, top_n=15):
    if df.empty or group_col is None or value_col is None:
        return pd.DataFrame()

    if group_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()

    temp = df.copy()
    temp[group_col] = temp[group_col].fillna("Non renseigné").astype(str)

    result = (
        temp.groupby(group_col, dropna=False)[value_col]
        .sum()
        .reset_index(name="Total")
        .sort_values("Total", ascending=False)
        .head(top_n)
    )

    return result


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


def get_unique_values(df, col):
    if col and col in df.columns:
        return sorted(df[col].dropna().astype(str).unique())
    return []


def section_title(icon_class, title):
    st.markdown(
        f"""
        <div class="section-title">
            <i class="{icon_class}"></i>
            <span>{title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def sub_section_title(icon_class, title):
    st.markdown(
        f"""
        <div class="sub-section-title">
            <i class="{icon_class}"></i>
            <span>{title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def sidebar_title(icon_class, title):
    st.markdown(
        f"""
        <div class="sidebar-title">
            <i class="{icon_class}"></i>
            <span>{title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_plotly_chart(fig, key):
    st.plotly_chart(fig, use_container_width=True, key=key)


def show_dataframe(df, key, height=420):
    st.dataframe(df, use_container_width=True, height=height, key=key)


def download_excel_button(df, filename, label, key):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Donnees filtrees")

    st.download_button(
        label=label,
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=key
    )


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

st.markdown(
    """
<div class="app-header">
    <div class="title-row">
        <span class="header-icon">
            <i class="fi fi-br-shopping-cart"></i>
        </span>
        <div>
            <h1>Dashboard Achats — Demandes & Commandes</h1>
            <p>
                Plateforme de pilotage pour analyser les demandes d'achat, les commandes,
                les fournisseurs, les articles, les divisions, les GAc et les montants achats
                à partir d'un fichier Excel.
            </p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    sidebar_title("fi fi-rr-settings-sliders", "Paramètres")

    st.markdown(
        """
        <div class="sidebar-note">
            Chargez votre fichier Excel contenant les demandes et/ou commandes achats.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Importer le fichier Excel",
        type=["xlsx", "xls"],
        key="upload_excel_achats"
    )

    st.markdown("---")
    sidebar_title("fi fi-rr-document", "Colonnes attendues")

    st.markdown(
        """
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
"""
    )


# ============================================================
# PAGE AVANT UPLOAD
# ============================================================

if uploaded_file is None:
    st.markdown(
        """
        <div class="warning-box">
            <i class="fi fi-rr-info"></i>
            <span>Veuillez importer un fichier Excel pour démarrer l'analyse.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    sub_section_title("fi fi-rr-apps", "Fonctionnalités de l'application")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(
            """
            <div class="card">
                <h4>
                    <span class="pro-icon"><i class="fi fi-rr-file-invoice"></i></span>
                    Analyse des demandes
                </h4>
                <p class="small-note">
                    Suivi des DA, articles demandés, demandeurs, GAc, quantités et évolution mensuelle.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            """
            <div class="card">
                <h4>
                    <span class="pro-icon"><i class="fi fi-rr-shopping-cart"></i></span>
                    Analyse des commandes
                </h4>
                <p class="small-note">
                    Analyse des commandes, fournisseurs, montants, divisions, devises et articles commandés.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            """
            <div class="card">
                <h4>
                    <span class="pro-icon"><i class="fi fi-rr-chart-histogram"></i></span>
                    Analyse croisée
                </h4>
                <p class="small-note">
                    Comparaison entre articles demandés et articles commandés pour détecter les écarts.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.stop()


# ============================================================
# LECTURE EXCEL
# ============================================================

try:
    file_bytes = uploaded_file.getvalue()
    sheet_names = get_sheet_names(file_bytes)
except Exception as e:
    st.error("Erreur lors de la lecture du fichier Excel. Vérifiez que le fichier est valide.")
    st.exception(e)
    st.stop()


with st.sidebar:
    st.markdown("---")
    sidebar_title("fi fi-rr-folder-open", "Feuilles Excel")

    demande_sheet = st.selectbox(
        "Feuille des demandes d'achat",
        options=["Aucune"] + sheet_names,
        index=1 if len(sheet_names) >= 1 else 0,
        key="select_sheet_demandes"
    )

    commande_sheet = st.selectbox(
        "Feuille des commandes achats",
        options=["Aucune"] + sheet_names,
        index=2 if len(sheet_names) >= 2 else 0,
        key="select_sheet_commandes"
    )


df_demandes = pd.DataFrame()
df_commandes = pd.DataFrame()

try:
    if demande_sheet != "Aucune":
        df_demandes = normalize_columns(read_sheet(file_bytes, demande_sheet))

    if commande_sheet != "Aucune":
        df_commandes = normalize_columns(read_sheet(file_bytes, commande_sheet))
except Exception as e:
    st.error("Erreur pendant la lecture des feuilles sélectionnées.")
    st.exception(e)
    st.stop()


# ============================================================
# MAPPING COLONNES
# ============================================================

dem_col_da = find_column(df_demandes, ["Dem.achat", "Demande achat", "DA"])
dem_col_article = find_column(df_demandes, ["Article"])
dem_col_designation = find_column(df_demandes, ["Désignation", "Designation"])
dem_col_gac = find_column(df_demandes, ["GAc", "GAC"])
dem_col_createur = find_column(df_demandes, ["Créé par", "Cree par", "Créateur"])
dem_col_demandeur = find_column(df_demandes, ["Demandeur"])
dem_col_quantite = find_column(df_demandes, ["Quantité", "Quantite"])
dem_col_date_da = find_column(df_demandes, ["Date DA", "Date demande"])
dem_col_date_lanc = find_column(df_demandes, ["Date lanc.", "Date lanc", "Date lancement"])
dem_col_div = find_column(df_demandes, ["Div.", "Div", "Division"])

cmd_col_article = find_column(df_commandes, ["Article"])
cmd_col_designation = find_column(df_commandes, ["Désignation", "Designation"])
cmd_col_doc = find_column(df_commandes, ["Doc achat", "Document achat", "Commande"])
cmd_col_date = find_column(df_commandes, ["Date doc.", "Date doc", "Date document"])
cmd_col_quantite = find_column(df_commandes, ["Quantité", "Quantite"])
cmd_col_fournisseur = find_column(df_commandes, ["Nom du fournisseur", "Fournisseur"])
cmd_col_prix = find_column(df_commandes, ["Prix net", "Prix"])
cmd_col_devise = find_column(df_commandes, ["Dev.", "Devise"])
cmd_col_gac = find_column(df_commandes, ["GAc", "GAC"])
cmd_col_div = find_column(df_commandes, ["Div.", "Div", "Division"])

if not df_demandes.empty:
    df_demandes = convert_dates(df_demandes, [dem_col_date_da, dem_col_date_lanc])
    df_demandes = convert_numeric(df_demandes, [dem_col_quantite])

if not df_commandes.empty:
    df_commandes = convert_dates(df_commandes, [cmd_col_date])
    df_commandes = convert_numeric(df_commandes, [cmd_col_quantite, cmd_col_prix])

    if cmd_col_quantite and cmd_col_prix:
        df_commandes["Montant estimé"] = (
            df_commandes[cmd_col_quantite].fillna(0) *
            df_commandes[cmd_col_prix].fillna(0)
        )
    elif cmd_col_prix:
        df_commandes["Montant estimé"] = df_commandes[cmd_col_prix].fillna(0)
    else:
        df_commandes["Montant estimé"] = 0


# ============================================================
# TABS PRINCIPAUX
# ============================================================

tab_overview, tab_demandes, tab_commandes, tab_compare, tab_data = st.tabs(
    [
        "Vue globale",
        "Demandes d'achat",
        "Commandes achats",
        "Analyse croisée",
        "Données"
    ]
)


# ============================================================
# TAB VUE GLOBALE
# ============================================================

with tab_overview:
    section_title("fi fi-br-home", "Vue globale du fichier importé")

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

    sub_section_title("fi fi-rr-chart-histogram", "Synthèse visuelle")

    left, right = st.columns(2)

    with left:
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
            show_plotly_chart(fig, "chart_overview_top_gac")
        else:
            st.info("Aucune donnée demande exploitable pour le graphique GAc.")

    with right:
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
            show_plotly_chart(fig, "chart_overview_top_fournisseurs")
        else:
            st.info("Aucune donnée commande exploitable pour le graphique fournisseurs.")


# ============================================================
# TAB DEMANDES
# ============================================================

with tab_demandes:
    section_title("fi fi-rr-file-invoice", "Analyse des demandes d’achat")

    if df_demandes.empty:
        st.warning("Aucune feuille de demandes sélectionnée ou feuille vide.")
    else:
        with st.sidebar:
            st.markdown("---")
            sidebar_title("fi fi-rr-filter", "Filtres demandes")

            dem_filters = {}

            if dem_col_gac:
                dem_filters[dem_col_gac] = st.multiselect(
                    "Filtrer par GAc",
                    get_unique_values(df_demandes, dem_col_gac),
                    key="filter_dem_gac"
                )

            if dem_col_demandeur:
                dem_filters[dem_col_demandeur] = st.multiselect(
                    "Filtrer par demandeur",
                    get_unique_values(df_demandes, dem_col_demandeur),
                    key="filter_dem_demandeur"
                )

            if dem_col_createur:
                dem_filters[dem_col_createur] = st.multiselect(
                    "Filtrer par créateur",
                    get_unique_values(df_demandes, dem_col_createur),
                    key="filter_dem_createur"
                )

            if dem_col_div:
                dem_filters[dem_col_div] = st.multiselect(
                    "Filtrer par division",
                    get_unique_values(df_demandes, dem_col_div),
                    key="filter_dem_division"
                )

            dem_date_range = None

            if dem_col_date_da and dem_col_date_da in df_demandes.columns and df_demandes[dem_col_date_da].notna().any():
                min_date = df_demandes[dem_col_date_da].min().date()
                max_date = df_demandes[dem_col_date_da].max().date()

                dem_date_range = st.date_input(
                    "Période Date DA",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="filter_dem_date_da"
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

        sub_section_title("fi fi-rr-chart-histogram", "Analyses principales")

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
                show_plotly_chart(fig, "chart_dem_division")

            elif dem_col_gac:
                data = safe_group_count(df_dem_filtered, dem_col_gac, dem_col_da, 15)
                fig = px.bar(
                    data,
                    x=dem_col_gac,
                    y="Nombre",
                    title="Nombre de demandes par GAc",
                    text="Nombre"
                )
                show_plotly_chart(fig, "chart_dem_gac")
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
                show_plotly_chart(fig, "chart_dem_top_designation")
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
                show_plotly_chart(fig, "chart_dem_top_demandeurs")

        with g4:
            if dem_col_date_da:
                trend = (
                    df_dem_filtered
                    .dropna(subset=[dem_col_date_da])
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
                    show_plotly_chart(fig, "chart_dem_evolution")
                else:
                    st.info("Aucune donnée temporelle disponible.")

        sub_section_title("fi fi-rr-database", "Qualité des données demandes")
        data_quality_card(df_dem_filtered)

        sub_section_title("fi fi-rr-table", "Données demandes filtrées")
        show_dataframe(df_dem_filtered, key="df_demandes_filtrees", height=420)

        download_excel_button(
            df_dem_filtered,
            "demandes_filtrees.xlsx",
            "Télécharger les demandes filtrées",
            key="download_demandes_filtrees"
        )


# ============================================================
# TAB COMMANDES
# ============================================================

with tab_commandes:
    section_title("fi fi-rr-shopping-cart", "Analyse des commandes achats")

    if df_commandes.empty:
        st.warning("Aucune feuille de commandes sélectionnée ou feuille vide.")
    else:
        with st.sidebar:
            st.markdown("---")
            sidebar_title("fi fi-rr-filter", "Filtres commandes")

            cmd_filters = {}

            if cmd_col_fournisseur:
                cmd_filters[cmd_col_fournisseur] = st.multiselect(
                    "Filtrer par fournisseur",
                    get_unique_values(df_commandes, cmd_col_fournisseur),
                    key="filter_cmd_fournisseur"
                )

            if cmd_col_div:
                cmd_filters[cmd_col_div] = st.multiselect(
                    "Filtrer par division commande",
                    get_unique_values(df_commandes, cmd_col_div),
                    key="filter_cmd_division"
                )

            if cmd_col_gac:
                cmd_filters[cmd_col_gac] = st.multiselect(
                    "Filtrer par GAc commande",
                    get_unique_values(df_commandes, cmd_col_gac),
                    key="filter_cmd_gac"
                )

            if cmd_col_devise:
                cmd_filters[cmd_col_devise] = st.multiselect(
                    "Filtrer par devise",
                    get_unique_values(df_commandes, cmd_col_devise),
                    key="filter_cmd_devise"
                )

            cmd_date_range = None

            if cmd_col_date and cmd_col_date in df_commandes.columns and df_commandes[cmd_col_date].notna().any():
                min_date = df_commandes[cmd_col_date].min().date()
                max_date = df_commandes[cmd_col_date].max().date()

                cmd_date_range = st.date_input(
                    "Période Date document",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="filter_cmd_date"
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

        sub_section_title("fi fi-rr-chart-histogram", "Analyses fournisseurs, articles et divisions")

        g1, g2 = st.columns(2)

        with g1:
            if cmd_col_fournisseur:
                data = safe_group_sum(df_cmd_filtered, cmd_col_fournisseur, "Montant estimé", 15)
                fig = px.bar(
                    data,
                    x="Total",
                    y=cmd_col_fournisseur,
                    orientationestimé",
                    text="Total"
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                show_plotly_chart(fig, "chart_cmd_top_fournisseurs")
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
                show_plotly_chart(fig, "chart_cmd_top_articles")
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
                show_plotly_chart(fig, "chart_cmd_division")

            elif cmd_col_gac:
                data = safe_group_sum(df_cmd_filtered, cmd_col_gac, "Montant estimé", 15)
                fig = px.pie(
                    data,
                    names=cmd_col_gac,
                    values="Total",
                    title="Répartition du montant par GAc",
                    hole=0.45
                )
                show_plotly_chart(fig, "chart_cmd_gac")

        with g4:
            if cmd_col_date:
                trend = (
                    df_cmd_filtered
                    .dropna(subset=[cmd_col_date])
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
                    show_plotly_chart(fig, "chart_cmd_evolution")
                else:
                    st.info("Aucune donnée temporelle disponible.")

        sub_section_title("fi fi-rr-ranking-star", "Classements avancés")

        k1, k2, k3 = st.columns(3)

        with k1:
            if cmd_col_fournisseur:
                top_nb_cmd = safe_group_count(df_cmd_filtered, cmd_col_fournisseur, cmd_col_doc, 10)
                st.markdown("#### Fournisseurs par nombre de commandes")
                show_dataframe(top_nb_cmd, key="df_top_fournisseurs_nb", height=330)

        with k2:
            if cmd_col_designation and cmd_col_quantite:
                top_qty = safe_group_sum(df_cmd_filtered, cmd_col_designation, cmd_col_quantite, 10)
                st.markdown("#### Articles par quantité")
                show_dataframe(top_qty, key="df_top_articles_qte", height=330)

        with k3:
            if cmd_col_gac:
                top_gac = safe_group_sum(df_cmd_filtered, cmd_col_gac, "Montant estimé", 10)
                st.markdown("#### GAc par montant")
                show_dataframe(top_gac, key="df_top_gac_montant", height=330)

        sub_section_title("fi fi-rr-database", "Qualité des données commandes")
        data_quality_card(df_cmd_filtered)

        sub_section_title("fi fi-rr-table", "Données commandes filtrées")
        show_dataframe(df_cmd_filtered, key="df_commandes_filtrees", height=420)

        download_excel_button(
            df_cmd_filtered,
            "commandes_filtrees.xlsx",
            "Télécharger les commandes filtrées",
            key="download_commandes_filtrees"
        )


# ============================================================
# TAB ANALYSE CROISÉE
# ============================================================

with tab_compare:
    section_title("fi fi-rr-search-alt", "Analyse croisée demandes vs commandes")

    if df_demandes.empty or df_commandes.empty:
        st.warning("L'analyse croisée nécessite les deux feuilles : demandes et commandes.")
    elif not dem_col_article or not cmd_col_article:
        st.warning("L'analyse croisée nécessite la colonne Article dans les deux feuilles.")
    else:
        articles_demandes = set(df_demandes[dem_col_article].dropna().astype(str))
        articles_commandes = set(df_commandes[cmd_col_article].dropna().astype(str))

        articles_communs = articles_demandes.intersection(articles_commandes)
        articles_non_commandes = articles_demandes - articles_commandes
        articles_commandes_hors_demandes = articles_commandes - articles_demandes

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("Articles demandés", format_number(len(articles_demandes)), "Articles présents dans les DA", "#2563eb")
        with c2:
            metric_card("Articles commandés", format_number(len(articles_commandes)), "Articles présents dans les commandes", "#16a34a")
        with c3:
            metric_card("Articles communs", format_number(len(articles_communs)), "Présents dans DA et commandes", "#7c3aed")
        with c4:
            metric_card("Demandés non commandés", format_number(len(articles_non_commandes)), "Présents en DA mais absents en commande", "#ef4444")

        sub_section_title("fi fi-rr-chart-pie-alt", "Couverture articles")

        coverage_df = pd.DataFrame(
            {
                "Catégorie": [
                    "Articles communs",
                    "Demandés non commandés",
                    "Commandés hors demandes"
                ],
                "Nombre": [
                    len(articles_communs),
                    len(articles_non_commandes),
                    len(articles_commandes_hors_demandes)
                ]
            }
        )

        fig = px.bar(
            coverage_df,
            x="Catégorie",
            y="Nombre",
            text="Nombre",
            title="Couverture entre demandes et commandes"
        )
        show_plotly_chart(fig, "chart_compare_couverture")

        if articles_non_commandes:
            sub_section_title("fi fi-rr-triangle-warning", "Articles demandés mais non commandés")

            non_cmd_df = df_demandes[
                df_demandes[dem_col_article].astype(str).isin(articles_non_commandes)
            ]

            show_dataframe(non_cmd_df, key="df_articles_non_commandes", height=350)

            download_excel_button(
                non_cmd_df,
                "articles_demandes_non_commandes.xlsx",
                "Télécharger la liste",
                key="download_articles_non_commandes"
            )
        else:
            st.success("Tous les articles demandés existent dans les commandes.")


# ============================================================
# TAB DONNÉES
# ============================================================

with tab_data:
    section_title("fi fi-rr-folder-open", "Exploration des données brutes")

    data_tab1, data_tab2 = st.tabs(["Demandes", "Commandes"])

    with data_tab1:
        if df_demandes.empty:
            st.info("Aucune donnée demande disponible.")
        else:
            sub_section_title("fi fi-rr-table", "Aperçu demandes")
            show_dataframe(df_demandes, key="df_demandes_brutes", height=500)

            sub_section_title("fi fi-rr-list", "Colonnes détectées demandes")
            st.write(list(df_demandes.columns))

    with data_tab2:
        if df_commandes.empty:
            st.info("Aucune donnée commande disponible.")
        else:
            sub_section_title("fi fi-rr-table", "Aperçu commandes")
            show_dataframe(df_commandes, key="df_commandes_brutes", height=500)

            sub_section_title("fi fi-rr-list", "Colonnes détectées commandes")
            st.write(list(df_commandes.columns))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    Icons by Flaticon
</div>
""",
    unsafe_allow_html=True
)
