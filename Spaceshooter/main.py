import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 12

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(spelare_rocket, (self.x, self.y))

class Astroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(astroid_small, (self.x, self.y))


# background
background_blue = pygame.image.load("Spaceshooter/assets/backgrounds/bg.png")
background_stars = pygame.image.load("Spaceshooter/assets/backgrounds/Stars-A.png")

# background scrolling
bg_y = 0

# sprites
astroid_small = pygame.image.load("Spaceshooter/assets/sprites/small-A.png")

original_space_ship = pygame.image.load("Spaceshooter/assets/sprites/SpaceShip.png")
spelare = pygame.transform.scale(original_space_ship, (original_space_ship.get_width() // 2, original_space_ship.get_height() // 2))
spelare_x = screen_width // 2 - 120 
spelare_y = screen_height - 200
spelare_speed = 6

spelare_jetmotor = pygame.image.load("Spaceshooter/assets/sprites/fire.png")
jetstream_x = spelare_x + 13.5
jetstream_y = spelare_y + 50

spelare_rocket = pygame.image.load("Spaceshooter/assets/sprites/bullet.png")

# Initialize rocket list and related variables
rocket_list = []
rocket_count = 0
rocket_cooldown = 20

# Initialize asteroid list
asteroids = []
# Create initial asteroid
asteroids.append(Astroid(random.randint(0, screen_width - astroid_small.get_width()), 100))
# Variables for asteroid spawning
asteroid_spawn_timer = 0
asteroid_spawn_delay = 60  # Frames between asteroid spawns

# Main game loop
running = True
while running:
    # Draw backgrounds
    screen.blit(background_blue, (0, 0))
    screen.blit(background_stars, (0, bg_y))
    screen.blit(background_stars, (0, bg_y - screen_height))
    
    # Scroll background
    bg_y += 1.2
    if bg_y >= screen_height:
        bg_y = 0

    # Draw and move all asteroids
    for asteroid in list(asteroids):  # Use a copy of the list for safe removal
        asteroid.draw()
        asteroid.move()
        
        # Remove asteroids that move off screen
        if asteroid.y > screen_height:
            asteroids.remove(asteroid)
    
    # Spawn new asteroids periodically
    asteroid_spawn_timer += 1
    if asteroid_spawn_timer >= asteroid_spawn_delay:
        asteroids.append(Astroid(random.randint(0, screen_width - astroid_small.get_width()), -50))
        asteroid_spawn_timer = 0

    # Draw player ship and jetstream
    screen.blit(spelare, (spelare_x, spelare_y))
    screen.blit(spelare_jetmotor, (jetstream_x, jetstream_y))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    
    # Handle rocket firing
    if keys[pygame.K_SPACE]:
        if rocket_count > rocket_cooldown:
            rocket_list.append(Rocket(spelare_x + 14, spelare_y))
            rocket_count = 0
            spelare_speed = 4
    else:
        spelare_speed = 6

    
       
    rocket_count += 1
    
    # Update and draw rockets
    for rocket in list(rocket_list):  # Use a copy of the list for safe removal
        rocket.move()
        rocket.draw()

        if rocket.y < -100:
            rocket_list.remove(rocket)

    # Update the display
    pygame.display.flip()

    # Add a small delay to control frame rate
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()