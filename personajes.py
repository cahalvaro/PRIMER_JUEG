import pygame
import Constantes
import math

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
        self.forma=self.image.get_rect()
        self.forma.center=(x,y)
        self.tipo=tipo
        self.golpe=False
        self.ultimo_golpe=pygame.time.get_ticks()
    
    def actualizar_coordenadas(self, tupla):
        self.forma.center=(tupla[0],tupla[1])

    
    def movimiento(self, delta_x, delta_y, obstaculos_tiles,exit_tile):
        posicion_pantalla=[0, 0]
        nivel_completado=False
        if delta_x< 0:
            self.flip=True
        if delta_x > 0:
            self.flip=False

        self.forma.x=self.forma.x + delta_x
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_x>0:
                    self.forma.right=obstacle[1].left
                if delta_x<0:
                    self.forma.left=obstacle[1].right
        
        self.forma.y=self.forma.y + delta_y
        for obstaculo in obstaculos_tiles:
            if obstaculo[1].colliderect(self.forma):
                if delta_y>0:
                    self.forma.bottom=obstaculo[1].top
                if delta_y<0:
                    self.forma.top=obstaculo[1].bottom


        #logica que solo aplica al jugador y no al enemigo
        if self.tipo==1:
            #chequear colision con el tile de salida 
            if exit_tile[1].colliderect(self.forma):
                nivel_completado=True
                print("Nivel Completado")
            #Actualizar la pantalla basado en la posicion del jugador
            #Mover la camara izquierda o derecha
            if self.forma.right>(Constantes.ANCHO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[0]=(Constantes.ANCHO_VENTANA-Constantes.LIMITE_PANTALLA)-self.forma.right
                self.forma.right = Constantes.ANCHO_VENTANA-Constantes.LIMITE_PANTALLA
            if self.forma.left<Constantes.LIMITE_PANTALLA:
                posicion_pantalla[0]=Constantes.LIMITE_PANTALLA-self.forma.left
                self.forma.left=Constantes.LIMITE_PANTALLA
        

            #Mover la camara izquierda o derecha
            if self.forma.bottom>(Constantes.ALTO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[1]=(Constantes.ALTO_VENTANA-Constantes.LIMITE_PANTALLA)-self.forma.bottom
                self.forma.bottom = Constantes.ALTO_VENTANA-Constantes.LIMITE_PANTALLA
            if self.forma.top<Constantes.LIMITE_PANTALLA:
                posicion_pantalla[1]=Constantes.LIMITE_PANTALLA-self.forma.top
                self.forma.top=Constantes.LIMITE_PANTALLA
            return posicion_pantalla, nivel_completado

    def enemigos(self,jugador, obstaculos_tiles, posicion_pantalla, exit_tile):
        ene_dx=0
        ene_dy=0
        #Reposicion de enemigos basado en la posicion de la pantalla o camara
        self.forma.x+=posicion_pantalla[0]
        self.forma.y+=posicion_pantalla[1]

        #Distancia con el jugador
        distancia=math.sqrt(((self.forma.centerx-jugador.forma.centerx)**2)+((self.forma.centery-jugador.forma.centery)**2))

        if distancia < Constantes.RANGO:
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx=-Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx=Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > jugador.forma.centery:
                ene_dy=-Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < jugador.forma.centery:
                ene_dy=Constantes.VELOCIDAD_ENEMIGO
        
        self.movimiento(ene_dx, ene_dy, obstaculos_tiles, exit_tile)     

        #Atacar al jugador 
        if distancia < Constantes.RANGO_ATAQUE and jugador.golpe==False:
            jugador.energia-=10
            jugador.golpe=True
            jugador.ultimo_golpe=pygame.time.get_ticks()
    
    def update(self):
        #Comprobar si el personaje a muerto
        if self.energia<=0:
            self.energia=0
            self.vivo=False
        #tiempo para volver a recibir daño
        golpe_cooldown=1000
        if self.tipo==1:
            if self.golpe==True:
                if pygame.time.get_ticks()-self.ultimo_golpe > golpe_cooldown:
                    self.golpe=False
            
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

    