import pygame
import Constantes

class Personaje():
    
    def __init__(self,x, y,animaciones, energia):
        self.score=0
        self.energia=energia
        self.vivo=True
        self.flip=False
        self.animaciones=animaciones
        #imagen de la animacion que se esta mostrando actualmente
        self.frame_index=0
        #Aqui se almacena la hora acutual (en milisegundos desde que se inicio pygame)
        self.update_time=pygame.time.get_ticks()
        self.image=animaciones[self.frame_index]
        self.forma=self.forma=self.image.get_rect()
        self.forma.center=(x,y)
    
    def movimiento(self, delta_x, delta_y):
        if delta_x< 0:
            self.flip=True
        if delta_x > 0:
            self.flip=False
            
        self.forma.x=self.forma.x + delta_x
        self.forma.y=self.forma.y + delta_y
    
    def update(self):
        #Comprobar si el personaje a muerto
        if self.energia<=0:
            self.energia=0
            self.vivo=False
            
        cooldown_animacion=100
        self.image=self.animaciones[self.frame_index]
        if pygame.time.get_ticks()-self.update_time >= cooldown_animacion:
            self.frame_index=self.frame_index + 1
            self.update_time=pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animaciones):
            self.frame_index=0

    def dibujar(self, interfaz):
        image_flip=pygame.transform.flip(self.image, self.flip,False)
        interfaz.blit(image_flip, self.forma)
        #pygame.draw.rect(interfaz,Constantes.COLOR_PERSONAJE, self.forma,1)

    