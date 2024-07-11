from random import randint, uniform, choice

import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

display_surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True
clock = pygame.time.Clock()


class Player:
    def __init__(self, image_size, speed):
        self.walk_frames = []
        for _ in range(4):
            frame = pygame.image.load(f'images/Player/Player_Run_{_ + 1}.png').convert_alpha()
            self.walk_frames.append(frame)
            self.walk_frames[_] = pygame.transform.scale(self.walk_frames[_], image_size)

        # Завантаження зображень
        self.idle = pygame.image.load('images/Player/Player_1.png').convert_alpha()
        self.idle = pygame.transform.scale(self.idle, image_size)
        self.surf = self.idle
        self.rect = self.surf.get_frect()
        self.is_flipped = False
        self.frame_index = 0
        self.flipped_surf = self.surf

        # Змінні гравця
        self.direction = pygame.Vector2(0, 0)
        self.speed = speed

        self.footstep_sound = pygame.mixer.Sound("sounds/Steps.ogg")
        self.footstep_time = 0

        self.can_shoot = True
        self.last_shot = 0

    def move(self, kb):
        self.direction.x = int(kb[pygame.K_RIGHT]) - int(kb[pygame.K_LEFT])
        self.direction.y = int(kb[pygame.K_DOWN]) - int(kb[pygame.K_UP])

        # Обмеження руху Гравця
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Рух Гравця
        if self.direction:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed * dt
        self.flipped_surf = pygame.transform.flip(player.surf, player.is_flipped, False)

    def flip(self):
        # Flip Гравця
        if self.direction.x == 1:
            self.is_flipped = False
        if self.direction.x == -1:
            self.is_flipped = True

    def animate(self):
        if self.direction:
            self.frame_index += 10 * dt
            self.surf = self.walk_frames[int(self.frame_index) % 4]

        else:
            self.frame_index = 0
            self.surf = self.idle

    def play_footstep(self):
        if self.direction and pygame.time.get_ticks() >= self.footstep_time + 200:
            self.footstep_sound.play()
            self.footstep_time = pygame.time.get_ticks()

    def shoot(self):
        if self.can_shoot and pygame.time.get_ticks() >= self.last_shot + 300:
            self.last_shot = pygame.time.get_ticks()
            shot_sound.stop()
            shot_sound.play()
            return True
        return False

    def update(self, kb):
        self.move(kb)
        self.animate()
        self.flip()
        self.play_footstep()


class Fireball:
    def __init__(self, size):
        self.surf = pygame.image.load('images/Fireball/Fireball_1.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, size)
        self.rotated = self.surf
        self.rect = self.surf.get_frect()
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(150, 400)
        self.rect.left = randint(0, SCREEN_WIDTH)
        self.rect.top = -100
        self.rotation = 0
        self.rotation_direction = choice([-1, 1])
        self.sound = choice(fireball_sounds)
        self.sound.set_volume(0.2)
        self.sound.play()

    def update(self):
        self.rect.center += self.direction * self.speed * dt
        self.surf = pygame.transform.rotozoom(self.rotated, self.rotation, 1)
        self.rotation += 400 * dt * self.rotation_direction
        self.rect = self.surf.get_frect(center=self.rect.center)
        if self.rect.top > SCREEN_HEIGHT:
            self.destroy()

    def destroy(self):
        index = fireballs.index(self)
        fireballs.pop(index)
        del self


class Waterball:
    def __init__(self, position):
        self.surf = pygame.image.load('images/WaterBall.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, [40, 40])
        self.rotated = self.surf
        self.rect = self.surf.get_frect(center=position)
        self.speed = 800
        self.direction = self.rotate_towards()

    def update(self):
        self.rect.center += self.direction * self.speed * dt

    def rotate_towards(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        wb_pos = pygame.Vector2(self.rect.center)
        dir_x = mouse_pos.x - wb_pos.x
        dir_y = mouse_pos.y - wb_pos.y
        return pygame.Vector2(dir_x, dir_y).normalize()

    def destroy(self):
        index = waterballs.index(self)
        waterballs.pop(index)
        del self


player = Player([80, 80], 500)

fireballs = []

fireball_event = pygame.event.custom_type()
pygame.time.set_timer(fireball_event, 500)

score_font = pygame.font.Font(None, 40)

main_music = pygame.mixer.Sound("sounds/Music.mp3")
main_music.play(loops=-1)

shot_sound = pygame.mixer.Sound("sounds/Shot.mp3")
shot_sound.set_volume(0.3)

# fireball_sounds = [pygame.mixer.Sound(f"sounds/Fireball/Fireball_{i + 1}.mp3") for i in range(6)]
fireball_sounds = []
for i in range(6):
    fireball_sounds.append(pygame.mixer.Sound(f"sounds/Fireball/Fireball_{i + 1}.mp3"))

waterballs = []


def display_score():
    ctime = pygame.time.get_ticks() // 100
    score_surf = score_font.render(str(ctime), True, (240, 240, 240))
    score_rect = score_surf.get_frect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    display_surface.blit(score_surf, score_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), score_rect.inflate(20, 12), 5, 10)


while running:
    dt = clock.tick() / 1000

    # Цикл Подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == fireball_event:
            randsize = randint(30, 80)
            fireballs.append(Fireball([randsize, randsize]))
        if event.type == pygame.MOUSEBUTTONDOWN and player.shoot():
            waterballs.append(Waterball(player.rect.center))

    # Оброблюємо власні алгоритми
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Логіка Fireball
    for fireball in fireballs:
        fireball.update()

    # Малюємо Гру
    display_surface.fill('black')
    display_score()
    display_surface.blit(player.flipped_surf, player.rect)

    for waterball in waterballs:
        display_surface.blit(waterball.surf, waterball.rect)
        waterball.update()

    for fireball in fireballs:
        display_surface.blit(fireball.surf, fireball.rect)
        if player.rect.colliderect(fireball.rect):
            running = False
        for waterball in waterballs:
            if waterball.rect.colliderect(fireball.rect):
                waterball.destroy()
                fireball.destroy()

    pygame.display.update()

print("Score:", pygame.time.get_ticks() // 100)
pygame.quit()
