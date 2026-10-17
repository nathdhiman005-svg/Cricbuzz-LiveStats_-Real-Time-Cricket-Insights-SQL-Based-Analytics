"""
Database connection, session management, and schema definition module.
Supports PostgreSQL (Neon/Cloud/Local), MySQL, and SQLite seamlessly with automatic fallback.
"""

import os
from datetime import date
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import (
    create_engine,
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Index,
    inspect
)
from sqlalchemy.engine import Engine

# Load environment variables
load_dotenv()

# Global metadata registry
metadata = MetaData()

# Define Tables using SQLAlchemy for dialect-agnostic DDL
teams_table = Table(
    "teams",
    metadata,
    Column("team_id", Integer, primary_key=True, autoincrement=True),
    Column("team_name", String(100), nullable=False, unique=True),
    Column("country", String(100), nullable=False),
    Column("short_code", String(10), nullable=True),
)

venues_table = Table(
    "venues",
    metadata,
    Column("venue_id", Integer, primary_key=True, autoincrement=True),
    Column("venue_name", String(150), nullable=False),
    Column("city", String(100), nullable=False),
    Column("country", String(100), nullable=False),
    Column("capacity", Integer, nullable=True),
)

series_table = Table(
    "series",
    metadata,
    Column("series_id", Integer, primary_key=True, autoincrement=True),
    Column("series_name", String(200), nullable=False),
    Column("host_country", String(100), nullable=False),
    Column("match_type", String(50), nullable=False),  # e.g., 'Bilateral', 'Tournament'
    Column("start_date", Date, nullable=False),
    Column("total_matches", Integer, nullable=False, default=1),
)

players_table = Table(
    "players",
    metadata,
    Column("player_id", Integer, primary_key=True, autoincrement=True),
    Column("team_id", Integer, ForeignKey("teams.team_id"), nullable=True),
    Column("full_name", String(150), nullable=False),
    Column("country", String(100), nullable=False),
    Column("playing_role", String(50), nullable=False),  # Batsman, Bowler, All-rounder, Wicket-keeper
    Column("batting_style", String(50), nullable=True),
    Column("bowling_style", String(50), nullable=True),
)

matches_table = Table(
    "matches",
    metadata,
    Column("match_id", Integer, primary_key=True, autoincrement=True),
    Column("series_id", Integer, ForeignKey("series.series_id"), nullable=True),
    Column("match_desc", String(255), nullable=False),
    Column("format", String(20), nullable=False),  # Test, ODI, T20I
    Column("match_date", Date, nullable=False),
    Column("team1_id", Integer, ForeignKey("teams.team_id"), nullable=False),
    Column("team2_id", Integer, ForeignKey("teams.team_id"), nullable=False),
    Column("venue_id", Integer, ForeignKey("venues.venue_id"), nullable=False),
    Column("toss_winner_id", Integer, ForeignKey("teams.team_id"), nullable=True),
    Column("toss_decision", String(20), nullable=True),  # bat, bowl
    Column("winner_id", Integer, ForeignKey("teams.team_id"), nullable=True),
    Column("victory_margin", Integer, nullable=True),
    Column("victory_type", String(20), nullable=True),  # runs, wickets, tie, no result
    Column("status", String(50), nullable=False, default="Completed"),
)

player_match_batting_table = Table(
    "player_match_batting",
    metadata,
    Column("batting_id", Integer, primary_key=True, autoincrement=True),
    Column("match_id", Integer, ForeignKey("matches.match_id"), nullable=False),
    Column("player_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("innings", Integer, nullable=False, default=1),
    Column("batting_position", Integer, nullable=False),
    Column("runs", Integer, nullable=False, default=0),
    Column("balls", Integer, nullable=False, default=0),
    Column("fours", Integer, nullable=False, default=0),
    Column("sixes", Integer, nullable=False, default=0),
    Column("strike_rate", Float, nullable=False, default=0.0),
    Column("is_out", Integer, nullable=False, default=1),  # 1: out, 0: not out
    Column("match_date", Date, nullable=False),
    Column("year", Integer, nullable=False),
    Column("quarter", String(10), nullable=False),  # e.g., '2023-Q1'
)

player_match_bowling_table = Table(
    "player_match_bowling",
    metadata,
    Column("bowling_id", Integer, primary_key=True, autoincrement=True),
    Column("match_id", Integer, ForeignKey("matches.match_id"), nullable=False),
    Column("player_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("innings", Integer, nullable=False, default=1),
    Column("overs", Float, nullable=False, default=0.0),
    Column("maidens", Integer, nullable=False, default=0),
    Column("runs_conceded", Integer, nullable=False, default=0),
    Column("wickets", Integer, nullable=False, default=0),
    Column("economy_rate", Float, nullable=False, default=0.0),
    Column("match_date", Date, nullable=False),
    Column("year", Integer, nullable=False),
    Column("quarter", String(10), nullable=False),
)

player_fielding_table = Table(
    "player_fielding",
    metadata,
    Column("fielding_id", Integer, primary_key=True, autoincrement=True),
    Column("match_id", Integer, ForeignKey("matches.match_id"), nullable=False),
    Column("player_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("catches", Integer, nullable=False, default=0),
    Column("stumpings", Integer, nullable=False, default=0),
)

partnerships_table = Table(
    "partnerships",
    metadata,
    Column("partnership_id", Integer, primary_key=True, autoincrement=True),
    Column("match_id", Integer, ForeignKey("matches.match_id"), nullable=False),
    Column("innings", Integer, nullable=False, default=1),
    Column("player1_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("player2_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("player1_position", Integer, nullable=False),
    Column("player2_position", Integer, nullable=False),
    Column("partnership_runs", Integer, nullable=False, default=0),
)

player_career_stats_table = Table(
    "player_career_stats",
    metadata,
    Column("stat_id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", Integer, ForeignKey("players.player_id"), nullable=False),
    Column("format", String(20), nullable=False),  # Test, ODI, T20I
    Column("matches_played", Integer, nullable=False, default=0),
    Column("total_runs", Integer, nullable=False, default=0),
    Column("batting_avg", Float, nullable=False, default=0.0),
    Column("strike_rate", Float, nullable=False, default=0.0),
    Column("centuries", Integer, nullable=False, default=0),
    Column("fifties", Integer, nullable=False, default=0),
    Column("highest_score", Integer, nullable=False, default=0),
    Column("total_wickets", Integer, nullable=False, default=0),
    Column("bowling_avg", Float, nullable=False, default=0.0),
    Column("economy_rate", Float, nullable=False, default=0.0),
    Column("catches", Integer, nullable=False, default=0),
    Column("stumpings", Integer, nullable=False, default=0),
)

# Indexes for analytical performance
Index("idx_players_country", players_table.c.country)
Index("idx_matches_date", matches_table.c.match_date)
Index("idx_matches_format", matches_table.c.format)
Index("idx_batting_player", player_match_batting_table.c.player_id)
Index("idx_batting_date", player_match_batting_table.c.match_date)
Index("idx_bowling_player", player_match_bowling_table.c.player_id)
Index("idx_bowling_date", player_match_bowling_table.c.match_date)
Index("idx_career_format", player_career_stats_table.c.format)


_ENGINE: Optional[Engine] = None

def get_database_url() -> str:
    """
    Retrieves and standardizes the database URL from .env.
    Falls back to local SQLite if not configured.
    """
    raw_url = os.getenv("DATABASE_URL", "").strip()
    
    if not raw_url:
        sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cricbuzz.db")
        return f"sqlite:///{sqlite_path}"

    # Normalize PostgreSQL schemes for psycopg2
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+"):
        return raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    return raw_url

def get_engine() -> Engine:
    """Returns a singleton SQLAlchemy Engine instance with connection pooling."""
    global _ENGINE
    if _ENGINE is None:
        db_url = get_database_url()
        connect_args = {}
        if db_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        elif "sslmode" not in db_url and "neon.tech" in db_url:
            connect_args = {"sslmode": "require"}
            
        _ENGINE = create_engine(
            db_url,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=300
        )
    return _ENGINE

def get_db_type() -> str:
    """Identifies the underlying database dialect ('postgresql', 'sqlite', 'mysql', etc.)."""
    try:
        engine = get_engine()
        return engine.dialect.name
    except Exception:
        return "unknown"

def check_db_status() -> Dict[str, Any]:
    """Tests the database connection and returns diagnostic information."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        return {
            "status": "connected",
            "dialect": engine.dialect.name,
            "url_masked": _mask_url(get_database_url()),
            "table_count": len(table_names),
            "tables": table_names,
            "message": f"Successfully connected to {engine.dialect.name.upper()} database."
        }
    except Exception as e:
        return {
            "status": "error",
            "dialect": "unknown",
            "url_masked": "",
            "table_count": 0,
            "tables": [],
            "message": str(e)
        }

def _mask_url(url: str) -> str:
    """Masks database passwords for safe display."""
    if "@" in url:
        prefix, host_part = url.split("@", 1)
        if ":" in prefix:
            scheme_user = prefix.rsplit(":", 1)[0]
            return f"{scheme_user}:****@{host_part}"
    return url

def init_db() -> bool:
    """Initializes the database schema by creating all required tables."""
    try:
        engine = get_engine()
        metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"Error initializing database schema: {e}")
        return False

def execute_query(sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Executes a SQL SELECT query and returns the result as a Pandas DataFrame."""
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(text(sql), conn, params=params)
    return df

def execute_non_query(sql: str, params: Optional[Dict[str, Any]] = None) -> int:
    """Executes an INSERT, UPDATE, or DELETE SQL statement within a transaction."""
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text(sql), params or {})
        return result.rowcount

def sync_db_sequences() -> None:
    """Synchronizes PostgreSQL sequence generators to max(id) across all tables."""
    engine = get_engine()
    if engine.dialect.name != "postgresql":
        return
        
    tables = [
        ("teams", "team_id"),
        ("venues", "venue_id"),
        ("series", "series_id"),
        ("players", "player_id"),
        ("matches", "match_id"),
        ("player_match_batting", "batting_id"),
        ("player_match_bowling", "bowling_id"),
        ("player_fielding", "fielding_id"),
        ("partnerships", "partnership_id"),
        ("player_career_stats", "stat_id")
    ]
    with engine.begin() as conn:
        for tbl, col in tables:
            try:
                seq_sql = f"SELECT setval(pg_get_serial_sequence('{tbl}', '{col}'), COALESCE(MAX({col}), 0) + 1, false) FROM {tbl};"
                conn.execute(text(seq_sql))
            except Exception:
                pass
