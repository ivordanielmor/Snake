# 3. Billentyűkezelés - A kurzor nyilai 20 pixellel mozgatják a kígyó fejét.

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                kigyo_x -= 20
            if event.key == pygame.K_RIGHT:
                kigyo_x += 20
            if event.key == pygame.K_UP:
                kigyo_y -= 20
            if event.key == pygame.K_DOWN:
                kigyo_y += 20

    # Képernyő törlés
    kepernyo.fill((0, 0, 0))

    pygame.draw.rect(kepernyo, zold, (kigyo_x, kigyo_y, kigyo_meret, kigyo_meret))
    pygame.display.flip()
    ora.tick(60)

pygame.quit() 
