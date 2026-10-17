"""
API handler for fetching real-time match data and statistics from Cricbuzz API.
Includes resilient fallback simulations when API keys are not supplied.
"""

import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
