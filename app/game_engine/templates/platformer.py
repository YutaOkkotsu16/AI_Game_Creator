"""
Platformer game template
"""
import pygame
import os
import random
import sys
import math

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.game_engine.engine import GameObject, Player
from config.settings import DEFAULT_GAME_WIDTH, DEFAULT_GAME_HEIGHT

class Platform(GameObject):
    """Platform game object"""
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        super().__init__(x, y, width, height, color)

class Collectible(GameObject):
    """Collectible game object"""
    def __init__(self, x, y, size=20, color=(255, 255, 0)):
        super().__init__(x, y, size, size, color)
        self.collected = False
    
    def update(self):
        super().update()
        # Simple animation - bob up and down
        self.y += math.sin(pygame.time.get_ticks() * 0.005) * 0.5
        self.rect.y = self.y

class Enemy(GameObject):
    """Enemy game object"""
    def __init__(self, x, y, width, height, patrol_distance=100, color=(255, 0, 0)):
        super().__init__(x, y, width, height, color)
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.direction = 1
        self.speed = 2
    
    def update(self):
        # Patrol back and forth
        self.x += self.speed * self.direction
        
        # Change direction at patrol boundaries
        if self.x > self.start_x + self.patrol_distance:
            self.direction = -1
        elif self.x < self.start_x:
            self.direction = 1
        
        super().update()

class PlatformerGame:
    """Platformer game manager"""
    def __init__(self, player, platforms, collectibles, enemies, goal):
        self.player = player
        self.platforms = platforms
        self.collectibles = collectibles
        self.enemies = enemies
        self.goal = goal
        self.score = 0
        self.level_complete = False
    
    def update(self):
        """Update game state"""
        # Player update
        self.player.update()
        
        # Platform collisions
        self.player.on_ground = False
        for platform in self.platforms:
            if (self.player.rect.bottom >= platform.rect.top and
                self.player.rect.bottom <= platform.rect.top + 10 and
                self.player.rect.right > platform.rect.left and
                self.player.rect.left < platform.rect.right):
                
                self.player.on_ground = True
                self.player.y = platform.rect.top - self.player.height
                self.player.velocity_y = 0
        
        # Collectible collisions
        for collectible in self.collectibles:
            if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                self.score += 1
        
        # Enemy collisions
        for enemy in self.enemies:
            enemy.update()
            if self.player.rect.colliderect(enemy.rect):
                # Reset player position on enemy collision
                self.player.x = 100
                self.player.y = 100
        
        # Goal collision
        if self.player.rect.colliderect(self.goal.rect):
            self.level_complete = True
            # Display completion message
            font = pygame.font.Font(None, 74)
            text = font.render("Level Complete!", True, (0, 255, 0))
            self.screen.blit(text, (DEFAULT_GAME_WIDTH // 2 - 200, DEFAULT_GAME_HEIGHT // 2))

    def draw(self, screen):
        """Draw all game elements"""
        self.screen = screen
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                collectible.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw goal
        self.goal.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        # Draw level complete message if applicable
        if self.level_complete:
            font = pygame.font.Font(None, 74)
            text = font.render("Level Complete!", True, (0, 255, 0))
            screen.blit(text, (DEFAULT_GAME_WIDTH // 2 - 200, DEFAULT_GAME_HEIGHT // 2))

def create_game_objects(game_params, assets_dir):
    """
    Create game objects based on the game parameters
    
    Args:
        game_params (dict): Game parameters from the AI parser
        assets_dir (str): Path to the assets directory
        
    Returns:
        list: List of game objects
    """
    import math  # Import here to avoid circular import
    
    # Create player
    player = Player(100, 100, 50, 50, (0, 255, 0))
    
    # Create platforms
    platforms = []
    
    # Ground platform
    platforms.append(Platform(0, 550, DEFAULT_GAME_WIDTH, 50))
    
    # Add some additional platforms based on environment
    environment = game_params.get("environment", "").lower()
    
    if "mountain" in environment or "hill" in environment:
        # Create a mountain-like layout
        platforms.append(Platform(300, 450, 200, 20))
        platforms.append(Platform(500, 350, 200, 20))
        platforms.append(Platform(200, 250, 150, 20))
    elif "cave" in environment or "underground" in environment:
        # Create a cave-like layout
        platforms.append(Platform(200, 450, 100, 20))
        platforms.append(Platform(400, 350, 100, 20))
        platforms.append(Platform(600, 450, 100, 20))
        platforms.append(Platform(300, 250, 100, 20))
    else:
        # Default layout
        platforms.append(Platform(200, 450, 150, 20))
        platforms.append(Platform(400, 350, 200, 20))
        platforms.append(Platform(100, 250, 150, 20))
    
    # Create collectibles
    collectibles = []
    for _ in range(5):
        x = random.randint(50, DEFAULT_GAME_WIDTH - 50)
        y = random.randint(50, 500)
        collectibles.append(Collectible(x, y))
    
    # Create enemies
    enemies = []
    obstacles = game_params.get("obstacles", ["basic obstacle"])
    
    for i, obstacle in enumerate(obstacles[:3]):  # Limit to 3 enemies for simplicity
        x = 300 + i * 150
        y = 500 - (i * 20)
        patrol_distance = random.randint(50, 150)
        enemies.append(Enemy(x, y, 40, 40, patrol_distance))
    
    # Create goal
    goal = GameObject(700, 100, 50, 50, (0, 0, 255))
    
    # Create game manager
    game_manager = PlatformerGame(player, platforms, collectibles, enemies, goal)
    
    # Return all objects including the game manager
    all_objects = [player, game_manager, *platforms, *collectibles, *enemies, goal]
    return all_objects