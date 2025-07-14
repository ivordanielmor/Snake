# HF. Egészítsd ki a mentett adatokat: tegyél bele egy "lives" kulcsot is (például "lives": 3), amit visszatöltéskor használ a program!

import pygame
import random
import os
import json

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

# Alapértékek
lives = 3
pontszam = 0
highscore = 0
hossz = 1
sarga_etel_x = -kigyo_meret
sarga_etel_y = -kigyo_meret
sarga_aktiv = False

if os.path.exists("savegame.json"):
    with open("savegame.json", "r") as json_file:
        adatok = json.load(json_file)

        snake_positions_raw = adatok.get("snake_positions", [])
        if isinstance(snake_positions_raw, list) and all(isinstance(pos, (list, tuple)) and len(pos) == 2 for pos in snake_positions_raw):
            kigyo_test = [tuple(pos) for pos in snake_positions_raw]
        else:
            kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
            kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
            kigyo_test = [(kigyo_x, kigyo_y)]

        irany = adatok.get("direction", "right")
        if irany not in ("left", "right", "up", "down"):
            irany = "right"

        pontszam = adatok.get("score", 0)
        if not isinstance(pontszam, int):
            pontszam = 0

        highscore = adatok.get("highscore", 0)
        if not isinstance(highscore, int):
            highscore = 0

        lives = adatok.get("lives", 3)
        if not isinstance(lives, int):
            lives = 3

        red_food = adatok.get("red_food", [100, 100])
        if (not isinstance(red_food, list) or len(red_food) != 2 or
            not all(isinstance(c, int) for c in red_food)):
            red_food = [100, 100]
        piros_etelx, piros_etely = red_food

        yellow_food = adatok.get("yellow_food", [-kigyo_meret, -kigyo_meret])
        if (not isinstance(yellow_food, list) or len(yellow_food) != 2 or
            not all(isinstance(c, int) for c in yellow_food)):
            yellow_food = [-kigyo_meret, -kigyo_meret]
        sarga_etel_x, sarga_etel_y = yellow_food

        sarga_aktiv = adatok.get("yellow_active", False)
        if not isinstance(sarga_aktiv, bool):
            sarga_aktiv = False

        hossz = adatok.get("length", 1)
        if not isinstance(hossz, int) or hossz < 1:
            hossz = 1

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
            sebesseg_x = kigyo_meret
            sebesseg_y = 0

        if kigyo_test:
            kigyo_x, kigyo_y = kigyo_test[-1]
        else:
            kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
            kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
            kigyo_test = [(kigyo_x, kigyo_y)]
else:
    kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
    kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
    piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
    piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret
    sebesseg_x = kigyo_meret
    sebesseg_y = 0
    kigyo_test = [(kigyo_x, kigyo_y)]

fut = True
game_over = False

while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and sebesseg_x == 0:
                sebesseg_x = -kigyo_meret
                sebesseg_y = 0
            elif event.key == pygame.K_RIGHT and sebesseg_x == 0:
                sebesseg_x = kigyo_meret
                sebesseg_y = 0
            elif event.key == pygame.K_UP and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = -kigyo_meret
            elif event.key == pygame.K_DOWN and sebesseg_y == 0:
                sebesseg_x = 0
                sebesseg_y = kigyo_meret
            elif event.key == pygame.K_r and game_over:
                kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
                kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
                sebesseg_x = kigyo_meret
                sebesseg_y = 0
                hossz = 1
                kigyo_test = [(kigyo_x, kigyo_y)]
                pontszam = 0
                lives = 3
                game_over = False

    if not game_over:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y

        # Falnak ütközés
        if kigyo_x < 0 or kigyo_x >= szelesseg or kigyo_y < 0 or kigyo_y >= magassag:
            lives -= 1
            if lives > 0:
                kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
                kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
                kigyo_test = [(kigyo_x, kigyo_y)]
            else:
                game_over = True
            continue  # ⬅️ Itt kilépünk a ciklusból, hogy ne történjen újabb életrontás!

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

        # Saját magának ütközés
        if (kigyo_x, kigyo_y) in kigyo_test[:-1]:
            lives -= 1
            if lives > 0:
                kigyo_x = (szelesseg // 2) // kigyo_meret * kigyo_meret
                kigyo_y = (magassag // 2) // kigyo_meret * kigyo_meret
                kigyo_test = [(kigyo_x, kigyo_y)]
            else:
                game_over = True
            continue  # ⬅️ Ugyanaz itt is: ha életrontás volt, kilépünk a ciklusból

        if kigyo_x == piros_etelx and kigyo_y == piros_etely:
            hossz += 1
            pontszam += 1
            if pontszam > highscore:
                highscore = pontszam
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

    lives_szoveg = betutipus.render(f"Lives: {lives}", True, (255, 255, 255))
    kepernyo.blit(lives_szoveg, (10, 90))

    if game_over:
        game_over_szoveg = betutipus.render("Game Over!", True, (255, 0, 0))
        kepernyo.blit(game_over_szoveg, (szelesseg // 2 - 100, magassag // 2))
        pygame.display.flip()
        pygame.time.delay(1500)

    pygame.display.flip()
    ora.tick(10)

    if not game_over:
        adatok = {
            "snake_positions": [list(pos) for pos in kigyo_test],
            "direction": "left" if sebesseg_x == -kigyo_meret else
                         "right" if sebesseg_x == kigyo_meret else
                         "up" if sebesseg_y == -kigyo_meret else
                         "down" if sebesseg_y == kigyo_meret else
                         "right",
            "score": pontszam,
            "highscore": highscore,
            "red_food": [piros_etelx, piros_etely],
            "yellow_food": [sarga_etel_x, sarga_etel_y],
            "yellow_active": sarga_aktiv,
            "length": hossz,
            "lives": lives,
        }
        with open("savegame.json", "w") as json_file:
            json.dump(adatok, json_file, indent=4)

pygame.quit()
