"""
Design System, Custom Theme, and UI Component Engine for Cricbuzz LiveStats.
Features obsidian dark-mode, glassmorphism, high-contrast typography, animated live badges, and Plotly templates.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# High-Contrast Design Tokens
THEME = {
    "bg_dark": "#0B0F19",
    "surface": "rgba(17, 24, 39, 0.88)",
    "surface_hover": "rgba(31, 41, 55, 0.95)",
    "border": "rgba(255, 255, 255, 0.14)",
    "border_glow": "rgba(16, 185, 129, 0.5)",
    "primary_emerald": "#10B981",
    "secondary_cyan": "#06B6D4",
    "accent_gold": "#F59E0B",
    "live_red": "#EF4444",
    "text_primary": "#FFFFFF",
    "text_secondary": "#E2E8F0",
    "text_muted": "#CBD5E1"
}

CUSTOM_CSS = """
<style>
/* Import Google Fonts: Outfit & JetBrains Mono */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Global Reset & Typography */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #F8FAFC !important;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 15%, #131C2E 0%, #0B0F19 60%, #050811 100%) !important;
    background-attachment: fixed !important;
}

/* Top Streamlit Header Bar Fix */
header[data-testid="stHeader"] {
    background: rgba(11, 15, 25, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

header[data-testid="stHeader"] * {
    color: #F1F5F9 !important;
}

/* Sidebar Canvas */
section[data-testid="stSidebar"] {
    background: #0B0F19 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(24px) !important;
}

/* Sidebar Navigation Items (High-Contrast Links) */
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] nav {
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}

[data-testid="stSidebarNav"] ul,
section[data-testid="stSidebar"] nav ul {
    gap: 8px !important;
}

[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] nav a,
section[data-testid="stSidebar"] a {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    margin-bottom: 6px !important;
    transition: all 0.2s ease-in-out !important;
    text-decoration: none !important;
    color: #F8FAFC !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNavLink"] span,
[data-testid="stSidebarNavLink"] div,
section[data-testid="stSidebar"] nav a span,
section[data-testid="stSidebar"] nav a div,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a div {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    text-transform: capitalize !important;
}

[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNavLink"]:hover,
section[data-testid="stSidebar"] nav a:hover,
section[data-testid="stSidebar"] a:hover {
    background: rgba(16, 185, 129, 0.22) !important;
    border-color: rgba(16, 185, 129, 0.5) !important;
    transform: translateX(4px) !important;
}

[data-testid="stSidebarNav"] a:hover span,
[data-testid="stSidebarNavLink"]:hover span,
section[data-testid="stSidebar"] nav a:hover span,
section[data-testid="stSidebar"] a:hover span {
    color: #34D399 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNavLink"][aria-current="page"],
section[data-testid="stSidebar"] nav a[aria-current="page"],
section[data-testid="stSidebar"] a[aria-current="page"] {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.35) 0%, rgba(6, 182, 212, 0.25) 100%) !important;
    border-color: #10B981 !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] span,
[data-testid="stSidebarNavLink"][aria-current="page"] span,
section[data-testid="stSidebar"] nav a[aria-current="page"] span,
section[data-testid="stSidebar"] a[aria-current="page"] span {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* High-Contrast Headings */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stHeadingWithActionElements"],
[data-testid="stHeadingWithActionElements"] *,
div[data-testid="stHeading"] *,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}

div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    color: #E2E8F0;
}

h2, .stMarkdown h2, div[data-testid="stMarkdownContainer"] h2 {
    color: #FFFFFF !important;
    font-size: 1.65rem !important;
    padding-bottom: 6px !important;
    margin-top: 24px !important;
    margin-bottom: 14px !important;
}

h3, .stMarkdown h3, div[data-testid="stMarkdownContainer"] h3 {
    color: #F1F5F9 !important;
    font-size: 1.3rem !important;
}

/* Glassmorphism Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(14px) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(16, 185, 129, 0.5) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2) !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] label,
div[data-testid="stMetricLabel"] p {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    font-size: 2.0rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-testid="stMetricDelta"] {
    color: #34D399 !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
    transition: all 0.2s ease-in-out !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
    background: linear-gradient(135deg, #34D399 0%, #10B981 100%) !important;
}

/* Form inputs & Selectboxes */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(17, 24, 39, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover {
    border-color: #10B981 !important;
}

/* Input label high contrast */
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p {
    color: #F1F5F9 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Dataframe & Tables */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    color: #CBD5E1 !important;
    padding: 10px 22px !important;
    border-radius: 8px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #10B981 !important;
    border-bottom: 3px solid #10B981 !important;
}

/* Code block container */
pre, code {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: rgba(15, 23, 42, 0.9) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #A7F3D0 !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: rgba(17, 24, 39, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(12px);
}

div[data-testid="stExpander"] summary {
    color: #F1F5F9 !important;
    font-weight: 600 !important;
}

/* Custom Live Pill Animation */
@keyframes pulseGlow {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1.05); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.live-dot {
    width: 10px;
    height: 10px;
    background-color: #EF4444;
    border-radius: 50%;
    display: inline-block;
    animation: pulseGlow 1.8s infinite;
    margin-right: 8px;
}

.badge-live {
    display: inline-flex;
    align-items: center;
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.5);
    color: #FCA5A5;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-format {
    display: inline-block;
    background: rgba(6, 182, 212, 0.2);
    border: 1px solid rgba(6, 182, 212, 0.45);
    color: #67E8F9;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.card-container {
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    margin-bottom: 20px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.card-container:hover {
    border-color: rgba(16, 185, 129, 0.4);
}

.card-container p {
    color: #CBD5E1 !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 0%, #A7F3D0 45%, #10B981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #CBD5E1 !important;
    font-weight: 400;
    margin-bottom: 24px;
    line-height: 1.5;
}

.sql-badge {
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
</style>
"""

def apply_custom_styles():
    """Injects global CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_hero(title: str, subtitle: str = "", badge: str = "LiveStats"):
    """Renders a stylish gradient hero banner."""
    sub_html = f'<div class="hero-subtitle">{subtitle}</div>' if subtitle else ""
    badge_html = f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;"><span class="badge-format">🏏 {badge}</span></div>' if badge else ""
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        {badge_html}
        <div class="hero-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_live_indicator():
    """Renders an animated pulse live badge."""
    return '<span class="badge-live"><span class="live-dot"></span>LIVE MATCH</span>'

def render_scorecard_banner(match_data: dict):
    """Renders an authentic, TV broadcast-style cricket match banner."""
    m = match_data
    t1 = m.get("team1", {})
    t2 = m.get("team2", {})
    status = m.get("status", "Live")
    fmt = m.get("format", "ODI")
    venue = m.get("venue", "Cricket Stadium")
    code1 = f"({t1['code']})" if t1.get('code') else ""
    code2 = f"({t2['code']})" if t2.get('code') else ""
    toss_display = f"🪙 {m.get('toss')}" if m.get('toss') and m.get('toss') != status else ""

    st.markdown(f"""
    <div class="card-container" style="border-left: 4px solid #10B981;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="badge-live"><span class="live-dot"></span>LIVE</span>
                <span class="badge-format">{fmt}</span>
                <span style="color: #CBD5E1; font-size: 0.9rem; font-weight: 500;">📍 {venue}</span>
            </div>
            <span style="color: #34D399; font-size: 0.9rem; font-weight: 700;">{m.get('series', '')}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 20px; padding: 10px 0;">
            <!-- Team 1 -->
            <div>
                <div style="font-size: 1.35rem; font-weight: 700; color: #FFFFFF;">{t1.get('name', 'Team 1')} {code1}</div>
                <div style="font-size: 1.9rem; font-weight: 800; color: #10B981; font-family: 'JetBrains Mono', monospace;">
                    {t1.get('score', '-')} <span style="font-size: 0.95rem; font-weight: 500; color: #CBD5E1;">({t1.get('overs', '-')} ov)</span>
                </div>
            </div>
            <!-- VS Separator -->
            <div style="text-align: center; color: #94A3B8; font-weight: 800; font-size: 1.2rem;">VS</div>
            <!-- Team 2 -->
            <div style="text-align: right;">
                <div style="font-size: 1.35rem; font-weight: 700; color: #FFFFFF;">{t2.get('name', 'Team 2')} {code2}</div>
                <div style="font-size: 1.9rem; font-weight: 800; color: #06B6D4; font-family: 'JetBrains Mono', monospace;">
                    {t2.get('score', '-')} <span style="font-size: 0.95rem; font-weight: 500; color: #CBD5E1;">({t2.get('overs', '-')} ov)</span>
                </div>
            </div>
        </div>
        <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 1.0rem; font-weight: 700; color: #FCD34D;">⚡ {status}</div>
            <div style="font-size: 0.9rem; color: #E2E8F0; font-weight: 500;">{toss_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_plotly_dark_template():
    """Returns a unified Plotly dark theme tailored to our emerald/cyan palette."""
    return go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="rgba(11, 15, 25, 0.0)",
            plot_bgcolor="rgba(17, 24, 39, 0.5)",
            font=dict(family="Outfit, sans-serif", color="#F8FAFC", size=13),
            xaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.08)",
                zerolinecolor="rgba(255, 255, 255, 0.15)",
                showline=True,
                linecolor="rgba(255, 255, 255, 0.15)",
                tickfont=dict(color="#E2E8F0")
            ),
            yaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.08)",
                zerolinecolor="rgba(255, 255, 255, 0.15)",
                showline=True,
                linecolor="rgba(255, 255, 255, 0.15)",
                tickfont=dict(color="#E2E8F0")
            ),
            colorway=["#10B981", "#06B6D4", "#F59E0B", "#8B5CF6", "#EC4899", "#3B82F6"]
        )
    )
