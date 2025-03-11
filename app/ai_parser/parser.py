"""
AI Parser module for processing game descriptions
"""
import json
from openai import OpenAI
import sys
import os

# Add the project root to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import OPENAI_API_KEY

# New way
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Your game description"}]
)
completion = response.choices[0].message.content

class GameDescriptionParser:
    """
    Parses natural language game descriptions into structured game parameters
    using a language model.
    """
    
    def __init__(self):
        """Initialize the parser"""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set. Please check your .env file.")
    
    def parse_description(self, description):
        """
        Parse a game description into structured game parameters
        
        Args:
            description (str): Natural language description of the game
            
        Returns:
            dict: Structured game parameters
        """
        # Define the prompt for the language model
        prompt = f"""
        You are a game design assistant. Convert the following game description 
        into a structured JSON format with the following keys:
        
        1. game_type: The type of game (platformer, puzzle, arcade, etc.)
        2. player_character: Description of the main character
        3. environment: Description of the game environment
        4. goal: The main objective of the game
        5. obstacles: List of obstacles or enemies
        6. mechanics: List of game mechanics
        
        Game Description: {description}
        
        Output only valid JSON without any explanation.
        """
        
        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can use a different model
                messages=[
                    {"role": "system", "content": "You are a game design assistant that outputs only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            # Extract and parse the JSON response
            result = response.choices[0].message.content.strip()
            game_params = json.loads(result)
            
            # Validate the required fields
            required_fields = ["game_type", "player_character", "environment", "goal"]
            for field in required_fields:
                if field not in game_params:
                    game_params[field] = "default"  # Provide defaults for missing fields
            
            return game_params
            
        except Exception as e:
            print(f"Error parsing game description: {e}")
            # Return default parameters if parsing fails
            return {
                "game_type": "platformer",
                "player_character": "character",
                "environment": "simple level",
                "goal": "reach the end",
                "obstacles": ["basic obstacle"],
                "mechanics": ["jump", "move"]
            }
    
    def get_game_template(self, game_params):
        """
        Determine the appropriate game template based on parsed parameters
        
        Args:
            game_params (dict): Structured game parameters
            
        Returns:
            str: Name of the template to use
        """
        # Simple logic to determine template based on game type
        game_type = game_params.get("game_type", "").lower()
        
        if "platformer" in game_type:
            return "platformer"
        elif "puzzle" in game_type:
            return "puzzle"
        elif "arcade" in game_type or "shooter" in game_type:
            return "arcade"
        else:
            # Default template
            return "platformer"

# Simple test function
def test_parser():
    parser = GameDescriptionParser()
    description = "A platformer game where a frog jumps through a swamp to collect flies and avoid alligators."
    result = parser.parse_description(description)
    print(json.dumps(result, indent=2))
    template = parser.get_game_template(result)
    print(f"Selected template: {template}")

if __name__ == "__main__":
    test_parser()