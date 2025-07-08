# HÁZI FELADAT: Állítsd be ,hogy a kígyó folyamatosan mozogjon (ne csak a billentyűlenyomásra)
#  és a mozgás irányát a legutolsó nyílbillentyű-esemény határozza meg.

import pygame

pygame.init()

kepernyo = pygame.display.set_mode((1920, 1080))

ora = pygame.time.Clock()

kigyo_meret = 20
kigyo_x = (1920 - kigyo_meret) // 2
kigyo_y = (1080 - kigyo_meret) // 2

# Mozgásirány változók (sebesség pixelben)
sebesseg_x = 20
sebesseg_y = 0

zold = (0, 255, 0)

fut = True

# Játék fő ciklusa
while fut:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fut = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sebesseg_x = -20
                sebesseg_y = 0
            if event.key == pygame.K_RIGHT:
                sebesseg_x = 20
                sebesseg_y = 0
            if event.key == pygame.K_UP:
                sebesseg_x = 0
                sebesseg_y = -20
            if event.key == pygame.K_DOWN:
                sebesseg_x = 0
                sebesseg_y = 20

    kigyo_x += sebesseg_x
    kigyo_y += sebesseg_y

    # Képernyő törlés
    kepernyo.fill((0, 0, 0))

    pygame.draw.rect(kepernyo, zold, (kigyo_x, kigyo_y, kigyo_meret, kigyo_meret))
    pygame.display.flip()
    ora.tick(10)

pygame.quit() 
