import pygame
import random
import json

pygame.init()

# --- KONZOLBÓL KÉRJÜK BE A JÁTÉKOSOK NEVÉT ---

def beker_jatekosok(szam=4):
    nevek = []
    print(f"Kérlek, add meg {szam} játékos nevét:")
    for i in range(szam):
        nev = input(f"Játékos {i+1} neve: ").strip()
        while not nev or nev in nevek:
            nev = input(f"A név nem lehet üres vagy ismétlődő. Játékos {i+1} neve: ").strip()
        nevek.append(nev)
    return nevek

jatekos_nevek = beker_jatekosok(4)

# --- TORNAMENT ADATSTRUKTÚRA ---

tournament = {
    "name": "Kígyó Verseny",
    "results": [{"player": nev, "wins": 0} for nev in jatekos_nevek]
}

# --- ALAPVETŐ PYGAME BEÁLLÍTÁSOK ---

szelesseg = 1280
magassag = 720
kigyo_meret = 20

kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
pygame.display.set_caption("Kígyó Verseny")

ora = pygame.time.Clock()

zold = (0, 255, 0)
piros = (200, 40, 40)
sarga = (255, 255, 0)
feher = (255, 255, 255)

betutipus = pygame.font.SysFont(None, 40)

def alaphelyzet():
    return (szelesseg // 2) // kigyo_meret * kigyo_meret, (magassag // 2) // kigyo_meret * kigyo_meret

def uj_etel_pozicio():
    return (random.randint(0, szelesseg // kigyo_meret - 1) * kigyo_meret,
            random.randint(0, magassag // kigyo_meret - 1) * kigyo_meret)

def draw_pontok(surface, allapotok, font, x, y):
    surface.blit(font.render("Játékosok pontjai:", True, feher), (x, y))
    offset = 40
    for i, player in enumerate(allapotok):
        szoveg = f"{player['nev']}: {player['pontszam']} pont"
        surface.blit(font.render(szoveg, True, feher), (x, y + offset))
        offset += 30

# --- JÁTÉKOSOK ÁLLAPOTA ---

allapotok = []
for nev in jatekos_nevek:
    allapotok.append({
        "nev": nev,
        "pontszam": 0,
        "lives": 3,
        "hossz": 1,
    })

akt_jatekos_idx = 0

# --- KÍGYÓ ÉS ÉTEL VÁLTOZÓK ---

def jatek_indito():
    x, y = alaphelyzet()
    return x, y, [(x, y)], kigyo_meret, 0, 3, 1

kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz = jatek_indito()

piros_etelx, piros_etely = uj_etel_pozicio()
sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
sarga_aktiv = False

sebesseg_x, sebesseg_y = kigyo_meret, 0

fut = True
game_over = False
varakozas_jatekosszokozre = False

while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.VIDEORESIZE:
            szelesseg, magassag = event.w, event.h
            kepernyo = pygame.display.set_mode((szelesseg, magassag), pygame.RESIZABLE)
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
                # Itt váltás indítása gombnyomásra (space vagy enter)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Játékos váltás
                    allapotok[akt_jatekos_idx]["pontszam"] = pontszam  # mentjük az aktuális pontot
                    akt_jatekos_idx += 1
                    if akt_jatekos_idx >= len(allapotok):
                        # Minden játékos végzett, vége a tornának
                        max_pont = -1
                        gyoztes_nev = None
                        for jatekos in allapotok:
                            if jatekos["pontszam"] > max_pont:
                                max_pont = jatekos["pontszam"]
                                gyoztes_nev = jatekos["nev"]
                        # Győzelmek növelése
                        for p in tournament["results"]:
                            if p["player"] == gyoztes_nev:
                                p["wins"] += 1
                                break
                        # Végeredmény megjelenítése és várakozás 5 mp
                        kepernyo.fill((0, 0, 0))
                        vege_szoveg = betutipus.render(f"A torna véget ért! Győztes: {gyoztes_nev} ({max_pont} pont)", True, feher)
                        kepernyo.blit(vege_szoveg, (szelesseg // 2 - vege_szoveg.get_width() // 2, magassag // 2))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        fut = False
                    else:
                        # Új játékos kezdése
                        kigyo_x, kigyo_y, kigyo_test, kigyo_meret, pontszam, lives, hossz = jatek_indito()
                        piros_etelx, piros_etely = uj_etel_pozicio()
                        sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
                        sarga_aktiv = False
                        sebesseg_x, sebesseg_y = kigyo_meret, 0
                        game_over = False
                        varakozas_jatekosszokozre = False

    if not game_over and not varakozas_jatekosszokozre:
        kigyo_x += sebesseg_x
        kigyo_y += sebesseg_y

        # Ütközés ellenőrzés
        if (kigyo_x < 0 or kigyo_x >= szelesseg or
            kigyo_y < 0 or kigyo_y >= magassag or
            (kigyo_x, kigyo_y) in kigyo_test[:-1]):

            lives -= 1
            if lives > 0:
                kigyo_x, kigyo_y = alaphelyzet()
                kigyo_test = [(kigyo_x, kigyo_y)]
                hossz = 1
                sebesseg_x, sebesseg_y = kigyo_meret, 0
            else:
                # Játék vége a jelenlegi játékosnak
                allapotok[akt_jatekos_idx]["pontszam"] = pontszam
                game_over = True
                varakozas_jatekosszokozre = True
            continue

        kigyo_test.append((kigyo_x, kigyo_y))
        if len(kigyo_test) > hossz:
            del kigyo_test[0]

        # Piros étel elfogyasztása
        if kigyo_x == piros_etelx and kigyo_y == piros_etely:
            hossz += 1
            pontszam += 1
            piros_etelx, piros_etely = uj_etel_pozicio()

        # Sárga étel aktiválása és elfogyasztása
        if sarga_aktiv and kigyo_x == sarga_etel_x and kigyo_y == sarga_etel_y:
            hossz += 3
            pontszam += 3
            sarga_aktiv = False
            sarga_etel_x, sarga_etel_y = -kigyo_meret, -kigyo_meret
        elif not sarga_aktiv and random.random() < 0.01:
            sarga_etel_x, sarga_etel_y = uj_etel_pozicio()
            sarga_aktiv = True

    # Rajzolás
    kepernyo.fill((0, 0, 0))
    for x, y in kigyo_test:
        pygame.draw.rect(kepernyo, zold, (x, y, kigyo_meret, kigyo_meret))
    pygame.draw.rect(kepernyo, piros, (piros_etelx, piros_etely, kigyo_meret, kigyo_meret))
    if sarga_aktiv:
        pygame.draw.rect(kepernyo, sarga, (sarga_etel_x, sarga_etel_y, kigyo_meret, kigyo_meret))

    kepernyo.blit(betutipus.render(f"Játékos: {allapotok[akt_jatekos_idx]['nev']}", True, feher), (10, 10))
    kepernyo.blit(betutipus.render(f"Pont: {pontszam}", True, feher), (10, 50))
    kepernyo.blit(betutipus.render(f"Életek: {lives}", True, feher), (10, 90))

    draw_pontok(kepernyo, allapotok, betutipus, szelesseg - 300, 10)

    if varakozas_jatekosszokozre:
        szoveg = betutipus.render("Játékos véget ért! Nyomj SPACE vagy ENTER-t a folytatáshoz.", True, feher)
        kepernyo.blit(szoveg, (szelesseg // 2 - szoveg.get_width() // 2, magassag // 2))

    pygame.display.update()
    ora.tick(10)

pygame.quit()

# --- Mentés JSON fájlba opcionálisan ---
with open("torna_eredmenyek.json", "w") as f:
    json.dump(tournament, f, indent=4)
