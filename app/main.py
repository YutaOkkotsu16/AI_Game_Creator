"""
Main application entry point for the AI Game Creator
"""
import os
import sys
import json
import argparse

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.ai_parser.parser import GameDescriptionParser
from app.game_engine.engine import GameEngine
from app.web.server import run_server

def run_web_interface():
    """Run the web interface"""
    print("Starting AI Game Creator web interface...")
    run_server()

# Add this to run_game() function in app/main.py
def run_game(template_name, params_file):
    """
    Run a game with the specified template and parameters
    """
    try:
        # Load game parameters
        with open(params_file, 'r') as f:
            game_params = json.load(f)
        
        print(f"Creating game with template: {template_name}")
        print(f"Game parameters: {json.dumps(game_params, indent=2)}")
        
        # Create and run the game
        engine = GameEngine()
        
        # Add better error reporting
        try:
            success = engine.create_game(template_name, game_params)
            
            if success:
                print("Game created successfully! Starting game...")
                engine.run()
            else:
                print("Failed to create game.")
                # Keep window open for user to see error
                input("Press Enter to close...")
        except Exception as e:
            print(f"Error in game engine: {e}")
            import traceback
            traceback.print_exc()
            # Keep window open for user to see error
            input("Press Enter to close...")
    
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        # Keep window open for user to see error
        input("Press Enter to close...")

def interactive_mode():
    """Run the game creator in interactive console mode"""
    parser = GameDescriptionParser()
    
    print("=" * 50)
    print("AI Game Creator - Interactive Mode")
    print("=" * 50)
    print("Describe the game you want to create:")
    
    description = input("> ")
    
    print("\nProcessing your description...")
    game_params = parser.parse_description(description)
    
    print("\nI understood your game as:")
    print(json.dumps(game_params, indent=2))
    
    template_name = parser.get_game_template(game_params)
    print(f"\nSelected template: {template_name}")
    
    print("\nCreating your game...")
    engine = GameEngine()
    success = engine.create_game(template_name, game_params)
    
    if success:
        print("Game created successfully! Starting game...")
        engine.run()
    else:
        print("Failed to create game.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Game Creator")
    parser.add_argument("--web", action="store_true", help="Run the web interface")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive console mode")
    parser.add_argument("template", nargs="?", help="Game template to use")
    parser.add_argument("params_file", nargs="?", help="Path to game parameters JSON file")
    
    args = parser.parse_args()
    
    if args.web:
        run_web_interface()
    elif args.interactive:
        interactive_mode()
    elif args.template and args.params_file:
        run_game(args.template, args.params_file)
    else:
        # Default to interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()