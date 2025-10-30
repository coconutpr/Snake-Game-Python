# snake.py
# Joc de la serp (Snake) fet amb pygame
# Controls: fletxes o W/A/S/D. Esc per sortir. R per reiniciar després de perdre.

import pygame
import random
import sys

# ---- Configuració ----
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
CELL_SIZE = 20  # mida del bloc (serp i menjar)
assert WINDOW_WIDTH % CELL_SIZE == 0 and WINDOW_HEIGHT % CELL_SIZE == 0
CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
YELLOW = (230, 200, 0)

FPS_INITIAL = 8  # velocitat inicial (frames per second)
FPS_ACCEL = 0.5  # augmenta la velocitat per cada 5 punts

# ---- Funcions utilitàries ----
def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

def random_food_position(snake):
    while True:
        x = random.randint(0, CELL_WIDTH - 1)
        y = random.randint(0, CELL_HEIGHT - 1)
        pos = (x, y)
        if pos not in snake:
            return pos

def draw_rect_cell(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

# ---- Joc ----
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - Python / Pygame")

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)

    # Estat del joc
    def reset_game():
        mid_x = CELL_WIDTH // 2
        mid_y = CELL_HEIGHT // 2
        snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        direction = (1, 0)  # moure cap a la dreta
        food = random_food_position(snake)
        score = 0
        fps = FPS_INITIAL
        return snake, direction, food, score, fps

    snake, direction, food, score, fps = reset_game()
    game_over = False

    while True:
        # ---- Esdeveniments ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not game_over:
                    # Controls: fletxes i WASD
                    if event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        direction = (1, 0)
                    elif event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        direction = (0, 1)
                else:
                    # En pantalla de "game over"
                    if event.key == pygame.K_r:
                        snake, direction, food, score, fps = reset_game()
                        game_over = False

        if not game_over:
            # ---- Actualitzar l'estat ----
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Comprovacions de col·lisions amb paret
            hx, hy = new_head
            if hx < 0 or hx >= CELL_WIDTH or hy < 0 or hy >= CELL_HEIGHT:
                game_over = True
            else:
                # Comprovació col·lisió amb si mateixa
                if new_head in snake:
                    game_over = True
                else:
                    snake.insert(0, new_head)

                    # Ha menjat el menjar?
                    if new_head == food:
                        score += 1
                        food = random_food_position(snake)
                        # augmenta velocitat cada 5 punts
                        fps = FPS_INITIAL + (score // 5) * FPS_ACCEL
                    else:
                        snake.pop()  # manté la longitud si no menja

        # ---- Renderitzar ----
        screen.fill(BLACK)
        draw_grid(screen)

        # Menjar
        draw_rect_cell(screen, food, RED)

        # Serp: cap i cos amb ombrejat simple
        if snake:
            # cap
            draw_rect_cell(screen, snake[0], YELLOW)
            # cos
            for segment in snake[1:]:
                draw_rect_cell(screen, segment, GREEN)
            # petit rellotge d'ombra per fer-la més agradable
            for i, segment in enumerate(snake[1:], start=1):
                if i % 2 == 0:
                    x, y = segment
                    subrect = pygame.Rect(x * CELL_SIZE + CELL_SIZE//4,
                                          y *CELL_SIZE + CELL_SIZE//4,
                                          CELL_SIZE//2, CELL_SIZE//2)
                    pygame.draw.rect(screen, DARK_GREEN, subrect)

        # Marc i puntuació
        score_surf = font.render(f"Punts: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            over_surf = big_font.render("GAME OVER", True, WHITE)
            sub_surf = font.render("Prem R per reiniciar o Esc per sortir", True, WHITE)
            over_rect = over_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
            sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
            screen.blit(over_surf, over_rect)
            screen.blit(sub_surf, sub_rect)

        pygame.display.flip()

        clock.tick(fps)

if __name__ == "__main__":
    main()
