# Snake – Multiplayer Snake Game Based on Pygame

This is a multiplayer snake game created using the [Pygame](https://www.pygame.org/news) library. Players take turns controlling the snake to eat food, grow longer, and avoid collisions. The game keeps track of scores in a tournament system.

---

## 🕹️ Gameplay

- At the start, players enter their names.
- Each player takes turns controlling the snake to earn as many points as possible.
- Eating red food increases the snake's length and scores points.
- Yellow food appears randomly and grants more points and length.
- Each player has lives; collisions cause the loss of a life.
- The game ends when all players finish their turns, and the highest scorer wins.

---

## 🧱 Structure

- **Pygame window:** Resizable game field with a HUD displaying scores and player statuses.
- **Main features:**
  - Player name input
  - Snake movement and collision detection
  - Different types of food (red and yellow)
  - Life and scoring system
  - Saving results to a JSON file (`savegame.json`)
- **Main game loop:** Manages gameplay and player turns.

---

## 🛠️ Installation & Running

### Requirements

- [Python 3](https://www.python.org/)
- [Pygame](https://www.pygame.org/news)

Install pygame with pip:

```bash
pip install pygame
```

### Running the game

Save the file as snake.py, then run:

```bash
python snake.py
```

---

## 🧠 Features Overview

- Multiplayer snake game with turn-based control  
- Tournament results saved in a JSON file (savegame.json)  
- Random special food (yellow) giving extra points and length  
- Life system for each player  
- Supports resizable window  

---

## 📷 Screenshot

![Screenshot](./images/snake.png)

---

## 📄 License

This project is free to use for learning purposes.

---

**Have fun playing! 🐍**

---

# Snake – Pygame alapú többszemélyes kígyós játék

Ez egy többszemélyes kígyós játék, amelyet a [Pygame](https://www.pygame.org/news) könyvtár segítségével készítettünk. A játékosok felváltva irányítják a kígyót, hogy egyenek, növekedjenek és elkerüljék az ütközéseket. A játék versenyrendszerben tartja nyilván a pontszámokat.

---

## 🕹️ Játékmenet

- A játék elején a játékosok beírják a nevüket.
- Minden játékos felváltva irányítja a kígyót, hogy minél több pontot szerezzen.
- A piros étel elfogyasztása növeli a kígyó hosszát és pontokat ad.
- Sárga étel véletlenszerűen jelenik meg, több pontot és hosszabbodást ad.
- Minden játékosnak van élete; az ütközések életvesztéssel járnak.
- A játék akkor ér véget, amikor minden játékos befejezte a körét, és a legtöbb pontot szerző nyer.

---

## 🧱 Felépítés

- **Pygame ablak:** Átméretezhető játéktér, HUD-dal, ami mutatja a pontszámokat és a játékos állapotát.
- **Főbb funkciók:**
  - Játékosnév bevitele
  - Kígyó mozgás és ütközésellenőrzés
  - Különböző típusú étel (piros és sárga)
  - Élet- és pontszámrendszer
  - Eredmények mentése JSON fájlba (`savegame.json`)
- **Fő játékhurok:** Kezeli a játékmenetet és a játékosok köröket.

---

## 🛠️ Telepítés és futtatás

### Követelmények

- [Python 3](https://www.python.org/)
- [Pygame](https://www.pygame.org/news)

Telepítés pip-pel:

```bash
pip install pygame
```

### A játék futtatása

Mentse a fájlt `snake.py` néven, majd futtassa:

```bash
python snake.py
```

---

## 🧠 Funkciók összefoglalása

- Többszemélyes kígyós játék körökre osztott irányítással  
- Versenyeredmények mentése JSON fájlba (savegame.json)  
- Véletlenszerű speciális étel (sárga), ami extra pontot és hosszabbodást ad  
- Életrendszer minden játékosnak  
- Átméretezhető ablak támogatása  

---

## 📷 Képernyőkép

![Képernyőkép](./images/screenshot.png)

---

## 📄 Licenc

Ez a projekt tanulási célokra szabadon használható.

---

**Kellemes játékot! 🐍**
