# 1. Étel generálása a rácsra - 
# Generálj minden körben véletlenszerű (x, y) pozíciót, ha nincs aktív "food", és rajzolj egy piros négyzetet oda.

import pygame
import random

pygame.init()

szelesseg = 1920
magassag = 1080

kepernyo = pygame.display.set_mode((1920, 1080))

ora = pygame.time.Clock()

kigyo_meret = 20
kigyo_x = (1920 - kigyo_meret) // 2
kigyo_y = (1080 - kigyo_meret) // 2

# Mozgásirány változók (sebesség pixelben)
racs_szelesseg = szelesseg // kigyo_meret
racs_magassag = magassag // kigyo_meret

etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
etely = random.randint(0, racs_magassag - 1) * kigyo_meret

sebesseg_x = 20
sebesseg_y = 0

zold = (0, 255, 0)
piros = (200, 40, 40)

fut = True

# Játék fő ciklusa
while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sebesseg_x = -20
                sebesseg_y = 0
            if event.key == pygame.K_RIGHT:
                sebesseg_x = 20
                sebesseg_y = 0
            if event.key == pygame.K_UP:
                sebesseg_x = 0
                sebesseg_y = -20
            if event.key == pygame.K_DOWN:
                sebesseg_x = 0
                sebesseg_y = 20

    kigyo_x += sebesseg_x
    kigyo_y += sebesseg_y

    # Képernyő törlés
    kepernyo.fill((0, 0, 0))

    pygame.draw.rect(kepernyo, zold, (kigyo_x, kigyo_y, kigyo_meret, kigyo_meret))
    pygame.draw.rect(kepernyo, piros, (etelx, etely, 20, 20))
    pygame.display.flip()
    ora.tick(10)

pygame.quit() 
