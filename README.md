# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A comprehensive, full-stack cricket analytics platform that integrates live cricket data with a relational SQL database inside an interactive **Streamlit** multi-page web application.

---

## 🌟 Key Highlights

- **⚡ Real-Time Live Match Insights**: Live scores, batsman/bowler metrics, current run rates, and recent ball commentaries via Cricbuzz REST API.
- **📊 Top Player Stats & Visualizations**: Interactive leaderboards for highest runs, centuries, averages, and best bowling economy with Plotly charts.
- **🔍 25 Advanced SQL Practice Queries**: Categorized into **Beginner**, **Intermediate**, and **Advanced** tiers covering window functions, CTEs, standard deviation, clutch match analysis, toss impact, and composite player rankings.
- **🛠️ Full CRUD Operations**: Administrative interface to Create, Read, Update, and Delete player and match records with instant database persistence.
- **🗄️ Database-Agnostic Design**: Seamlessly switches between zero-config **SQLite** and production-grade **MySQL / PostgreSQL**.

---

## 🏗️ Project Architecture

```text
cricbuzz_livestats/
├── app.py                      # Main entry point & global layout configuration
├── requirements.txt            # Required Python packages
├── README.md                   # Setup guide and technical documentation
├── .env.example                # Template for RapidAPI keys & database credentials
├── pages/                      # Multi-page Streamlit views
│   ├── home.py                 # Overview, domain use-cases, and architecture
│   ├── live_matches.py         # Real-time live match scorecard & commentary
│   ├── top_stats.py            # Leading batting/bowling statistics & charts
│   ├── sql_queries.py          # Interactive execution engine for all 25 SQL queries
│   └── crud_operations.py      # Form-based CRUD interface for player data
├── utils/                      # Modular backend utilities
│   ├── db_connection.py        # Database-agnostic connection pool (SQLite / MySQL)
│   ├── api_handler.py          # Cricbuzz RapidAPI client with fallback & caching
│   ├── query_catalog.py        # Central repository for the 25 SQL queries & metadata
│   └── styles.py               # Custom UI tokens, dark-mode CSS, glassmorphism cards
└── notebooks/                  # Interactive experimentation
    └── data_fetching.ipynb     # API endpoint validation and ETL prototype
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone <your-github-repo-url>
cd <repo-folder>

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Copy `.env.example` to `.env` and provide your RapidAPI key if available:
```bash
cp .env.example .env
```
*(If no API key is provided, the application automatically uses high-fidelity simulation data for seamless offline grading and testing).*

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 🧮 25 SQL Practice Questions Breakdown

- **Beginner (Q1–Q8)**: Filter Indian players, recent matches, ODI top run scorers, stadium capacity >50k, wins per team, player roles, format records, 2024 series.
- **Intermediate (Q9–Q16)**: All-rounder dual criteria, recent 20 match details, multi-format player comparisons, home vs. away win analysis, 100+ run consecutive partnerships, venue-specific bowling averages, clutch close matches ($<50$ runs / $<5$ wickets), year-over-year player batting evolution.
- **Advanced (Q17–Q25)**: Toss impact on victory %, limited-overs economy leaders, batting consistency via Standard Deviation, cross-format $>20$ match averages, multi-discipline weighted formula scoring, head-to-head prediction model, player momentum & form classification (*Excellent/Good/Average/Poor*), top batting pairs, and quarterly time-series career trajectory analyzer.
