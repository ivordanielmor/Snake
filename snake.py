# HÁZI FELADAT: Mentéskor a kígyó aktuális irányát (pl. "left") is írd ki a fájlba, és betöltéskor ezt is állítsd vissza!

import pygame
import random
import os

pygame.init()

szelesseg = 1920
magassag = 1080
kepernyo = pygame.display.set_mode((szelesseg, magassag))
ora = pygame.time.Clock()

kigyo_meret = 20
racs_szelesseg = szelesseg // kigyo_meret
racs_magassag = magassag // kigyo_meret

zold = (0, 255, 0)
piros = (200, 40, 40)
sarga = (255, 255, 0)
betutipus = pygame.font.SysFont(None, 40)

piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret

sarga_etel_x = -kigyo_meret
sarga_etel_y = -kigyo_meret
sarga_aktiv = False

pontszam = 0

try:
    with open("highscore.txt", "r") as file:
        sor = file.read().strip()
        if ":" in sor:
            highscore = int(sor.split(":")[1].strip())
        else:
            highscore = int(sor)
except (FileNotFoundError, ValueError):
    highscore = 0

# Alapértelmezett pozíciók és irány
kigyo_test = []
sebesseg_x = kigyo_meret
sebesseg_y = 0

if os.path.exists("kigyopozi.txt"):
    try:
        with open("kigyopozi.txt", "r") as f:
            sorok = f.readlines()
            if len(sorok) >= 2:
                poziciok = sorok[0].strip().split(":")
                irany = sorok[1].strip()

                for poz in poziciok:
                    x_str, y_str = poz.split(",")
                    kigyo_test.append((int(x_str), int(y_str)))

                kigyo_x, kigyo_y = kigyo_test[-1]
                hossz = len(kigyo_test)

                if irany == "left":
                    sebesseg_x = -kigyo_meret
                    sebesseg_y = 0
                elif irany == "right":
                    sebesseg_x = kigyo_meret
                    sebesseg_y = 0
                elif irany == "up":
                    sebesseg_x = 0
                    sebesseg_y = -kigyo_meret
                elif irany == "down":
                    sebesseg_x = 0
                    sebesseg_y = kigyo_meret
            else:
                raise ValueError("Hibás kigyopozi.txt formátum!")
    except Exception as e:
        print(f"Hiba a kigyopozi.txt beolvasásakor: {e}")
        kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
        kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
        hossz = 1
        kigyo_test = [(kigyo_x, kigyo_y)]
else:
    kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
    kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
    hossz = 1
    kigyo_test = [(kigyo_x, kigyo_y)]

fut = True
game_over = False

while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Kilépésnél mentés, de csak ha nincs game over!
            if not game_over:
                with open("kigyopozi.txt", "w") as f:
                    pozisor = ":".join([f"{x},{y}" for x, y in kigyo_test])
                    if sebesseg_x == -kigyo_meret:
                        irany = "left"
                    elif sebesseg_x == kigyo_meret:
                        irany = "right"
                    elif sebesseg_y == -kigyo_meret:
                        irany = "up"
                    elif sebesseg_y == kigyo_meret:
                        irany = "down"
                    else:
                        irany = "right"
                    f.write(pozisor + "\n" + irany)
            fut = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and sebesseg_x == 0:
                sebesseg_x = -kigyo_meret
                sebesseg_y = 0
            if event.key == pygame.K_RIGHT and sebesseg_x == 0:
                sebesseg_x = kigyo_meret
                sebesseg_y = 0
            if event.key == pygame.K_UP and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = -kigyo_meret
            if event.key == pygame.K_DOWN and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = kigyo_meret
            if event.key == pygame.K_r:
                if game_over:
                    kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
                    kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
                    sebesseg_x = kigyo_meret
                    sebesseg_y = 0
                    kigyo_test = [(kigyo_x, kigyo_y)]
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

        game_over_szoveg = betutipus.render("Game Over!", True, (255, 0, 0))
        kepernyo.blit(game_over_szoveg, (szelesseg // 2 - 100, magassag // 2))
        pygame.display.flip()
        pygame.time.delay(1500)

    pygame.display.flip()
    ora.tick(10)

pygame.quit()
