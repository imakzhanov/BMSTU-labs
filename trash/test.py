import pygame
import math
import sys

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Анимации - выберите номер")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_BLUE = (135, 206, 235)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
GRASS_GREEN = (34, 139, 34)
SAND = (244, 164, 96)
PINK = (255, 192, 203)

# Шрифты
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)


def draw_menu():
    """Рисует меню выбора анимации"""
    screen.fill(LIGHT_BLUE)

    title = font_large.render("ВЫБЕРИТЕ АНИМАЦИЮ (1-25)", True, DARK_BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Показываем доступные анимации
    y = 120
    for i in range(1, 26):
        text = font_small.render(f"{i}. {animations[i]['name']}", True, BLACK)
        col = (i - 1) // 13
        x = 100 + col * 300
        screen.blit(text, (x, y + ((i - 1) % 13) * 25))

    prompt = font_medium.render("Нажмите номер на клавиатуре (1-25)", True, BLACK)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 80))

    pygame.display.flip()


def wait_for_choice():
    """Ожидает ввод номера анимации"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    return event.key - pygame.K_1 + 1
                if pygame.K_0 <= event.key <= pygame.K_9:
                    # Для двухзначных чисел
                    pass
        draw_menu()
        clock.tick(30)
    return None


# ==================== АНИМАЦИИ ====================

def animation_1():  # Человек пьёт чай
    angle = 0
    pinky_angle = 0
    direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Тело человека
        pygame.draw.rect(screen, BLUE, (350, 300, 100, 150))
        pygame.draw.circle(screen, (255, 200, 150), (400, 270), 40)

        # Движение 1: рука с чашкой ко рту
        arm_angle = math.sin(angle) * 0.5
        hand_x = 450 + math.sin(arm_angle) * 30
        hand_y = 280 + math.cos(arm_angle) * 20

        pygame.draw.line(screen, BLUE, (400, 320), (hand_x, hand_y), 10)
        pygame.draw.circle(screen, BROWN, (int(hand_x), int(hand_y)), 15)  # чашка

        # Движение 2: отставленный мизинец
        pinky_angle = math.sin(angle * 2) * 30
        pinky_x = hand_x + 20 + math.sin(pinky_angle) * 10
        pinky_y = hand_y - 10
        pygame.draw.line(screen, (255, 200, 150), (hand_x + 15, hand_y - 5),
                         (pinky_x, pinky_y), 4)

        angle += 0.05

        # Глаза
        pygame.draw.circle(screen, BLACK, (385, 260), 5)
        pygame.draw.circle(screen, BLACK, (415, 260), 5)

        pygame.display.flip()
        clock.tick(60)


def animation_2():  # Надевание рюкзака
    arm_angle = 0
    body_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Движение 2: корпус наклоняется
        body_angle = math.sin(arm_angle) * 10
        center_x = 400 + body_angle

        # Тело
        pygame.draw.rect(screen, BLUE, (center_x - 50, 300, 100, 150))
        pygame.draw.circle(screen, (255, 200, 150), (int(center_x), 270), 40)

        # Движение 1: рука в лямку
        arm_angle_val = math.sin(arm_angle) * 40
        hand_x = center_x + 50 + arm_angle_val
        hand_y = 320
        pygame.draw.line(screen, BLUE, (center_x + 30, 320), (hand_x, hand_y), 10)

        # Рюкзак
        pygame.draw.rect(screen, GREEN, (center_x - 30, 310, 60, 80))

        arm_angle += 0.05

        pygame.display.flip()
        clock.tick(60)


def animation_3():  # Зевание
    mouth_height = 0
    arms_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Тело
        pygame.draw.rect(screen, BLUE, (350, 300, 100, 150))
        pygame.draw.circle(screen, (255, 200, 150), (400, 270), 40)

        # Движение 1: рот открывается
        mouth_height = 10 + math.sin(arms_angle) * 15
        pygame.draw.ellipse(screen, RED, (385, 275, 30, mouth_height))

        # Движение 2: руки тянутся вверх
        arm_up = math.sin(arms_angle) * 50
        pygame.draw.line(screen, BLUE, (370, 320), (350, 250 - arm_up), 10)
        pygame.draw.line(screen, BLUE, (430, 320), (450, 250 - arm_up), 10)

        arms_angle += 0.05

        # Глаза (закрыты)
        pygame.draw.line(screen, BLACK, (380, 260), (390, 260), 3)
        pygame.draw.line(screen, BLACK, (410, 260), (420, 260), 3)

        pygame.display.flip()
        clock.tick(60)


def animation_4():  # Удар по мячу ногой
    leg_angle = 0
    arm_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Земля
        pygame.draw.rect(screen, GRASS_GREEN, (0, 450, WIDTH, 150))

        # Тело
        pygame.draw.rect(screen, RED, (350, 280, 80, 120))
        pygame.draw.circle(screen, (255, 200, 150), (390, 250), 35)

        # Движение 2: противоположная рука для баланса
        arm_angle_val = math.sin(arm_angle) * 30
        pygame.draw.line(screen, RED, (380, 300), (340, 270 - arm_angle_val), 8)

        # Движение 1: замах ногой
        leg_angle_val = math.sin(leg_angle) * 60
        leg_x = 380 + leg_angle_val
        leg_y = 420
        pygame.draw.line(screen, BLUE, (370, 400), (leg_x, leg_y), 12)

        # Мяч
        pygame.draw.circle(screen, ORANGE, (450, 430), 20)

        leg_angle += 0.05
        arm_angle = leg_angle  # синхронно

        pygame.display.flip()
        clock.tick(60)


def animation_5():  # Бросок баскетбольного мяча
    ball_y = 300
    ball_vy = 0
    hand_angle = 0
    shooting = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE and not shooting:
                    shooting = True
                    ball_vy = -15

        screen.fill(WHITE)

        # Кольцо
        pygame.draw.circle(screen, RED, (600, 200), 25, 3)
        pygame.draw.rect(screen, RED, (575, 200, 50, 10))

        # Тело
        pygame.draw.rect(screen, BLUE, (300, 280, 80, 120))
        pygame.draw.circle(screen, (255, 200, 150), (340, 250), 35)

        # Движение 1: рука выталкивает мяч
        hand_angle = math.sin(pygame.time.get_ticks() / 200) * 30 if not shooting else hand_angle
        hand_x = 360 + hand_angle

        # Движение 2: кисть делает толчок
        wrist_angle = math.sin(pygame.time.get_ticks() / 100) * 20

        pygame.draw.line(screen, BLUE, (340, 300), (hand_x, 270), 8)
        pygame.draw.line(screen, (255, 200, 150), (hand_x, 270),
                         (hand_x + wrist_angle, 260), 5)

        # Мяч
        if shooting:
            ball_y += ball_vy
            ball_vy += 0.5
            if ball_y > 500:
                shooting = False
                ball_y = 300
            pygame.draw.circle(screen, ORANGE, (hand_x + 20, int(ball_y)), 15)
        else:
            pygame.draw.circle(screen, ORANGE, (hand_x + 20, 280), 15)

        pygame.display.flip()
        clock.tick(60)


def animation_6():  # Бег на месте
    leg_phase = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Земля
        pygame.draw.rect(screen, GRASS_GREEN, (0, 450, WIDTH, 150))

        # Движение 1: ноги бегут
        leg_offset = math.sin(leg_phase) * 30

        # Левая нога
        pygame.draw.line(screen, BLUE, (360, 420), (340 + leg_offset, 450), 12)
        # Правая нога
        pygame.draw.line(screen, BLUE, (380, 420), (400 - leg_offset, 450), 12)

        # Тело
        pygame.draw.rect(screen, RED, (340, 300, 80, 120))
        pygame.draw.circle(screen, (255, 200, 150), (380, 270), 35)

        # Движение 2: противоположная рука
        arm_offset = math.sin(leg_phase + math.pi) * 30
        pygame.draw.line(screen, RED, (360, 320), (330 + arm_offset, 290), 8)
        pygame.draw.line(screen, RED, (400, 320), (430 - arm_offset, 290), 8)

        leg_phase += 0.1

        pygame.display.flip()
        clock.tick(60)


def animation_7():  # Плавание кролем
    arm_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(LIGHT_BLUE)

        # Вода
        pygame.draw.rect(screen, BLUE, (0, 350, WIDTH, 250))

        # Тело пловца (горизонтально)
        pygame.draw.ellipse(screen, (255, 200, 150), (350, 300, 100, 40))

        # Движение 1: гребок рукой
        arm_angle_val = math.sin(arm_angle) * 60
        pygame.draw.line(screen, (255, 200, 150), (400, 310),
                         (450 + arm_angle_val, 290), 8)

        # Движение 2: голова поворачивается для вдоха
        head_turn = math.sin(arm_angle * 2) * 20
        pygame.draw.circle(screen, (255, 200, 150), (360 + head_turn, 300), 20)

        arm_angle += 0.1

        pygame.display.flip()
        clock.tick(60)


def animation_8():  # Подтягивание на турнике
    body_y = 0
    leg_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Движение 1: тело поднимается вверх
        body_y = math.sin(leg_angle) * 50
        body_y = max(0, body_y)

        # Турник
        pygame.draw.line(screen, GRAY, (300, 100), (500, 100), 10)
        pygame.draw.line(screen, GRAY, (320, 100), (320, 200), 10)
        pygame.draw.line(screen, GRAY, (480, 100), (480, 200), 10)

        # Руки
        pygame.draw.line(screen, (255, 200, 150), (340, 100), (370, 200 - body_y), 8)
        pygame.draw.line(screen, (255, 200, 150), (460, 100), (430, 200 - body_y), 8)

        # Тело
        pygame.draw.rect(screen, RED, (360, 200 - body_y, 80, 100))
        pygame.draw.circle(screen, (255, 200, 150), (400, 190 - body_y), 30)

        # Движение 2: ноги сгибаются
        leg_angle_val = math.sin(leg_angle) * 20
        pygame.draw.line(screen, BLUE, (370, 300 - body_y), (350, 340 - body_y + leg_angle_val), 10)
        pygame.draw.line(screen, BLUE, (430, 300 - body_y), (450, 340 - body_y + leg_angle_val), 10)

        leg_angle += 0.05

        pygame.display.flip()
        clock.tick(60)


def animation_9():  # Кошка умывается
    paw_angle = 0
    ear_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Тело кошки
        pygame.draw.ellipse(screen, ORANGE, (300, 300, 150, 100))
        pygame.draw.circle(screen, ORANGE, (370, 280), 40)

        # Хвост
        pygame.draw.line(screen, ORANGE, (450, 330), (500, 300), 8)

        # Движение 2: ухо дёргается
        ear_angle = math.sin(paw_angle * 3) * 5
        pygame.draw.polygon(screen, ORANGE, [(350, 250), (360, 220 + ear_angle), (370, 250)])
        pygame.draw.polygon(screen, ORANGE, [(380, 250), (390, 220 - ear_angle), (400, 250)])

        # Движение 1: лапа трёт морду
        paw_x = 380 + math.sin(paw_angle) * 20
        paw_y = 280 + math.cos(paw_angle * 2) * 15
        pygame.draw.ellipse(screen, ORANGE, (int(paw_x), int(paw_y), 20, 15))

        # Глаза
        pygame.draw.circle(screen, GREEN, (360, 275), 5)
        pygame.draw.circle(screen, GREEN, (390, 275), 5)

        paw_angle += 0.1

        pygame.display.flip()
        clock.tick(60)


def animation_10():  # Собака виляет хвостом
    tail_angle = 0
    tongue_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(WHITE)

        # Тело
        pygame.draw.ellipse(screen, BROWN, (300, 300, 180, 100))
        pygame.draw.circle(screen, BROWN, (320, 280), 40)

        # Движение 1: хвост
        tail_angle = math.sin(pygame.time.get_ticks() / 100) * 30
        tail_end_x = 480 + math.cos(math.radians(tail_angle)) * 40
        tail_end_y = 320 + math.sin(math.radians(tail_angle)) * 20
        pygame.draw.line(screen, BROWN, (470, 330), (tail_end_x, tail_end_y), 12)

        # Движение 2: язык высовывается
        tongue_out = math.sin(tongue_angle) * 15
        pygame.draw.ellipse(screen, PINK, (305, 285, 15, 10 + tongue_out))

        # Нос и глаза
        pygame.draw.circle(screen, BLACK, (290, 275), 5)
        pygame.draw.circle(screen, BLACK, (300, 260), 3)
        pygame.draw.circle(screen, BLACK, (320, 260), 3)

        tongue_angle += 0.1

        pygame.display.flip()
        clock.tick(60)


def animation_11():  # Птица чистит перья
    beak_angle = 0
    wing_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(SKY_BLUE)

        # Тело
        pygame.draw.ellipse(screen, BLUE, (350, 250, 100, 60))
        pygame.draw.circle(screen, BLUE, (370, 240), 25)

        # Движение 1: клюв захватывает перо
        beak_angle = math.sin(pygame.time.get_ticks() / 150) * 20
        beak_x = 350 + beak_angle
        pygame.draw.polygon(screen, YELLOW, [(345, 235), (beak_x, 245), (345, 255)])

        # Движение 2: крыло приподнимается
        wing_angle = math.sin(pygame.time.get_ticks() / 200) * 30
        wing_points = [(380, 260), (420, 250 + wing_angle), (430, 280 + wing_angle), (390, 280)]
        pygame.draw.polygon(screen, BLUE, wing_points)

        # Глаз
        pygame.draw.circle(screen, BLACK, (365, 235), 3)

        pygame.display.flip()
        clock.tick(60)


def animation_12():  # Рыба в аквариуме
    fin_angle = 0
    mouth_angle = 0
    x = 300

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(LIGHT_BLUE)

        # Аквариум
        pygame.draw.rect(screen, BLUE, (50, 50, 700, 400), 3)

        # Движение рыбы
        x += 2
        if x > 700:
            x = 50

        # Движение 1: плавники
        fin_angle = math.sin(pygame.time.get_ticks() / 100) * 20
        fin_points = [(int(x) + 20, 200), (int(x) + 40, 180 + fin_angle), (int(x) + 50, 200)]
        pygame.draw.polygon(screen, ORANGE, fin_points)

        # Тело
        pygame.draw.ellipse(screen, ORANGE, (int(x), 180, 60, 40))

        # Движение 2: рот открывается
        mouth_angle = math.sin(pygame.time.get_ticks() / 150) * 5
        pygame.draw.ellipse(screen, RED, (int(x) + 5, 190, 10, 5 + mouth_angle))

        # Глаз
        pygame.draw.circle(screen, BLACK, (int(x) + 35, 190), 4)

        pygame.display.flip()
        clock.tick(60)


# Словарь с анимациями
animations = {
    1: {"func": animation_1, "name": "Человек пьёт чай"},
    2: {"func": animation_2, "name": "Надевание рюкзака"},
    3: {"func": animation_3, "name": "Зевание"},
    4: {"func": animation_4, "name": "Удар по мячу ногой"},
    5: {"func": animation_5, "name": "Бросок баскетбольного мяча"},
    6: {"func": animation_6, "name": "Бег на месте"},
    7: {"func": animation_7, "name": "Плавание кролем"},
    8: {"func": animation_8, "name": "Подтягивание на турнике"},
    9: {"func": animation_9, "name": "Кошка умывается"},
    10: {"func": animation_10, "name": "Собака виляет хвостом"},
    11: {"func": animation_11, "name": "Птица чистит перья"},
    12: {"func": animation_12, "name": "Рыба в аквариуме"},
    # Можно добавить остальные анимации по аналогии
}


def main():
    while True:
        choice = wait_for_choice()
        if choice is None:
            break
        if choice in animations:
            animations[choice]["func"]()
        else:
            # Если анимация не реализована
            screen.fill(WHITE)
            text = font_medium.render(f"Анимация {choice} в разработке", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(1500)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
