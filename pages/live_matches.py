import streamlit as st
import time
from utils.styles import apply_custom_styles, render_hero, render_scorecard_banner
from utils.api_handler import (
    get_live_matches,
    get_match_details,
    get_match_commentary,
    sync_completed_match_to_db,
    has_valid_api_key
)

st.set_page_config(
    page_title="Live Cricket Matches | Cricbuzz LiveStats",
    page_icon="⚡",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="Real-Time Live Match Center",
    subtitle="Ball-by-ball scorecards, on-pitch batter and bowler telemetry, and live commentary powered by Cricbuzz API.",
    badge="Live Cricket Ticker"
)

# Header Control Bar
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])

with ctrl_col1:
    api_active = has_valid_api_key()
    if api_active:
        st.markdown('<span style="color:#10B981; font-weight:600;">● Connected to Cricbuzz RapidAPI</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#F59E0B; font-weight:600;">● Live Simulation Engine (High-Fidelity Real-Time Mode)</span>', unsafe_allow_html=True)

with ctrl_col2:
    if st.button("🔄 Refresh Live Scores", use_container_width=True):
        st.toast("Refreshing live match data from Cricbuzz API...", icon="⚡")
        time.sleep(0.5)
        st.rerun()

with ctrl_col3:
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)

# Fetch active matches
matches = get_live_matches()

if not matches:
    st.info("No live international matches are currently in progress. Please check back during scheduled match hours or use simulation mode.")
else:
    # Match Selector
    match_options = {f"{m['description']} [{m['format']}] - {m['status'][:35]}...": m['id'] for m in matches}
    selected_label = st.selectbox("🎯 Select Match to View Scorecard & Telemetry:", list(match_options.keys()))
    selected_id = match_options[selected_label]
    
    match = get_match_details(selected_id)
    
    if match:
        # Full Scorecard Hero Banner
        render_scorecard_banner(match)
        
        state = match.get("current_state")
        if state:
            # Active In-Play Telemetry Columns
            tel_col1, tel_col2 = st.columns([1, 1])
            
            with tel_col1:
                st.markdown("""
                <div style="font-size: 1.1rem; font-weight: 700; color: #10B981; margin-bottom: 8px;">
                    🏏 Batters at the Crease
                </div>
                """, unsafe_allow_html=True)
                
                batters = state.get("batters", [])
                for b in batters:
                    on_strike_badge = '<span style="background: rgba(16,185,129,0.2); color:#34D399; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;">STRIKER *</span>' if b.get("on_strike") else ""
                    st.markdown(f"""
                    <div style="background: rgba(17,24,39,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: #FFFFFF; font-size: 1.15rem;">{b['name']} {on_strike_badge}</div>
                            <div style="font-size: 0.88rem; color: #E2E8F0; font-weight: 500;">Fours: {b.get('fours', 0)} | Sixes: {b.get('sixes', 0)}</div>
                        </div>
                        <div style="text-align: right; font-family: 'JetBrains Mono', monospace;">
                            <div style="font-size: 1.4rem; font-weight: 800; color: #FCD34D;">{b['runs']} <span style="font-size: 0.95rem; color:#CBD5E1; font-weight: 600;">({b['balls']}b)</span></div>
                            <div style="font-size: 0.88rem; color: #34D399; font-weight: 700;">SR: {b.get('sr', 0.0)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with tel_col2:
                st.markdown("""
                <div style="font-size: 1.1rem; font-weight: 700; color: #06B6D4; margin-bottom: 8px;">
                    🎯 Current Bowler & Run Rate
                </div>
                """, unsafe_allow_html=True)
                
                bowler = state.get("bowler", {})
                st.markdown(f"""
                <div style="background: rgba(17,24,39,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; color: #FFFFFF; font-size: 1.15rem;">{bowler.get('name', 'Active Bowler')}</div>
                        <div style="font-size: 0.88rem; color: #E2E8F0; font-weight: 500;">Maidens: {bowler.get('maidens', 0)} | Economy: {bowler.get('econ', 0.0)}</div>
                    </div>
                    <div style="text-align: right; font-family: 'JetBrains Mono', monospace;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #67E8F9;">
                            {bowler.get('wickets', 0)} / {bowler.get('runs', 0)}
                            <span style="font-size: 0.95rem; color:#CBD5E1; font-weight: 600;">({bowler.get('overs', '0.0')} ov)</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                
                # Run Rate and Target Cards
                crr = state.get("crr")
                rrr = state.get("rrr")
                req_runs = state.get("required_runs")
                balls_rem = state.get("balls_remaining")
                
                m_sub1, m_sub2 = st.columns(2)
                with m_sub1:
                    st.metric(label="Current Run Rate (CRR)", value=f"{crr:.2f}" if crr else "-")
                with m_sub2:
                    st.metric(label="Required Run Rate (RRR)", value=f"{rrr:.2f}" if rrr else "N/A", delta=f"{req_runs} runs in {balls_rem} balls" if req_runs else None)

            # Recent Over Deliveries Strip
            recent_overs = state.get("recent_overs", [])
            if recent_overs:
                st.markdown("<div style='font-size: 0.92rem; font-weight: 600; color: #E2E8F0; margin-top: 10px; margin-bottom: 6px;'>Recent Deliveries (Last 2 Overs):</div>", unsafe_allow_html=True)
                balls_html = ""
                for ball in recent_overs:
                    if ball == "|":
                        balls_html += '<span style="color:#94A3B8; font-weight:800; margin: 0 6px;">|</span>'
                    elif ball == "W":
                        balls_html += '<span style="background:#EF4444; color:#FFF; font-weight:800; padding: 4px 10px; border-radius:50%; margin: 0 3px; font-size: 0.8rem;">W</span>'
                    elif ball in ["4", "6"]:
                        balls_html += f'<span style="background:#10B981; color:#FFF; font-weight:800; padding: 4px 10px; border-radius:50%; margin: 0 3px; font-size: 0.8rem;">{ball}</span>'
                    elif ball == "0":
                        balls_html += '<span style="background:rgba(255,255,255,0.14); color:#F1F5F9; font-weight:700; padding: 4px 9px; border-radius:50%; margin: 0 3px; font-size: 0.8rem;">•</span>'
                    else:
                        balls_html += f'<span style="background:rgba(6,182,212,0.25); color:#67E8F9; font-weight:700; padding: 4px 10px; border-radius:50%; margin: 0 3px; font-size: 0.8rem;">{ball}</span>'
                
        else:
            st.info("ℹ️ Session paused (Stumps / Innings Break / Weather Delay). In-play telemetry (active batters & bowlers) will display when play resumes.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Commentary Stream and Database Sync Pipeline
        comm_col, sync_col = st.columns([2, 1])

        with comm_col:
            st.subheader("🎙️ Live Ball-by-Ball Commentary")
            commentary = get_match_commentary(selected_id)
            if commentary:
                for c in commentary:
                    st.markdown(f"""
                    <div style="background: rgba(17,24,39,0.5); border-left: 3px solid #10B981; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #10B981;">Over {c.get('over')}:</span>
                        <span style="color: #F8FAFC; margin-left: 8px; font-size: 0.95rem;">{c.get('text')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Live commentary feed starting shortly.")

        with sync_col:
            st.subheader("📥 Data Sync Pipeline")
            if st.button("⚡ Sync Match into Database", use_container_width=True):
                with st.spinner("Executing database ingestion transaction..."):
                    sync_res = sync_completed_match_to_db(selected_id)
                    if sync_res["success"]:
                        st.success(sync_res["message"])
                    else:
                        st.error(sync_res["message"])

if auto_refresh:
    time.sleep(30)
    st.rerun()
