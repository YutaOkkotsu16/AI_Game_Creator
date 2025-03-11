"""
Game Engine module for generating and running games
"""
import pygame
import os
import sys
import json
import random
from importlib import import_module

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import DEFAULT_GAME_WIDTH, DEFAULT_GAME_HEIGHT, FPS, TEMPLATES_DIR, ASSETS_DIR

class GameEngine:
    """
    Core game engine that generates and runs games based on templates and parameters
    """
    
    def __init__(self):
        """Initialize the game engine"""
        pygame.init()
        self.screen = pygame.display.set_mode((DEFAULT_GAME_WIDTH, DEFAULT_GAME_HEIGHT))
        pygame.display.set_caption("AI Game Creator")
        self.clock = pygame.time.Clock()
        self.running = False
        self.game_objects = []
        
    def create_game(self, template_name, game_params):
        """
        Create a game based on a template and parameters
        
        Args:
            template_name (str): Name of the template to use
            game_params (dict): Game parameters
            
        Returns:
            bool: Success or failure
        """
        try:
            # For debugging, print the full path
            full_template_path = f"app.game_engine.templates.{template_name}"
            print(f"Trying to load template from: {full_template_path}")
            
            # Load the template module
            template_path = f"app.game_engine.templates.{template_name}"
            template = import_module(template_path)
            
            # Create game objects based on the template
            self.game_objects = template.create_game_objects(game_params, ASSETS_DIR)
            
            # Set game title based on description
            pygame.display.set_caption(f"AI Game: {game_params.get('game_type', 'Game')}")
            
            return True
        except Exception as e:
            print(f"Error creating game: {e}")
            return False
    
    def run(self):
        """Run the game loop"""
        self.running = True
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Pass events to game objects
                for obj in self.game_objects:
                    if hasattr(obj, 'handle_event'):
                        obj.handle_event(event)
            
            # Update game objects
            for obj in self.game_objects:
                if hasattr(obj, 'update'):
                    obj.update()
            
            # Render
            self.screen.fill((0, 0, 0))  # Clear screen
            
            # Draw game objects
            for obj in self.game_objects:
                if hasattr(obj, 'draw'):
                    obj.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def stop(self):
        """Stop the game loop"""
        self.running = False

# Base game object class for templates to use
class GameObject:
    """Base class for all game objects"""
    
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        """Initialize the game object"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None
    
    def update(self):
        """Update the game object"""
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """Draw the game object"""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

class Player(GameObject):
    """Player game object"""
    
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        """Initialize the player"""
        super().__init__(x, y, width, height, color)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = 10
        self.gravity = 0.5
        self.on_ground = False
    
    def handle_event(self, event):
        """Handle player input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity_x = -self.speed
            if event.key == pygame.K_RIGHT:
                self.velocity_x = self.speed
            if event.key == pygame.K_SPACE and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False
        
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.velocity_x = 0
    
    def update(self):
        """Update player position and physics"""
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Check boundaries (simple collision with screen edges)
        if self.x < 0:
            self.x = 0
        if self.x > DEFAULT_GAME_WIDTH - self.width:
            self.x = DEFAULT_GAME_WIDTH - self.width
        
        if self.y > DEFAULT_GAME_HEIGHT - self.height:
            self.y = DEFAULT_GAME_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        # Update rect position
        super().update()

# Example test function
def test_engine():
    engine = GameEngine()
    
    # Create a simple player object for testing
    player = Player(100, 100, 50, 50)
    platform = GameObject(50, 500, 700, 20, (100, 100, 100))
    
    engine.game_objects = [player, platform]
    engine.run()


if __name__ == "__main__":
    test_engine()