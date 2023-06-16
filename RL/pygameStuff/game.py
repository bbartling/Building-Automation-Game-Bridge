import pygame
import sys

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mario Level")
clock = pygame.time.Clock()

# Load Mario image and create rectangle
mario_image = pygame.image.load("mario.png")
mario_rect = pygame.Rect(100, 500, 40, 40)  # Adjusted size
mario_image = pygame.transform.scale(mario_image, (40, 40))  # Adjusted size

# Load question box image and create rectangle
question_box_image = pygame.image.load("question_box.png")
question_box_rect = pygame.Rect(150, 50, 40, 40)  # Adjusted position and size
question_box_image = pygame.transform.scale(question_box_image, (40, 40))  # Adjusted size
question_box_active = True

# Create platforms
platforms = [
    pygame.Rect(50, 500, 200, 10),
    pygame.Rect(300, 450, 200, 10),
    pygame.Rect(150, 175, 200, 10),
    pygame.Rect(210, 400, 200, 10),
    pygame.Rect(260, 300, 200, 10),
]

# Set up variables for vertical movement
falling = True
vertical_velocity = 0.0
jump_power = 14.0
gravity = 0.6

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario_rect.move_ip(-5, 0)
    if keys[pygame.K_RIGHT]:
        mario_rect.move_ip(5, 0)
    if keys[pygame.K_SPACE] and not falling:
        vertical_velocity -= jump_power
        falling = True

    # Apply gravity
    vertical_velocity += gravity
    mario_rect.move_ip(0, vertical_velocity)

    # Check for collisions with platforms
    for platform in platforms:
        if mario_rect.colliderect(platform):
            # Handle collision
            if vertical_velocity > 0:
                mario_rect.bottom = platform.top
                falling = False
                vertical_velocity = 0.0
            elif vertical_velocity < 0:
                mario_rect.top = platform.bottom
                vertical_velocity = 0.0

    # Check if Mario touches the question box
    if mario_rect.colliderect(question_box_rect) and question_box_active:
        # Handle victory
        running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), platform)

    # Draw question box
    if question_box_active:
        screen.blit(question_box_image, question_box_rect)

    # Draw Mario
    screen.blit(mario_image, mario_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
