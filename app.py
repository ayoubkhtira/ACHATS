import streamlit as st
import pandas as pd
import plotly.express as px

# ========================================================
# CONFIG
# ========================================================
st.set_page_config(page_title="Procurement Platform", layout="wide")

# ========================================================
# SESSION INIT
# ========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ========================================================
# LOGIN SYSTEM
# ========================================================
def login():
    st.title("🔐 Login Plateforme Achats")

    username = st.text_input("User")
    password = st.text_input("Password", type="password")

    if st.button("Connexion"):
        if username == "achats" and password == "1234":
            st.session_state.logged_in = True
            st.success("Connecté ✅")
            st.rerun()
        else:
            st.error("Identifiants incorrects")

if not st.session_state.logged_in:
    login()
    st.stop()

# ========================================================
# DARK MODE
# ========================================================
def apply_theme():
    if st.session_state.dark_mode:
        bg = "#0f172a"
        text = "white"
        card = "#111827"
    else:
        bg = "#f7f9fc"
        text = "#111"
        card = "white"

    st.markdown(f"""
    <style>
    .main {{background:{bg}; color:{text};}}
    .card {{
        background:{card};
        padding:20px;
        border-radius:16px;
        box-shadow:0 5px 15px rgba(0,0,0,0.08);
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ========================================================
# SIDEBAR NAVIGATION (MULTI PAGE)
# ========================================================
with st.sidebar:

    st.markdown("## 🛒 Menu")

    page = st.radio(
        "",
        ["📊 Dashboard", "📦 Analyse", "🔄 Matching DA vs Commandes", "📁 Données"]
    )

    st.markdown("---")

    st.toggle("🌙 Dark Mode", key="dark_mode")

    st.markdown("---")

    st.markdown("### 📤 Upload fichiers")

    files = st.file_uploader(
        "Importer fichiers Excel",
        type=["xlsx"],
        accept_multiple_files=True
    )

# ========================================================
# LOAD DATA
# ========================================================
dfs = []
if files:
    for file in files:
        df = pd.read_excel(file)
        df["source"] = file.name
        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)
else:
    data = None

# ========================================================
# KPI CARD
# ========================================================
def metric(label, value):
    st.markdown(f"""
    <div class="card">
        <h4>{label}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

# ========================================================
# PAGE 1 - DASHBOARD
# ========================================================
if page == "📊 Dashboard":

    st.title("📊 Dashboard Global")

    if data is None:
        st.warning("Importer un fichier")
        st.stop()

    c1, c2, c3 = st.columns(3)

    with c1:
        metric("Lignes", len(data))
    with c2:
        metric("Colonnes", len(data.columns))
    with c3:
        metric("Sources", data["source"].nunique())

    if len(data.columns) > 0:
        col = data.columns[0]
        fig = px.histogram(data, x=col, title="Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ========================================================
# PAGE 2 - ANALYSE
# ========================================================
if page == "📦 Analyse":

    st.title("📦 Analyse data")

    if data is None:
        st.stop()

    col = st.selectbox("Choisir colonne", data.columns)

    if col:
        fig = px.bar(
            data[col].value_counts().head(10),
            title="Top valeurs"
        )
        st.plotly_chart(fig, use_container_width=True)

# ========================================================
# PAGE 3 - MATCHING
# ========================================================
if page == "🔄 Matching DA vs Commandes":

    st.title("🔄 Matching DA vs Commandes")

    if data is None:
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        col_da = st.selectbox("Colonne DA", data.columns)

    with col2:
        col_cmd = st.selectbox("Colonne Commandes", data.columns)

    if col_da and col_cmd:

        da_set = set(data[col_da].astype(str))
        cmd_set = set(data[col_cmd].astype(str))

        common = da_set & cmd_set
        missing = da_set - cmd_set

        c1, c2 = st.columns(2)

        c1.metric("Match", len(common))
        c2.metric("Non commandés", len(missing))

        if missing:
            df_missing = data[data[col_da].astype(str).isin(missing)]
            st.dataframe(df_missing)

# ========================================================
# PAGE 4 - DATA
# ========================================================
if page == "📁 Données":

    st.title("📁 Exploration")

    if data is None:
        st.stop()

    st.dataframe(data, use_container_width=True)

# ========================================================
# FOOTER
# ========================================================
st.markdown("""
<hr>
<center>Procurement Platform • Ayoub KHTIRA</center>
""", unsafe_allow_html=True)
