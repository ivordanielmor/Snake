# 1. Ablak indítása - Indítsd el a 600x400-as ablakot és állítsd be, hogy a játék 10 FPS-sel fusson.

import pygame

pygame.init()

kepernyo = pygame.display.set_mode((600, 400))

ora = pygame.time.Clock()

# Játék fő ciklusa
while True:
    # Események kezelése (pl. kilépés)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Képernyő törlés
    kepernyo.fill((0, 0, 0))  # Fekete háttér

    # Frissítjük a képernyőt
    pygame.display.flip()

    # Állítsuk be a 10 FPS-t
    ora.tick(10)  # 10 FPS beállítása
    