# Pancake Collector Game (Final Version)

from pygame import *
from random import randint
from time import time as timer

# ------------------ INIT ------------------
init()
mixer.init()
font.init()

# ------------------ SETTINGS ------------------
win_width = 700
win_height = 500

goal = 20
max_miss = 10

score = 0
miss = 0
run = True
finish = False
hit_time = 0

# ------------------ FILES ------------------
img_back = "wallp.jpg"

img_hero_closed = "akito closed.png"
img_hero_open = "akito open.png"

img_pancake = "pancak.png"

eat_sound = mixer.Sound("nom nom.mp3")
eat_sound.set_volume(0.8)
mixer.music.load("tacos.mp3")
mixer.music.set_volume(0.4)   # atur volume (0.0 – 1.0)
mixer.music.play(-1)          # -1 = loop selamanya


# ------------------ WINDOW ------------------
display.set_caption("Pancake Collector")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# ------------------ FONTS ------------------
font_big = font.Font(None, 80)
font_small = font.SysFont("Arial", 36)

win_text = font_big.render("AKITO'S ALREADY FULL!", True, (246, 63, 0))
lose_text = font_big.render("AKITO IS STILL HUNGRY!", True, (246, 63, 0))

# ------------------ CLASSES ------------------
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, sx, sy, speed):
        super().__init__()
        self.image = transform.scale(
            image.load(img).convert_alpha(),
            (sx, sy)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, x, y):
        super().__init__(img_hero_closed, x, y, 100, 125, 10)
        self.image_closed = transform.scale(
            image.load(img_hero_closed).convert_alpha(),
            (100, 125)
        )
        self.image_open = transform.scale(
            image.load(img_hero_open).convert_alpha(),
            (100, 125)
        )
        self.image = self.image_closed

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 105:
            self.rect.x += self.speed

    def eat(self):
        self.image = self.image_open

    def close_mouth(self):
        self.image = self.image_closed


class Pancake(GameSprite):
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y > win_height:
            miss += 1
            self.reset_pos()

    def reset_pos(self):
        self.rect.y = randint(-300, -50)
        self.rect.x = randint(80, win_width - 80)

# ------------------ OBJECTS ------------------
ship = Player(5, win_height - 150)

pancakes = sprite.Group()
for i in range(5):
    pancake = Pancake(
        img_pancake,
        randint(80, win_width - 80),
        randint(-300, -50),
        90, 65,
        randint(5, 7)
    )
    pancakes.add(pancake)

# ------------------ GAME LOOP ------------------
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        pancakes.update()

        ship.draw()
        pancakes.draw(window)

        # -------- COLLISION (EAT PANCAKE) --------
        hit_list = sprite.spritecollide(ship, pancakes, False)
        for pancake in hit_list:
            score += 1
            ship.eat()
            eat_sound.play()
            hit_time = timer()
            pancake.reset_pos()

        if timer() - hit_time > 0.3:
            ship.close_mouth()

        # -------- UI --------
        score_text = font_small.render(f"Pancake: {score}", True, (3, 95, 126))
        miss_text = font_small.render(f"Miss: {miss}/{max_miss}", True, (3, 95, 126))
        window.blit(score_text, (10, 10))
        window.blit(miss_text, (10, 45))

        # -------- WIN / LOSE --------
        win_rect = win_text.get_rect(center=(win_width // 2, win_height // 2))
        lose_rect = lose_text.get_rect(center=(win_width // 2, win_height // 2))

        if score >= goal:
            finish = True
            mixer.music.stop()
            window.blit(win_text, win_rect)


        if miss >= max_miss:
            finish = True
            mixer.music.stop()
            window.blit(lose_text, lose_rect)



        display.update()
        time.delay(30)

    else:
        time.delay(3000)
        score = 0
        miss = 0
        finish = False
        mixer.music.play(-1)

        pancakes.empty()
        for i in range(5):
            pancake = Pancake(
                img_pancake,
                randint(80, win_width - 80),
                randint(-300, -50),
                90, 65,
                randint(5, 7)
            )
            pancakes.add(pancake)
