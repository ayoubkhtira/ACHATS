import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

# PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Achats Analytics",
    page_icon="🛒",
    layout="wide"
)

# ============================================================
# CLEAN FUNCTIONS
# ============================================================

def format_number(x):
    try:
        return f"{int(x):,}".replace(",", " ")
    except:
        return "0"


def format_amount(x):
    try:
        return f"{x:,.2f}".replace(",", " ").replace(".", ",")
    except:
        return "0,00"


# ============================================================
# PDF GENERATION
# ============================================================

def create_pdf(df_dem, df_cmd):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "title",
        fontSize=18,
        textColor=colors.HexColor("#0f5132"),
        spaceAfter=20
    )

    section = ParagraphStyle(
        "section",
        fontSize=13,
        textColor=colors.HexColor("#0f5132"),
        spaceAfter=10
    )

    # ===== KPI =====
    nb_dem = len(df_dem)
    nb_cmd = len(df_cmd)

    montant = 0
    if "Montant estimé" in df_cmd.columns:
        montant = df_cmd["Montant estimé"].sum()

    data_kpi = [
        ["Indicateur", "Valeur"],
        ["Demandes", format_number(nb_dem)],
        ["Commandes", format_number(nb_cmd)],
        ["Montant total", format_amount(montant)]
    ]

    def make_table(data):
        t = Table(data)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16a34a")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.3, colors.grey)
        ]))
        return t

    elements = []

    elements.append(Paragraph("Rapport Achats", title))
    elements.append(Paragraph(f"Généré le {datetime.now()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("KPI", section))
    elements.append(make_table(data_kpi))

    # ===== DEMANDES =====
    elements.append(PageBreak())
    elements.append(Paragraph("Demandes", section))

    if not df_dem.empty:
        elements.append(make_table(
            [["ID", "Article", "Quantité"]] +
            df_dem.head(10)[["Dem.achat", "Article", "Quantité"]].astype(str).values.tolist()
        ))

    # ===== COMMANDES =====
    elements.append(PageBreak())
    elements.append(Paragraph("Commandes", section))

    if not df_cmd.empty:
        elements.append(make_table(
            [["Doc", "Fournisseur", "Montant"]] +
            df_cmd.head(10)[["Doc achat", "Nom du fournisseur", "Montant estimé"]].astype(str).values.tolist()
        ))

    # ===== ANALYSE =====
    elements.append(PageBreak())
    elements.append(Paragraph("Analyse", section))

    elements.append(Paragraph(
        "• Optimiser le suivi des demandes non converties.<br/>"
        "• Surveiller les fournisseurs à fort impact.<br/>"
        "• Automatiser le reporting achats.",
        styles["Normal"]
    ))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# ============================================================
# UPLOAD
# ============================================================

file = st.sidebar.file_uploader("Excel", type=["xlsx"])

if file is None:
    st.info("Importer un fichier Excel")
    st.stop()

df = pd.ExcelFile(file)

dem_sheet = st.sidebar.selectbox("Feuille demandes", df.sheet_names)
cmd_sheet = st.sidebar.selectbox("Feuille commandes", df.sheet_names)

df_dem = pd.read_excel(file, sheet_name=dem_sheet)
df_cmd = pd.read_excel(file, sheet_name=cmd_sheet)

# ============================================================
# PREP
# ============================================================

for col in df_cmd.columns:
    if "prix" in col.lower():
        df_cmd[col] = pd.to_numeric(df_cmd[col], errors="coerce")

if "Quantité" in df_cmd.columns and "Prix net" in df_cmd.columns:
    df_cmd["Montant estimé"] = df_cmd["Quantité"] * df_cmd["Prix net"]

# ============================================================
# KPI
# ============================================================

c1, c2, c3 = st.columns(3)

c1.metric("Demandes", len(df_dem))
c2.metric("Commandes", len(df_cmd))

montant = df_cmd["Montant estimé"].sum() if "Montant estimé" in df_cmd else 0
c3.metric("Montant", format_amount(montant))

# ============================================================
# CHART
# ============================================================

if "Nom du fournisseur" in df_cmd.columns:
    data = df_cmd.groupby("Nom du fournisseur")["Montant estimé"].sum().reset_index()

    fig = px.bar(data, x="Nom du fournisseur", y="Montant estimé")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TABLES
# ============================================================

st.subheader("Demandes")
st.dataframe(df_dem)

st.subheader("Commandes")
st.dataframe(df_cmd)

# ============================================================
# DOWNLOAD PDF
# ============================================================

st.subheader("Export PDF")

pdf = create_pdf(df_dem, df_cmd)

st.download_button(
    "📄 Télécharger rapport PDF",
    pdf,
    file_name="rapport_achats.pdf",
    mime="application/pdf"
)
