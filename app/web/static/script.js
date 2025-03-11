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