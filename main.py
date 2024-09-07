import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра попади в корзину")

# Загрузка иконки и изображений
icon = pygame.image.load("screens/logo3.png")
pygame.display.set_icon(icon)

# Цвета
WHITE = (212, 255, 212)
BLACK = (0, 0, 0)
GREEN = (212, 255, 212)
RED = (255, 0, 0)  # Добавим красный для сигнала

# Параметры игры
cup_speed = 10
basket_speed = 5
red_duration = 1000  # Время, на которое корзина станет красной (в миллисекундах)

# Загрузка изображений
basket_img = pygame.image.load("screens/basket40.png")
cup_img = pygame.image.load("screens/cup30.png")
background_img = pygame.image.load("screens/background.jpg")  # Загрузка фонового изображения

# Изменение размера изображений
basket_width, basket_height = basket_img.get_size()
cup_width, cup_height = cup_img.get_size()

# Позиции и размеры объектов
cup_x = WIDTH // 2 - cup_width // 2
cup_y = HEIGHT - cup_height - 10
cup_moving = False
cup_angle = 0  # Угол поворота стакана

basket_x = random.randint(0, WIDTH - basket_width)
basket_y = 100

# Кнопка конца игры
button_width, button_height = 150, 50
button_x = WIDTH - button_width
button_y = 10

# Счет и количество попыток
score = 0
attempts = 0
font = pygame.font.SysFont(None, 36)

# Таймер для отслеживания времени красного цвета корзины
red_timer = 0


def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))


def draw_button(x, y, w, h, text):
    pygame.draw.rect(screen, GREEN, (x, y, w, h))
    draw_text(text, x + 20, y + 10)


def draw_game(cup_x, cup_y, basket_x, basket_y, score, attempts, cup_angle, basket_color):
    screen.fill(WHITE)

    # Отображаем мусорный бак
    pygame.draw.rect(screen, basket_color, (basket_x, basket_y, basket_width, basket_height))  # Цвет корзины
    screen.blit(basket_img, (basket_x, basket_y))

    # Отображаем вращающийся стаканчик
    rotated_cup = pygame.transform.rotate(cup_img, cup_angle)
    rotated_cup_rect = rotated_cup.get_rect(center=(cup_x + cup_width // 2, cup_y + cup_height // 2))
    screen.blit(rotated_cup, rotated_cup_rect.topleft)

    draw_text(f"Попаданий: {score}", 10, 10)
    draw_text(f"Попыток: {attempts}", 10, 50)
    draw_button(button_x, button_y, button_width, button_height, "    СТОП")
    pygame.display.flip()


# Главный цикл игры
running = True
basket_color = GREEN  # Цвет корзины по умолчанию
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Проверка, нажата ли кнопка "Конец игры"
            if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                running = False

    keys = pygame.key.get_pressed()

    # Движение стаканчика влево и вправо
    if keys[pygame.K_LEFT] and cup_x > 0:
        cup_x -= cup_speed
    if keys[pygame.K_RIGHT] and cup_x < WIDTH - cup_width:
        cup_x += cup_speed

    # Стаканчик летит вверх по нажатию клавиши Enter
    if keys[pygame.K_RETURN] and not cup_moving:
        cup_moving = True
        attempts += 1  # Увеличение количества попыток при каждом запуске

    # Движение стаканчика вверх
    if cup_moving:
        cup_y -= cup_speed
        cup_angle += 10  # Увеличиваем угол поворота стакана
        if cup_y < 0:
            cup_y = HEIGHT - cup_height - 10
            cup_moving = False
            cup_angle = 0  # Сбрасываем угол поворота после остановки

    # Проверка на попадание в корзину
    if (
            basket_x < cup_x < basket_x + basket_width or basket_x < cup_x + cup_width < basket_x + basket_width) and cup_y <= basket_y + basket_height:
        score += 1
        cup_y = HEIGHT - cup_height - 10
        cup_moving = False
        basket_x = random.randint(0, WIDTH - basket_width)
        basket_color = RED  # Изменяем цвет корзины на красный при попадании
        red_timer = pygame.time.get_ticks()  # Запоминаем время попадания
        cup_angle = 0  # Сбрасываем угол поворота

    # Проверка времени: если прошло достаточно времени с момента попадания, вернуть цвет корзины в зеленый
    if pygame.time.get_ticks() - red_timer > red_duration:
        basket_color = GREEN

    # Рандомное движение корзины
    basket_x += basket_speed
    if basket_x <= 0 or basket_x >= WIDTH - basket_width:
        basket_speed = -basket_speed

    draw_game(cup_x, cup_y, basket_x, basket_y, score, attempts, cup_angle, basket_color)

pygame.quit()
