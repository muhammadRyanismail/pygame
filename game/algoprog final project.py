import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump King")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
sprite_sheet = pygame.image.load("character_spritesheet.png").convert_alpha()
platform_texture = pygame.image.load("platform_texture.png").convert_alpha()
sky_background = pygame.image.load("sky_background.png").convert_alpha()
sky_background = pygame.transform.scale(sky_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 20
        self.y = SCREEN_HEIGHT - 60
        self.width = 40
        self.height = 40

        # Animation settings
        self.current_frame = 0
        self.animation_frames = []
        self.load_sprites()

        # Physics properties
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 1

    def load_sprites(self):
        sprite_width = 32
        sprite_height = 32
        for i in range(3):
            frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            scaled_frame = pygame.transform.scale(frame, (self.width, self.height))
            self.animation_frames.append(scaled_frame)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += 5
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def jump(self):
        self.velocity_y = self.jump_power

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

    def check_collision(self, platforms):
        for platform in platforms:
            if (
                self.x + self.width > platform.x
                and self.x < platform.x + platform.width
                and self.y + self.height <= platform.y
                and self.y + self.height + self.velocity_y >= platform.y
            ):
                self.jump()
                return True
        return False

    def draw(self):
        current_sprite = self.animation_frames[self.current_frame]
        screen.blit(current_sprite, (self.x, self.y))

# Platform class
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

    def draw(self):
        platform_image = pygame.transform.scale(platform_texture, (self.width, self.height))
        screen.blit(platform_image, (self.x, self.y))

# Generate random platforms
def generate_platforms():
    platforms = []
    for i in range(6):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = i * (SCREEN_HEIGHT // 6)
        platforms.append(Platform(x, y))
    return platforms

# Constants for platform dimensions
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10

# Main game loop
def main():
    player = Player()
    platforms = generate_platforms()

    score = 0
    running = True
    while running:
        screen.blit(sky_background, (0, 0))  # Draw the background
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        player.move(keys)
        player.apply_gravity()
        if player.check_collision(platforms):
            score += 1

        # Scroll platforms and player upwards
        if player.y < SCREEN_HEIGHT // 4:
            player.y += 5
            for platform in platforms:
                platform.y += 5
                if platform.y > SCREEN_HEIGHT:
                    platform.y = 0
                    platform.x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                    score += 1

        # Check if player falls off the screen
        if player.y > SCREEN_HEIGHT:
            print(f"Game Over! Your score: {score}")
            running = False

        # Draw player and platforms
        player.draw()
        for platform in platforms:
            platform.draw()

        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
