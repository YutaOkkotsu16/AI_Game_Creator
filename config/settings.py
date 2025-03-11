"""
Configuration settings for the AI Game Creator
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Game settings
DEFAULT_GAME_WIDTH = 800
DEFAULT_GAME_HEIGHT = 600
FPS = 60

# Template settings
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            "app", "game_engine", "templates")

# Asset settings
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

# Check if API key is set
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please add it to your .env file or export it directly.")