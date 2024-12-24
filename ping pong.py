import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг с ИИ и счётом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройки ракетки
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 10

# Настройки мяча
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Создание ракеток
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Создание мяча
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

# Счёт
player_score = 0
opponent_score = 0

# Шрифт для отображения счёта
font = pygame.font.Font(None, 50)

# Функция для рестарта игры
def reset_game():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

# Основной цикл игры
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление ракетками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:  # Управление стрелкой вверх
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:  # Управление стрелкой вниз
        player_paddle.y += PADDLE_SPEED

    # Логика ИИ для противника
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += PADDLE_SPEED
    if opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= PADDLE_SPEED

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок мяча от верхней и нижней границ
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Отскок мяча от ракеток
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Проверка на пропуск мяча
    if ball.left <= 0:
        opponent_score += 1
        reset_game()
    if ball.right >= WIDTH:
        player_score += 1
        reset_game()

    # Отрисовка
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, player_paddle)
    pygame.draw.rect(WINDOW, WHITE, opponent_paddle)
    pygame.draw.ellipse(WINDOW, WHITE, ball)
    pygame.draw.aaline(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Отображение счёта
    score_text = font.render(f"{player_score}:{opponent_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 40))
    WINDOW.blit(score_text, score_rect)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)
