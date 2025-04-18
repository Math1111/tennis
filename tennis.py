import pygame
# модуль sys для работы с аргументами командной строки
import sys
import math  # Для работы с векторами скорости

# функция для искуственного интеллекта второго игрока
def update_ai():
    # Если мяч движется в сторону второго игрока
    if ball_rect.x > SCREEN_WIDTH // 2:
        # Если мяч выше центра ракетки, то двигаем ракетку вверх
        distance = ball_rect.centery - paddle2_rect.centery
        paddle2_rect.centery += distance * 0.6  # 0.1–0.2 — чувствительность, можно поэкспериментировать
    else:
        # Возвращаем ракетку в центр
        paddle2_rect.centery += (SCREEN_HEIGHT // 2 - paddle2_rect.centery) * 0.05


    # Проверяем, чтобы ракетка не вышла за границы экрана
    if paddle2_rect.top < 0:#<=
        paddle2_rect.top = 0
    if paddle2_rect.bottom >= SCREEN_HEIGHT:
        paddle2_rect.bottom = SCREEN_HEIGHT

    # Если мяч движется в сторону первого игрока, то центрируем ракетку
    else:
        paddle2_rect.centery += (SCREEN_HEIGHT // 2 - paddle2_rect.centery) / PADDLE_SPEED


# цвета ракеток и фона
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# размеры экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# размеры и скорость ракеток
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# размеры и начальная скорость мяча
BALL_SIZE = 10
INITIAL_BALL_SPEED = 5
BALL_SPEED_X = INITIAL_BALL_SPEED
BALL_SPEED_Y = INITIAL_BALL_SPEED

# FPS
FPS = 60

# Начальные координаты ракеток и мяча с помощью Rect
paddle1_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2_rect = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Начальный счет для обоих игроков
score1 = 0
score2 = 0

# Инициализируем библиотеку PyGame и создаем окно с заголовком "Pong"
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пинг Понг")

# Объект для контроля FPS
clock = pygame.time.Clock()

# Основной шрифт игры
font = pygame.font.Font(None, 48)

# Загружаем звуковые эффекты
bounce_sound = pygame.mixer.Sound("otscok.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
# режим игры: True - с искуственным интеллектом, False - с человеком
ai_mode = True

# Проверяем аргументы командной строкой
if len(sys.argv) > 1:
    if sys.argv[1] == "-human": # Если первый аргумент --human
        ai_mode = False # Устанавливаем режим игры с человеком

running = True

while running:
    # Обрабатываем события
    for event in pygame.event.get():
        # Если пользователь закрыл окно, то завершаем игру
        if event.type == pygame.QUIT:
            running = False

    # Получаем состояния клавиш
    keys = pygame.key.get_pressed()

    # Если нажата клавиша W, то перемещаем первую ракетку вверх
    if keys[pygame.K_w]:
        paddle1_rect.y -= PADDLE_SPEED

    # Если нажата клавиша S, то перемещаем первую ракетку вниз
    if keys[pygame.K_s]:
        paddle1_rect.y += PADDLE_SPEED

    # Проверяем, чтобы ракетка не вышла за нижнюю границу экрана
    if paddle1_rect.top <= 0:
        paddle1_rect.top = 0
    if paddle1_rect.bottom >= SCREEN_HEIGHT:
        paddle1_rect.bottom = SCREEN_HEIGHT

    # Если режим игры с человеком и нажата клавиша UP, то перемещаем вторую ракетку вверх
    if not ai_mode and keys[pygame.K_UP]:
        paddle2_rect.y -= PADDLE_SPEED

    # Если режим игры с человеком и нажата клавиша DOWN, то перемещаем вторую ракетку вниз
    if not ai_mode and keys[pygame.K_DOWN]:
        paddle2_rect.y += PADDLE_SPEED

    # Обновляем искуственный интеллект второго игрока
    if ai_mode:
        update_ai()

    # Обновляем координаты мяча
    ball_rect.x += BALL_SPEED_X
    ball_rect.y += BALL_SPEED_Y

    # Проверяем столкновение мяча с верхней и нижней границами экрана
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y
        bounce_sound.play()

    # Проверяем столкновение мяча с ракетками
    if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
        # Увеличиваем скорость на 10%
        BALL_SPEED_X *= -1.1  # Меняем направление и увеличиваем скорость
        BALL_SPEED_Y *= 1.1   # Увеличиваем вертикальную составляющую скорости
        bounce_sound.play()

    # Проверяем забитые очки
    if ball_rect.left <= 0:
        score2 += 1
        score_sound.play()
        ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Сбрасываем скорость мяча при забитии гола
        BALL_SPEED_X = INITIAL_BALL_SPEED if score1 + score2 % 2 == 0 else -INITIAL_BALL_SPEED
        BALL_SPEED_Y = INITIAL_BALL_SPEED
    if ball_rect.right >= SCREEN_WIDTH:
        score1 += 1
        score_sound.play()
        ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Сбрасываем скорость мяча при забитии гола
        BALL_SPEED_X = INITIAL_BALL_SPEED if score1 + score2 % 2 == 0 else -INITIAL_BALL_SPEED
        BALL_SPEED_Y = INITIAL_BALL_SPEED

    # Очищаем экран
    screen.fill(BLACK)

    # Рисуем ракетки и мяч
    pygame.draw.rect(screen, WHITE, paddle1_rect)
    pygame.draw.rect(screen, WHITE, paddle2_rect)
    pygame.draw.ellipse(screen, WHITE, ball_rect)

    # линия посередине экрана
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)

    # счет игроков
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

    # Обновляем экран
    pygame.display.flip()

    # Контролируем FPS
    clock.tick(FPS)

    # Завершаем работу библиотеки PyGame
pygame.quit()