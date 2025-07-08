# 2. Kígyó kirajzolása - Rajzolj egy 20x20 pixeles zöld négyzetet a képernyő közepére.

import pygame

pygame.init()

kepernyo = pygame.display.set_mode((600, 400))

ora = pygame.time.Clock()

kigyo_meret = 20
kigyo_x = (600 - kigyo_meret) // 2
kigyo_y = (400 - kigyo_meret) // 2

zold = (0, 255, 0)

fut = True

# Játék fő ciklusa
while fut:
    # Események kezelése (pl. kilépés)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False

    # Képernyő törlés
    kepernyo.fill((0, 0, 0))

    pygame.draw.rect(kepernyo, zold, (kigyo_x, kigyo_y, kigyo_meret, kigyo_meret))
    pygame.display.flip()
    ora.tick(60)

pygame.quit() 
