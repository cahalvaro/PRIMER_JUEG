import pygame
import Constantes

class Personaje():
    
    def __init__(self,x, y,image):
        self.flip=False
        self.image=image
        self.forma=pygame.Rect(0, 0, Constantes.ANCHO_PERSONAJE, Constantes.ALTO_PERSONAJE)
        self.forma.center=(x,y)
    
    def movimiento(self, delta_x, delta_y):
        if delta_x< 0:
            self.flip=True
        if delta_x > 0:
            self.flip=False
        self.forma.x=self.forma.x + delta_x
        self.forma.y=self.forma.y + delta_y

    def dibujar(self, interfaz):
        image_flip=pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(image_flip, self.forma)
        #pygame.draw.rect(interfaz,Constantes.COLOR_PERSONAJE, self.forma,1)

    