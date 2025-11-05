import pygame
import random
import time
import math
import os

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 840, 650
FPS = 60
BG_SCROLL_SPEED = 2
BASE_CAR_SPEED = 5
PLAYER_SPEED = 7
JUMP_SPEED = 15
MAX_JUMP_DISTANCE = 200
JUMP_COOLDOWN = 5  # секунд
LANE_POSITIONS = [(227, -100), (351, -100), (485, -100), (617, -100)]
DIFFICULTY_INTERVAL = 20  # Очков между повышениями сложности

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки")
clock = pygame.time.Clock()


class DifficultySystem:
    def __init__(self):
        self.level = 1
        self.car_speed = BASE_CAR_SPEED
        self.spawn_rate = FPS  # Кадров между спавнами
        self.double_spawn_chance = 0.25  # Шанс спавна второй машины

    def update(self, score):
        """Обновляет уровень сложности на основе счета"""
        new_level = 1 + score // DIFFICULTY_INTERVAL
        if new_level > self.level:
            self.level = new_level
            self.car_speed = BASE_CAR_SPEED + min(10, self.level * 0.5)  # Макс +10 к скорости
            self.spawn_rate = max(30, FPS - self.level * 5)  # Минимум 0.5 секунды между спавнами
            self.double_spawn_chance = min(0.5, 0.25 + self.level * 0.01)  # Макс 50% шанс

    def get_difficulty_color(self):
        """Возвращает цвет индикатора сложности"""
        if self.level < 5:
            return GREEN
        elif self.level < 10:
            return YELLOW
        else:
            return RED


# Загрузка изображений
def load_image(path, scale=None):
    try:
        img = pygame.image.load(path)
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        # Создаем заглушку
        surf = pygame.Surface((50, 100))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf


# Загрузка ресурсов
try:
    bg = load_image("image/1556547969.png", (WIDTH, HEIGHT))
    bg2 = bg.copy()
    img = load_image("image/image/7.png")
    img_car = [load_image(f"image/car/Slice {i}.png") for i in range(1, 9)]
    player_img = load_image("image/player/Slice 9.png")
except Exception as e:
    print(f"Ошибка загрузки ресурсов: {e}")
    # Выход или обработка ошибки

# Шрифты
try:
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
except:
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 40)


class Car(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], speed: float):
        super().__init__()
        self.original_image = random.choice(img_car)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.is_kill = False

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Player(Car):
    def __init__(self):
        super().__init__((WIDTH // 2, HEIGHT - 100), 0)
        self.original_image = player_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.speed = PLAYER_SPEED
        self.is_jumping = False
        self.jump_distance = 0
        self.last_jump_time = 0
        self.invincible = False
        self.scale_factor = 1.0
        self.max_scale = 1.3
        self.min_scale = 0.9

    def can_jump(self):
        return time.time() - self.last_jump_time >= JUMP_COOLDOWN

    def jump(self):
        if not self.is_jumping and self.can_jump():
            self.is_jumping = True
            self.invincible = True
            self.jump_distance = 0
            self.last_jump_time = time.time()

    def update_scale(self):
        if self.is_jumping:
            progress = self.jump_distance / MAX_JUMP_DISTANCE
            scale = self.min_scale + (self.max_scale - self.min_scale) * abs(math.sin(progress * math.pi))
            self.scale_factor = scale

            scaled_size = (int(self.original_image.get_width() * scale),
                           int(self.original_image.get_height() * scale))
            self.image = pygame.transform.scale(self.original_image, scaled_size)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.scale_factor != 1.0:
            self.scale_factor = 1.0
            self.image = self.original_image
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        keys = pygame.key.get_pressed()

        # Обработка прыжка
        if self.is_jumping:
            self.rect.y -= JUMP_SPEED
            self.jump_distance += JUMP_SPEED

            if self.jump_distance >= MAX_JUMP_DISTANCE:
                self.is_jumping = False
                self.invincible = False

        self.update_scale()

        # Обычное управление
        if not self.is_jumping:
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
            if keys[pygame.K_a] and self.rect.left > 145:
                self.rect.x -= self.speed
            if keys[pygame.K_d] and self.rect.right < WIDTH - 145:
                self.rect.x += self.speed

        # Ограничение движения
        self.rect.y = max(10, min(self.rect.y, HEIGHT - self.rect.height - 10))


def load_high_score():
    try:
        with open("score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    try:
        with open("score.txt", "w") as file:
            file.write(str(score))
    except IOError as e:
        print(f"Ошибка сохранения счета: {e}")


def draw_difficulty_indicator(surface, difficulty):
    """Рисует индикатор сложности"""
    level_text = small_font.render(f"Уровень: {difficulty.level}", True, WHITE)
    surface.blit(level_text, (10, 50))

    # Индикатор в виде цветной полосы
    indicator_width = 100
    filled_width = min(indicator_width, difficulty.level * 5)
    color = difficulty.get_difficulty_color()

    pygame.draw.rect(surface, (50, 50, 50), (10, 90, indicator_width, 20))
    pygame.draw.rect(surface, color, (10, 90, filled_width, 20))
    pygame.draw.rect(surface, WHITE, (10, 90, indicator_width, 20), 2)


def main():
    bg_y = 0
    score = 0
    max_score = load_high_score()
    game_active = True

    player = Player()
    enemy_sprites = pygame.sprite.Group()
    spawn_timer = 0
    difficulty = DifficultySystem()

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping and player.can_jump():
                    player.jump()
                if not game_active and event.key == pygame.K_r:
                    # Рестарт игры
                    game_active = True
                    player = Player()
                    enemy_sprites.empty()
                    score = 0
                    difficulty = DifficultySystem()

        # Отрисовка фона
        screen.blit(bg, (0, bg_y))
        screen.blit(bg2, (0, bg_y - HEIGHT))
        bg_y = (bg_y + BG_SCROLL_SPEED) % HEIGHT

        if game_active:
            # Обновление сложности
            difficulty.update(score)

            # Спавн врагов
            spawn_timer += 1
            if spawn_timer >= difficulty.spawn_rate:
                spawn_timer = 0
                lane = random.choice(LANE_POSITIONS)
                enemy = Car(lane, difficulty.car_speed)
                enemy_sprites.add(enemy)

                # Шанс спавна второго врага
                if random.random() < difficulty.double_spawn_chance:
                    other_lanes = [pos for pos in LANE_POSITIONS if pos != lane]
                    if other_lanes:
                        enemy = Car(random.choice(other_lanes), difficulty.car_speed)
                        enemy_sprites.add(enemy)

            # Обновление спрайтов
            enemy_sprites.update()
            player.update()

            # Отрисовка
            enemy_sprites.draw(screen)
            screen.blit(player.image, player.rect)

            # Отображение информации
            score_text = font.render(f"Очки: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
            screen.blit(img, (WIDTH - 30 - img.get_width(), 30))

            # КД прыжка
            cooldown = max(0, JUMP_COOLDOWN - (time.time() - player.last_jump_time))
            cooldown_text = small_font.render(f"Прыжок: {int(cooldown)}s", True, WHITE)
            screen.blit(cooldown_text, (10, 10))

            # Индикатор сложности
            draw_difficulty_indicator(screen, difficulty)

            # Коллизия
            if not player.invincible and pygame.sprite.spritecollide(player, enemy_sprites, False):
                game_active = False
                max_score = max(score, max_score)
                save_high_score(max_score)

            # Увеличение счета
            for enemy in enemy_sprites:
                if enemy.rect.top > HEIGHT:
                    enemy.kill()
                    score += 1
        else:
            # Экран окончания игры
            screen.fill(BLACK)
            label = font.render("Game Over!", True, WHITE)
            label_score = font.render(f"Очки: {score}", True, WHITE)
            high_score_text = font.render(f"Рекорд: {max_score}", True, WHITE)
            level_text = font.render(f"Достигнутый уровень: {difficulty.level}", True, WHITE)
            hint = font.render("Нажмите R для рестарта", True, WHITE)

            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 4 - 50))
            screen.blit(label_score, (WIDTH // 2 - label_score.get_width() // 2, HEIGHT // 4 + 20))
            screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 4 + 90))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 4 + 160))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 4 + 230))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()