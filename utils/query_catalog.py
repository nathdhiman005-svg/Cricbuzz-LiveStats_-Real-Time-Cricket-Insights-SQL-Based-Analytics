"""
Catalog of 25 comprehensive SQL analytical queries for cricket insights.
Structured by complexity tier: Beginner (Q1-Q8), Intermediate (Q9-Q16), Advanced (Q17-Q25).
Provides SQL statements, explanations, UI input parameter schemas, and Plotly visualization metadata.
"""

from typing import Dict, List, Any, Optional

QUERIES: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # BEGINNER LEVEL (QUESTIONS 1 - 8)
    # =========================================================================
    "Q1": {
        "id": "Q1",
        "number": 1,
        "level": "Beginner",
        "category": "Player & Squad Intelligence",
        "title": "🇮🇳 Squad Profiles & Specialization Styles",
        "question": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "description": "Demonstrates basic SELECT and WHERE filtering to isolate international squad members by national affiliation, displaying their specialization styles.",
        "sql": """SELECT 
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = :country
ORDER BY full_name ASC;""",
        "default_params": {"country": "India"},
        "param_schema": {
            "country": {
                "type": "selectbox",
                "label": "Select Country",
                "options": ["India", "Australia", "England", "South Africa", "Pakistan", "New Zealand", "West Indies", "Sri Lanka"],
                "default": "India"
            }
        },
        "chart_type": "table",
        "chart_config": {}
    },

    "Q2": {
        "id": "Q2",
        "number": 2,
        "level": "Beginner",
        "category": "Match & Team Records",
        "title": "⏱️ Recent 30-Day International Fixtures",
        "question": "Show all cricket matches that were played in the last 30 days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first.",
        "description": "Performs relational INNER JOINs across matches, teams, and venues, filtering for encounters played in the last 30 days relative to the latest match date.",
        "sql": """SELECT 
    m.match_desc,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    v.venue_name,
    v.city,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= (SELECT MAX(match_date) - INTERVAL '30 days' FROM matches)
ORDER BY m.match_date DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "table",
        "chart_config": {}
    },

    "Q3": {
        "id": "Q3",
        "number": 3,
        "level": "Beginner",
        "category": "Player & Squad Intelligence",
        "title": "🏏 All-Time Top 10 ODI Run Scorers & Averages",
        "question": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first.",
        "description": "Extracts career batting aggregates for ODI cricket, ordering by total runs scored to identify historical batting leaders alongside consistency metrics.",
        "sql": """SELECT 
    p.full_name AS player_name,
    cs.total_runs,
    cs.batting_avg,
    cs.centuries
FROM player_career_stats cs
JOIN players p ON cs.player_id = p.player_id
WHERE cs.format = :format
ORDER BY cs.total_runs DESC
LIMIT :top_n;""",
        "default_params": {"format": "ODI", "top_n": 10},
        "param_schema": {
            "format": {
                "type": "selectbox",
                "label": "Cricket Format",
                "options": ["ODI", "Test", "T20I"],
                "default": "ODI"
            },
            "top_n": {
                "type": "slider",
                "label": "Top N Players",
                "min": 5,
                "max": 25,
                "default": 10
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "total_runs",
            "color": "batting_avg",
            "title": "Top Run Scorers (Total Runs & Average)"
        }
    },

    "Q4": {
        "id": "Q4",
        "number": 4,
        "level": "Beginner",
        "category": "Venues & Infrastructure",
        "title": "🏟️ Premier World Stadiums (50,000+ Capacity)",
        "question": "Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.",
        "description": "Applies numerical threshold filtering on venue infrastructure attributes to rank premier world cricket coliseums by spectator capacity.",
        "sql": """SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > :min_capacity
ORDER BY capacity DESC;""",
        "default_params": {"min_capacity": 50000},
        "param_schema": {
            "min_capacity": {
                "type": "slider",
                "label": "Minimum Capacity",
                "min": 25000,
                "max": 100000,
                "step": 5000,
                "default": 50000
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "venue_name",
            "y": "capacity",
            "color": "country",
            "title": "Top World Venues by Seating Capacity"
        }
    },

    "Q5": {
        "id": "Q5",
        "number": 5,
        "level": "Beginner",
        "category": "Match & Team Records",
        "title": "🏆 International Match Victories by Nation",
        "question": "Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.",
        "description": "Computes aggregate historical match victories by grouping on winning team identifiers, providing an overall international leaderboard.",
        "sql": """SELECT 
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
GROUP BY t.team_name
ORDER BY total_wins DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "bar",
        "chart_config": {
            "x": "team_name",
            "y": "total_wins",
            "title": "Total Match Victories by Nation"
        }
    },

    "Q6": {
        "id": "Q6",
        "number": 6,
        "level": "Beginner",
        "category": "Player & Squad Intelligence",
        "title": "🎯 Squad Composition & Tactical Role Distribution",
        "question": "Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.",
        "description": "Aggregates squad distribution across tactical playing specializations using COUNT and GROUP BY operations.",
        "sql": """SELECT 
    playing_role,
    COUNT(player_id) AS player_count
FROM players
WHERE playing_role IS NOT NULL
GROUP BY playing_role
ORDER BY player_count DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "donut",
        "chart_config": {
            "names": "playing_role",
            "values": "player_count",
            "title": "Playing Role Breakdown"
        }
    },

    "Q7": {
        "id": "Q7",
        "number": 7,
        "level": "Beginner",
        "category": "Player & Squad Intelligence",
        "title": "⚡ Format Peak Individual Batting Benchmarks",
        "question": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format.",
        "description": "Joins individual batting performances with match formats and applies the MAX aggregate function to establish format-level single-innings scoring benchmarks.",
        "sql": """SELECT 
    m.format,
    MAX(b.runs) AS highest_individual_score
FROM player_match_batting b
JOIN matches m ON b.match_id = m.match_id
GROUP BY m.format
ORDER BY highest_individual_score DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "bar",
        "chart_config": {
            "x": "format",
            "y": "highest_individual_score",
            "title": "Highest Individual Innings Score Across Formats"
        }
    },

    "Q8": {
        "id": "Q8",
        "number": 8,
        "level": "Beginner",
        "category": "Match & Team Records",
        "title": "🗓️ 2024 International Series Calendar",
        "question": "Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.",
        "description": "Applies calendar date boundary conditions to identify all international tours and tournaments originating within the specified calendar year.",
        "sql": """SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE start_date >= :start_range AND start_date <= :end_range
ORDER BY start_date ASC;""",
        "default_params": {"start_range": "2024-01-01", "end_range": "2024-12-31"},
        "param_schema": {
            "year": {
                "type": "selectbox",
                "label": "Filter by Year",
                "options": [2021, 2022, 2023, 2024, 2025, 2026],
                "default": 2024
            }
        },
        "chart_type": "table",
        "chart_config": {}
    },

    # =========================================================================
    # INTERMEDIATE LEVEL (QUESTIONS 9 - 16)
    # =========================================================================
    "Q9": {
        "id": "Q9",
        "number": 9,
        "level": "Intermediate",
        "category": "Player & Squad Intelligence",
        "title": "🌟 Elite All-Rounder Club (Dual Milestones: Runs & Wickets)",
        "question": "Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name, total runs, total wickets, and the cricket format.",
        "description": "Utilizes dual HAVING / WHERE conjunctions across separate disciplines (batting & bowling) to filter elite all-rounders surpassing both thresholds.",
        "sql": """SELECT 
    p.full_name AS player_name,
    cs.format,
    cs.total_runs,
    cs.total_wickets,
    cs.batting_avg,
    cs.bowling_avg
FROM player_career_stats cs
JOIN players p ON cs.player_id = p.player_id
WHERE cs.total_runs >= :min_runs 
  AND cs.total_wickets >= :min_wickets
ORDER BY cs.total_runs DESC, cs.total_wickets DESC;""",
        "default_params": {"min_runs": 200, "min_wickets": 5},
        "param_schema": {
            "min_runs": {
                "type": "slider",
                "label": "Minimum Career Runs",
                "min": 100,
                "max": 1000,
                "step": 50,
                "default": 200
            },
            "min_wickets": {
                "type": "slider",
                "label": "Minimum Career Wickets",
                "min": 5,
                "max": 50,
                "step": 5,
                "default": 5
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "total_runs",
            "color": "total_wickets",
            "title": "Elite All-Rounders (Runs vs Wickets Taken)"
        }
    },

    "Q10": {
        "id": "Q10",
        "number": 10,
        "level": "Intermediate",
        "category": "Match & Team Records",
        "title": "📋 Recent Completed International Match Scorecards",
        "question": "Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.",
        "description": "Combines four-table relational INNER JOINs across matches, teams (home, away, and winner), and venues to produce rich match scorecard summaries.",
        "sql": """SELECT 
    m.match_desc,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    tw.team_name AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN teams tw ON m.winner_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'Completed'
ORDER BY m.match_date DESC
LIMIT :limit_matches;""",
        "default_params": {"limit_matches": 20},
        "param_schema": {
            "limit_matches": {
                "type": "slider",
                "label": "Matches to Display",
                "min": 5,
                "max": 50,
                "default": 20
            }
        },
        "chart_type": "table",
        "chart_config": {}
    },

    "Q11": {
        "id": "Q11",
        "number": 11,
        "level": "Intermediate",
        "category": "Player & Squad Intelligence",
        "title": "🔄 Cross-Format Batting Performance (Test vs ODI vs T20I)",
        "question": "Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test cricket, ODI cricket, and T20I cricket, along with their overall batting average across all formats.",
        "description": "Executes pivot-style conditional aggregation using CASE WHEN expressions with GROUP BY and HAVING COUNT(DISTINCT format) >= 2.",
        "sql": """SELECT 
    p.full_name AS player_name,
    COALESCE(SUM(CASE WHEN cs.format = 'Test' THEN cs.total_runs ELSE 0 END), 0) AS test_runs,
    COALESCE(SUM(CASE WHEN cs.format = 'ODI' THEN cs.total_runs ELSE 0 END), 0) AS odi_runs,
    COALESCE(SUM(CASE WHEN cs.format = 'T20I' THEN cs.total_runs ELSE 0 END), 0) AS t20i_runs,
    ROUND(AVG(cs.batting_avg)::numeric, 2) AS overall_batting_avg,
    SUM(cs.total_runs) AS combined_runs
FROM player_career_stats cs
JOIN players p ON cs.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT cs.format) >= :min_formats
ORDER BY combined_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_formats": 2, "top_n": 15},
        "param_schema": {
            "min_formats": {
                "type": "slider",
                "label": "Minimum Distinct Formats",
                "min": 2,
                "max": 3,
                "default": 2
            },
            "top_n": {
                "type": "slider",
                "label": "Top Players",
                "min": 5,
                "max": 30,
                "default": 15
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": ["test_runs", "odi_runs", "t20i_runs"],
            "title": "Cross-Format Run Comparison (Test vs ODI vs T20I)"
        }
    },

    "Q12": {
        "id": "Q12",
        "number": 12,
        "level": "Intermediate",
        "category": "Match & Team Records",
        "title": "🌍 Home vs Away Winning Dominance by Nation",
        "question": "Analyze each international team's performance when playing at home versus playing away. Determine whether each team played at home or away based on whether the venue country matches the team's country. Count wins for each team in both home and away conditions.",
        "description": "Employs Common Table Expressions (CTEs) and conditional CASE logic to determine home/away venue context and calculate comparative win rates.",
        "sql": """WITH team_match_context AS (
    SELECT 
        t.team_name,
        CASE 
            WHEN v.country = t.country THEN 'Home'
            ELSE 'Away'
        END AS match_condition,
        CASE 
            WHEN m.winner_id = t.team_id THEN 1 
            ELSE 0 
        END AS is_win
    FROM matches m
    JOIN venues v ON m.venue_id = v.venue_id
    JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
)
SELECT 
    team_name,
    SUM(CASE WHEN match_condition = 'Home' THEN is_win ELSE 0 END) AS home_wins,
    SUM(CASE WHEN match_condition = 'Away' THEN is_win ELSE 0 END) AS away_wins,
    COUNT(CASE WHEN match_condition = 'Home' THEN 1 END) AS home_matches_played,
    COUNT(CASE WHEN match_condition = 'Away' THEN 1 END) AS away_matches_played,
    SUM(is_win) AS total_wins
FROM team_match_context
GROUP BY team_name
HAVING COUNT(*) > 0
ORDER BY total_wins DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "bar",
        "chart_config": {
            "x": "team_name",
            "y": ["home_wins", "away_wins"],
            "title": "Home vs Away Victories by Nation"
        }
    },

    "Q13": {
        "id": "Q13",
        "number": 13,
        "level": "Intermediate",
        "category": "Match & Team Records",
        "title": "🤝 Century Batting Partnerships (Consecutive Order Pairs)",
        "question": "Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings. Show both player names, their combined partnership runs, and which innings it occurred in.",
        "description": "Analyzes consecutive crease partnerships using position adjacency conditions (ABS(pos1 - pos2) = 1) filtered for century stands.",
        "sql": """SELECT 
    p1.full_name AS batter_1,
    p2.full_name AS batter_2,
    prt.player1_position AS pos_1,
    prt.player2_position AS pos_2,
    prt.innings,
    m.match_desc,
    prt.partnership_runs
FROM partnerships prt
JOIN players p1 ON prt.player1_id = p1.player_id
JOIN players p2 ON prt.player2_id = p2.player_id
JOIN matches m ON prt.match_id = m.match_id
WHERE prt.partnership_runs >= :min_runs
  AND ABS(prt.player1_position - prt.player2_position) = 1
ORDER BY prt.partnership_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_runs": 50, "top_n": 15},
        "param_schema": {
            "min_runs": {
                "type": "slider",
                "label": "Minimum Partnership Runs",
                "min": 50,
                "max": 150,
                "step": 10,
                "default": 50
            },
            "top_n": {
                "type": "slider",
                "label": "Top Partnerships",
                "min": 5,
                "max": 30,
                "default": 15
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "batter_1",
            "y": "partnership_runs",
            "color": "innings",
            "title": "Top Consecutive Batting Partnerships"
        }
    },

    "Q14": {
        "id": "Q14",
        "number": 14,
        "level": "Intermediate",
        "category": "Venues & Infrastructure",
        "title": "🎯 Venue-Specific Bowling Mastery & Economy Analysis",
        "question": "Examine bowling performance at different venues. For bowlers who have played at least 3 matches at the same venue, calculate their average economy rate, total wickets taken, and number of matches played at each venue. Focus on bowlers who bowled at least 4 overs in each match.",
        "description": "Calculates venue-level bowling aggregates with multi-column GROUP BY (player, venue) and HAVING filters for spell workload.",
        "sql": """SELECT 
    p.full_name AS bowler_name,
    v.venue_name,
    v.city,
    COUNT(DISTINCT bw.match_id) AS matches_at_venue,
    SUM(bw.wickets) AS total_wickets,
    ROUND(AVG(bw.economy_rate)::numeric, 2) AS avg_economy_rate
FROM player_match_bowling bw
JOIN players p ON bw.player_id = p.player_id
JOIN matches m ON bw.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE bw.overs >= :min_overs_per_match
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name, v.city
HAVING COUNT(DISTINCT bw.match_id) >= :min_matches_at_venue
ORDER BY total_wickets DESC, avg_economy_rate ASC
LIMIT :limit_records;""",
        "default_params": {"min_overs_per_match": 2.0, "min_matches_at_venue": 2, "limit_records": 15},
        "param_schema": {
            "min_overs_per_match": {
                "type": "slider",
                "label": "Min Overs per Spell",
                "min": 1.0,
                "max": 10.0,
                "step": 1.0,
                "default": 2.0
            },
            "min_matches_at_venue": {
                "type": "slider",
                "label": "Min Matches at Venue",
                "min": 2,
                "max": 5,
                "default": 2
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "bowler_name",
            "y": "total_wickets",
            "color": "avg_economy_rate",
            "title": "Venue Wicket Takers & Economy"
        }
    },

    "Q15": {
        "id": "Q15",
        "number": 15,
        "level": "Intermediate",
        "category": "Advanced Metrics & Momentum",
        "title": "🔥 Clutch Match Performance in High-Pressure Finishes",
        "question": "Identify players who perform exceptionally well in close matches. A close match is defined as one decided by less than 50 runs OR less than 5 wickets. For these close matches, calculate each player's average runs scored, total close matches played, and how many of those close matches their team won when they batted.",
        "description": "Leverages a CTE to identify tight-margin thriller matches (<50 runs or <5 wickets) and computes player batting averages in high-pressure situations.",
        "sql": """WITH close_matches AS (
    SELECT match_id, winner_id
    FROM matches
    WHERE (victory_type = 'runs' AND victory_margin < 50)
       OR (victory_type = 'wickets' AND victory_margin < 5)
)
SELECT 
    p.full_name AS player_name,
    COUNT(b.match_id) AS close_matches_batted,
    ROUND(AVG(b.runs)::numeric, 2) AS avg_runs_in_close_matches,
    SUM(b.runs) AS total_close_match_runs,
    SUM(CASE WHEN m.winner_id = p.team_id THEN 1 ELSE 0 END) AS close_match_team_wins
FROM player_match_batting b
JOIN close_matches cm ON b.match_id = cm.match_id
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
GROUP BY p.player_id, p.full_name, p.team_id
HAVING COUNT(b.match_id) >= :min_close_matches
ORDER BY avg_runs_in_close_matches DESC
LIMIT :top_n;""",
        "default_params": {"min_close_matches": 2, "top_n": 15},
        "param_schema": {
            "min_close_matches": {
                "type": "slider",
                "label": "Minimum Close Matches Played",
                "min": 1,
                "max": 5,
                "default": 2
            },
            "top_n": {
                "type": "slider",
                "label": "Top Players",
                "min": 5,
                "max": 25,
                "default": 15
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "avg_runs_in_close_matches",
            "color": "close_match_team_wins",
            "title": "Highest Batting Averages in Pressure Finishes"
        }
    },

    "Q16": {
        "id": "Q16",
        "number": 16,
        "level": "Intermediate",
        "category": "Advanced Metrics & Momentum",
        "title": "📈 Year-over-Year Batting Evolution & Strike Rate Trends",
        "question": "Track how players' batting performance changes over different years. For matches since 2020, show each player's average runs per match and average strike rate for each year. Only include players who played at least 5 matches in that year.",
        "description": "Aggregates longitudinal batting progression grouped by calendar year and player, displaying scoring volume and strike rate evolution.",
        "sql": """SELECT 
    p.full_name AS player_name,
    b.year,
    COUNT(DISTINCT b.match_id) AS matches_played,
    ROUND(AVG(b.runs)::numeric, 2) AS avg_runs_per_match,
    ROUND(AVG(b.strike_rate)::numeric, 2) AS avg_strike_rate,
    SUM(b.runs) AS total_runs_in_year
FROM player_match_batting b
JOIN players p ON b.player_id = p.player_id
WHERE b.year >= :since_year
GROUP BY p.player_id, p.full_name, b.year
HAVING COUNT(DISTINCT b.match_id) >= :min_matches_per_year
ORDER BY avg_runs_per_match DESC, b.year DESC
LIMIT :limit_records;""",
        "default_params": {"since_year": 2021, "min_matches_per_year": 2, "limit_records": 20},
        "param_schema": {
            "since_year": {
                "type": "selectbox",
                "label": "Since Year",
                "options": [2021, 2022, 2023, 2024],
                "default": 2021
            },
            "min_matches_per_year": {
                "type": "slider",
                "label": "Min Matches per Year",
                "min": 2,
                "max": 10,
                "default": 2
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "avg_runs_per_match",
            "color": "year",
            "title": "Year-over-Year Batting Averages"
        }
    },

    # =========================================================================
    # ADVANCED LEVEL (QUESTIONS 17 - 25)
    # =========================================================================
    "Q17": {
        "id": "Q17",
        "number": 17,
        "level": "Advanced",
        "category": "Match & Team Records",
        "title": "🎲 Toss Decision Advantage & Match Victory Percentage",
        "question": "Investigate whether winning the toss gives teams an advantage in winning matches. Calculate what percentage of matches are won by the team that wins the toss, broken down by their toss decision (choosing to bat first or bowl first).",
        "description": "Calculates probabilistic match conversion rates based on tactical toss decisions (batting first vs fielding first) using conditional aggregation.",
        "sql": """SELECT 
    toss_decision,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS toss_winner_match_wins,
    ROUND((SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) * 100.0 / COUNT(*))::numeric, 2) AS win_percentage_when_won_toss
FROM matches
WHERE toss_decision IS NOT NULL AND winner_id IS NOT NULL
GROUP BY toss_decision
ORDER BY total_matches DESC;""",
        "default_params": {},
        "param_schema": {},
        "chart_type": "donut",
        "chart_config": {
            "names": "toss_decision",
            "values": "total_matches",
            "title": "Toss Decision Distribution & Win Rate"
        }
    },

    "Q18": {
        "id": "Q18",
        "number": 18,
        "level": "Advanced",
        "category": "Player & Squad Intelligence",
        "title": "🎯 Limited-Overs Economy Benchmarks (ODI & T20I)",
        "question": "Find the most economical bowlers in limited-overs cricket (ODI and T20 formats). Calculate each bowler's overall economy rate and total wickets taken. Only consider bowlers who have bowled in at least 10 matches and bowled at least 2 overs per match on average.",
        "description": "Evaluates white-ball run containment efficiency using multi-match workload filters across ODI and T20I formats.",
        "sql": """SELECT 
    p.full_name AS bowler_name,
    p.country,
    COUNT(DISTINCT bw.match_id) AS matches_bowled,
    ROUND(SUM(bw.overs)::numeric, 1) AS total_overs,
    SUM(bw.wickets) AS total_wickets,
    ROUND((SUM(bw.runs_conceded) / (SUM(bw.overs) + 0.0001))::numeric, 2) AS overall_economy_rate
FROM player_match_bowling bw
JOIN matches m ON bw.match_id = m.match_id
JOIN players p ON bw.player_id = p.player_id
WHERE m.format IN ('ODI', 'T20I')
GROUP BY p.player_id, p.full_name, p.country
HAVING COUNT(DISTINCT bw.match_id) >= :min_matches
   AND (SUM(bw.overs) / COUNT(DISTINCT bw.match_id)) >= :min_avg_overs
ORDER BY overall_economy_rate ASC, total_wickets DESC
LIMIT :top_n;""",
        "default_params": {"min_matches": 3, "min_avg_overs": 2.0, "top_n": 15},
        "param_schema": {
            "min_matches": {
                "type": "slider",
                "label": "Minimum Matches Bowled",
                "min": 2,
                "max": 15,
                "default": 3
            },
            "min_avg_overs": {
                "type": "slider",
                "label": "Min Avg Overs/Match",
                "min": 1.0,
                "max": 4.0,
                "step": 0.5,
                "default": 2.0
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "bowler_name",
            "y": "overall_economy_rate",
            "color": "total_wickets",
            "title": "Most Economical Limited-Overs Bowlers"
        }
    },

    "Q19": {
        "id": "Q19",
        "number": 19,
        "level": "Advanced",
        "category": "Advanced Metrics & Momentum",
        "title": "📊 Batting Consistency Index (Low Standard Deviation Ranking)",
        "question": "Determine which batsmen are most consistent in their scoring. Calculate the average runs scored and the standard deviation of runs for each player. Only include players who have faced at least 10 balls per innings and played since 2022. A lower standard deviation indicates more consistent performance.",
        "description": "Applies statistical variance modeling using STDDEV_SAMP(runs) to discover reliable, low-variance batting anchors.",
        "sql": """SELECT 
    p.full_name AS player_name,
    p.country,
    COUNT(b.batting_id) AS qualifying_innings,
    ROUND(AVG(b.runs)::numeric, 2) AS avg_runs,
    ROUND(STDDEV_SAMP(b.runs)::numeric, 2) AS score_std_deviation,
    MAX(b.runs) AS peak_score
FROM player_match_batting b
JOIN players p ON b.player_id = p.player_id
WHERE b.balls >= :min_balls_faced 
  AND b.year >= :since_year
GROUP BY p.player_id, p.full_name, p.country
HAVING COUNT(b.batting_id) >= :min_innings
ORDER BY score_std_deviation ASC, avg_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_balls_faced": 10, "since_year": 2022, "min_innings": 3, "top_n": 15},
        "param_schema": {
            "min_balls_faced": {
                "type": "slider",
                "label": "Min Balls Faced",
                "min": 5,
                "max": 30,
                "step": 5,
                "default": 10
            },
            "min_innings": {
                "type": "slider",
                "label": "Min Innings",
                "min": 2,
                "max": 10,
                "default": 3
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "score_std_deviation",
            "color": "avg_runs",
            "title": "Batting Consistency (Lower Std Dev = Higher Consistency)"
        }
    },

    "Q20": {
        "id": "Q20",
        "number": 20,
        "level": "Advanced",
        "category": "Player & Squad Intelligence",
        "title": "🌐 Multi-Format Match Workload & Format Batting Averages",
        "question": "Analyze how many matches each player has played in different cricket formats and their batting average in each format. Show the count of Test matches, ODI matches, and T20 matches for each player, along with their respective batting averages. Only include players who have played at least 20 total matches across all formats.",
        "description": "Cross-format matrix grouping player workload and format-specific averages across international cricket tiers.",
        "sql": """SELECT 
    p.full_name AS player_name,
    p.country,
    COALESCE(SUM(CASE WHEN cs.format = 'Test' THEN cs.matches_played ELSE 0 END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN cs.format = 'Test' THEN cs.batting_avg ELSE NULL END), 0.0) AS test_avg,
    COALESCE(SUM(CASE WHEN cs.format = 'ODI' THEN cs.matches_played ELSE 0 END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN cs.format = 'ODI' THEN cs.batting_avg ELSE NULL END), 0.0) AS odi_avg,
    COALESCE(SUM(CASE WHEN cs.format = 'T20I' THEN cs.matches_played ELSE 0 END), 0) AS t20i_matches,
    COALESCE(MAX(CASE WHEN cs.format = 'T20I' THEN cs.batting_avg ELSE NULL END), 0.0) AS t20i_avg,
    SUM(cs.matches_played) AS total_matches_all_formats
FROM player_career_stats cs
JOIN players p ON cs.player_id = p.player_id
GROUP BY p.player_id, p.full_name, p.country
HAVING SUM(cs.matches_played) >= :min_total_matches
ORDER BY total_matches_all_formats DESC
LIMIT :top_n;""",
        "default_params": {"min_total_matches": 5, "top_n": 15},
        "param_schema": {
            "min_total_matches": {
                "type": "slider",
                "label": "Minimum Matches Across Formats",
                "min": 3,
                "max": 25,
                "default": 5
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "total_matches_all_formats",
            "title": "Total International Matches Across Formats"
        }
    },

    "Q21": {
        "id": "Q21",
        "number": 21,
        "level": "Advanced",
        "category": "Advanced Metrics & Momentum",
        "title": "🎖️ Multi-Discipline Composite Player Ranking System",
        "question": "Create a comprehensive performance ranking system for players. Combine their batting performance (runs scored, batting average, strike rate), bowling performance (wickets taken, bowling average, economy rate), and fielding performance (catches, stumpings) into a single weighted score. Use this formula and rank players: Batting points: (runs_scored × 0.01) + (batting_average × 0.5) + (strike_rate × 0.3); Bowling points: (wickets_taken × 2) + ((50 - bowling_average) × 0.5) + ((6 - economy_rate) × 2); Fielding points: (catches × 3) + (stumpings × 5). Rank the top performers in each cricket format.",
        "description": "Implements an all-discipline composite index combining weighted metrics from batting, bowling, and fielding using window RANK().",
        "sql": """WITH player_composite_points AS (
    SELECT 
        p.full_name AS player_name,
        p.country,
        cs.format,
        cs.total_runs,
        cs.batting_avg,
        cs.strike_rate,
        cs.total_wickets,
        cs.bowling_avg,
        cs.economy_rate,
        cs.catches,
        cs.stumpings,
        -- Batting points: (runs * 0.01) + (avg * 0.5) + (sr * 0.3)
        ROUND(((cs.total_runs * 0.01) + (cs.batting_avg * 0.5) + (cs.strike_rate * 0.3))::numeric, 2) AS batting_points,
        -- Bowling points: (wickets * 2) + ((50 - avg) * 0.5) + ((6 - econ) * 2)
        ROUND((CASE WHEN cs.total_wickets > 0 THEN ((cs.total_wickets * 2.0) + ((50.0 - cs.bowling_avg) * 0.5) + ((6.0 - cs.economy_rate) * 2.0)) ELSE 0.0 END)::numeric, 2) AS bowling_points,
        -- Fielding points: (catches * 3) + (stumpings * 5)
        ROUND(((cs.catches * 3.0) + (cs.stumpings * 5.0))::numeric, 2) AS fielding_points
    FROM player_career_stats cs
    JOIN players p ON cs.player_id = p.player_id
    WHERE cs.format = :format
)
SELECT 
    player_name,
    country,
    format,
    batting_points,
    bowling_points,
    fielding_points,
    ROUND((batting_points + bowling_points + fielding_points)::numeric, 2) AS total_composite_score,
    RANK() OVER (ORDER BY (batting_points + bowling_points + fielding_points) DESC) AS format_rank
FROM player_composite_points
ORDER BY total_composite_score DESC
LIMIT :top_n;""",
        "default_params": {"format": "ODI", "top_n": 15},
        "param_schema": {
            "format": {
                "type": "selectbox",
                "label": "Format",
                "options": ["ODI", "Test", "T20I"],
                "default": "ODI"
            },
            "top_n": {
                "type": "slider",
                "label": "Top Ranked Players",
                "min": 5,
                "max": 30,
                "default": 15
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": ["batting_points", "bowling_points", "fielding_points"],
            "title": "Composite Player Ranking Breakdown"
        }
    },

    "Q22": {
        "id": "Q22",
        "number": 22,
        "level": "Advanced",
        "category": "Match & Team Records",
        "title": "⚔️ Head-to-Head Team Rivalry & Match Prediction Matrix",
        "question": "Build a head-to-head match prediction analysis between teams. For each pair of teams that have played at least 5 matches against each other in the last 3 years, calculate: Total matches played between them, Wins for each team, Average victory margin when each team wins, Performance when batting first vs bowling first at different venues, Overall win percentage for each team in this head-to-head record.",
        "description": "Normalizes bilateral rivalry team pairings to compute head-to-head win distributions and victory margins for match forecasting.",
        "sql": """WITH h2h_base AS (
    SELECT 
        CASE WHEN t1.team_name < t2.team_name THEN t1.team_name ELSE t2.team_name END AS team_a,
        CASE WHEN t1.team_name < t2.team_name THEN t2.team_name ELSE t1.team_name END AS team_b,
        m.match_id,
        m.winner_id,
        m.victory_margin,
        t1.team_name AS team1_name,
        t2.team_name AS team2_name,
        tw.team_name AS winner_name
    FROM matches m
    JOIN teams t1 ON m.team1_id = t1.team_id
    JOIN teams t2 ON m.team2_id = t2.team_id
    LEFT JOIN teams tw ON m.winner_id = tw.team_id
    WHERE m.match_date >= (SELECT MAX(match_date) - INTERVAL '3 years' FROM matches)
)
SELECT 
    team_a,
    team_b,
    COUNT(match_id) AS total_encounters,
    COUNT(CASE WHEN winner_name = team_a THEN 1 END) AS team_a_wins,
    COUNT(CASE WHEN winner_name = team_b THEN 1 END) AS team_b_wins,
    ROUND((COUNT(CASE WHEN winner_name = team_a THEN 1 END) * 100.0 / COUNT(match_id))::numeric, 1) AS team_a_win_pct,
    ROUND((COUNT(CASE WHEN winner_name = team_b THEN 1 END) * 100.0 / COUNT(match_id))::numeric, 1) AS team_b_win_pct,
    ROUND(AVG(CASE WHEN winner_name = team_a AND victory_margin IS NOT NULL THEN victory_margin END)::numeric, 1) AS team_a_avg_margin,
    ROUND(AVG(CASE WHEN winner_name = team_b AND victory_margin IS NOT NULL THEN victory_margin END)::numeric, 1) AS team_b_avg_margin
FROM h2h_base
GROUP BY team_a, team_b
HAVING COUNT(match_id) >= :min_h2h_matches
ORDER BY total_encounters DESC;""",
        "default_params": {"min_h2h_matches": 2},
        "param_schema": {
            "min_h2h_matches": {
                "type": "slider",
                "label": "Minimum H2H Matches",
                "min": 2,
                "max": 8,
                "default": 2
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "team_a",
            "y": ["team_a_wins", "team_b_wins"],
            "title": "Head-to-Head Encounters & Win Counts"
        }
    },

    "Q23": {
        "id": "Q23",
        "number": 23,
        "level": "Advanced",
        "category": "Advanced Metrics & Momentum",
        "title": "⚡ Player Momentum & Recent Form Classifier",
        "question": "Analyze recent player form and momentum. For each player's last 10 batting performances, calculate: Average runs in their last 5 matches vs their last 10 matches, Recent strike rate trends, Number of scores above 50 in recent matches, A consistency score based on standard deviation. Based on these metrics, categorize players as being in 'Excellent Form', 'Good Form', 'Average Form', or 'Poor Form'.",
        "description": "Applies ROW_NUMBER() window partitioning to evaluate the last 5 vs last 10 innings and classifies current momentum status.",
        "sql": """WITH ranked_innings AS (
    SELECT 
        b.player_id,
        p.full_name AS player_name,
        p.country,
        b.runs,
        b.strike_rate,
        ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY b.match_date DESC) AS innings_recency
    FROM player_match_batting b
    JOIN players p ON b.player_id = p.player_id
),
last_10_innings AS (
    SELECT 
        player_id,
        player_name,
        country,
        COUNT(*) AS total_recent_innings,
        ROUND(AVG(CASE WHEN innings_recency <= 5 THEN runs END)::numeric, 2) AS last_5_avg_runs,
        ROUND(AVG(runs)::numeric, 2) AS last_10_avg_runs,
        ROUND(AVG(strike_rate)::numeric, 2) AS recent_avg_strike_rate,
        COUNT(CASE WHEN runs >= 50 THEN 1 END) AS fifty_plus_scores,
        ROUND(COALESCE(STDDEV_SAMP(runs), 0)::numeric, 2) AS consistency_stddev
    FROM ranked_innings
    WHERE innings_recency <= 10
    GROUP BY player_id, player_name, country
    HAVING COUNT(*) >= :min_innings
)
SELECT 
    player_name,
    country,
    total_recent_innings,
    last_5_avg_runs,
    last_10_avg_runs,
    recent_avg_strike_rate,
    fifty_plus_scores,
    consistency_stddev,
    CASE 
        WHEN last_5_avg_runs >= 50 OR fifty_plus_scores >= 3 THEN '🔥 Excellent Form'
        WHEN last_5_avg_runs >= 35 OR fifty_plus_scores >= 2 THEN '🟢 Good Form'
        WHEN last_5_avg_runs >= 20 THEN '🟡 Average Form'
        ELSE '🔴 Poor Form'
    END AS form_status
FROM last_10_innings
ORDER BY last_5_avg_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_innings": 3, "top_n": 20},
        "param_schema": {
            "min_innings": {
                "type": "slider",
                "label": "Min Recent Innings",
                "min": 2,
                "max": 10,
                "default": 3
            },
            "top_n": {
                "type": "slider",
                "label": "Top Players",
                "min": 5,
                "max": 30,
                "default": 20
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "last_5_avg_runs",
            "color": "form_status",
            "title": "Player Recent Batting Form (Last 5 Innings Avg)"
        }
    },

    "Q24": {
        "id": "Q24",
        "number": 24,
        "level": "Advanced",
        "category": "Match & Team Records",
        "title": "🤝 Top Batting Combinations & Partnership Success Rate",
        "question": "Study successful batting partnerships to identify the best player combinations. For pairs of players who have batted together as consecutive batsmen (positions differ by 1) in at least 5 partnerships: Calculate their average partnership runs, Count how many of their partnerships exceeded 50 runs, Find their highest partnership score, Calculate their success rate (percentage of good partnerships), Rank the most successful batting partnerships.",
        "description": "Calculates batting partnership conversion rates and ranks consecutive batsman duos using window RANK().",
        "sql": """SELECT 
    p1.full_name AS batter_1,
    p2.full_name AS batter_2,
    COUNT(prt.partnership_id) AS total_partnerships,
    ROUND(AVG(prt.partnership_runs)::numeric, 2) AS avg_partnership_runs,
    MAX(prt.partnership_runs) AS highest_partnership,
    COUNT(CASE WHEN prt.partnership_runs >= 50 THEN 1 END) AS fifty_plus_stands,
    ROUND((COUNT(CASE WHEN prt.partnership_runs >= 50 THEN 1 END) * 100.0 / COUNT(prt.partnership_id))::numeric, 2) AS success_rate_pct,
    RANK() OVER (ORDER BY AVG(prt.partnership_runs) DESC) AS partnership_rank
FROM partnerships prt
JOIN players p1 ON prt.player1_id = p1.player_id
JOIN players p2 ON prt.player2_id = p2.player_id
WHERE ABS(prt.player1_position - prt.player2_position) = 1
GROUP BY p1.player_id, p1.full_name, p2.player_id, p2.full_name
HAVING COUNT(prt.partnership_id) >= :min_partnerships
ORDER BY avg_partnership_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_partnerships": 2, "top_n": 15},
        "param_schema": {
            "min_partnerships": {
                "type": "slider",
                "label": "Minimum Partnerships",
                "min": 2,
                "max": 6,
                "default": 2
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "batter_1",
            "y": "avg_partnership_runs",
            "color": "success_rate_pct",
            "title": "Top Batting Pairs (Avg Runs & 50+ Success Rate)"
        }
    },

    "Q25": {
        "id": "Q25",
        "number": 25,
        "level": "Advanced",
        "category": "Advanced Metrics & Momentum",
        "title": "📈 Quarterly Time-Series Career Trajectory & Evolution Analyzer",
        "question": "Perform a time-series analysis of player performance evolution. Track how each player's batting performance changes over time by: Calculating quarterly averages for runs and strike rate, Comparing each quarter's performance to the previous quarter using LAG(), Identifying whether performance is improving, declining, or stable, Determining overall career trajectory over the last few years, Categorizing players' career phase as 'Career Ascending', 'Career Declining', or 'Career Stable'. Only analyze players with data spanning at least 6 quarters and a minimum of 3 matches per quarter.",
        "description": "Performs multi-step quarterly time-series tracking with LAG() window functions to categorize long-term career trajectory.",
        "sql": """WITH quarterly_perf AS (
    SELECT 
        b.player_id,
        p.full_name AS player_name,
        p.country,
        b.quarter,
        COUNT(DISTINCT b.match_id) AS matches_in_quarter,
        ROUND(AVG(b.runs)::numeric, 2) AS qtr_avg_runs,
        ROUND(AVG(b.strike_rate)::numeric, 2) AS qtr_avg_sr,
        LAG(ROUND(AVG(b.runs)::numeric, 2)) OVER (PARTITION BY b.player_id ORDER BY b.quarter ASC) AS prev_qtr_avg_runs
    FROM player_match_batting b
    JOIN players p ON b.player_id = p.player_id
    GROUP BY b.player_id, p.full_name, p.country, b.quarter
),
quarter_trends AS (
    SELECT 
        player_id,
        player_name,
        country,
        quarter,
        matches_in_quarter,
        qtr_avg_runs,
        prev_qtr_avg_runs,
        CASE 
            WHEN prev_qtr_avg_runs IS NULL THEN 'Baseline'
            WHEN qtr_avg_runs > prev_qtr_avg_runs * 1.05 THEN 'Improving'
            WHEN qtr_avg_runs < prev_qtr_avg_runs * 0.95 THEN 'Declining'
            ELSE 'Stable'
        END AS quarter_trend
    FROM quarterly_perf
),
player_trajectories AS (
    SELECT 
        player_id,
        player_name,
        country,
        COUNT(DISTINCT quarter) AS total_quarters_active,
        ROUND(AVG(qtr_avg_runs)::numeric, 2) AS overall_avg_runs,
        COUNT(CASE WHEN quarter_trend = 'Improving' THEN 1 END) AS improving_quarters,
        COUNT(CASE WHEN quarter_trend = 'Declining' THEN 1 END) AS declining_quarters
    FROM quarter_trends
    GROUP BY player_id, player_name, country
    HAVING COUNT(DISTINCT quarter) >= :min_quarters
)
SELECT 
    player_name,
    country,
    total_quarters_active,
    overall_avg_runs,
    improving_quarters,
    declining_quarters,
    CASE 
        WHEN improving_quarters > declining_quarters THEN '🚀 Career Ascending'
        WHEN declining_quarters > improving_quarters THEN '📉 Career Declining'
        ELSE '⚖️ Career Stable'
    END AS career_trajectory
FROM player_trajectories
ORDER BY overall_avg_runs DESC
LIMIT :top_n;""",
        "default_params": {"min_quarters": 2, "top_n": 20},
        "param_schema": {
            "min_quarters": {
                "type": "slider",
                "label": "Minimum Active Quarters",
                "min": 2,
                "max": 6,
                "default": 2
            }
        },
        "chart_type": "bar",
        "chart_config": {
            "x": "player_name",
            "y": "overall_avg_runs",
            "color": "career_trajectory",
            "title": "Quarterly Career Trajectory Classifications"
        }
    }
}

# =========================================================================
# HELPER QUERY RETRIEVAL FUNCTIONS
# =========================================================================

def get_query(query_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves metadata and SQL for a specific query ID (e.g., 'Q1')."""
    return QUERIES.get(query_id)

def get_queries_by_level(level: str) -> List[Dict[str, Any]]:
    """Returns all queries matching a specified complexity level ('Beginner', 'Intermediate', 'Advanced')."""
    return [q for q in QUERIES.values() if q["level"].lower() == level.lower()]

def get_queries_by_category(category: str) -> List[Dict[str, Any]]:
    """Returns all queries matching a specified domain category."""
    return [q for q in QUERIES.values() if q.get("category", "").lower() == category.lower()]

def get_all_queries() -> List[Dict[str, Any]]:
    """Returns full catalog of configured queries in sequential order."""
    return sorted(list(QUERIES.values()), key=lambda x: x["number"])

def get_levels() -> List[str]:
    """Returns distinct query complexity levels present in catalog."""
    levels = []
    for q in QUERIES.values():
        if q["level"] not in levels:
            levels.append(q["level"])
    return levels

def get_categories() -> List[str]:
    """Returns distinct domain categories present in catalog."""
    cats = []
    for q in QUERIES.values():
        c = q.get("category", "General")
        if c not in cats:
            cats.append(c)
    return cats
