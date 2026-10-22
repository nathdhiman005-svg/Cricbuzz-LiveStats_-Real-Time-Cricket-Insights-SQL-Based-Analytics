import streamlit as st
from utils.styles import apply_custom_styles, render_hero, THEME
from utils.db_connection import check_db_status, execute_query
from utils.api_handler import get_live_matches, has_valid_api_key

# Page Configuration
st.set_page_config(
    page_title="Cricbuzz LiveStats | Cricket Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Obsidian Dark-Mode & Glassmorphic CSS
apply_custom_styles()

# Check Database & API Status
db_status = check_db_status()
api_active = has_valid_api_key()

# =========================================================================
# SIDEBAR: NAVIGATION, BRANDING & HEALTH STATUS
# =========================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 20px 0;">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🏏</div>
        <div style="font-size: 1.35rem; font-weight: 800; color: #10B981; letter-spacing: -0.02em;">Cricbuzz LiveStats</div>
        <div style="font-size: 0.88rem; color: #E2E8F0; font-weight: 500;">Real-Time Insights & SQL Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Diagnostic Indicators
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #F1F5F9; text-transform: uppercase; margin-bottom: 8px;'>System Status</div>", unsafe_allow_html=True)
    
    if db_status["status"] == "connected":
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <div style="font-size: 0.88rem; color: #34D399; font-weight: 700;">● Database Connected</div>
            <div style="font-size: 0.8rem; color: #E2E8F0; font-weight: 500;">Neon {db_status['dialect'].upper()} ({db_status['table_count']} tables)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.16); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <div style="font-size: 0.88rem; color: #F87171; font-weight: 700;">● Database Offline</div>
            <div style="font-size: 0.8rem; color: #E2E8F0; font-weight: 500;">Check connection in .env</div>
        </div>
        """, unsafe_allow_html=True)
        
    api_badge_color = "#34D399" if api_active else "#FCD34D"
    api_label = "RapidAPI Active" if api_active else "Live Simulation Mode"
    api_desc = "Connected to RapidAPI" if api_active else "High-fidelity live stream"
    
    st.markdown(f"""
    <div style="background: rgba(6, 182, 212, 0.16); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 8px; padding: 10px 14px; margin-bottom: 16px;">
        <div style="font-size: 0.88rem; color: {api_badge_color}; font-weight: 700;">● {api_label}</div>
        <div style="font-size: 0.8rem; color: #E2E8F0; font-weight: 500;">{api_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.85rem; color: #CBD5E1; text-align: center; font-weight: 500;">
        Cricbuzz LiveStats v2.0<br>
        Sports Analytics & SQL Engine
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
# MAIN APP LANDING PAGE
# =========================================================================

render_hero(
    title="Cricket News and Analytics Hub",
    subtitle="",
    badge="Enterprise Sports Technology"
)

# Live Matches Ticker Section
st.markdown("## ⚡ Live Match Ticker")
live_list = get_live_matches()

if live_list:
    featured_matches = live_list[:6]
    for row_idx in range(0, len(featured_matches), 3):
        row_slice = featured_matches[row_idx : row_idx + 3]
        ticker_cols = st.columns(len(row_slice))
        for i, m in enumerate(row_slice):
            with ticker_cols[i]:
                t1 = m.get("team1", {})
                t2 = m.get("team2", {})
                st.markdown(f"""
                <div class="card-container" style="padding: 18px; margin-bottom: 16px; height: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="badge-format">{m.get('format')}</span>
                        <span class="badge-live"><span class="live-dot"></span>LIVE</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1.12rem; color: #FFFFFF; margin-bottom: 4px; min-height: 48px;">{m.get('description')}</div>
                    <div style="font-size: 0.88rem; color: #E2E8F0; margin-bottom: 10px; font-weight: 500;">📍 {m.get('venue', '').split(',')[0]}</div>
                    <div style="background: rgba(0,0,0,0.35); border-radius: 8px; padding: 10px 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.95rem;">
                        <div style="margin-bottom: 4px;"><span style="color: #FFFFFF; font-weight: 700;">{t1.get('code', t1.get('name', 'T1')[:3])}:</span> <span style="color:#34D399; font-weight:800;">{t1.get('score')}</span></div>
                        <div><span style="color: #FFFFFF; font-weight: 700;">{t2.get('code', t2.get('name', 'T2')[:3])}:</span> <span style="color:#67E8F9; font-weight:800;">{t2.get('score')}</span></div>
                    </div>
                    <div style="font-size: 0.88rem; color: #FDE047; font-weight: 700; margin-top: 10px; min-height: 38px;">
                        {m.get('status')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    if len(live_list) > 6:
        st.markdown(f"<div style='color: #94A3B8; font-size: 0.9rem; text-align: right; margin-top: -6px;'>Showing 6 of {len(live_list)} active matches. See the <b>Live Matches</b> page for all scorecards.</div>", unsafe_allow_html=True)

st.markdown("---")

# Feature Modules Navigation Grid
st.markdown("## 🧭 Application Modules")
mod_col1, mod_col2 = st.columns(2)

with mod_col1:
    st.markdown("""
    <div class="card-container">
        <div style="font-size: 1.45rem; font-weight: 800; color: #34D399; margin-bottom: 8px;">
            ⚡ 1. Live Matches & Commentary
        </div>
        <p style="color: #E2E8F0; font-size: 0.98rem; line-height: 1.6;">
            Follow real-time ball-by-ball scorecards, active batter & bowler statistics, current run rates (CRR), required run rates (RRR), and live match commentary powered by the Cricbuzz API.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-container">
        <div style="font-size: 1.45rem; font-weight: 800; color: #67E8F9; margin-bottom: 8px;">
            🔍 2. Analytical Engine
        </div>
        <p style="color: #E2E8F0; font-size: 0.98rem; line-height: 1.6;">
            Interactive query console executing structured analytical questions spanning player benchmarks, bowling metrics, team statistics, and dynamic Plotly charts.
        </p>
    </div>
    """, unsafe_allow_html=True)

with mod_col2:
    st.markdown("""
    <div class="card-container">
        <div style="font-size: 1.45rem; font-weight: 800; color: #FCD34D; margin-bottom: 8px;">
            📊 3. Top Player Statistics & Visualizations
        </div>
        <p style="color: #E2E8F0; font-size: 0.98rem; line-height: 1.6;">
            Explore leaderboards across Test, ODI, and T20I formats for most runs, centuries, batting averages, highest individual scores, most wickets, and best bowling economy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-container">
        <div style="font-size: 1.45rem; font-weight: 800; color: #C084FC; margin-bottom: 8px;">
            🛠️ 4. Player's Record Management
        </div>
        <p style="color: #E2E8F0; font-size: 0.98rem; line-height: 1.6;">
            Manage player rosters and match records with form-based Create, Read, Update, and Delete operations persisting directly to your Neon PostgreSQL database with transaction safety.
        </p>
    </div>
    """, unsafe_allow_html=True)

