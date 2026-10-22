import streamlit as st
from utils.styles import apply_custom_styles, render_hero

st.set_page_config(
    page_title="Home & Platform Guide | Cricbuzz LiveStats",
    page_icon="🏠",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="Cricket Intelligence & Platform Guide",
    subtitle="Comprehensive breakdown of industry use cases, analytical capabilities, and quick-start navigation.",
    badge="Platform Overview"
)

# Quick-Start Navigation Hub
st.subheader("🚀 Quick-Start Navigation Guide")
st.markdown("<p style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.95rem;'>Select a module from the left sidebar to start exploring real-time telemetry, leaderboards, analytical queries, or database management.</p>", unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    st.markdown("""
    <div class="card-container" style="border-left: 4px solid #10B981; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #34D399;">
                🔴 Live Matches & Telemetry
            </div>
            <span class="badge-format" style="border-color: rgba(16,185,129,0.5); color: #34D399; background: rgba(16,185,129,0.15);">Sidebar: Live Matches</span>
        </div>
        <p style="color: #E2E8F0; font-size: 0.94rem; line-height: 1.6; margin-bottom: 12px;">
            Stream real-time ball-by-ball updates, live scorecards, active batter & bowler statistics, current run rates (CRR), required run rates (RRR), and live match commentary powered by the Cricbuzz API.
        </p>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">
            ⚡ Features: Auto-sync telemetry • Live over summaries • Commentary feeds
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-container" style="border-left: 4px solid #F59E0B; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #FCD34D;">
                ⚡ Analytical Engine
            </div>
            <span class="badge-format" style="border-color: rgba(245,158,11,0.5); color: #FCD34D; background: rgba(245,158,11,0.15);">Sidebar: Analytics Hub</span>
        </div>
        <p style="color: #E2E8F0; font-size: 0.94rem; line-height: 1.6; margin-bottom: 12px;">
            Execute 25 curated analytical queries covering historical team head-to-heads, death-over strike rates, bowling economies, partnership trends, and tight finish distributions with dynamic parameter controls.
        </p>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">
            🔍 Features: Parameterized filters • Instant SQL execution • Interactive Plotly charts
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="card-container" style="border-left: 4px solid #06B6D4; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #67E8F9;">
                📊 Top Player Statistics
            </div>
            <span class="badge-format" style="border-color: rgba(6,182,212,0.5); color: #67E8F9; background: rgba(6,182,212,0.15);">Sidebar: Top Stats</span>
        </div>
        <p style="color: #E2E8F0; font-size: 0.94rem; line-height: 1.6; margin-bottom: 12px;">
            Explore career benchmarks and leaderboards across international formats (ODI, T20I, Test) for most runs, centuries, batting averages, highest scores, wickets, and bowling economies.
        </p>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">
            📈 Features: Format comparative tabs • Career aggregates • Visual stat breakdowns
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-container" style="border-left: 4px solid #C084FC; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #C084FC;">
                🛠️ Player's Record Management
            </div>
            <span class="badge-format" style="border-color: rgba(192,132,252,0.5); color: #C084FC; background: rgba(192,132,252,0.15);">Sidebar: Record Management</span>
        </div>
        <p style="color: #E2E8F0; font-size: 0.94rem; line-height: 1.6; margin-bottom: 12px;">
            Manage player rosters and match records with form-based Create, Read, Update, and Delete operations persisting directly to your PostgreSQL database with transaction safety.
        </p>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">
            🔒 Features: Live CRUD forms • Transaction validation • Database integrity
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# Industry & Business Use Cases Grid
st.subheader("💼 Industry & Business Use Cases")
st.markdown("<p style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.95rem;'>How live streaming analytics and persistent historical relational modeling empower sports organizations.</p>", unsafe_allow_html=True)

uc1, uc2, uc3 = st.columns(3)

with uc1:
    st.markdown("""
    <div class="card-container" style="border-top: 3px solid #10B981; height: 100%;">
        <div style="font-size: 1.18rem; font-weight: 700; color: #34D399; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            📺 Sports Media & Broadcast
        </div>
        <ul style="color: #E2E8F0; font-size: 0.92rem; line-height: 1.7; padding-left: 18px; margin-bottom: 0;">
            <li>Real-time ball updates for live digital commentary feeds</li>
            <li>Player form analytics for pre-match and mid-innings studio shows</li>
            <li>Historical matchup trends and win probability predictions</li>
            <li>Phase-by-phase scoring rate graphics and milestone alerts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with uc2:
    st.markdown("""
    <div class="card-container" style="border-top: 3px solid #06B6D4; height: 100%;">
        <div style="font-size: 1.18rem; font-weight: 700; color: #67E8F9; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            🎮 Fantasy Cricket Platforms
        </div>
        <ul style="color: #E2E8F0; font-size: 0.92rem; line-height: 1.7; padding-left: 18px; margin-bottom: 0;">
            <li>Player recent form tracking (Last 5 vs 10 matches)</li>
            <li>Head-to-head bowler vs batter match-ups for team selection</li>
            <li>Live strike rates, boundary percentages, and wicket economy metrics</li>
            <li>Dynamic captaincy and vice-captaincy pick recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with uc3:
    st.markdown("""
    <div class="card-container" style="border-top: 3px solid #F59E0B; height: 100%;">
        <div style="font-size: 1.18rem; font-weight: 700; color: #FCD34D; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            📈 Cricket Analytics Firms
        </div>
        <ul style="color: #E2E8F0; font-size: 0.92rem; line-height: 1.7; padding-left: 18px; margin-bottom: 0;">
            <li>Multi-discipline weighted ranking models across formats</li>
            <li>Quarter-over-quarter and career trajectory evaluation</li>
            <li>Pressure performance modeling in close match finishes</li>
            <li>Venue-specific toss advantage and pitch behavioral analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
