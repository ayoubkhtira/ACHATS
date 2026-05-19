import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Procurement Analytics Platform",
    page_icon="🛒",
    layout="wide"
)

# CLEAN UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CSS GLOBAL PREMIUM
# ============================================================

st.markdown("""
<style>

/* GLOBAL */
.main { background: #f7f9fc; }

/* HEADER */
.app-header {
    background: linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb);
    padding: 30px;
    border-radius: 24px;
    color: white;
    margin-bottom: 25px;
    animation: fadeIn 0.6s ease;
}
.title-row {
    display:flex;
    align-items:center;
    gap:20px;
}
.header-icon {
    font-size:32px;
    background:rgba(255,255,255,0.15);
    padding:20px;
    border-radius:18px;
    transition:0.3s;
}
.header-icon:hover { transform:scale(1.1) rotate(-5deg); }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#111827);
}
.sidebar-title {
    padding:12px;
    color:white;
    font-weight:800;
    background:rgba(255,255,255,0.05);
    border-radius:12px;
    margin-bottom:10px;
}
section[data-testid="stSidebar"] label {
    color:#cbd5e1 !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background:white;
    border-radius:16px;
    padding:10px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:12px;
    font-weight:800;
}
.stTabs [aria-selected="true"] {
    background:#2563eb !important;
    color:white !important;
}

/* KPI */
.metric {
    background:white;
    padding:20px;
    border-radius:16px;
    box-shadow:0 8px 20px rgba(0,0,0,0.05);
    transition:0.3s;
}
.metric:hover { transform: translateY(-5px); }

.metric-value {
    font-size:32px;
    font-weight:900;
}

/* FOOTER */
.footer {
    text-align:center;
    margin-top:40px;
    color:#94a3b8;
}

/* ANIMATION */
@keyframes fadeIn {
    from {opacity:0; transform:translateY(15px);}
    to {opacity:1;}
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="app-header">
    <div class="title-row">
        <div class="header-icon">🛒</div>
        <div>
            <h1>Procurement Analytics Platform</h1>
            <p>Analyse intelligente des demandes et commandes achats</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Paramètres</div>', unsafe_allow_html=True)

    file = st.file_uploader("Importer fichier Excel", type=["xlsx"])

# ============================================================
# FUNCTIONS
# ============================================================

@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

def metric(label, value):
    st.markdown(f"""
    <div class="metric">
        <div>{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN LOGIC
# ============================================================

if file is None:
    st.info("Importer un fichier pour commencer")
    st.stop()

df = load_excel(file)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(["📊 Overview", "📦 Analyse", "📄 Data"])

# ============================================================
# TAB 1
# ============================================================

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        metric("Lignes", len(df))
    with col2:
        metric("Colonnes", len(df.columns))
    with col3:
        metric("Valeurs nulles", df.isna().sum().sum())

    if len(df.columns) >= 2:
        fig = px.histogram(df, x=df.columns[0])
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2
# ============================================================

with tab2:

    col = st.selectbox("Choisir colonne", df.columns)

    if col:
        fig = px.bar(
            df[col].value_counts().head(10),
            title="Top valeurs"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3
# ============================================================

with tab3:
    st.dataframe(df, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
Plateforme Achats • Développé par Ayoub KHTIRA
</div>
""", unsafe_allow_html=True)
