import pygame

FRAMES_PER_SECOND = 75

# Initialize Pygame
pygame.init()

# Tuple representing width and height in pixels
screen_size = (1024, 768)

# Create window with given size
display_surface = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()

    display_surface.fill((0,0,0))

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)