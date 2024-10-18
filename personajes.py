import pygame
import Constantes

class Personaje():
    
    def __init__(self,x, y,animaciones, energia,tipo):
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
        self.tipo=tipo

    
    def movimiento(self, delta_x, delta_y):
        posicion_pantalla=[0, 0]
        if delta_x< 0:
            self.flip=True
        if delta_x > 0:
            self.flip=False
            
        self.forma.x=self.forma.x + delta_x
        self.forma.y=self.forma.y + delta_y

        #logica que solo aplica al jugador y no al enemigo
        if self.tipo==1:
            #Actualizar la pantalla basado en la posicion del jugador
            #Mover la camara izquierda o derecha
            if self.forma.right>(Constantes.ANCHO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[0]=(Constantes.ANCHO_VENTANA-Constantes.LIMITE_PANTALLA)-self.forma.right
                self.forma.right = Constantes.ANCHO_VENTANA-Constantes.LIMITE_PANTALLA
            if self.forma.left<Constantes.LIMITE_PANTALLA:
                posicion_pantalla[0]=Constantes.LIMITE_PANTALLA-self.forma.right
                self.forma.left=Constantes.LIMITE_PANTALLA
        

            #Mover la camara izquierda o derecha
            if self.forma.bottom>(Constantes.ALTO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[1]=(Constantes.ALTO_VENTANA-Constantes.LIMITE_PANTALLA)-self.forma.bottom
                self.forma.bottom = Constantes.ALTO_VENTANA-Constantes.LIMITE_PANTALLA
            if self.forma.top<Constantes.LIMITE_PANTALLA:
                posicion_pantalla[1]=Constantes.LIMITE_PANTALLA-self.forma.top
                self.forma.top=Constantes.LIMITE_PANTALLA
            return posicion_pantalla

    def enemigos(self, posicion_pantalla):
        #Reposicion de enemigos basado en la posicion de la pantalla o camara
        self.forma.x+=posicion_pantalla[0]
        self.forma.y+=posicion_pantalla[1]      
    
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

    