import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_custom_styles, render_hero, get_plotly_dark_template
from utils.db_connection import execute_query

st.set_page_config(
    page_title="Top Player Statistics | Cricbuzz LiveStats",
    page_icon="📊",
    layout="wide"
)

apply_custom_styles()
dark_template = get_plotly_dark_template()

render_hero(
    title="Top International Cricket Statistics",
    subtitle="Interactive leaderboards, scoring milestones, and bowling effectiveness benchmarks across cricket formats.",
    badge="Player Analytics"
)

# Format & Filter Selector
filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])

with filter_col1:
    selected_format = st.selectbox("🏏 Select Format:", ["ODI", "Test", "T20I"], index=0)

with filter_col2:
    top_limit = st.slider("Display Top Players:", min_value=5, max_value=25, value=10, step=5)

# Tabs: Batting vs Bowling vs Milestones
tab_bat, tab_bowl, tab_milestones = st.tabs([
    "🏏 Leading Batters (Runs & Averages)",
    "🎯 Premier Bowlers (Wickets & Economy)",
    "🏆 Centuries & Peak Innings"
])

# =========================================================================
# TAB 1: BATTING LEADERBOARDS
# =========================================================================
with tab_bat:
    st.subheader(f"Top {top_limit} Run Scorers in {selected_format} Cricket")
    
    bat_sql = """
        SELECT 
            p.full_name AS "Player Name",
            p.country AS "Country",
            p.batting_style AS "Batting Style",
            cs.matches_played AS "Matches",
            cs.total_runs AS "Total Runs",
            cs.batting_avg AS "Batting Avg",
            cs.strike_rate AS "Strike Rate",
            cs.centuries AS "Centuries",
            cs.fifties AS "Fifties",
            cs.highest_score AS "High Score"
        FROM player_career_stats cs
        JOIN players p ON cs.player_id = p.player_id
        WHERE cs.format = :fmt
        ORDER BY cs.total_runs DESC
        LIMIT :lim;
    """
    df_bat = execute_query(bat_sql, {"fmt": selected_format, "lim": top_limit})
    
    if not df_bat.empty:
        # Metrics Top Highlight
        leader = df_bat.iloc[0]
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Format Run Leader", leader["Player Name"], f"{leader['Total Runs']:,} Runs")
        with m2:
            st.metric("Top Batting Average", f"{df_bat['Batting Avg'].max():.2f}", f"Peak: {leader['Player Name']}")
        with m3:
            st.metric("Most Centuries", f"{int(df_bat['Centuries'].max())}", "Hundreds")
        with m4:
            st.metric("Highest Strike Rate", f"{df_bat['Strike Rate'].max():.2f}", "Balls / 100")
            
        # Plotly Bar Chart: Total Runs & Average
        fig_bat = px.bar(
            df_bat,
            x="Player Name",
            y="Total Runs",
            color="Batting Avg",
            color_continuous_scale="Viridis",
            hover_data=["Country", "Strike Rate", "Centuries", "High Score"],
            title=f"Total Runs and Batting Averages ({selected_format})"
        )
        fig_bat.update_layout(template=dark_template, height=420)
        st.plotly_chart(fig_bat, use_container_width=True)
        
        # Interactive Table
        st.dataframe(df_bat, use_container_width=True, hide_index=True)
    else:
        st.info("No records found for selected format.")

# =========================================================================
# TAB 2: BOWLING LEADERBOARDS
# =========================================================================
with tab_bowl:
    st.subheader(f"Top {top_limit} Wicket-Takers in {selected_format} Cricket")
    
    bowl_sql = """
        SELECT 
            p.full_name AS "Bowler Name",
            p.country AS "Country",
            p.bowling_style AS "Bowling Style",
            cs.matches_played AS "Matches",
            cs.total_wickets AS "Wickets Taken",
            cs.bowling_avg AS "Bowling Avg",
            cs.economy_rate AS "Economy Rate",
            cs.catches AS "Catches"
        FROM player_career_stats cs
        JOIN players p ON cs.player_id = p.player_id
        WHERE cs.format = :fmt AND cs.total_wickets > 0
        ORDER BY cs.total_wickets DESC, cs.economy_rate ASC
        LIMIT :lim;
    """
    df_bowl = execute_query(bowl_sql, {"fmt": selected_format, "lim": top_limit})
    
    if not df_bowl.empty:
        # Metrics Top Highlight
        w_leader = df_bowl.iloc[0]
        w1, w2, w3, w4 = st.columns(4)
        with w1:
            st.metric("Leading Wicket-Taker", w_leader["Bowler Name"], f"{w_leader['Wickets Taken']} Wickets")
        with w2:
            st.metric("Best Bowling Average", f"{df_bowl['Bowling Avg'].min():.2f}", "Runs/Wicket")
        with w3:
            st.metric("Best Economy Rate", f"{df_bowl['Economy Rate'].min():.2f}", "Runs/Over")
        with w4:
            st.metric("Most Catches Taken", f"{int(df_bowl['Catches'].max())}", "Fielding")
            
        # Scatter Plot: Wickets vs Economy Rate
        fig_bowl = px.scatter(
            df_bowl,
            x="Economy Rate",
            y="Wickets Taken",
            size="Wickets Taken",
            color="Country",
            hover_name="Bowler Name",
            hover_data=["Bowling Avg", "Matches"],
            title=f"Wickets vs Economy Rate Analysis ({selected_format})"
        )
        fig_bowl.update_layout(template=dark_template, height=420)
        st.plotly_chart(fig_bowl, use_container_width=True)
        
        # Interactive Table
        st.dataframe(df_bowl, use_container_width=True, hide_index=True)
    else:
        st.info("No bowling records available for selected criteria.")

# =========================================================================
# TAB 3: CENTURIES & PEAK INNINGS
# =========================================================================
with tab_milestones:
    st.subheader(f"Single-Innings Benchmarks ({selected_format})")
    
    peak_sql = """
        SELECT 
            p.full_name AS "Player Name",
            p.country AS "Country",
            b.runs AS "Runs Scored",
            b.balls AS "Balls Faced",
            b.fours AS "Fours",
            b.sixes AS "Sixes",
            b.strike_rate AS "Strike Rate",
            b.match_date AS "Match Date",
            m.match_desc AS "Match Description"
        FROM player_match_batting b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.format = :fmt
        ORDER BY b.runs DESC
        LIMIT :lim;
    """
    df_peak = execute_query(peak_sql, {"fmt": selected_format, "lim": top_limit})
    
    if not df_peak.empty:
        fig_peak = px.bar(
            df_peak,
            x="Player Name",
            y="Runs Scored",
            color="Strike Rate",
            color_continuous_scale="Plasma",
            hover_data=["Balls Faced", "Fours", "Sixes", "Match Date"],
            title=f"Highest Individual Innings ({selected_format})"
        )
        fig_peak.update_layout(template=dark_template, height=420)
        st.plotly_chart(fig_peak, use_container_width=True)
        
        st.dataframe(df_peak, use_container_width=True, hide_index=True)
    else:
        st.info("No innings records found.")
