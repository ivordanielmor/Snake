# HÁZI FELADAT
# Top 5 futam: ki volt az 5 legjobb (player + score + timestamp)? Tipp: df.nlargest(5, "score").
# Heti összesítés: df.set_index("timestamp").groupby("player").resample("W")["score"].sum(), majd heti kumulált pont.
# Mentés: scores_weekly.csv, scores_weekly_cum.csv.
# Mini kihívás: írd ki a HUD-ra a játékos eddigi összpontját a CSV-ből beolvasva a futam elején.

# --- Importok ---
import pygame
import random
import json
import os
from datetime import datetime
import pandas as pd
import time

pygame.init()

# --- Segédfüggvény a futam-naplózáshoz ---
def log_run_to_csv(player, score, length, lives_left, tournament_name, yellow_eaten, red_eaten, duration_s, path="scores.csv"):
    """Egy futam eredményének naplózása CSV-be (append)."""
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "player": player,
        "score": int(score),
        "length": int(length),
        "lives_left": int(lives_left),
        "tournament": tournament_name,
        "yellow_eaten": int(yellow_eaten),
        "red_eaten": int(red_eaten),
        "duration_s": int(duration_s)
    }
    df = pd.DataFrame([row])
    header_needed = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header_needed, index=False, encoding="utf-8")

# --- Játékosok bekérése ---
def beker_jatekosok(szam=4):
    nevek = []
    print(f"Kérlek, add meg {szam} játékos nevét:")
    for i in range(szam):
        nev = input(f"Játékos {i+1} neve: ").strip()
        while not nev or nev in nevek:
            nev = input(f"A név nem lehet üres vagy ismétlődő. Játékos {i+1} neve: ").strip()
        nevek.append(nev)
    return nevek

jatekos_nevek = beker_jatekosok()

# --- Korábban mentett állapot betöltése ---
try:
    with open("savegame.json", "r") as f:
        adat = json.load(f)
        tournament = adat.get("tournament", {
            "name": "Kígyó Verseny",
            "results": [{"player": nev, "wins": 0} for nev in jatekos_nevek]
        })
except FileNotFoundError:
    adat = {}
    tournament = {
        "name": "Kígyó Verseny",
        "results": [{"player": nev, "wins": 0} for nev in jatekos_nevek]
    }

# --- PYGAME BEÁLLÍTÁSOK ---
szelesseg, magassag = 1280, 720
kigyo_meret = 20
hud_magassag = 200   # <-- NAGYOBB HUD, hogy ne lógjanak ki a szövegek
palya_bal, palya_felső = 0, hud_magassag
palya_jobb, palya_also = szelesseg, magassag

kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
pygame.display.set_caption("Kígyó Verseny")
ora = pygame.time.Clock()

szinek = {"zold": (0, 255, 0), "piros": (200, 40, 40), "sarga": (255, 255, 0), "feher": (255, 255, 255)}
betutipus = pygame.font.SysFont(None, 24)

def alaphelyzet():
    x = (szelesseg // 2) // kigyo_meret * kigyo_meret
    y = ((hud_magassag + kigyo_meret) // kigyo_meret) * kigyo_meret
    return x, y

def uj_etel_pozicio():
    return (
        random.randint(0, (palya_jobb // kigyo_meret) - 1) * kigyo_meret,
        random.randint((palya_felső + kigyo_meret) // kigyo_meret, (palya_also // kigyo_meret) - 1) * kigyo_meret
    )

def draw_pontok(surface, allapotok, font, x, y):
    surface.blit(font.render("Játékosok pontjai:", True, szinek["feher"]), (x, y))
    offset = 20
    for player in allapotok:
        szoveg = f"{player['nev']}: {player['pontszam']} pont"
        surface.blit(font.render(szoveg, True, szinek["feher"]), (x, y + offset))
        offset += 20

allapotok = [{"nev": nev, "pontszam": 0, "lives": 3, "hossz": 1} for nev in jatekos_nevek]
akt_jatekos_idx = 0

def jatek_indito():
    x, y = alaphelyzet()
    # Összpontszám kiszámítása az aktuális játékoshoz a scores.csv-ből
    total_score = 0
    if os.path.exists("scores.csv"):
        df = pd.read_csv("scores.csv")
        if akt_jatekos_idx < len(allapotok):
            current_player = allapotok[akt_jatekos_idx]["nev"]
            total_score = df[df["player"] == current_player]["score"].sum()
    return x, y, [(x, y)], kigyo_meret, 0, 3, 1, 0, 0, time.time(), total_score

kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz, yellow_eaten, red_eaten, start_time, total_score = jatek_indito()
piros_etelx, piros_etely = uj_etel_pozicio()
sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
sarga_aktiv = False

sebesseg_x, sebesseg_y = kigyo_meret, 0
fut = True
game_over = False
varakozas_jatekosszokozre = False
logged_this_player = False

# --- Főciklus ---
while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.VIDEORESIZE:
            szelesseg, magassag = event.w, event.h
            kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
            palya_jobb = szelesseg
            palya_also = magassag
        if event.type == pygame.KEYDOWN:
            if not varakozas_jatekosszokozre:
                if event.key == pygame.K_LEFT and sebesseg_x == 0:
                    sebesseg_x, sebesseg_y = -kigyo_meret, 0
                elif event.key == pygame.K_RIGHT and sebesseg_x == 0:
                    sebesseg_x, sebesseg_y = kigyo_meret, 0
                elif event.key == pygame.K_UP and sebesseg_y == 0:
                    sebesseg_x, sebesseg_y = 0, -kigyo_meret
                elif event.key == pygame.K_DOWN and sebesseg_y == 0:
                    sebesseg_x, sebesseg_y = 0, kigyo_meret
            else:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    # --- CSV naplózás, egyszer futamonként ---
                    if not logged_this_player:
                        current_player = allapotok[akt_jatekos_idx]["nev"]
                        duration_s = time.time() - start_time
                        log_run_to_csv(
                            player=current_player,
                            score=pontszam,
                            length=hossz,
                            lives_left=lives,
                            tournament_name=tournament["name"],
                            yellow_eaten=yellow_eaten,
                            red_eaten=red_eaten,
                            duration_s=duration_s
                        )
                        logged_this_player = True

                    allapotok[akt_jatekos_idx]["pontszam"] = pontszam
                    akt_jatekos_idx += 1
                    if akt_jatekos_idx >= len(allapotok):
                        max_pont = max(j["pontszam"] for j in allapotok)
                        gyoztesek = [j["nev"] for j in allapotok if j["pontszam"] == max_pont]
                        for p in tournament["results"]:
                            if p["player"] in gyoztesek:
                                p["wins"] += 1
                        kepernyo.fill((0, 0, 0))
                        gyoztes_szoveg = ", ".join(gyoztesek)
                        szoveg = betutipus.render(f"A torna véget ért! Győztes(ek): {gyoztes_szoveg} ({max_pont} pont)", True, szinek["feher"])
                        kepernyo.blit(szoveg, (szelesseg // 2 - szoveg.get_width() // 2, magassag // 2))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        fut = False
                    else:
                        kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz, yellow_eaten, red_eaten, start_time, total_score = jatek_indito()
                        piros_etelx, piros_etely = uj_etel_pozicio()
                        sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
                        sarga_aktiv = False
                        sebesseg_x, sebesseg_y = kigyo_meret, 0
                        game_over = False
                        varakozas_jatekosszokozre = False
                        logged_this_player = False

    if not game_over and not varakozas_jatekosszokozre:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y
        if (kigyo_x < palya_bal or kigyo_x >= palya_jobb or kigyo_y < palya_felső or kigyo_y >= palya_also or (kigyo_x, kigyo_y) in kigyo_test[:-1]):
            lives -= 1
            if lives > 0:
                kigyo_x, kigyo_y = alaphelyzet()
                kigyo_test = [(kigyo_x - i * kigyo_meret, kigyo_y) for i in reversed(range(hossz))]
                sebesseg_x, sebesseg_y = kigyo_meret, 0
            else:
                allapotok[akt_jatekos_idx]["pontszam"] = pontszam
                game_over = True
                varakozas_jatekosszokozre = True
            continue

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

        if kigyo_x == piros_etelx and kigyo_y == piros_etely:
            hossz += 1
            pontszam += 1
            red_eaten += 1
            piros_etelx, piros_etely = uj_etel_pozicio()

        if sarga_aktiv and kigyo_x == sarga_etel_x and kigyo_y == sarga_etel_y:
            hossz += 3
            pontszam += 3
            yellow_eaten += 1
            sarga_aktiv = False
            sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
        elif not sarga_aktiv and random.random() < 0.01:
            sarga_etel_x, sarga_etel_y = uj_etel_pozicio()
            sarga_aktiv = True

    # --- RAJZOLÁS ---
    kepernyo.fill((0, 0, 0))
    pygame.draw.rect(kepernyo, (50, 50, 50), (palya_bal, palya_felső, palya_jobb - palya_bal, palya_also - palya_felső))
    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, szinek["zold"], (x, y, kigyo_meret, kigyo_meret))
    pygame.draw.rect(kepernyo, szinek["piros"], (piros_etelx, piros_etely, kigyo_meret, kigyo_meret))
    if sarga_aktiv:
        pygame.draw.rect(kepernyo, szinek["sarga"], (sarga_etel_x, sarga_etel_y, kigyo_meret, kigyo_meret))
    if akt_jatekos_idx < len(allapotok):
        kepernyo.blit(betutipus.render(f"Játékos: {allapotok[akt_jatekos_idx]['nev']}", True, szinek["feher"]), (10, 10))

    # --- Bal oldali statisztikák automatikusan sorban ---
    sor_y = 40
    sorok = [
        f"Pont: {pontszam}",
        f"Életek: {lives}",
        f"Piros ételek: {red_eaten}",
        f"Sárga ételek: {yellow_eaten}",
        f"Összpont: {total_score}"
    ]
    for i, szoveg in enumerate(sorok):
        kepernyo.blit(betutipus.render(szoveg, True, szinek["feher"]), (10, sor_y + i * 25))

    # --- Jobb oldali összpontok ---
    draw_pontok(kepernyo, allapotok, betutipus, szelesseg - 280, 10)

    if varakozas_jatekosszokozre:
        szoveg = betutipus.render("Játékos véget ért! Nyomj SPACE vagy ENTER-t a folytatáshoz.", True, szinek["feher"])
        kepernyo.blit(szoveg, (szelesseg // 2 - szoveg.get_width() // 2, magassag // 2))

    pygame.display.update()
    ora.tick(10)

pygame.quit()

# --- Állapot mentése JSON-be ---
adat["tournament"] = tournament
with open("savegame.json", "w") as f:
    json.dump(adat, f, indent=4)

# --- Házi feladat: Top 5 futam és heti összesítés ---
if os.path.exists("scores.csv"):
    df = pd.read_csv("scores.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 1. Top 5 futam
    top_5_runs = df.nlargest(5, "score")[["player", "score", "timestamp"]]
    print("\nTop 5 futam:")
    print(top_5_runs)

    # 2. Heti összesítés
    weekly_scores = df.set_index("timestamp").groupby("player").resample("W")["score"].sum().reset_index()
    weekly_scores.to_csv("scores_weekly.csv", index=False, encoding="utf-8")
    print("\nHeti összesítés (scores_weekly.csv):")
    print(weekly_scores)

    # 3. Heti kumulált pontszám
    weekly_cum_scores = weekly_scores.groupby("player")["score"].cumsum().reset_index()
    weekly_cum_scores["player"] = weekly_scores["player"]
    weekly_cum_scores["timestamp"] = weekly_scores["timestamp"]
    weekly_cum_scores = weekly_cum_scores[["timestamp", "player", "score"]]
    weekly_cum_scores.to_csv("scores_weekly_cum.csv", index=False, encoding="utf-8")
    print("\nHeti kumulált pontszám (scores_weekly_cum.csv):")
    print(weekly_cum_scores)
else:
    print("A scores.csv fájl nem található.")
