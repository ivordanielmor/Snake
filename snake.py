# 3. Győztes kiválasztása
# A legtöbb győzelem alapján kiválasztja a győztest
import pygame
import random
import os
import json

pygame.init()

# Képernyő beállítása: resizeable, hogy a rendszer ablakozó vezérlői megmaradjanak
szelesseg = 1280
magassag = 720
kigyo_meret = 20
kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
pygame.display.set_caption("Kígyó Verseny")

ora = pygame.time.Clock()

zold = (0, 255, 0)
piros = (200, 40, 40)
sarga = (255, 255, 0)

betutipus = pygame.font.SysFont(None, 40)

# Tournament alapértelmezett érték
tournament = {
    "name": "Default Tournament",
    "results": [
        {"player": "Alice", "wins": 0},
        {"player": "Bob", "wins": 0}
    ]
}

def add_result(filename, player_name):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"tournament": {"results": []}}

    if "tournament" not in data:
        data["tournament"] = {"results": []}
    if "results" not in data["tournament"]:
        data["tournament"]["results"] = []

    results = data["tournament"]["results"]

    for player in results:
        if player["player"] == player_name:
            player["wins"] += 1
            break
    else:
        results.append({"player": player_name, "wins": 1})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def gyoztes_kivalasztasa(tournament_data):
    results = tournament_data.get("results", [])
    if not results:
        return "Nincs adat", 0
    gyoztes = max(results, key=lambda x: x.get("wins", 0))
    return gyoztes["player"], gyoztes["wins"]

def alaphelyzet():
    return (szelesseg // 2) // kigyo_meret * kigyo_meret, (magassag // 2) // kigyo_meret * kigyo_meret

# Alapértékek
lives = 3
pontszam = 0
highscore = 0
hossz = 1
sarga_etel_x = -kigyo_meret
sarga_etel_y = -kigyo_meret
sarga_aktiv = False

racs_szelesseg = szelesseg // kigyo_meret
racs_magassag = magassag // kigyo_meret

if os.path.exists("savegame.json"):
    with open("savegame.json", "r") as f:
        try:
            adatok = json.load(f)

            tournament_data = adatok.get("tournament", {})
            if isinstance(tournament_data, dict):
                tournament.update(tournament_data)

            kigyo_test = [tuple(pos) for pos in adatok.get("snake_positions", []) if isinstance(pos, list) and len(pos) == 2]
            if not kigyo_test:
                kigyo_x, kigyo_y = alaphelyzet()
                kigyo_test = [(kigyo_x, kigyo_y)]

            irany = adatok.get("direction", "right")
            if irany == "left":
                sebesseg_x, sebesseg_y = -kigyo_meret, 0
            elif irany == "right":
                sebesseg_x, sebesseg_y = kigyo_meret, 0
            elif irany == "up":
                sebesseg_x, sebesseg_y = 0, -kigyo_meret
            elif irany == "down":
                sebesseg_x, sebesseg_y = 0, kigyo_meret
            else:
                sebesseg_x, sebesseg_y = kigyo_meret, 0

            pontszam = int(adatok.get("score", 0))
            highscore = int(adatok.get("highscore", 0))
            lives = int(adatok.get("lives", 3))

            piros_etelx, piros_etely = adatok.get("red_food", [100, 100])
            sarga_etel_x, sarga_etel_y = adatok.get("yellow_food", [-kigyo_meret, -kigyo_meret])
            sarga_aktiv = adatok.get("yellow_active", False)
            hossz = int(adatok.get("length", 1))

            kigyo_x, kigyo_y = kigyo_test[-1]

        except Exception:
            kigyo_x, kigyo_y = alaphelyzet()
            piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
            piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret
            sebesseg_x, sebesseg_y = kigyo_meret, 0
            kigyo_test = [(kigyo_x, kigyo_y)]
else:
    kigyo_x, kigyo_y = alaphelyzet()
    piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
    piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret
    sebesseg_x, sebesseg_y = kigyo_meret, 0
    kigyo_test = [(kigyo_x, kigyo_y)]

fut = True
game_over = False
game_over_handled = False

while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.VIDEORESIZE:
            szelesseg, magassag = event.w, event.h
            kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
            racs_szelesseg = szelesseg // kigyo_meret
            racs_magassag = magassag // kigyo_meret
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and sebesseg_x == 0:
                sebesseg_x, sebesseg_y = -kigyo_meret, 0
            elif event.key == pygame.K_RIGHT and sebesseg_x == 0:
                sebesseg_x, sebesseg_y = kigyo_meret, 0
            elif event.key == pygame.K_UP and sebesseg_y == 0:
                sebesseg_x, sebesseg_y = 0, -kigyo_meret
            elif event.key == pygame.K_DOWN and sebesseg_y == 0:
                sebesseg_x, sebesseg_y = 0, kigyo_meret
            elif event.key == pygame.K_r and game_over:
                kigyo_x, kigyo_y = alaphelyzet()
                sebesseg_x, sebesseg_y = kigyo_meret, 0
                hossz = 1
                kigyo_test = [(kigyo_x, kigyo_y)]
                pontszam = 0
                lives = 3
                game_over = False
                game_over_handled = False

    if not game_over:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y

        if kigyo_x < 0 or kigyo_x >= szelesseg or kigyo_y < 0 or kigyo_y >= magassag or (kigyo_x, kigyo_y) in kigyo_test[:-1]:
            lives -= 1
            if lives > 0:
                kigyo_x, kigyo_y = alaphelyzet()
                kigyo_test = [(kigyo_x, kigyo_y)]
            else:
                game_over = True
            continue

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

        if kigyo_x == piros_etelx and kigyo_y == piros_etely:
            hossz += 1
            pontszam += 1
            if pontszam > highscore:
                highscore = pontszam
            piros_etelx = random.randint(0, racs_szelesseg - 1) * kigyo_meret
            piros_etely = random.randint(0, racs_magassag - 1) * kigyo_meret

        if sarga_aktiv and kigyo_x == sarga_etel_x and kigyo_y == sarga_etel_y:
            hossz += 3
            pontszam += 3
            sarga_aktiv = False
        elif not sarga_aktiv and random.random() < 0.01:
            sarga_etel_x = random.randint(0, racs_szelesseg - 1) * kigyo_meret
            sarga_etel_y = random.randint(0, racs_magassag - 1) * kigyo_meret
            sarga_aktiv = True

    kepernyo.fill((0, 0, 0))
    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, zold, (x, y, kigyo_meret, kigyo_meret))
    pygame.draw.rect(kepernyo, piros, (piros_etelx, piros_etely, kigyo_meret, kigyo_meret))
    if sarga_aktiv:
        pygame.draw.rect(kepernyo, sarga, (sarga_etel_x, sarga_etel_y, kigyo_meret, kigyo_meret))

    kepernyo.blit(betutipus.render(f"Pont: {pontszam}", True, (255, 255, 255)), (10, 10))
    kepernyo.blit(betutipus.render(f"Highscore: {highscore}", True, (255, 255, 255)), (10, 50))
    kepernyo.blit(betutipus.render(f"Lives: {lives}", True, (255, 255, 255)), (10, 90))

    if game_over:
        if not game_over_handled:
            add_result("savegame.json", "Alice")
            game_over_handled = True

        kepernyo.blit(betutipus.render("Game Over!", True, (255, 0, 0)), (szelesseg // 2 - 100, magassag // 2))
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
            "tournament": tournament
        }
        with open("savegame.json", "w") as f:
            json.dump(adatok, f, indent=4)

pygame.quit()

# Győztes kiíratása
nyertes_nev, nyertes_gyozelmek = gyoztes_kivalasztasa(tournament)
print(f"A győztes: {nyertes_nev} {nyertes_gyozelmek} győzelemmel.")
