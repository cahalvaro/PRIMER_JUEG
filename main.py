import pygame
import Constantes
from personajes import Personaje
from weapon import Weapon
from textos import DamageText
from items import Item
from mundo import Mundo
import os
import csv

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

#Variables 
posicion_pantalla=[0, 0]
nivel=1

#fuentes
font=pygame.font.Font("assets//fonts//mago3.ttf", 25)



#importar imagenes
 
#Energia
corazon_vacio=pygame.image.load("assets//images//items//heart_empty.png").convert_alpha()
corazon_vacio=escalar_img(corazon_vacio, Constantes.SCALA_CORAZON)
corazon_mitad=pygame.image.load("assets//images//items//heart_half.png").convert_alpha()
corazon_mitad=escalar_img(corazon_mitad, Constantes.SCALA_CORAZON)
corazon_lleno=pygame.image.load("assets//images//items//heart_full.png").convert_alpha()
corazon_lleno=escalar_img(corazon_lleno, Constantes.SCALA_CORAZON)


#personaje

animaciones=[]
for i in range (7):
    img=pygame.image.load(f"assets//images//characters//player//Player_{i}.png").convert_alpha()
    img =escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos 
directorio_enemigos="assets//images//characters//enemies"
tipo_enemigos=nombre_carpetas(directorio_enemigos)
animacion_enemigos=[]
for eni in tipo_enemigos:
    lista_temp=[]
    ruta_temp=f"assets//images//characters//enemies//{eni}"
    num_animaciones=contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo=pygame.image.load(f"{ruta_temp}//{eni}_{i}.png").convert_alpha()
        img_enemigo=escalar_img(img_enemigo, Constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animacion_enemigos.append(lista_temp)

#Arma
imagen_pistola=pygame.image.load(f"assets//images//weapons//gun.png").convert_alpha()
imagen_pistola=escalar_img(imagen_pistola, Constantes.SCALA_ARMA)

#Balas
imagen_balas=pygame.image.load(f"assets//images//weapons//bullet.png").convert_alpha()
imagen_balas=escalar_img(imagen_balas, Constantes.SCALA_ARMA)

#Cargar imagenes del mundo
tile_list = []
for x in range(Constantes.TILE_TYPES):
    tile_image=pygame.image.load(f"assets//images//tiles//tile ({x+1}).png")
    tile_image=pygame.transform.scale(tile_image, (Constantes.TILE_SIZE, Constantes.TILE_SIZE))
    tile_list.append(tile_image)

#Cargar imagenes de los items
posion_roja=pygame.image.load("assets//images//items//potion.png")
posion_roja=escalar_img(posion_roja, 0.035)

coin_images=[]
ruta_img="assets//images//items//coin"
num_coin_images=contar_elementos(ruta_img)
for i in range(num_coin_images):
    img=pygame.image.load(f"assets//images//items//coin//coin_{i+1}.png")
    img=escalar_img(img, 0.03)
    coin_images.append(img)

item_imagenes=[coin_images, [posion_roja]]

def dibujar_texto(texto, fuente, color, x, y):
    img=fuente.render(texto, True, color)
    ventana.blit(img, (x,y))

def vida_jugador():
    c_mitad_dibujado=False
    for i in range(5):
        if jugador.energia>=((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 20 > 0 and c_mitad_dibujado==False:
            ventana.blit(corazon_mitad, (5+i*50, 5))
            c_mitad_dibujado=True
        else:
            ventana.blit(corazon_vacio, (5+i*50, 5))

world_data=[]


for fila in range(Constantes.FILAS):
    filas=[5]*Constantes.COLUMNAS
    world_data.append(filas)

#Cargar el archivo con el nivel
with open("niveles//nivel_test.csv", newline='') as csvfile:
    reader=csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y]=int(columna)

world=Mundo()
world.process_data(world_data,tile_list, item_imagenes, animacion_enemigos)


def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, Constantes.BLANCO, (x*Constantes.TILE_SIZE,0), (x*Constantes.TILE_SIZE, Constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, Constantes.BLANCO, (0, x*Constantes.TILE_SIZE), (Constantes.ANCHO_VENTANA,x*Constantes.TILE_SIZE))



#crear un jugador de la clase personaje
jugador=Personaje(50,60,animaciones,20,1)

#Crear una lista de enemigos
lista_enemigos=[]
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#Crear un arma de la clase weapon
pistola=Weapon(imagen_pistola, imagen_balas)

#Crear un grupo de sprites
grupo_damage_text=pygame.sprite.Group()
grupo_balas=pygame.sprite.Group()
grupo_items=pygame.sprite.Group()

#añadir items desde la data del nivel
for item in world.lista_item:
    grupo_items.add(item)


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


    dibujar_grid()

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
    posicion_pantalla=jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles)

    #Actualizar el mapa
    world.update(posicion_pantalla)
    
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
        damage, pos_damage=bala.update(lista_enemigos)
        if damage:
            damage_text=DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, Constantes.ROJO)
            grupo_damage_text.add(damage_text)

    #Actualiza el daño
    grupo_damage_text.update(posicion_pantalla)

    #Actualizar items
    grupo_items.update(posicion_pantalla, jugador)


    #dibujar mundo
    world.draw(ventana)


    #Dibujar al jugador
    jugador.dibujar(ventana)

    #Dibujar enemigo
    for ene in lista_enemigos:
        ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla)
        ene.dibujar(ventana)

    #dibujar el arma
    pistola.dibujar(ventana)

    #dibujar balas

    for bala in grupo_balas:
        bala.dibujar(ventana)

    #dibujar los corazones 
    vida_jugador()

    #dibujar textos
    grupo_damage_text.draw(ventana)
    dibujar_texto(f"Score: {jugador.score}", font, (255,255,0), 700, 5)
    #nivel
    dibujar_texto(f"Nivel:"+str(nivel), font, Constantes.BLANCO,Constantes.ANCHO_VENTANA/2, 5)
    #dibujar items
    grupo_items.draw(ventana)

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
