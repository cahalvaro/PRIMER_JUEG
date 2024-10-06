import pygame
import Constantes
from personajes import Personaje

jugador=Personaje(50,50)

pygame.init()

ventana=pygame.display.set_mode((Constantes.ANCHO_VENTANA,Constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi primer juego")
run=True
while run==True:
    jugador.dibujar(ventana)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()

pygame.quit()
