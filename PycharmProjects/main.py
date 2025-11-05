import pygame
import random
import time
import math


FPS = 60
LINES = ((233, -130), (360, -120), (485, -100), (617, -115))
WIDTH, HEIGHT = 840, 650

pygame.init()

IMG_JUMP = [pygame.image.load(f"image/image/{i}.png") for i in range(6,12)]
IMG_CAR = [pygame.image.load(f"image/car/Slice {i}.png") for i in range(1,9)]
BG = pygame.image.load("image/1556547969.png")
player_img = pygame.image.load("image/player/Slice 9.png")
BG2 = BG.copy()
BG_y = 0
spawn_rate = 0.25
score = 0
difficulty = 15
speed_car = 5
timer =0
bg_speed = 2
max_score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки")
pygame.display.set_icon(pygame.image.load("image/gameicon.png"))
font = pygame.font.SysFont(None, 60)
label = font.render("Game Over!", True, "white")


class Car(pygame.sprite.Sprite):
    def __init__(self, dect: tuple[int, int] = (0,0)):
        super().__init__()
        self.image = random.choice(IMG_CAR)
        self.rect = self.image.get_rect(center = dect)

    def update(self, surface):
        self.rect.y += speed_car
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Player(Car):
    def __init__(self):
        super().__init__()
        self.dist = 7
        self.image = player_img
        self.rect = player_img.get_rect(center = (WIDTH // 2, HEIGHT - 100))
        self.is_jumping = False
        self.jump_speed = 15
        self.jump_distance = 0
        self.max_jump_distance = 200
        self.last_jump_time = 0
        self.jump_cooldown = 5
        self.scale_orig = 1.0
        self.max_scale = 1.3


    def can_jump(self):
        return time.time() - self.last_jump_time >= self.jump_cooldown

    def jump(self):
        if not self.is_jumping and self.can_jump():
            self.is_jumping = True
            self.jump_distance = 0
            self.last_jump_time = time.time()

    def update_scale(self):
        if self.is_jumping:
            # Используем sin для плавного увеличения/уменьшения
            scale = 1 + (self.max_scale - 1) * abs(math.sin((self.jump_distance / self.max_jump_distance) * math.pi))
            self.scale_orig = scale

            # Масштабирую изображение
            orig_rect = player_img.get_rect()
            scaled_size = (int(orig_rect.width * scale), int(orig_rect.height * scale))
            self.image = pygame.transform.scale(player_img, scaled_size)
            # Сохраняю центр машинки
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        #Возвращаю image и rect в изначальное состояние для предотвращения багов
        elif self.scale_orig != 1.0:
            self.scale_orig = 1.0
            self.image = player_img
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, surface):
        key = pygame.key.get_pressed()
        # Обработка прыжка
        if self.is_jumping:
            self.rect.y -= self.jump_speed
            self.jump_distance += self.jump_speed

            if self.jump_distance >= self.max_jump_distance:
                self.is_jumping = False

        # Обновление масштаба
        self.update_scale()

        # Обычное управление
        if not self.is_jumping:
            if key[pygame.K_w]:
                self.rect.y -= self.dist
            elif key[pygame.K_s]:
                self.rect.y += self.dist
            if key[pygame.K_a] and self.rect.left > 145:
                self.rect.x -= self.dist
            elif key[pygame.K_d] and self.rect.right < WIDTH - 145:
                self.rect.x += self.dist

        # Активация прыжка
        if key[pygame.K_SPACE]:
            self.jump()

        # Отображение информации
        cooldown_left = int(max(0, 1 +self.jump_cooldown - (time.time() - self.last_jump_time)))
        screen.blit(IMG_JUMP[cooldown_left], (WIDTH - 30 - IMG_JUMP[cooldown_left].get_size()[0], 30))

        # Ограничение движения
        self.rect.y = max(10, min(self.rect.y, HEIGHT - 10 - self.image.get_size()[1]))
        surface.blit(self.image, (self.rect.x, self.rect.y))

try:
    with open("score.txt") as file:
        for i in file:
            max_score = int(i)
except:
    max_score = 0

def write_to_file(score):
    if max_score < score:
        with open("score.txt", 'w') as file:
            file.write(str(score))
def create_blurred_surface(surface, alpha=128):
    sur = pygame.Surface((WIDTH, HEIGHT))
    sur.blit(surface, (0, 0))
    darken = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darken.fill((0, 0, 0, alpha))
    sur.blit(darken, (0, 0))
    return sur


player = Player()
my_random = [0, 1, 2, 3]
run = True
game = False
main = True
clock = pygame.time.Clock()
enemy_sprites = pygame.sprite.Group()
title = font.render("ГОНКИ", True, (255, 255, 255))
label3 = font.render("Нажмите R чтобы играть!",True, (255, 255, 255))

while run:
    # Движение дороги и проверка на X
    screen.blit(BG, (0, BG_y))
    screen.blit(BG2, (0, BG_y - HEIGHT))
    BG_y += bg_speed
    if BG_y >= 650:
        BG_y = 0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            write_to_file(score)
        if e.type == pygame.KEYDOWN and main == True:
            if e.key == pygame.K_r:
                game = True
                main = False

    # Начальное меню
    if main:
        blurred_bg = create_blurred_surface(screen)
        screen.blit(blurred_bg, (0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        label4 = font.render(f"Лучший результат: {max_score}", True, (255,255,255))
        screen.blit(label3, (WIDTH // 2 - label3.get_width() // 2, HEIGHT // 4 + 100))
        screen.blit(label4, (WIDTH // 2 - label4.get_width() // 2, HEIGHT // 4 + 200))
    elif game:
        timer+=1
        # Усложнение игры
        if score > 1 and score % 5 == 0 and difficulty >=-15:
            difficulty-=10
            speed_car += 1
            bg_speed +=1
            if score % 40 ==0 and spawn_rate <0.70:
                spawn_rate+=0.15

        # Появление врагов
        if timer >= FPS + difficulty:
            timer = 0
            line1 = random.choice(LINES)
            car = Car(line1)
            enemy_sprites.add(car)
            if random.random() <= spawn_rate:
                lines_copy = [i for i in LINES if i != line1]
                car = Car(random.choice(lines_copy))
                enemy_sprites.add(car)


        enemy_sprites.update(screen)
        player.update(screen)

        # Проверка столкновений
        if not player.is_jumping and pygame.sprite.spritecollide(player, enemy_sprites, False):
            game = False

        for e in enemy_sprites:
            if e.rect.y > HEIGHT:
                e.kill()
                score += 1

    else:
        write_to_file(score)
        blurred_bg = create_blurred_surface(screen)
        screen.blit(blurred_bg, (0, 0))
        label_score = font.render(f"Кол-во очков: {score}", True, "white")
        rlabel_rect = label3.get_rect(topleft=(WIDTH / 2 - label.get_size()[0] / 2, HEIGHT / 2 + 50))
        screen.blit(label, (WIDTH / 2 - label.get_size()[0] / 2, HEIGHT / 2 - 50))
        screen.blit(label_score, (WIDTH / 2 - label_score.get_size()[0] / 2, HEIGHT / 2 + 25))
        screen.blit(label3, (WIDTH / 2 - label3.get_size()[0] / 2, HEIGHT / 2 + 100))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game = True
            player = Player()
            enemy_sprites.empty()
            timer = score = 0
            bg_speed = 2
            speed_car = 5
            difficulty = 15
            spawn_rate = 0.25

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()