"""
Web server module for the AI Game Creator
"""
from flask import Flask, render_template, request, jsonify
import os
import sys
import subprocess
import threading
import json

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.ai_parser.parser import GameDescriptionParser

app = Flask(__name__)
parser = GameDescriptionParser()

# Directory for templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app.template_folder = template_dir

# Directory for static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.static_folder = static_dir

@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")

@app.route("/create_game", methods=["POST"])
def create_game():
    """Create a game from a description"""
    description = request.form.get("description", "")
    
    if not description:
        return jsonify({"error": "No description provided"}), 400
    
    try:
        # Parse the description
        game_params = parser.parse_description(description)
        
        # Determine the appropriate template
        template_name = parser.get_game_template(game_params)
        
        # Save the game parameters to a temporary file
        params_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "game_params.json")
        
        with open(params_file, "w") as f:
            json.dump(game_params, f)
        
        # Start the game in a separate process
        game_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "main.py")
        
        # Run the game
        threading.Thread(target=lambda: subprocess.run(
            [sys.executable, game_script, template_name, params_file],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )).start()
        
        return jsonify({
            "success": True,
            "message": "Game created! Check the game window.",
            "game_params": game_params
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_template_dirs():
    """Create the template and static directories if they don't exist"""
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    
    # Create a basic HTML template
    index_path = os.path.join(template_dir, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, "w") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>AI Game Creator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>AI Game Creator</h1>
        <p>Describe the game you want to create:</p>
        
        <form id="game-form">
            <textarea id="game-description" rows="5" placeholder="E.g., A platformer game where a frog jumps through a swamp to collect flies and avoid alligators."></textarea>
            <button type="submit">Create Game</button>
        </form>
        
        <div id="result" class="hidden">
            <h2>Game Created!</h2>
            <p>Your game is running in a separate window. Here's what I understood:</p>
            <pre id="game-params"></pre>
        </div>
        
        <div id="error" class="hidden">
            <h2>Error</h2>
            <p id="error-message"></p>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
            """)

def run_server(host='127.0.0.1', port=5000, debug=True):
    """Run the web server"""
    create_template_dirs()
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_server()
    
    # Create a basic CSS file
    css_path = os.path.join(static_dir, "style.css")
    if not os.path.exists(css_path):
        with open(css_path, "w") as f:
            f.write("""
* {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    background-color: #f5f5f5;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    color: #333;
}

textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
    font-size: 16px;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
}

button:hover {
    background-color: #45a049;
}

.hidden {
    display: none;
}

#result, #error {
    margin-top: 20px;
    padding: 15px;
    border-radius: 4px;
}

#result {
    background-color: #dff0d8;
    border: 1px solid #d6e9c6;
    color: #3c763d;
}

#error {
    background-color: #f2dede;
    border: 1px solid #ebccd1;
    color: #a94442;
}

pre {
    background-color: #f8f8f8;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
}
            """)
    
    # Create a basic JavaScript file
    js_path = os.path.join(static_dir, "script.js")
    if not os.path.exists(js_path):
        with open(js_path, "w") as f:
            f.write("""
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('game-form');
    const descriptionInput = document.getElementById('game-description');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');
    const gameParamsDisplay = document.getElementById('game-params');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const description = descriptionInput.value.trim();
        
        if (!description) {
            showError('Please enter a game description.');
            return;
        }
        
        // Show loading state
        form.querySelector('button').textContent = 'Creating...';
        form.querySelector('button').disabled = true;
        
        // Hide previous results
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        
        // Submit the request
        const formData = new FormData();
        formData.append('description', description);
        
        fetch('/create_game', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                showResult(data);
            }
        })
        .catch(error => {
            showError('An error occurred: ' + error.message);
        })
        .finally(() => {
            // Reset button
            form.querySelector('button').textContent = 'Create Game';
            form.querySelector('button').disabled = false;
        });
    });
    
    function showResult(data) {
        gameParamsDisplay.textContent = JSON.stringify(data.game_params, null, 2);
        resultDiv.classList.remove('hidden');
        errorDiv.classList.add('hidden');
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
    }
});
            """)