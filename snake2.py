import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Realistic Snake Game")


BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (0, 255, 127)
SNAKE_HEAD_COLOR = (0, 200, 100)
FOOD_COLOR = (255, 85, 0)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
EYE_COLOR = (0, 0, 0)


BLOCK_SIZE = 20
SPEED = 10

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, block in enumerate(snake):
        x, y = block
        color = SNAKE_HEAD_COLOR if i == len(snake) - 1 else SNAKE_COLOR
        pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), border_radius=6)
        
        if i == len(snake) - 1:
            pygame.draw.circle(screen, EYE_COLOR, (x + 5, y + 6), 2)
            pygame.draw.circle(screen, EYE_COLOR, (x + 15, y + 6), 2)

def draw_food(position):
    x, y = position
    pygame.draw.rect(screen, FOOD_COLOR, (x, y, BLOCK_SIZE, BLOCK_SIZE), border_radius=5)

def display_text(text, y_offset=0):
    msg = font.render(text, True, TEXT_COLOR)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + y_offset))

def get_random_food(snake):
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:
            return (x, y)

def game_over_screen(score):
    screen.fill((20, 20, 20))
    display_text("💀 GAME OVER 💀", -40)
    display_text(f"Score: {score}", 10)
    display_text("Press R to Restart or Q to Quit", 50)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop():
    snake = [(100, 100), (120, 100)]
    direction = (BLOCK_SIZE, 0)
    food = get_random_food(snake)
    score = 0

    running = True
    while running:
        clock.tick(SPEED)
        screen.fill(BG_COLOR)
        draw_grid()
        draw_food(food)
        draw_snake(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                    direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                    direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                    direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                    direction = (BLOCK_SIZE, 0)

        
        head_x, head_y = snake[-1]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Check collisions
        if (
            new_head in snake
            or new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_over_screen(score)

        snake.append(new_head)

        if new_head == food:
            score += 1
            food = get_random_food(snake)
        else:
            snake.pop(0)

        pygame.display.flip()

    pygame.quit()


game_loop()


