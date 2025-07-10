# 3. Pontszám kiírása - A pontszám minden körben a bal felső sarokban.

import pygame
import random

pygame.init()

szelesseg = 1920
magassag = 1080

kepernyo = pygame.display.set_mode((szelesseg, magassag))
ora = pygame.time.Clock()

kigyo_meret = 20

kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret

racs_szelesseg = szelesseg // kigyo_meret
racs_magassag = magassag // kigyo_meret

etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
etely = random.randint(0, racs_magassag - 1) * kigyo_meret

sebesseg_x = 20
sebesseg_y = 0

zold = (0, 255, 0)
piros = (200, 40, 40)

kigyo_test = []
hossz = 1

betutipus = pygame.font.SysFont(None, 40)

fut = True

while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and sebesseg_x == 0:
                sebesseg_x = -20
                sebesseg_y = 0
            if event.key == pygame.K_RIGHT and sebesseg_x == 0:
                sebesseg_x = 20
                sebesseg_y = 0
            if event.key == pygame.K_UP and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = -20
            if event.key == pygame.K_DOWN and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = 20

    kigyo_x += sebesseg_x
    kigyo_y += sebesseg_y

    kigyo_test.append((kigyo_x, kigyo_y))

    if len(kigyo_test) > hossz:
        del kigyo_test[0]

    if kigyo_x == etelx and kigyo_y == etely:
        hossz += 1
        etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
        etely = random.randint(0, racs_magassag - 1) * kigyo_meret

    kepernyo.fill((0, 0, 0))

    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, zold, (x, y, kigyo_meret, kigyo_meret))

    pygame.draw.rect(kepernyo, piros, (etelx, etely, kigyo_meret, kigyo_meret))

    pontszoveg = betutipus.render(f"Pont: {hossz - 1}", True, (255, 255, 255))
    kepernyo.blit(pontszoveg, (10, 10))

    pygame.display.flip()
    ora.tick(10)

pygame.quit()
