import pygame
from random import randint

UNIT = 30
WIDTH = 20
HEIGHT = 30

screen = pygame.display.set_mode((WIDTH * UNIT, HEIGHT * UNIT))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

# =========================================== draw functions

COLOR_SNAKE = (68, 252, 120)
COLOR_POINT = (188, 35, 35)
COLOR_HEAD = (2, 96, 28)
COLOR_GRID = (40, 40, 40)
BACKGROUND = (0, 0, 0)


def draw_grid():
    for frame in range(HEIGHT):
        end_point = WIDTH * UNIT, frame * UNIT
        start_pint = 0, frame * UNIT
        pygame.draw.line(screen, COLOR_GRID, start_pint, end_point)

    for frame in range(WIDTH):
        end_point = frame * UNIT, 0
        start_pint = frame * UNIT, HEIGHT * UNIT
        pygame.draw.line(screen, COLOR_GRID, start_pint, end_point)


# =========================================== draw functions

# =========================================== fruits

MAX_POINTS = 50
points = []


def handle_fruits():
    while len(points) < MAX_POINTS:
        x = randint(0, WIDTH - 1)
        y = randint(0, HEIGHT - 1)

        if not (x, y) in points + snake:
            points.append((x, y))


def draw_fruits():
    for point in points:
        x = point[0] * UNIT
        y = point[1] * UNIT
        pygame.draw.rect(screen, COLOR_POINT, (x, y, UNIT, UNIT))


# =========================================== fruits

# =========================================== snake

x_snake = randint(0, WIDTH - 1)
y_snake = randint(0, HEIGHT - 1)

snake = [(x_snake, y_snake)]

direction = [0]


# 0 - up, 1 - right, 2 - down, 3 - left

def snake_gethead():
    return snake[-1]


def snake_pop_tail():
    snake.remove(snake[0])


def snake_eat_fruit():
    head = snake_gethead()
    if head in points:
        points.remove(head)
        return True
    else:
        return False


def snake_game_over():
    return snake_gethead() in snake[:-1]


def draw_snake():
    for segment in snake:
        x = segment[0] * UNIT
        y = segment[1] * UNIT
        pygame.draw.rect(screen, COLOR_SNAKE, (x, y, UNIT, UNIT))

    head = snake_gethead()
    x = head[0] * UNIT + 5
    y = head[1] * UNIT + 5
    pygame.draw.rect(screen, COLOR_HEAD, (x, y, UNIT - 10, UNIT - 10))


def snake_move():
    d = direction[0]
    head_x, head_y = snake_gethead()

    if d == 0:
        x_new = head_x
        y_new = head_y - 1

        if y_new < 0:
            y_new += HEIGHT

    elif d == 1:

        x_new = head_x + 1
        y_new = head_y

        if x_new > WIDTH - 1:
            x_new -= WIDTH

    elif d == 2:

        x_new = head_x
        y_new = head_y + 1

        if y_new > HEIGHT - 1:
            y_new -= HEIGHT

    else:

        x_new = head_x - 1
        y_new = head_y

        if x_new < 0:
            x_new += WIDTH

    new_head = (x_new, y_new)
    snake.append(new_head)

    if not snake_eat_fruit():
        snake_pop_tail()


# =========================================== snake

# =========================================== handle_player_movement

def handle_player_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and direction[0] != 2:
        direction[0] = 0

    elif keys[pygame.K_s] and direction[0] != 0:
        direction[0] = 2

    elif keys[pygame.K_a] and direction[0] != 1:
        direction[0] = 3

    elif keys[pygame.K_d] and direction[0] != 3:
        direction[0] = 1


# =========================================== handle_player_movement

while True:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill(BACKGROUND)
    handle_fruits()
    draw_fruits()
    handle_player_movement()
    snake_move()

    if snake_game_over():
        print(f'GAME OVER \nscore: {len(snake) - 1}')
        exit()

    draw_snake()
    draw_grid()

    pygame.display.update()
