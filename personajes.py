import pygame
import Constantes

class Personaje():
    
    def __init__(self,x, y):
        self.forma=pygame.Rect(0, 0, Constantes.ANCHO_PERSONAJE, Constantes.ALTO_PERSONAJE)
        self.forma.center=(x,y)

    def dibujar(self, interfaz):
        pygame.draw.rect(interfaz,Constantes.COLOR_PERSONAJE, self.forma)