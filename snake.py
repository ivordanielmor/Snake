# 2. Állapot betöltése - Olvasd vissza a fájlt, és generáld le újra a kígyót testét.

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

betutipus = pygame.font.SysFont(None, 40)

sarga_etel_x = -kigyo_meret
sarga_etel_y = -kigyo_meret
sarga_aktiv = False

kigyo_test = []
hossz = 1

pontszam = 0

betutipus = pygame.font.SysFont(None, 40)
# # Highscore beolvasása
try:
    with open("highscore.txt", "r") as file:
        sor = file.read().strip()
        if ":" in sor:
            highscore = int(sor.split(":")[1].strip())
        else:
            highscore = int(sor)
except (FileNotFoundError, ValueError):
    highscore = 0

# Kígyó pozíciók betöltése
kigyo_test = []
try:
    with open("kigyopozi.txt", "r") as f:
        adat = f.read().strip()
        if adat != "":
            poziciok = adat.split(":")
            for poz in poziciok:
                x_str, y_str = poz.split(",")
                kigyo_test.append((int(x_str), int(y_str)))
            kigyo_x, kigyo_y = kigyo_test[-1]
            hossz = len(kigyo_test)
        else:
            kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
            kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
            hossz = 1
except FileNotFoundError:
    kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
    kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
    hossz = 1
    kigyo_test = []

if not kigyo_test:
    kigyo_test = [(kigyo_x, kigyo_y)]

fut = True
game_over = False

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
            if event.key == pygame.K_r:
                 if game_over:

                    kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
                    kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
                    sebesseg_x = 20
                    sebesseg_y = 0
                    kigyo_test = []
                    hossz = 1
                    pontszam = 0
                    game_over = False

    if not game_over:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y

        if kigyo_x < 0 or kigyo_x >= szelesseg or kigyo_y < 0 or kigyo_y >= magassag:
            game_over = True

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

         # kígyó pozícióinak fájlba írása:
        with open("kigyopozi.txt", "w") as f:
            pozisor = ";".join([f"{x},{y}" for x, y in kigyo_test])
            f.write(pozisor)
        
        if (kigyo_x, kigyo_y) in kigyo_test[:-1]:
            game_over = True

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

    highscore_szoveg = betutipus.render(f"Highscore: {highscore}", True, (255, 255, 255))
    kepernyo.blit(highscore_szoveg, (10, 50))

    if game_over:
        if pontszam > highscore:
            highscore = pontszam
            with open("highscore.txt", "w") as file:
                file.write(f"Highscore: {highscore}")
        with open("kigyopozi.txt", "w") as f:
            pozisor = ":".join([f"{x},{y}" for x, y in kigyo_test])
            f.write(pozisor)
        game_over_szoveg = betutipus.render("Game Over!", True, (255, 0, 0))
        
        kepernyo.blit(game_over_szoveg, (szelesseg // 2 - 100, magassag // 2))
        pygame.display.flip()
        pygame.time.delay(1500)

    pygame.display.flip()
    ora.tick(10)

pygame.quit()
