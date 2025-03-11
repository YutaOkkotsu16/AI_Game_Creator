# AI Game Creator Platform - MVP

This is a minimal viable product (MVP) for an AI Game Creator platform that allows users to create simple games by describing them in natural language.

## Project Structure

```
ai-game-creator/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main application entry point
│   ├── ai_parser/       # AI text processing module
│   │   ├── __init__.py
│   │   └── parser.py    # Handles processing game descriptions
│   ├── game_engine/     # Game generation module
│   │   ├── __init__.py
│   │   ├── engine.py    # Core game engine functions
│   │   └── templates/   # Game templates
│   └── web/             # Web interface
│       ├── __init__.py
│       └── server.py    # Simple web server
├── assets/              # Game assets (sprites, sounds, etc.)
├── config/              # Configuration files
│   └── settings.py      # API keys and settings
├── tests/               # Test cases
└── requirements.txt     # Dependencies
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (or alternative LLM API)
- Dependencies listed in requirements.txt

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-game-creator.git
   cd ai-game-creator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

### Running the Application

#### Web Interface

1. Start the web server:
   ```
   python app/main.py --web
   ```

2. Open your browser and go to `http://127.0.0.1:5000`

3. Enter a game description and click "Create Game"

#### Interactive Console Mode

1. Run the application in interactive mode:
   ```
   python app/main.py --interactive
   ```

2. Follow the prompts to describe your game

## How It Works

1. **User Input**: The user describes a game they want to create
2. **AI Processing**: The AI parser analyzes the description and extracts key game parameters
3. **Template Selection**: The system selects an appropriate game template
4. **Game Generation**: The game engine creates a game based on the template and parameters
5. **Game Execution**: The generated game is launched in a separate window

## Extending the Platform

### Adding New Templates

1. Create a new template file in `app/game_engine/templates/`
2. Implement the `create_game_objects()` function
3. Update the `get_game_template()` function in `app/ai_parser/parser.py` to recognize and use your new template

### Improving the AI Parser

1. Enhance the prompt in `app/ai_parser/parser.py`
2. Add more parameters to extract from the description
3. Improve the mapping between extracted parameters and game elements

### Adding More Game Elements

1. Create new game object classes in `app/game_engine/engine.py`
2. Update the templates to use the new game objects
3. Extend the game engine to support new features

## Limitations

- The current MVP only supports simple 2D platformer games
- Limited game mechanics and elements
- Basic graphics and no sound
- No persistent storage for created games

## Future Enhancements

- Support for more game genres (puzzle, arcade, RPG, etc.)
- Custom sprite generation based on descriptions
- Sound and music generation
- Saving and sharing created games
- More complex game mechanics and AI behaviors
- Mobile support

## Core Concepts Learned

- **AI Integration**: Using large language models to process natural language input
- **Game Development**: Basic principles of game design and development
- **Software Architecture**: Building a modular and extensible system
- **Web Development**: Creating a simple web interface for user interaction
- **Python Programming**: Practical application of Python for a real-world project

## License

This project is licensed under the MIT License - see the LICENSE file for details.