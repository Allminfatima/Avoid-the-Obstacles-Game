import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define player properties
player_width = 40
player_height = 60
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 7

# Define obstacle properties
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 5

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Obstacles")

# Define clock for frame rate control
clock = pygame.time.Clock()

# Define font
font = pygame.font.SysFont(None, 35)

# Function to display text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Function to handle player movement
def handle_player_movement(keys_pressed, player_x):
    if keys_pressed[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys_pressed[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    return player_x

# Function to create obstacles
def create_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = -obstacle_height
    return [x, y]

# Function to show Game Over message
def game_over_message(score):
    screen.fill(WHITE)
    draw_text("Game Over", font, RED, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 30)
    draw_text(f"Your Score: {score}", font, BLACK, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 10)
    pygame.display.update()
    pygame.time.delay(3000)  # Pause for 3 seconds before quitting the game

# Main game loop
def game_loop():
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - player_height - 10
    
    obstacles = []
    spawn_time = 40  # Higher number = less frequent obstacle spawn
    counter = 0
    
    score = 0
    run_game = True
    
    while run_game:
        clock.tick(60)  # Set the FPS to 60
        counter += 1
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
        
        keys_pressed = pygame.key.get_pressed()
        player_x = handle_player_movement(keys_pressed, player_x)

        # Spawn obstacles periodically
        if counter % spawn_time == 0:
            obstacles.append(create_obstacle())
        
        # Move obstacles
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
        
        # Remove obstacles that have fallen off the screen
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < SCREEN_HEIGHT]
        
        # Check for collisions
        for obstacle in obstacles:
            if player_y < obstacle[1] + obstacle_height and player_y + player_height > obstacle[1]:
                if player_x < obstacle[0] + obstacle_width and player_x + player_width > obstacle[0]:
                    game_over_message(score)  # Show Game Over message
                    run_game = False  # End the game
        
        # Update score
        score += 1

        # Drawing
        screen.fill(WHITE)
        
        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
        
        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
        
        # Draw score
        draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)
        
        pygame.display.update()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game_loop()
