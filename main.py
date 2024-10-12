import pygame
import Constantes
from personajes import Personaje
from weapon import Weapon
import os

#Funciones 
#Escalar imagenes 
def escalar_img(image, scale):
    w=image.get_width()
    h=image.get_height()
    nueva_imagen=pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

#Funcion para contar elementos 
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#Funcion listar nombres elementos 
def nombre_carpetas(directorio):
    return os.listdir(directorio)



pygame.init()
ventana=pygame.display.set_mode((Constantes.ANCHO_VENTANA,Constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi primer juego")



#importar imagenes 

#personaje

animaciones=[]
for i in range (7):
    img=pygame.image.load(f"assets//images//characters//player//Player_{i}.png").convert_alpha()
    img =escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos 
directorio_enemigos="assets\images\characters\enemies"
tipo_enemigos=nombre_carpetas(directorio_enemigos)
animacion_enemigos=[]
for eni in tipo_enemigos:
    lista_temp=[]
    ruta_temp=f"assets\images\characters\enemies\{eni}"
    num_animaciones=contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo=pygame.image.load(f"{ruta_temp}\{eni}_{i}.png").convert_alpha()
        img_enemigo=escalar_img(img_enemigo, Constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animacion_enemigos.append(lista_temp)

#Arma
imagen_pistola=pygame.image.load(f"assets//images//weapons//gun.png").convert_alpha()
imagen_pistola=escalar_img(imagen_pistola, Constantes.SCALA_ARMA)

#Balas
imagen_balas=pygame.image.load(f"assets//images//weapons//bullet.png").convert_alpha()
imagen_balas=escalar_img(imagen_balas, Constantes.SCALA_ARMA)


#crear un jugador de la clase personaje
jugador=Personaje(50,50,animaciones,100)

#crear un enemigo de la calse personaje
goblin=Personaje(400, 300, animacion_enemigos[0],100)
honguito=Personaje(200, 200, animacion_enemigos[1],100)
goblin_2=Personaje(100, 250, animacion_enemigos[0],100)
honguito_2=Personaje(350, 350, animacion_enemigos[1],100)

#Crear una lista de enemigos
lista_enemigos=[]
lista_enemigos.append(goblin)
lista_enemigos.append(goblin_2)
lista_enemigos.append(honguito)
lista_enemigos.append(honguito_2)

#Crear un arma de la clase weapon
pistola=Weapon(imagen_pistola, imagen_balas)

#Crear un grupo de sprites
grupo_balas=pygame.sprite.Group()

#Definir las variables del movimiento del juego
mover_arriba=False
mover_abajo=False
mover_izquierda=False
mover_derecha=False

#Controlar el frame rate
reloj=pygame.time.Clock()

run=True
while run==True:
    #Que vaya a 60 fps
    reloj.tick(Constantes.FPS)

    ventana.fill(Constantes.COLOR_BG)

    #Calcular el movimiento del jugador
    delta_x=0
    delta_y=0

    if mover_derecha==True:
        delta_x=Constantes.VELOCIDAD

    if mover_izquierda==True:
        delta_x=-Constantes.VELOCIDAD
    
    if mover_arriba==True:
        delta_y=-Constantes.VELOCIDAD

    if mover_abajo==True:
        delta_y=Constantes.VELOCIDAD
    
    #Mover al jugador
    jugador.movimiento(delta_x, delta_y)
    
    #Actualiza estado del jugador 
    jugador.update()

    #Actualiza estado del enemigo
    for ene in lista_enemigos:
        ene.update()


    #Actualiza el estado del arma
    bala=pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)

    for bala in grupo_balas:
        bala.update(lista_enemigos)


    #Dibujar al jugador
    jugador.dibujar(ventana)

    #Dibujar enemigo
    for ene in lista_enemigos:
        ene.dibujar(ventana)

    #dibujar el arma
    pistola.dibujar(ventana)

    #dibujar balas

    for bala in grupo_balas:
        bala.dibujar(ventana)

    for event in pygame.event.get():
        #Para cerrar el juego
        if event.type==pygame.QUIT:
            run=False
    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                mover_izquierda=True
            if event.key==pygame.K_d:
                mover_derecha=True
            if event.key==pygame.K_w:
                mover_arriba=True
            if event.key==pygame.K_s:
                mover_abajo=True

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                mover_izquierda=False
            if event.key==pygame.K_d:
                mover_derecha=False
            if event.key==pygame.K_w:
                mover_arriba=False
            if event.key==pygame.K_s:
                mover_abajo=False

    pygame.display.update()

pygame.quit()
