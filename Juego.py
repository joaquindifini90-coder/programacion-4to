import pygame
import random

# ===== PERSONALIZÁ ACÁ =====
COLOR = (50, 205, 50)   # color de la serpiente (rojo, verde, azul)
SPEED = 110             # milisegundos por paso (menos = más rápida)
# ===========================

S = 20  # tamaño de cada cuadrito

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 28)


def reset():
    global snake, direction, food, started
    snake = [(10, 10), (9, 10), (8, 10)]  # 3 bloques, el primero es la cabeza
    direction = (1, 0)
    food = (15, 10)
    started = False


def draw():
    screen.fill((34, 34, 34))

    # comida
    pygame.draw.rect(screen, (255, 0, 0), (food[0] * S, food[1] * S, S, S))

    # serpiente
    for x, y in snake:
        pygame.draw.rect(screen, COLOR, (x * S, y * S, S - 1, S - 1))

    # ojos (dos cuadraditos blancos del lado hacia donde mira)
    hx, hy = snake[0]
    dx, dy = direction
    for lado in (-1, 1):
        ex = hx * S + 8 + dx * 5 - dy * 4 * lado
        ey = hy * S + 8 + dy * 5 + dx * 4 * lado
        pygame.draw.rect(screen, (255, 255, 255), (ex, ey, 4, 4))

    # textos
    screen.blit(font.render("Puntos: " + str(len(snake) - 3), True, (255, 255, 255)), (10, 10))
    if not started:
        screen.blit(font.render("Toca una flecha para empezar", True, (255, 255, 255)), (80, 190))

    pygame.display.flip()


reset()
last_move = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            new = None
            if event.key == pygame.K_UP:
                new = (0, -1)
            elif event.key == pygame.K_DOWN:
                new = (0, 1)
            elif event.key == pygame.K_LEFT:
                new = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                new = (1, 0)

            # no se puede ir para atrás
            if new and new != (-direction[0], -direction[1]):
                direction = new
                started = True  # la primera flecha arranca el juego

    now = pygame.time.get_ticks()
    if started and now - last_move >= SPEED:
        last_move = now
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # choque con pared o con ella misma
        if head[0] < 0 or head[1] < 0 or head[0] > 19 or head[1] > 19 or head in snake:
            screen.blit(font.render("Game Over", True, (255, 255, 255)), (150, 150))
            pygame.display.flip()
            pygame.time.wait(1000)
            reset()
        else:
            snake.insert(0, head)
            if head == food:
                food = (random.randint(0, 19), random.randint(0, 19))
            else:
                snake.pop()

    draw()