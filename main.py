import pygame
import random
import math
import asyncio

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
INITIAL_FPS = 10
FPS = INITIAL_FPS  # Define FPS as a global variable
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2) * CELL_SIZE, (GRID_HEIGHT // 2) * CELL_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.colors = [(0, 255, 0), (65, 105, 225), (255, 215, 0), (255, 140, 0), (0, 0, 255), (50, 205, 50), (238, 130, 238),(0, 255, 255)]  # List of neon colors
        self.color_index = 0
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % WIDTH), (cur[1] + (y * CELL_SIZE)) % HEIGHT)
        if new in self.positions[2:]:
            return True  # Collision with itself
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2) * CELL_SIZE, (GRID_HEIGHT // 2) * CELL_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = self.colors[(self.color_index + i) % len(self.colors)]  # Cycle through neon colors
            pygame.draw.circle(surface, color, (p[0] + CELL_SIZE // 2, p[1] + CELL_SIZE // 2), CELL_SIZE // 2)  # Draw each segment of the snake as a circle
            pygame.draw.circle(surface, WHITE, (p[0] + CELL_SIZE // 2, p[1] + CELL_SIZE // 2), CELL_SIZE // 2, 1)

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Main function
async def main():
    global FPS  # Declare FPS as global

    snake = Snake()
    food = Food()
    speed_increase = 0
    running = True
    collided = False
    collision_message = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not collided:  # Disable movement after collision
                        snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    if not collided:
                        snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    if not collided:
                        snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    if not collided:
                        snake.turn(RIGHT)
                elif event.key == pygame.K_c and collided:  # Reset the game after collision
                    snake.reset()
                    collided = False
                    speed_increase = 0
                    FPS = INITIAL_FPS

        if not collided:
            collided = snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            if snake.score % 5 == 0:  # Increase speed every 5 preys eaten
                speed_increase += 1
                FPS = INITIAL_FPS + speed_increase * 2

        screen.fill((0, 0, 0))
        snake.draw(screen)
        food.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(text, (10, 10))

        if collided:
            font = pygame.font.SysFont(None, 30)
            text = font.render("You collided with yourself! Press 'C' to start again", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.update()
        clock.tick(FPS)
        
    
        await asyncio.sleep(0)
    pygame.quit()
    
    


asyncio.run(main())
