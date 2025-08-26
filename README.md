import pygame
import random
import json
import os
from datetime import datetime
import pandas as pd
import time

pygame.init()

# --- Segédfüggvény a futam-naplózáshoz ---
def futam_naplozas_csv_be(player: str, score: float, length: int, lives_left: int, tournament_name: str, yellow_eaten: int, red_eaten: int, duration_s: float, path: str = "scores.csv") -> None:
    """Futam adatait CSV fájlba menti.

    Stratégia:
        1) Új sor létrehozása a megadott paraméterekkel.
        2) Ha a fájl nem létezik, fejlécet ad hozzá.
        3) A sorokat UTF-8 kódolással menti a megadott fájlba.

    Argumentumok:
        player (str): A játékos neve.
        score (float): A játékos pontszáma.
        length (int): A kígyó hossza.
        lives_left (int): A hátralévő életek száma.
        tournament_name (str): A torna neve.
        yellow_eaten (int): A sárga ételek száma.
        red_eaten (int): A piros ételek száma.
        duration_s (float): A futam időtartama másodpercekben.
        path (str): A kimeneti CSV fájl elérési útja (alapértelmezett: 'scores.csv').

    Visszatérés:
        None: A függvény nem ad vissza értéket, csak fájlba ír.
    """
    sor = {
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
    df = pd.DataFrame([sor])
    header_needed = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header_needed, index=False, encoding="utf-8")

# --- Játékosok bekérése ---
def jatekosok_bekerese(szam: int = 4) -> list:
    """Játékosok neveinek bekérése a felhasználótól.

    Stratégia:
        1) A megadott számú játékos nevét kéri be.
        2) Ellenőrzi, hogy a név nem üres és nem ismétlődik.

    Argumentumok:
        szam (int): A bekérendő játékosok száma (alapértelmezett: 4).

    Visszatérés:
        list: A játékosok neveit tartalmazó lista.
    """
    nevek = []
    print(f"Kérlek, add meg {szam} játékos nevét:")
    for i in range(szam):
        nev = input(f"Játékos {i+1} neve: ").strip()
        while not nev or nev in nevek:
            nev = input(f"A név nem lehet üres vagy ismétlődő. Játékos {i+1} neve: ").strip()
        nevek.append(nev)
    return nevek

jatekos_nevek = jatekosok_bekerese()

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
hud_magassag = 180  # Növelt HUD magasság a kártyák teljes befogadásához
palya_bal, palya_felso = 0, hud_magassag  # Játékterület a HUD alatt kezdődik
palya_jobb, palya_also = szelesseg, magassag

kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
pygame.display.set_caption("Kígyó Verseny")
ora = pygame.time.Clock()

szinek = {
    "zold": (0, 200, 0),
    "piros": (200, 40, 40),
    "sarga": (255, 200, 0),
    "feher": (255, 255, 255),
    "hud_hatter": (0, 0, 0)
}
betutipus = pygame.font.SysFont("Arial", 20, bold=True)

def alap_helyzet() -> tuple:
    """Kígyó kezdeti pozíciójának meghatározása.

    Stratégia:
        1) A kígyó kezdőpontja a képernyő közepén van, igazítva a rácsra.
        2) A HUD magassága felett kezdődik.

    Argumentumok:
        Nincs argumentum.

    Visszatérés:
        tuple: A kígyó (x, y) koordinátái.
    """
    x = (szelesseg // 2) // kigyo_meret * kigyo_meret
    y = ((hud_magassag + kigyo_meret) // kigyo_meret) * kigyo_meret
    return x, y

def uj_etel_pozicio() -> tuple:
    """Új étel véletlenszerű pozíciójának generálása a játékterületen.

    Stratégia:
        1) A pozíció a játékterület rácsára igazodik.
        2) A HUD és a játékterület szélétől távol tartja.

    Argumentumok:
        Nincs argumentum.

    Visszatérés:
        tuple: Az étel (x, y) koordinátái.
    """
    return (
        random.randint(0, (palya_jobb // kigyo_meret) - 1) * kigyo_meret,
        random.randint((palya_felso + kigyo_meret) // kigyo_meret, (palya_also // kigyo_meret) - 1) * kigyo_meret
    )

def kartya_rajzolasa(surface, x: int, y: int, w: int, h: int, title: str, rows: list) -> None:
    """Kártya rajzolása a képernyőre a megadott adatokkal.

    Stratégia:
        1) Létrehoz egy átlátszó felületet a kártyához.
        2) Címet és sorokat rajzol a kártyára.
        3) A szövegeket igazítja a kártya belsejébe.

    Argumentumok:
        surface: A rajzolási felület (pl. képernyő).
        x (int): A kártya bal felső sarkának x koordinátája.
        y (int): A kártya bal felső sarkának y koordinátája.
        w (int): A kártya szélessége.
        h (int): A kártya magassága.
        title (str): A kártya címe.
        rows (list): A kártyán megjelenítendő sorok szövege.

    Visszatérés:
        None: A függvény nem ad vissza értéket, csak rajzol.
    """
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (30, 30, 30, 180), (0, 0, w, h), border_radius=12)
    surface.blit(s, (x, y))

    title_surf = betutipus.render(title, True, szinek["sarga"])
    surface.blit(title_surf, (x + 10, y + 5))

    offset_y = 30
    for sor in rows:
        sor_surf = betutipus.render(sor, True, szinek["feher"])
        surface.blit(sor_surf, (x + 10, y + offset_y))
        offset_y += 22

allapotok = [{"nev": nev, "pontszam": 0, "lives": 3, "hossz": 1} for nev in jatekos_nevek]
akt_jatekos_idx = 0

def jatek_inditas() -> tuple:
    """Játék inicializálása új játékos számára.

    Stratégia:
        1) Kezdeti pozíciót állít be a kígyónak.
        2) Betölti a játékos eddigi pontszámát, ha létezik.

    Argumentumok:
        Nincs argumentum.

    Visszatérés:
        tuple: (x, y, kigyo_test, kigyo_meret, pontszam, lives, hossz, yellow_eaten, red_eaten, start_time, total_score).
    """
    x, y = alap_helyzet()
    total_score = 0
    if os.path.exists("scores.csv"):
        df = pd.read_csv("scores.csv")
        if akt_jatekos_idx < len(allapotok):
            current_player = allapotok[akt_jatekos_idx]["nev"]
            total_score = df[df["player"] == current_player]["score"].sum()
    return x, y, [(x, y)], kigyo_meret, 0, 3, 1, 0, 0, time.time(), total_score

# Kezdeti értékek
kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz, yellow_eaten, red_eaten, start_time, total_score = jatek_inditas()
piros_etelx, piros_etely = uj_etel_pozicio()
sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
sarga_aktiv = False
sarga_idozito = 0  # Időzítő a sárga kocka megjelenéséhez
sarga_eltunes_ido = 0  # Véletlenszerű eltűnés ideje

sebesseg_x, sebesseg_y = kigyo_meret, 0
fut = True
game_over = False
varakozas_jatekosokre = False
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
            if not varakozas_jatekosokre:
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
                    if not logged_this_player:
                        current_player = allapotok[akt_jatekos_idx]["nev"]
                        duration_s = time.time() - start_time
                        futam_naplozas_csv_be(current_player, pontszam, hossz, lives, tournament["name"], yellow_eaten, red_eaten, duration_s)
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
                        kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz, yellow_eaten, red_eaten, start_time, total_score = jatek_inditas()
                        piros_etelx, piros_etely = uj_etel_pozicio()
                        sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
                        sarga_aktiv = False
                        sarga_idozito = 0
                        sarga_eltunes_ido = 0
                        sebesseg_x, sebesseg_y = kigyo_meret, 0
                        game_over = False
                        varakozas_jatekosokre = False
                        logged_this_player = False

    if not game_over and not varakozas_jatekosokre:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y
        if (kigyo_x < palya_bal or kigyo_x >= palya_jobb or kigyo_y < palya_felso or kigyo_y >= palya_also or (kigyo_x, kigyo_y) in kigyo_test[:-1]):
            lives -= 1
            if lives > 0:
                kigyo_x, kigyo_y = alap_helyzet()
                kigyo_test = [(kigyo_x - i * kigyo_meret, kigyo_y) for i in reversed(range(hossz))]
                sebesseg_x, sebesseg_y = kigyo_meret, 0
            else:
                allapotok[akt_jatekos_idx]["pontszam"] = pontszam
                game_over = True
                varakozas_jatekosokre = True
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
            sarga_idozito = time.time()  # Időzítő elindítása
            sarga_eltunes_ido = random.uniform(3.0, 9.0)  # Véletlenszerű eltűnés 3-9 mp között

        # Ellenőrzés a sárga kocka eltűnésére
        if sarga_aktiv:
            eltelt_ido = time.time() - sarga_idozito
            if eltelt_ido >= sarga_eltunes_ido:  # Eltűnés a véletlenszerű idő elérésekor
                sarga_aktiv = False
                sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
                sarga_idozito = 0
                sarga_eltunes_ido = 0

    # --- RAJZOLÁS ---
    kepernyo.fill((0, 0, 0))
    # HUD háttér rajzolása
    pygame.draw.rect(kepernyo, szinek["hud_hatter"], (0, 0, szelesseg, hud_magassag))
    # Játékterület rajzolása
    pygame.draw.rect(kepernyo, (50, 50, 50), (palya_bal, palya_felso, palya_jobb - palya_bal, palya_also - palya_felso))
    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, szinek["zold"], (x, y, kigyo_meret, kigyo_meret))
    pygame.draw.rect(kepernyo, szinek["piros"], (piros_etelx, piros_etely, kigyo_meret, kigyo_meret))
    if sarga_aktiv:
        pygame.draw.rect(kepernyo, szinek["sarga"], (sarga_etel_x, sarga_etel_y, kigyo_meret, kigyo_meret))

    # --- Modern HUD kártyák a HUD területén ---
    if akt_jatekos_idx < len(allapotok):
        # Bal oldali kártya (jelenlegi játékos statisztikái) a HUD-on
        sorok = [
            f"Pont: {pontszam}",
            f"Életek: {lives}",
            f"Piros: {red_eaten}",
            f"Sárga: {yellow_eaten}",
            f"Összpont: {total_score}"
        ]
        kartya_szelesseg = 250
        kartya_x = 10
        kartya_rajzolasa(kepernyo, kartya_x, 10, kartya_szelesseg, 150, f"Játékos: {allapotok[akt_jatekos_idx]['nev']}", sorok)

        # Jobb oldali kártya (minden játékos pontszáma) a HUD-on
        sorok = [f"{p['nev']}: {p['pontszam']}p" for p in allapotok]
        kartya_szelesseg = 260
        kartya_x = szelesseg - kartya_szelesseg - 10
        max_kartya_magassag = 150  # Magasság korlátozása a HUD-on belül
        kartya_rajzolasa(kepernyo, kartya_x, 10, kartya_szelesseg, min(max_kartya_magassag, 40 + 22 * len(sorok)), "Ponttábla", sorok)

    if varakozas_jatekosokre:
        szoveg = betutipus.render("Vége! SPACE/ENTER a folytatáshoz.", True, szinek["feher"])
        kepernyo.blit(szoveg, (szelesseg // 2 - szoveg.get_width() // 2, magassag // 2))

    pygame.display.update()
    ora.tick(10)

pygame.quit()

# --- Állapot mentése JSON-be ---
adat["tournament"] = tournament
with open("savegame.json", "w") as f:
    json.dump(adat, f, indent=4)
    