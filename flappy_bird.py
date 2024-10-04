import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.1
FLAP_STRENGTH = -4
PIPE_GAP = 250
PIPE_SPEED = 1.5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Load Assets
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    flappy_bird_path = os.path.join(current_directory, 'flappy_bird.png')
    BIRD_IMAGE = pygame.image.load(flappy_bird_path).convert_alpha()
    BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (int(BIRD_IMAGE.get_width() * 0.066), int(BIRD_IMAGE.get_height() * 0.066)))
    
    rectangle_path = os.path.join(current_directory, 'rectangle.png')
    PIPE_IMAGE = pygame.image.load(rectangle_path).convert_alpha()
    PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_IMAGE.get_width(), SCREEN_HEIGHT // 2))
    
    background_path = os.path.join(current_directory, 'background.png')
    BACKGROUND_IMAGE = pygame.image.load(background_path).convert()
except pygame.error as e:
    print(f"Error loading assets: {e}")
    sys.exit()

# Clock to control the frame rate
clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.image = BIRD_IMAGE
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT / 2))
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()
        if self.rect.top <= 0:
            self.rect.top = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.top_rect = PIPE_IMAGE.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = PIPE_IMAGE.get_rect(midtop=(self.x, self.height + PIPE_GAP))

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        screen.blit(pygame.transform.flip(PIPE_IMAGE, False, True), self.top_rect)
        screen.blit(PIPE_IMAGE, self.bottom_rect)

    def is_off_screen(self):
        return self.x < -PIPE_IMAGE.get_width()

# Check for collision
def check_collision(bird, pipes):
    for pipe in pipes:
        bird_rect = bird.rect.inflate(-10, -10)
        if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
            return True
    return False

# Main game loop
def game_loop():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * (SCREEN_WIDTH // 2)) for i in range(2)]
    score = 0
    passed_pipes = []

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()
        bird.draw(screen)

        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)
            if pipe.is_off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))

            if pipe not in passed_pipes and bird.rect.left > pipe.top_rect.right:
                score += 1
                passed_pipes.append(pipe)

        font = pygame.font.Font(None, 36)
        score_surface = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_surface, (10, 10))

        if check_collision(bird, pipes):
            return

        pygame.display.update()
        clock.tick(FPS)

# Start the game
def main():
    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        font = pygame.font.Font(None, 48)
        text_surface = font.render('Press Space to Start', True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

if __name__ == "__main__":
    main()