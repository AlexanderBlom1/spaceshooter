import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Font setup
font_large = pygame.font.SysFont('Arial', 64)
font_medium = pygame.font.SysFont('Arial', 36)

FÄRG_LISTA = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]
explosioner = []

class Partikel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.livstid = random.randint(20, 50)  # Hur länge partikeln lever
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig rörelse i x-led
        self.hastighet_y = random.uniform(-2, 2)  # Slumpmässig rörelse i y-led
        self.radius = random.randint(3, 6)  # Storlek på partikeln
        self.färg = random.choice(FÄRG_LISTA)  # Slumpmässig färg

    def uppdatera(self):
        self.x += self.hastighet_x  # Flytta partikeln i x-led
        self.y += self.hastighet_y  # Flytta partikeln i y-led
        self.livstid -= 1  # Minska livslängden

    def rita(self, skärm):
        if self.livstid > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius)

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 12
        self.width = spelare_rocket.get_width()
        self.height = spelare_rocket.get_height()

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(spelare_rocket, (self.x, self.y))
        
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Astroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1.5, 2.5) 
        self.rotation = 0  
        self.rotation_speed = random.uniform(-1, 1)
        self.horizontal_drift = random.uniform(-2, 2)
        self.image = astroid_small
        self.rotated_image = self.image  
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.x += self.horizontal_drift 
        self.rotation += self.rotation_speed  
        self.rotation %= 360 

        # Rotate the asteroid image
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.rotated_image, self.rect.topleft)
        
    def get_hitbox(self):
        # Use the rotated image's rect for more accurate collision
        return self.rect

class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (220, 220, 220)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('Arial', 28)
        
    def draw(self):
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2, border_radius=8)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# Load game assets
def load_game_assets():
    global background_blue, background_stars, astroid_small
    global original_space_ship, spelare, spelare_jetmotor, spelare_rocket
    
    # background
    background_blue = pygame.image.load("Spaceshooter/assets/backgrounds/bg.png")
    background_stars = pygame.image.load("Spaceshooter/assets/backgrounds/Stars-A.png")
    
    # sprites
    astroid_small = pygame.image.load("Spaceshooter/assets/sprites/small-A.png")
    
    original_space_ship = pygame.image.load("Spaceshooter/assets/sprites/SpaceShip.png")
    spelare = pygame.transform.scale(original_space_ship, (original_space_ship.get_width() // 2, original_space_ship.get_height() // 2))
    
    spelare_jetmotor = pygame.image.load("Spaceshooter/assets/sprites/fire.png")
    spelare_rocket = pygame.image.load("Spaceshooter/assets/sprites/bullet.png")

# Initialize game state
def init_game():
    global spelare_x, spelare_y, spelare_speed, spelare_width, spelare_height
    global jetstream_x, jetstream_y
    global rocket_list, rocket_count, rocket_cooldown
    global asteroids, asteroid_spawn_timer, asteroid_spawn_delay
    global bg_y, score, spelare_hitbox

    global player_health
    player_health = 4
    
    # Player ship position and size
    spelare_width = spelare.get_width()
    spelare_height = spelare.get_height()
    
    # Player ship position and speed
    spelare_x = screen_width // 2 - spelare_width // 2
    spelare_y = screen_height - 200
    spelare_speed = 6
    
    # Create player hitbox (slightly smaller than the actual sprite for better gameplay)
    hitbox_reduction = 10  # Pixels to reduce from each side
    spelare_hitbox = pygame.Rect(
        spelare_x + hitbox_reduction, 
        spelare_y + hitbox_reduction, 
        spelare_width - 2 * hitbox_reduction, 
        spelare_height - 2 * hitbox_reduction
    )
    
    # Jetstream position - centered under the ship
    jetstream_x = spelare_x + (spelare_width - spelare_jetmotor.get_width()) // 2
    jetstream_y = spelare_y + spelare_height - 40
    
    # Initialize rocket list and related variables
    rocket_list = []
    rocket_count = 0
    rocket_cooldown = 20
    
    # Set rocket dimensions for all future rockets
    if not hasattr(Rocket, 'width_set'):
        Rocket.width = spelare_rocket.get_width()
        Rocket.height = spelare_rocket.get_height()
        Rocket.width_set = True
    
    # Initialize asteroid list
    asteroids = []
    # Create initial asteroid
    asteroids.append(Astroid(random.randint(0, screen_width - astroid_small.get_width()), 100))
    # Variables for asteroid spawning
    asteroid_spawn_timer = 0
    asteroid_spawn_delay = 15  # Frames between asteroid spawns
    
    # Background scrolling
    bg_y = 0
    
    # Score
    score = 0

# Game states
GAME_PLAYING = 0
GAME_MENU = -1
GAME_OVER = 1

# Load assets
load_game_assets()

# Initialize game
init_game()

# Create restart button
restart_button = Button(screen_width//2 - 100, screen_height//2 + 50, 200, 60, "Play Again")
start_button = Button(screen_width//2 - 100, screen_height//2, 200, 60, "START GAME")

# Initialize score
score = 0

# Set initial game state

game_state = GAME_MENU

# Debug mode for hitbox visualization (set to True to see hitboxes)
debug_mode = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for button clicks in game over state
        if game_state == GAME_OVER and restart_button.is_clicked(event):
            # Reset the game
            init_game()
            game_state = GAME_PLAYING
        
        # Toggle debug mode with D key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            debug_mode = not debug_mode
    
    # Playing state
        # Meny-läge
    if game_state == GAME_MENU:
        screen.blit(background_blue, (0, 0))
        screen.blit(background_stars, (0, bg_y))
        screen.blit(background_stars, (0, bg_y - screen_height))
        
        # Scrolla bakgrund
        bg_y += 1
        if bg_y >= screen_height:
            bg_y = 0

        # Titeltext
        title_text = font_large.render("SPACE SHOOTER", True, WHITE)
        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//2 - 150))
        
        # Start-knapp
        start_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if start_button.is_clicked(event):
                init_game()
                game_state = GAME_PLAYING

    if game_state == GAME_PLAYING:
        # Draw backgrounds
        screen.blit(background_blue, (0, 0))
        screen.blit(background_stars, (0, bg_y))
        screen.blit(background_stars, (0, bg_y - screen_height))

        health_bar_x = 20
        health_bar_y = 60
        bar_width = 200
        bar_height = 20
        health_ratio = player_health / 4
        current_bar_width = int(bar_width * health_ratio)

        # Background bar (gray)
        pygame.draw.rect(screen, (100, 100, 100), (health_bar_x, health_bar_y, bar_width, bar_height))
        # Health (green to red)
        health_color = (255 - int(155 * health_ratio), int(255 * health_ratio), 0)
        pygame.draw.rect(screen, health_color, (health_bar_x, health_bar_y, current_bar_width, bar_height))
        # Health border
        pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, bar_width, bar_height), 2)
        
        # Scroll background
        bg_y += 2
        if bg_y >= screen_height:
            bg_y = 0
    
        # Draw and move all asteroids
        for asteroid in list(asteroids):  # Use a copy of the list for safe removal
            asteroid.draw()
            asteroid.move()
            
            # Remove asteroids that move off screen
            if asteroid.y > screen_height:
                asteroids.remove(asteroid)
                
            # Debug: Draw asteroid hitbox
            if debug_mode:
                pygame.draw.rect(screen, (0, 255, 0), asteroid.get_hitbox(), 1)
        
        # Spawn new asteroids periodically
        asteroid_spawn_timer += 1
        if asteroid_spawn_timer >= asteroid_spawn_delay:
            asteroids.append(Astroid(random.randint(0, screen_width - astroid_small.get_width()), -50))
            asteroid_spawn_timer = 0
    
        # Draw player ship and jetstream
        screen.blit(spelare, (spelare_x, spelare_y))
        screen.blit(spelare_jetmotor, (jetstream_x, jetstream_y))
        
        # Debug: Draw player hitbox
        if debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), spelare_hitbox, 1)
    
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            spelare_x -= spelare_speed
            jetstream_x -= spelare_speed
        if keys[pygame.K_d]:
            spelare_x += spelare_speed
            jetstream_x += spelare_speed
        if keys[pygame.K_w]:
            spelare_y -= spelare_speed
            jetstream_y -= spelare_speed
        if keys[pygame.K_s]:        
            spelare_y += spelare_speed
            jetstream_y += spelare_speed
            
        # Update player hitbox position to match player position
        spelare_hitbox.x = spelare_x + (spelare_width - spelare_hitbox.width) // 2
        spelare_hitbox.y = spelare_y + (spelare_height - spelare_hitbox.height) // 2
        
        # Handle rocket firing
        if keys[pygame.K_SPACE]:
            if rocket_count > rocket_cooldown:
                # Center the rocket on the ship
                rocket_x = spelare_x + (spelare_width - Rocket.width) // 2
                rocket_list.append(Rocket(rocket_x, spelare_y))
                rocket_count = 0
                spelare_speed = 4
        else:
            spelare_speed = 6
    
        # Handle rocket collision with asteroids
        for rocket in list(rocket_list):
            rocket_hitbox = rocket.get_hitbox()
            
            # Debug: Draw rocket hitbox
            if debug_mode:
                pygame.draw.rect(screen, (0, 0, 255), rocket_hitbox, 1)
                
            for asteroid in list(asteroids):
                asteroid_hitbox = asteroid.get_hitbox()
                if rocket_hitbox.colliderect(asteroid_hitbox):
                    if rocket in rocket_list:
                        rocket_list.remove(rocket)
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)

                    # Create explosion at the asteroid's position
                    explosion = [Partikel(asteroid.rect.centerx, asteroid.rect.centery) for _ in range(30)]
                    explosioner.append(explosion)

                    # Increase score when asteroid is destroyed
                    score += 10
                    
        # Update and draw explosions
        for explosion in explosioner:
            for partikel in explosion:
                partikel.uppdatera()
                partikel.rita(screen)

        # Remove dead particles (those with a lifespan of 0)
        explosioner = [[p for p in explosion if p.livstid > 0] for explosion in explosioner]
        explosioner = [e for e in explosioner if len(e) > 0]  # Remove empty explosions
    
        # Handle ship collision with asteroids
        for asteroid in list(asteroids):
            asteroid_hitbox = asteroid.get_hitbox()
            if spelare_hitbox.colliderect(asteroid_hitbox):
                asteroids.remove(asteroid)
                player_health -= 1
        
        if player_health <= 0:
            game_state = GAME_OVER
    
        rocket_count += 1
        
        # Update and draw rockets
        for rocket in list(rocket_list):  # Use a copy of the list for safe removal
            rocket.move()
            rocket.draw()
    
            if rocket.y < -100:
                rocket_list.remove(rocket)
        
        # Draw score
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Draw debug mode indicator
        if debug_mode:
            debug_text = font_medium.render("DEBUG MODE (F1 to toggle)", True, (255, 255, 0))
            screen.blit(debug_text, (screen_width - debug_text.get_width() - 20, 20))
        
    # Game Over state
    elif game_state == GAME_OVER:
        # Draw background
        screen.blit(background_blue, (0, 0))
        screen.blit(background_stars, (0, bg_y))
        screen.blit(background_stars, (0, bg_y - screen_height))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Draw Game Over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 - 100))
        
        # Draw final score
        final_score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (screen_width//2 - final_score_text.get_width()//2, screen_height//2))
        
        # Draw restart button
        restart_button.draw()

    # Update the display
    pygame.display.flip()

    # Add a small delay to control frame rate
    pygame.time.delay(1)

# Quit Pygame
pygame.quit()       