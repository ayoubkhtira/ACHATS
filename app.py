st.markdown("""
<style>

/* ================= GLOBAL ================= */

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 1.2rem;
}

/* ================= HEADER PREMIUM ================= */

.app-header {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(30,58,138,0.92),
            rgba(37,99,235,0.90)
        );

    padding: 34px 38px;
    border-radius: 28px;
    margin-bottom: 30px;

    color: white;

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    box-shadow: 0 10px 30px rgba(15,23,42,0.20);

    animation: fadeInUp 0.7s ease;
}

.app-header::before {
    content: "";
    position: absolute;

    width: 300px;
    height: 300px;

    background: rgba(255,255,255,0.06);
    border-radius: 50%;

    top: -120px;
    right: -80px;

    filter: blur(10px);
}

.title-row {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-icon {
    width: 70px;
    height: 70px;

    border-radius: 20px;

    background: rgba(255,255,255,0.12);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 30px;

    transition: 0.3s;
}

.header-icon:hover {
    transform: scale(1.1) rotate(-5deg);
}

.app-header h1 {
    margin: 0;
    font-size: 38px;
    font-weight: 900;
}

.app-header p {
    margin-top: 8px;
    color: rgba(255,255,255,0.85);
}

/* ================= SIDEBAR PREMIUM ================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 10px;

    padding: 12px;
    border-radius: 14px;

    background: rgba(255,255,255,0.05);
    margin-bottom: 10px;

    transition: 0.3s;
}

.sidebar-title:hover {
    transform: translateX(5px);
}

.sidebar-title span {
    color: white;
    font-weight: 800;
}

/* inputs */
section[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
}

/* ================= TABS MODERN ================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: white;
    padding: 10px;
    border-radius: 16px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 20px;

    font-weight: 800;
    transition: 0.3s;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #eff6ff;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
}

/* ================= CARDS ================= */

.card, .metric-card {
    transition: 0.3s;
}

.card:hover, .metric-card:hover {
    transform: translateY(-5px);
}

/* KPI */
.metric-value {
    font-size: 34px;
    font-weight: 900;

    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)
