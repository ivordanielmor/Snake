# 1. Falütközés detektálása - Állítsd le a játékot és jelenítsd meg "Game Over!", ha a kígyó feje kimegy a pályáról.

import pygame
import random

pygame.init()

szelesseg = 1920
magassag = 1080

game_over = False

kepernyo = pygame.display.set_mode((szelesseg, magassag))
ora = pygame.time.Clock()

kigyo_meret = 20

kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret

racs_szelesseg = szelesseg // kigyo_meret
racs_magassag = magassag // kigyo_meret

piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret

sebesseg_x = 20
sebesseg_y = 0

zold = (0, 255, 0)
piros = (200, 40, 40)
sarga = (255, 255, 0)

sarga_etel_x = -kigyo_meret
sarga_etel_y = -kigyo_meret
sarga_aktiv = False

kigyo_test = []
hossz = 1

pontszam = 0

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

    if not game_over:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y

        if kigyo_x < 0 or kigyo_x >= szelesseg or kigyo_y < 0 or kigyo_y >= magassag:
            game_over = True

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

    if kigyo_x == piros_etelx and kigyo_y == piros_etely:
        hossz += 1
        pontszam += 1
        piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
        piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret

    if sarga_aktiv:
        if kigyo_x == sarga_etel_x and kigyo_y == sarga_etel_y:
            hossz += 3
            pontszam += 3
            sarga_aktiv = False
    else:
        if random.random() < 0.01:
            sarga_etel_x = random.randint(0, racs_szelesseg - 1) * kigyo_meret
            sarga_etel_y = random.randint(0, racs_magassag - 1) * kigyo_meret
            sarga_aktiv = True

    kepernyo.fill((0, 0, 0))

    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, zold, (x, y, kigyo_meret, kigyo_meret))

    pygame.draw.rect(kepernyo, piros, (piros_etelx, piros_etely, kigyo_meret, kigyo_meret))

    if sarga_aktiv:
        pygame.draw.rect(kepernyo, sarga, (sarga_etel_x, sarga_etel_y, kigyo_meret, kigyo_meret))

    pontszoveg = betutipus.render(f"Pont: {pontszam}", True, (255, 255, 255))
    kepernyo.blit(pontszoveg, (10, 10))

    if game_over:
        game_over_szoveg = betutipus.render("Game Over!", True, (255, 0, 0))
        kepernyo.blit(game_over_szoveg, (szelesseg // 2 - 100, magassag // 2))

    pygame.display.flip()
    ora.tick(10)

pygame.quit()
