import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.styles import apply_custom_styles, render_hero
from utils.db_connection import execute_query, execute_non_query, get_engine, sync_db_sequences

st.set_page_config(
    page_title="Record Management | Cricbuzz LiveStats",
    page_icon="🛠️",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="Player's Record Management",
    subtitle="",
    badge="Database Administration"
)

# Fetch available teams for dropdowns
teams_df = execute_query("SELECT team_id, team_name, country FROM teams ORDER BY team_name ASC")
team_options = {row["team_name"]: row["team_id"] for _, row in teams_df.iterrows()} if not teams_df.empty else {"India": 1}

# Tab Navigation
tab_read, tab_create, tab_update, tab_delete = st.tabs([
    "🔍 Search & View Records (Read)",
    "➕ Register New Player (Create)",
    "✏️ Modify Player Profiles (Update)",
    "🗑️ Remove Player (Delete)"
])

# =========================================================================
# TAB 1: READ / SEARCH
# =========================================================================
with tab_read:
    st.subheader("Player Registry & Search Explorer")
    
    s_col1, s_col2, s_col3 = st.columns([2, 1, 1])
    with s_col1:
        search_query = st.text_input("Search Player by Name:", placeholder="e.g., Virat Kohli, Smith, Bumrah...")
    with s_col2:
        country_filter = st.selectbox("Filter Country:", ["All Countries"] + sorted(list(teams_df["country"].unique())))
    with s_col3:
        role_filter = st.selectbox("Filter Role:", ["All Roles", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        
    query_sql = """
        SELECT 
            p.player_id AS "ID",
            p.full_name AS "Full Name",
            p.country AS "Country",
            COALESCE(t.team_name, 'Unassigned') AS "Team",
            p.playing_role AS "Role",
            p.batting_style AS "Batting Style",
            p.bowling_style AS "Bowling Style",
            COALESCE(SUM(cs.total_runs), 0) AS "Career Runs",
            COALESCE(SUM(cs.total_wickets), 0) AS "Career Wickets"
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        LEFT JOIN player_career_stats cs ON p.player_id = cs.player_id
        WHERE 1=1
    """
    params = {}
    
    if search_query:
        query_sql += " AND p.full_name ILIKE :search"
        params["search"] = f"%{search_query}%"
        
    if country_filter != "All Countries":
        query_sql += " AND p.country = :country"
        params["country"] = country_filter
        
    if role_filter != "All Roles":
        query_sql += " AND p.playing_role = :role"
        params["role"] = role_filter
        
    query_sql += " GROUP BY p.player_id, p.full_name, p.country, t.team_name, p.playing_role, p.batting_style, p.bowling_style ORDER BY p.player_id DESC LIMIT 50;"
    
    results_df = execute_query(query_sql, params)
    
    st.markdown(f"**Showing {len(results_df)} matching players:**")
    st.dataframe(results_df, use_container_width=True, hide_index=True)

# =========================================================================
# TAB 2: CREATE
# =========================================================================
with tab_create:
    st.subheader("Register a New International Player")
    st.markdown("Add a new player profile directly into the relational database.")
    
    with st.form("create_player_form"):
        f_col1, f_col2 = st.columns(2)
        
        with f_col1:
            new_name = st.text_input("Full Name *", placeholder="e.g., Yashasvi Jaiswal")
            new_country = st.text_input("Nationality / Country *", placeholder="e.g., India")
            new_team = st.selectbox("Assigned Team *", list(team_options.keys()))
            
        with f_col2:
            new_role = st.selectbox("Primary Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            new_bat = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
            new_bowl = st.selectbox("Bowling Style", [
                "Right-arm fast", "Right-arm fast-medium", "Right-arm medium",
                "Right-arm offbreak", "Right-arm legbreak",
                "Left-arm fast", "Left-arm fast-medium",
                "Slow left-arm orthodox", "Left-arm wrist spin", "None"
            ])
            
        st.markdown("<br>", unsafe_allow_html=True)
        init_career = st.checkbox("Initialize career stats record (Format: T20I / ODI)?", value=True)
        
        submitted = st.form_submit_button("➕ Save Player to Database", use_container_width=True)
        
        if submitted:
            if not new_name.strip() or not new_country.strip():
                st.error("Please fill in both Player Name and Country.")
            else:
                try:
                    sync_db_sequences()
                    team_id = team_options[new_team]
                    engine = get_engine()
                    with engine.begin() as conn:
                        res = conn.execute(
                            text("""
                                INSERT INTO players (full_name, country, team_id, playing_role, batting_style, bowling_style)
                                VALUES (:name, :country, :tid, :role, :bat, :bowl)
                                RETURNING player_id;
                            """),
                            {
                                "name": new_name.strip(),
                                "country": new_country.strip(),
                                "tid": team_id,
                                "role": new_role,
                                "bat": new_bat,
                                "bowl": new_bowl
                            }
                        )
                        new_pid = res.scalar()
                        
                        if init_career:
                            conn.execute(
                                text("""
                                    INSERT INTO player_career_stats (player_id, format, matches_played, total_runs, batting_avg, strike_rate, centuries, fifties, highest_score, total_wickets, bowling_avg, economy_rate, catches, stumpings)
                                    VALUES (:pid, 'T20I', 1, 45, 45.0, 155.0, 0, 0, 45, 0, 0.0, 0.0, 0, 0);
                                """),
                                {"pid": new_pid}
                            )
                            
                    st.success(f"🎉 Successfully created player '{new_name}' with Player ID #{new_pid}!")
                    st.toast(f"Player #{new_pid} registered!", icon="✅")
                except Exception as e:
                    st.error(f"Error creating player: {str(e)}")

# =========================================================================
# TAB 3: UPDATE
# =========================================================================
with tab_update:
    st.subheader("Update Existing Player Profile")
    
    players_list_df = execute_query("SELECT player_id, full_name, country, playing_role FROM players ORDER BY full_name ASC")
    
    if players_list_df.empty:
        st.info("No players available to update.")
    else:
        player_selector = {f"{row['full_name']} ({row['country']} - {row['playing_role']}) [ID: {row['player_id']}]": row['player_id'] for _, row in players_list_df.iterrows()}
        selected_player_str = st.selectbox("Select Player to Edit:", list(player_selector.keys()))
        target_pid = player_selector[selected_player_str]
        
        # Load current data
        current_data = execute_query("SELECT * FROM players WHERE player_id = :pid", {"pid": target_pid})
        
        if not current_data.empty:
            curr = current_data.iloc[0]
            
            with st.form("update_player_form"):
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    up_name = st.text_input("Full Name", value=curr["full_name"])
                    up_country = st.text_input("Country", value=curr["country"])
                    current_team_id = curr.get("team_id")
                    
                    team_names = list(team_options.keys())
                    current_team_name = [k for k, v in team_options.items() if v == current_team_id]
                    def_team_idx = team_names.index(current_team_name[0]) if current_team_name else 0
                    up_team = st.selectbox("Team Affiliation", team_names, index=def_team_idx)
                    
                with u_col2:
                    roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                    def_role_idx = roles.index(curr["playing_role"]) if curr["playing_role"] in roles else 0
                    up_role = st.selectbox("Playing Role", roles, index=def_role_idx)
                    
                    bat_styles = ["Right-hand bat", "Left-hand bat"]
                    def_bat_idx = bat_styles.index(curr.get("batting_style", "Right-hand bat")) if curr.get("batting_style") in bat_styles else 0
                    up_bat = st.selectbox("Batting Technique", bat_styles, index=def_bat_idx)
                    
                    up_bowl = st.text_input("Bowling Technique", value=curr.get("bowling_style") or "Right-arm medium")
                    
                update_submitted = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)
                
                if update_submitted:
                    try:
                        execute_non_query(
                            """
                            UPDATE players
                            SET full_name = :name,
                                country = :country,
                                team_id = :tid,
                                playing_role = :role,
                                batting_style = :bat,
                                bowling_style = :bowl
                            WHERE player_id = :pid;
                            """,
                            {
                                "name": up_name.strip(),
                                "country": up_country.strip(),
                                "tid": team_options[up_team],
                                "role": up_role,
                                "bat": up_bat,
                                "bowl": up_bowl.strip(),
                                "pid": target_pid
                            }
                        )
                        st.success(f"✅ Player #{target_pid} ({up_name}) updated successfully!")
                        st.toast("Profile updated!", icon="💾")
                    except Exception as e:
                        st.error(f"Error updating player: {str(e)}")

# =========================================================================
# TAB 4: DELETE
# =========================================================================
with tab_delete:
    st.subheader("Remove Player from Database")
    st.warning("⚠️ Deleting a player cascades and permanently removes their associated career stats, batting entries, and bowling records.")
    
    if not players_list_df.empty:
        del_selector = {f"{row['full_name']} ({row['country']}) [ID: {row['player_id']}]": row['player_id'] for _, row in players_list_df.iterrows()}
        del_player_str = st.selectbox("Select Player to Delete:", list(del_selector.keys()), key="del_select")
        del_pid = del_selector[del_player_str]
        
        confirm_check = st.checkbox(f"Yes, I confirm I want to permanently delete Player #{del_pid}")
        
        if st.button("🗑️ Permanently Delete Player", type="primary", disabled=not confirm_check):
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    # Cascade delete associated records
                    conn.execute(text("DELETE FROM player_career_stats WHERE player_id = :pid"), {"pid": del_pid})
                    conn.execute(text("DELETE FROM player_fielding WHERE player_id = :pid"), {"pid": del_pid})
                    conn.execute(text("DELETE FROM player_match_batting WHERE player_id = :pid"), {"pid": del_pid})
                    conn.execute(text("DELETE FROM player_match_bowling WHERE player_id = :pid"), {"pid": del_pid})
                    conn.execute(text("DELETE FROM partnerships WHERE player1_id = :pid OR player2_id = :pid"), {"pid": del_pid})
                    conn.execute(text("DELETE FROM players WHERE player_id = :pid"), {"pid": del_pid})
                    
                st.success(f"Player #{del_pid} and all associated records have been deleted.")
                st.toast("Player record deleted.", icon="🗑️")
            except Exception as e:
                st.error(f"Error deleting player: {str(e)}")
