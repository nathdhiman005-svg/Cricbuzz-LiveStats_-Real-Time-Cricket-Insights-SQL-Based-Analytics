"""
Seed script to populate Neon PostgreSQL with authentic international cricket data from Cricsheet.
Parses genuine international Test, ODI, and T20I matches (2021-2026).
"""

import os
import sys
import json
import zipfile
import re
from datetime import datetime
from collections import defaultdict

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set UTF-8 encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import pandas as pd
from sqlalchemy import text
from utils.db_connection import (

    get_engine,
    init_db,
    teams_table,
    venues_table,
    series_table,
    players_table,
    matches_table,
    player_match_batting_table,
    player_match_bowling_table,
    player_fielding_table,
    partnerships_table,
    player_career_stats_table
)

# Known Stadium Capacities & Country mapping
KNOWN_VENUES = {
    "Narendra Modi Stadium": {"capacity": 132000, "country": "India"},
    "Melbourne Cricket Ground": {"capacity": 100024, "country": "Australia"},
    "Eden Gardens": {"capacity": 68000, "country": "India"},
    "Perth Stadium": {"capacity": 60000, "country": "Australia"},
    "Rajiv Gandhi International Stadium": {"capacity": 55000, "country": "India"},
    "Adelaide Oval": {"capacity": 53583, "country": "Australia"},
    "Greenfield International Stadium": {"capacity": 50000, "country": "India"},
    "Sydney Cricket Ground": {"capacity": 48000, "country": "Australia"},
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium": {"capacity": 50000, "country": "India"},
    "Arun Jaitley Stadium": {"capacity": 41842, "country": "India"},
    "M. Chinnaswamy Stadium": {"capacity": 40000, "country": "India"},
    "M. A. Chidambaram Stadium": {"capacity": 38200, "country": "India"},
    "Wankhede Stadium": {"capacity": 33108, "country": "India"},
    "Lord's": {"capacity": 31100, "country": "England"},
    "The Oval": {"capacity": 27500, "country": "England"},
    "Old Trafford": {"capacity": 26000, "country": "England"},
    "Edgbaston": {"capacity": 25000, "country": "England"},
    "Headingley": {"capacity": 18350, "country": "England"},
    "Trent Bridge": {"capacity": 17500, "country": "England"},
    "National Stadium, Karachi": {"capacity": 34228, "country": "Pakistan"},
    "Gaddafi Stadium": {"capacity": 27000, "country": "Pakistan"},
    "Rawalpindi Cricket Stadium": {"capacity": 28000, "country": "Pakistan"},
    "Wanderers Stadium": {"capacity": 34000, "country": "South Africa"},
    "SuperSport Park": {"capacity": 22000, "country": "South Africa"},
    "Newlands": {"capacity": 25000, "country": "South Africa"},
    "Kingsmead": {"capacity": 25000, "country": "South Africa"},
    "Eden Park": {"capacity": 42000, "country": "New Zealand"},
    "Basin Reserve": {"capacity": 11600, "country": "New Zealand"},
    "Hagley Oval": {"capacity": 18000, "country": "New Zealand"},
    "Kensington Oval": {"capacity": 28000, "country": "West Indies"},
    "Queen's Park Oval": {"capacity": 20000, "country": "West Indies"},
    "R. Premadasa Stadium": {"capacity": 35000, "country": "Sri Lanka"},
    "Pallekele International Cricket Stadium": {"capacity": 35000, "country": "Sri Lanka"},
    "Dubai International Cricket Stadium": {"capacity": 25000, "country": "United Arab Emirates"},
    "Sharjah Cricket Stadium": {"capacity": 16000, "country": "United Arab Emirates"},
    "Sheikh Zayed Stadium": {"capacity": 20000, "country": "United Arab Emirates"},
    "Sher-e-Bangla National Cricket Stadium": {"capacity": 26000, "country": "Bangladesh"},
}

KNOWN_TEAMS = {
    "India": {"country": "India", "short": "IND"},
    "Australia": {"country": "Australia", "short": "AUS"},
    "England": {"country": "England", "short": "ENG"},
    "South Africa": {"country": "South Africa", "short": "RSA"},
    "Pakistan": {"country": "Pakistan", "short": "PAK"},
    "New Zealand": {"country": "New Zealand", "short": "NZL"},
    "West Indies": {"country": "West Indies", "short": "WI"},
    "Sri Lanka": {"country": "Sri Lanka", "short": "SL"},
    "Bangladesh": {"country": "Bangladesh", "short": "BAN"},
    "Afghanistan": {"country": "Afghanistan", "short": "AFG"},
    "Netherlands": {"country": "Netherlands", "short": "NED"},
    "Ireland": {"country": "Ireland", "short": "IRE"},
    "Zimbabwe": {"country": "Zimbabwe", "short": "ZIM"},
    "Scotland": {"country": "Scotland", "short": "SCO"},
    "Nepal": {"country": "Nepal", "short": "NEP"},
    "Oman": {"country": "Oman", "short": "OMA"},
    "United States of America": {"country": "USA", "short": "USA"},
    "Canada": {"country": "Canada", "short": "CAN"},
    "Namibia": {"country": "Namibia", "short": "NAM"},
    "Papua New Guinea": {"country": "Papua New Guinea", "short": "PNG"},
}

KNOWN_PLAYER_PROFILES = {
    "V Kohli": {"full_name": "Virat Kohli", "country": "India", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "RG Sharma": {"full_name": "Rohit Sharma", "country": "India", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "Shubman Gill": {"full_name": "Shubman Gill", "country": "India", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "KL Rahul": {"full_name": "KL Rahul", "country": "India", "role": "Wicket-keeper", "bat": "Right-hand bat", "bowl": "None"},
    "SA Yadav": {"full_name": "Suryakumar Yadav", "country": "India", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "RR Pant": {"full_name": "Rishabh Pant", "country": "India", "role": "Wicket-keeper", "bat": "Left-hand bat", "bowl": "None"},
    "HH Pandya": {"full_name": "Hardik Pandya", "country": "India", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm fast-medium"},
    "RA Jadeja": {"full_name": "Ravindra Jadeja", "country": "India", "role": "All-rounder", "bat": "Left-hand bat", "bowl": "Slow left-arm orthodox"},
    "AR Patel": {"full_name": "Axar Patel", "country": "India", "role": "All-rounder", "bat": "Left-hand bat", "bowl": "Slow left-arm orthodox"},
    "JJ Bumrah": {"full_name": "Jasprit Bumrah", "country": "India", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "Mohammed Shami": {"full_name": "Mohammed Shami", "country": "India", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "Mohammed Siraj": {"full_name": "Mohammed Siraj", "country": "India", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "Kuldeep Yadav": {"full_name": "Kuldeep Yadav", "country": "India", "role": "Bowler", "bat": "Left-hand bat", "bowl": "Left-arm wrist spin"},
    "YS Chahal": {"full_name": "Yuzvendra Chahal", "country": "India", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "SPD Smith": {"full_name": "Steve Smith", "country": "Australia", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "DA Warner": {"full_name": "David Warner", "country": "Australia", "role": "Batsman", "bat": "Left-hand bat", "bowl": "Right-arm legbreak"},
    "TM Head": {"full_name": "Travis Head", "country": "Australia", "role": "Batsman", "bat": "Left-hand bat", "bowl": "Right-arm offbreak"},
    "M Labuschagne": {"full_name": "Marnus Labuschagne", "country": "Australia", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "MR Marsh": {"full_name": "Mitchell Marsh", "country": "Australia", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "GJ Maxwell": {"full_name": "Glenn Maxwell", "country": "Australia", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "MP Stoinis": {"full_name": "Marcus Stoinis", "country": "Australia", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "AT Carey": {"full_name": "Alex Carey", "country": "Australia", "role": "Wicket-keeper", "bat": "Left-hand bat", "bowl": "None"},
    "PJ Cummins": {"full_name": "Pat Cummins", "country": "Australia", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "MA Starc": {"full_name": "Mitchell Starc", "country": "Australia", "role": "Bowler", "bat": "Left-hand bat", "bowl": "Left-arm fast"},
    "JR Hazlewood": {"full_name": "Josh Hazlewood", "country": "Australia", "role": "Bowler", "bat": "Left-hand bat", "bowl": "Right-arm fast-medium"},
    "A Zampa": {"full_name": "Adam Zampa", "country": "Australia", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "JE Root": {"full_name": "Joe Root", "country": "England", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "BA Stokes": {"full_name": "Ben Stokes", "country": "England", "role": "All-rounder", "bat": "Left-hand bat", "bowl": "Right-arm fast-medium"},
    "JC Buttler": {"full_name": "Jos Buttler", "country": "England", "role": "Wicket-keeper", "bat": "Right-hand bat", "bowl": "None"},
    "JM Bairstow": {"full_name": "Jonny Bairstow", "country": "England", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "LS Livingstone": {"full_name": "Liam Livingstone", "country": "England", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "CR Woakes": {"full_name": "Chris Woakes", "country": "England", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm fast-medium"},
    "AU Rashid": {"full_name": "Adil Rashid", "country": "England", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "MA Wood": {"full_name": "Mark Wood", "country": "England", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "Babar Azam": {"full_name": "Babar Azam", "country": "Pakistan", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "Mohammad Rizwan": {"full_name": "Mohammad Rizwan", "country": "Pakistan", "role": "Wicket-keeper", "bat": "Right-hand bat", "bowl": "None"},
    "Fakhar Zaman": {"full_name": "Fakhar Zaman", "country": "Pakistan", "role": "Batsman", "bat": "Left-hand bat", "bowl": "Slow left-arm orthodox"},
    "Shaheen Shah Afridi": {"full_name": "Shaheen Shah Afridi", "country": "Pakistan", "role": "Bowler", "bat": "Left-hand bat", "bowl": "Left-arm fast"},
    "Haris Rauf": {"full_name": "Haris Rauf", "country": "Pakistan", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "Shadab Khan": {"full_name": "Shadab Khan", "country": "Pakistan", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm legbreak"},
    "Q de Kock": {"full_name": "Quinton de Kock", "country": "South Africa", "role": "Wicket-keeper", "bat": "Left-hand bat", "bowl": "None"},
    "H Klaasen": {"full_name": "Heinrich Klaasen", "country": "South Africa", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "T Bavuma": {"full_name": "Temba Bavuma", "country": "South Africa", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "AK Markram": {"full_name": "Aiden Markram", "country": "South Africa", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "DA Miller": {"full_name": "David Miller", "country": "South Africa", "role": "Batsman", "bat": "Left-hand bat", "bowl": "Right-arm offbreak"},
    "K Rabada": {"full_name": "Kagiso Rabada", "country": "South Africa", "role": "Bowler", "bat": "Left-hand bat", "bowl": "Right-arm fast"},
    "A波 Nortje": {"full_name": "Anrich Nortje", "country": "South Africa", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast"},
    "KS Williamson": {"full_name": "Kane Williamson", "country": "New Zealand", "role": "Batsman", "bat": "Right-hand bat", "bowl": "Right-arm offbreak"},
    "DJ Mitchell": {"full_name": "Daryl Mitchell", "country": "New Zealand", "role": "All-rounder", "bat": "Right-hand bat", "bowl": "Right-arm medium"},
    "DP Conway": {"full_name": "Devon Conway", "country": "New Zealand", "role": "Wicket-keeper", "bat": "Left-hand bat", "bowl": "Right-arm medium"},
    "TA Boult": {"full_name": "Trent Boult", "country": "New Zealand", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Left-arm fast-medium"},
    "TG Southee": {"full_name": "Tim Southee", "country": "New Zealand", "role": "Bowler", "bat": "Right-hand bat", "bowl": "Right-arm fast-medium"},
    "MJ Santner": {"full_name": "Mitchell Santner", "country": "New Zealand", "role": "All-rounder", "bat": "Left-hand bat", "bowl": "Slow left-arm orthodox"},
}

def clean_venue_name(raw_venue: str):
    """Extracts stadium name and determines city and capacity."""
    parts = raw_venue.split(",")
    main_name = parts[0].strip()
    city = parts[1].strip() if len(parts) > 1 else "Unknown"
    
    # Match with known venues
    capacity = 30000
    country = "International"
    for v_key, v_info in KNOWN_VENUES.items():
        if v_key.lower() in main_name.lower():
            capacity = v_info["capacity"]
            country = v_info["country"]
            break
            
    return main_name, city, country, capacity

def get_quarter_str(dt: datetime) -> str:
    """Returns 'YYYY-QX' string for a date."""
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"

def seed_database_from_cricsheet(max_matches_per_format=80):
    """Parses real Cricsheet matches and seeds Neon PostgreSQL."""
    print("🚀 Initializing database schema...")
    init_db()
    engine = get_engine()
    
    # Registries to track database IDs
    teams_map = {}      # name -> team_id
    venues_map = {}     # name -> venue_id
    series_map = {}     # name -> series_id
    players_map = {}    # name -> player_id
    
    # Track stats for aggregation
    player_career = defaultdict(lambda: {
        "format": "", "matches": set(), "runs": 0, "balls": 0,
        "dismissals": 0, "fours": 0, "sixes": 0, "centuries": 0, "fifties": 0, "highest_score": 0,
        "overs": 0.0, "legal_balls": 0, "maidens": 0, "runs_conceded": 0, "wickets": 0,
        "catches": 0, "stumpings": 0
    })

    # Prepare batch insertion lists
    teams_to_insert = []
    venues_to_insert = []
    series_to_insert = []
    players_to_insert = []
    matches_to_insert = []
    batting_to_insert = []
    bowling_to_insert = []
    fielding_to_insert = []
    partnerships_to_insert = []

    # Format files to process
    dataset_configs = [
        ("ODIs", "odis_json.zip", "ODI"),
        ("T20Is", "t20s_json.zip", "T20I"),
        ("Tests", "tests_json.zip", "Test"),
    ]

    print("\n📂 Scanning Cricsheet packages...")

    for label, zip_path, fmt_name in dataset_configs:
        if not os.path.exists(zip_path):
            print(f"Skipping {label}: {zip_path} not found.")
            continue
            
        print(f"Processing {label} from {zip_path}...")
        z = zipfile.ZipFile(zip_path)
        all_files = [f for f in z.namelist() if f.endswith(".json")]
        
        # Filter files from 2021 to 2026, prioritizing major teams
        selected_matches = []
        for f in all_files:
            try:
                # Read lightweight meta
                d = json.loads(z.read(f).decode("utf-8"))
                dates = d.get("info", {}).get("dates", [])
                if not dates:
                    continue
                match_date_str = str(dates[0])
                if not any(match_date_str.startswith(str(yr)) for yr in range(2021, 2027)):
                    continue
                    
                teams = d.get("info", {}).get("teams", [])
                # Prioritize top international sides
                major_teams = {"India", "Australia", "England", "South Africa", "Pakistan", "New Zealand", "West Indies", "Sri Lanka"}
                is_major = bool(set(teams) & major_teams)
                
                selected_matches.append((is_major, match_date_str, f, d))
                if len(selected_matches) >= max_matches_per_format * 2:
                    break
            except Exception:
                continue

        # Sort: major matches first, then latest dates
        selected_matches.sort(key=lambda x: (x[0], x[1]), reverse=True)
        final_matches = [item[3] for item in selected_matches[:max_matches_per_format]]
        print(f"  Selected {len(final_matches)} {fmt_name} matches for processing.")

        for d in final_matches:
            info = d.get("info", {})
            dates = info.get("dates", [])
            if not dates:
                continue
                
            match_date_dt = datetime.strptime(str(dates[0])[:10], "%Y-%m-%d").date()
            year = match_date_dt.year
            quarter_str = get_quarter_str(match_date_dt)
            teams = info.get("teams", [])
            if len(teams) < 2:
                continue
                
            team1_name, team2_name = teams[0], teams[1]
            
            # 1. Ensure Teams Exist
            for tname in [team1_name, team2_name]:
                if tname not in teams_map:
                    tid = len(teams_map) + 1
                    tinfo = KNOWN_TEAMS.get(tname, {"country": tname, "short": tname[:3].upper()})
                    teams_map[tname] = tid
                    teams_to_insert.append({
                        "team_id": tid,
                        "team_name": tname,
                        "country": tinfo["country"],
                        "short_code": tinfo["short"]
                    })
                    
            team1_id = teams_map[team1_name]
            team2_id = teams_map[team2_name]
            
            # 2. Ensure Venue Exists
            raw_venue = info.get("venue", "International Stadium")
            v_name, v_city, v_country, v_cap = clean_venue_name(raw_venue)
            if v_name not in venues_map:
                vid = len(venues_map) + 1
                venues_map[v_name] = vid
                venues_to_insert.append({
                    "venue_id": vid,
                    "venue_name": v_name,
                    "city": v_city,
                    "country": v_country,
                    "capacity": v_cap
                })
            venue_id = venues_map[v_name]
            
            # 3. Ensure Series Exists
            event_info = info.get("event", {})
            series_name = event_info.get("name", f"{team1_name} vs {team2_name} {fmt_name} Series {year}")
            if series_name not in series_map:
                sid = len(series_map) + 1
                series_map[series_name] = sid
                series_to_insert.append({
                    "series_id": sid,
                    "series_name": series_name,
                    "host_country": v_country,
                    "match_type": "Tournament" if "Cup" in series_name else "Bilateral",
                    "start_date": match_date_dt,
                    "total_matches": 3
                })
            series_id = series_map[series_name]
            
            # 4. Create Match Record
            match_id = len(matches_to_insert) + 1
            toss_info = info.get("toss", {})
            toss_winner_name = toss_info.get("winner")
            toss_winner_id = teams_map.get(toss_winner_name) if toss_winner_name in teams_map else None
            toss_decision = toss_info.get("decision", "bat")
            
            outcome = info.get("outcome", {})
            winner_name = outcome.get("winner")
            winner_id = teams_map.get(winner_name) if winner_name in teams_map else None
            
            by_info = outcome.get("by", {})
            if "runs" in by_info:
                victory_margin = by_info["runs"]
                victory_type = "runs"
            elif "wickets" in by_info:
                victory_margin = by_info["wickets"]
                victory_type = "wickets"
            else:
                victory_margin = 0
                victory_type = "tie" if outcome.get("result") == "tie" else "no result"
                
            match_desc = f"{team1_name} vs {team2_name}, {event_info.get('match_number', '')} {fmt_name}".strip(", ")
            matches_to_insert.append({
                "match_id": match_id,
                "series_id": series_id,
                "match_desc": match_desc,
                "format": fmt_name,
                "match_date": match_date_dt,
                "team1_id": team1_id,
                "team2_id": team2_id,
                "venue_id": venue_id,
                "toss_winner_id": toss_winner_id,
                "toss_decision": toss_decision,
                "winner_id": winner_id,
                "victory_margin": victory_margin,
                "victory_type": victory_type,
                "status": "Completed"
            })
            
            # 5. Register All Players in this Match
            match_players = info.get("players", {})
            for t_side, p_list in match_players.items():
                t_owner_id = teams_map.get(t_side)
                for p_name in p_list:
                    if p_name not in players_map:
                        pid = len(players_map) + 1
                        players_map[p_name] = pid
                        p_prof = KNOWN_PLAYER_PROFILES.get(p_name, {})
                        full_name = p_prof.get("full_name", p_name)
                        p_country = p_prof.get("country", KNOWN_TEAMS.get(t_side, {}).get("country", "International"))
                        role = p_prof.get("role", "Batsman")
                        bat_style = p_prof.get("bat", "Right-hand bat")
                        bowl_style = p_prof.get("bowl", "Right-arm medium")
                        
                        players_to_insert.append({
                            "player_id": pid,
                            "team_id": t_owner_id,
                            "full_name": full_name,
                            "country": p_country,
                            "playing_role": role,
                            "batting_style": bat_style,
                            "bowling_style": bowl_style
                        })
                        
            # 6. Parse Innings Deliveries (Batting, Bowling, Partnerships, Fielding)
            innings_list = d.get("innings", [])
            for inn_idx, inn in enumerate(innings_list, 1):
                batting_team_name = inn.get("team")
                overs = inn.get("overs", [])
                
                inn_batting = defaultdict(lambda: {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "is_out": 0, "pos": 0})
                inn_bowling = defaultdict(lambda: {"legal_balls": 0, "maidens": 0, "runs": 0, "wickets": 0})
                batting_order = []
                
                # Active partnership tracking
                current_pair = [None, None]  # [striker, non_striker]
                pair_runs = 0
                
                for over_obj in overs:
                    over_num = over_obj.get("over", 0)
                    deliveries = over_obj.get("deliveries", [])
                    over_conceded = 0
                    has_legal = False
                    
                    for deliv in deliveries:
                        batter = deliv.get("batter")
                        bowler = deliv.get("bowler")
                        non_striker = deliv.get("non_striker")
                        runs_dict = deliv.get("runs", {})
                        b_runs = runs_dict.get("batter", 0)
                        e_runs = runs_dict.get("extras", 0)
                        tot_runs = runs_dict.get("total", 0)
                        
                        # Batting order tracking
                        if batter and batter not in batting_order:
                            batting_order.append(batter)
                        if non_striker and non_striker not in batting_order:
                            batting_order.append(non_striker)
                            
                        # Batting increments
                        inn_batting[batter]["runs"] += b_runs
                        extras_dict = deliv.get("extras", {})
                        if "wides" not in extras_dict:
                            inn_batting[batter]["balls"] += 1
                            has_legal = True
                            inn_bowling[bowler]["legal_balls"] += 1
                            
                        if b_runs == 4:
                            inn_batting[batter]["fours"] += 1
                        elif b_runs == 6:
                            inn_batting[batter]["sixes"] += 1
                            
                        # Bowling increments
                        inn_bowling[bowler]["runs"] += (b_runs + extras_dict.get("wides", 0) + extras_dict.get("noballs", 0))
                        over_conceded += (b_runs + extras_dict.get("wides", 0) + extras_dict.get("noballs", 0))
                        
                        # Partnerships
                        pair_key = tuple(sorted([batter, non_striker]))
                        pair_runs += tot_runs
                        
                        # Wickets & Fielding
                        if "wickets" in deliv:
                            for w in deliv["wickets"]:
                                out_player = w.get("player_out")
                                if out_player:
                                    inn_batting[out_player]["is_out"] = 1
                                    
                                w_kind = w.get("kind", "")
                                if w_kind not in ["run out", "retired hurt"]:
                                    inn_bowling[bowler]["wickets"] += 1
                                    
                                # Fielders
                                for fldr in w.get("fielders", []):
                                    f_name = fldr.get("name")
                                    if f_name in players_map:
                                        f_id = players_map[f_name]
                                        c_cnt = 1 if w_kind == "caught" else 0
                                        s_cnt = 1 if w_kind == "stumped" else 0
                                        fielding_to_insert.append({
                                            "match_id": match_id,
                                            "player_id": f_id,
                                            "catches": c_cnt,
                                            "stumpings": s_cnt
                                        })
                                        # Aggregate career fielding
                                        career_key = (f_name, fmt_name)
                                        player_career[career_key]["catches"] += c_cnt
                                        player_career[career_key]["stumpings"] += s_cnt
                                        
                            # End current partnership on wicket
                            p1_idx = batting_order.index(batter) + 1 if batter in batting_order else 1
                            p2_idx = batting_order.index(non_striker) + 1 if non_striker in batting_order else 2
                            if abs(p1_idx - p2_idx) == 1 and pair_runs > 0:
                                p1_id = players_map.get(batter)
                                p2_id = players_map.get(non_striker)
                                if p1_id and p2_id:
                                    partnerships_to_insert.append({
                                        "match_id": match_id,
                                        "innings": inn_idx,
                                        "player1_id": min(p1_id, p2_id),
                                        "player2_id": max(p1_id, p2_id),
                                        "player1_position": min(p1_idx, p2_idx),
                                        "player2_position": max(p1_idx, p2_idx),
                                        "partnership_runs": pair_runs
                                    })
                            pair_runs = 0
                            
                    if has_legal and over_conceded == 0:
                        inn_bowling[bowler]["maidens"] += 1
                        
                # Save Batting Records
                for p_name, b_stat in inn_batting.items():
                    if p_name in players_map:
                        p_id = players_map[p_name]
                        pos = batting_order.index(p_name) + 1 if p_name in batting_order else 11
                        b_runs = b_stat["runs"]
                        b_balls = b_stat["balls"]
                        sr = round((b_runs / b_balls) * 100.0, 2) if b_balls > 0 else 0.0
                        batting_to_insert.append({
                            "match_id": match_id,
                            "player_id": p_id,
                            "innings": inn_idx,
                            "batting_position": pos,
                            "runs": b_runs,
                            "balls": b_balls,
                            "fours": b_stat["fours"],
                            "sixes": b_stat["sixes"],
                            "strike_rate": sr,
                            "is_out": b_stat["is_out"],
                            "match_date": match_date_dt,
                            "year": year,
                            "quarter": quarter_str
                        })
                        # Career aggregation
                        c_key = (p_name, fmt_name)
                        player_career[c_key]["format"] = fmt_name
                        player_career[c_key]["matches"].add(match_id)
                        player_career[c_key]["runs"] += b_runs
                        player_career[c_key]["balls"] += b_balls
                        player_career[c_key]["dismissals"] += b_stat["is_out"]
                        player_career[c_key]["fours"] += b_stat["fours"]
                        player_career[c_key]["sixes"] += b_stat["sixes"]
                        if b_runs > player_career[c_key]["highest_score"]:
                            player_career[c_key]["highest_score"] = b_runs
                        if b_runs >= 100:
                            player_career[c_key]["centuries"] += 1
                        elif b_runs >= 50:
                            player_career[c_key]["fifties"] += 1
                            
                # Save Bowling Records
                for p_name, bw_stat in inn_bowling.items():
                    if p_name in players_map and bw_stat["legal_balls"] > 0:
                        p_id = players_map[p_name]
                        leg_balls = bw_stat["legal_balls"]
                        overs_float = round((leg_balls // 6) + (leg_balls % 6) / 10.0, 1)
                        overs_dec = leg_balls / 6.0
                        econ = round(bw_stat["runs"] / overs_dec, 2) if overs_dec > 0 else 0.0
                        bowling_to_insert.append({
                            "match_id": match_id,
                            "player_id": p_id,
                            "innings": inn_idx,
                            "overs": overs_float,
                            "maidens": bw_stat["maidens"],
                            "runs_conceded": bw_stat["runs"],
                            "wickets": bw_stat["wickets"],
                            "economy_rate": econ,
                            "match_date": match_date_dt,
                            "year": year,
                            "quarter": quarter_str
                        })
                        # Career aggregation
                        c_key = (p_name, fmt_name)
                        player_career[c_key]["format"] = fmt_name
                        player_career[c_key]["matches"].add(match_id)
                        player_career[c_key]["legal_balls"] += leg_balls
                        player_career[c_key]["maidens"] += bw_stat["maidens"]
                        player_career[c_key]["runs_conceded"] += bw_stat["runs"]
                        player_career[c_key]["wickets"] += bw_stat["wickets"]

    # 7. Build Career Stats Records
    career_to_insert = []
    for (p_name, fmt_name), stats in player_career.items():
        if p_name in players_map:
            p_id = players_map[p_name]
            m_count = len(stats["matches"])
            r_tot = stats["runs"]
            dis = stats["dismissals"] if stats["dismissals"] > 0 else 1
            b_avg = round(r_tot / dis, 2)
            sr = round((r_tot / stats["balls"]) * 100.0, 2) if stats["balls"] > 0 else 0.0
            
            w_tot = stats["wickets"]
            rc = stats["runs_conceded"]
            bw_avg = round(rc / w_tot, 2) if w_tot > 0 else 0.0
            ov_dec = stats["legal_balls"] / 6.0
            econ = round(rc / ov_dec, 2) if ov_dec > 0 else 0.0
            
            career_to_insert.append({
                "player_id": p_id,
                "format": fmt_name,
                "matches_played": m_count,
                "total_runs": r_tot,
                "batting_avg": b_avg,
                "strike_rate": sr,
                "centuries": stats["centuries"],
                "fifties": stats["fifties"],
                "highest_score": stats["highest_score"],
                "total_wickets": w_tot,
                "bowling_avg": bw_avg,
                "economy_rate": econ,
                "catches": stats["catches"],
                "stumpings": stats["stumpings"]
            })

    print("\n⚡ Pushing records into Neon PostgreSQL database...")
    
    # Clean existing data safely inside transaction
    with engine.begin() as conn:
        print("  Cleaning old records...")
        conn.execute(text("TRUNCATE TABLE player_career_stats, partnerships, player_fielding, player_match_bowling, player_match_batting, matches, players, series, venues, teams CASCADE;"))

    # Batch Insert Helper
    def bulk_insert(table, data_list, name):
        if not data_list:
            return
        df = pd.DataFrame(data_list)
        df.to_sql(table.name, engine, if_exists="append", index=False, chunksize=1000)
        print(f"  ✅ Inserted {len(data_list):,} records into {name}")

    bulk_insert(teams_table, teams_to_insert, "teams")
    bulk_insert(venues_table, venues_to_insert, "venues")
    bulk_insert(series_table, series_to_insert, "series")
    bulk_insert(players_table, players_to_insert, "players")
    bulk_insert(matches_table, matches_to_insert, "matches")
    bulk_insert(player_match_batting_table, batting_to_insert, "player_match_batting")
    bulk_insert(player_match_bowling_table, bowling_to_insert, "player_match_bowling")
    bulk_insert(player_fielding_table, fielding_to_insert, "player_fielding")
    bulk_insert(partnerships_table, partnerships_to_insert, "partnerships")
    bulk_insert(player_career_stats_table, career_to_insert, "player_career_stats")

    print("\n🎉 Seeding from Cricsheet completed successfully!")

if __name__ == "__main__":
    seed_database_from_cricsheet()
