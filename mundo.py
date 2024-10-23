import pygame
import Constantes
from items import Item
from personajes import Personaje

#lista de obstaculos
#paredes
obstaculos=[0,1,2,3,4,10,15,20,25,30,35,40,41,42,43,44,45,50,51,52,53,54,55,66,67,36,37,5]
#puertas
puerta_cerrada=[36,37,66,67]

class Mundo():
    def __init__(self):
        self.map_tiles=[]
        self.obstaculos_tiles=[]
        self.exit_tile=None
        self.lista_item=[]
        self.lista_enemigo=[]
        self.puertas_cerradas_tiles=[]

    def process_data(self, data, tile_list,item_imagenes, animacion_enemigos):
        self.level_length=len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image=tile_list[tile]
                image_rect=image.get_rect()
                image_x=x*Constantes.TILE_SIZE
                image_y=y*Constantes.TILE_SIZE
                image_rect.center=(image_x,image_y)
                tile_data=[image, image_rect, image_x,image_y, tile]
                #Agregar tiles a obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)

                #tiles de puertas
                if tile in puerta_cerrada:
                    self.puertas_cerradas_tiles.append(tile_data)
                #Tile de salida
                elif tile==84:
                    self.exit_tile=tile_data
                #Crear monedas
                elif tile==86:
                    moneda=Item(image_x, image_y, 0,item_imagenes[0])
                    self.lista_item.append(moneda)
                    tile_data[0]=tile_list[12]
                #Crear posiones
                elif tile==89:
                    posion=Item(image_x, image_y, 1,item_imagenes[1])
                    self.lista_item.append(posion)
                    tile_data[0]=tile_list[12]
                #Crear honguito
                elif tile==74:
                    honguito=Personaje(image_x, image_y,animacion_enemigos[1],200,2)
                    self.lista_enemigo.append(honguito)
                    tile_data[0]=tile_list[12]
                elif tile==77:
                    goblin=Personaje(image_x, image_y,animacion_enemigos[0],300,2)
                    self.lista_enemigo.append(goblin)
                    tile_data[0]=tile_list[12]


                self.map_tiles.append(tile_data)
    def cambiar_puerta(self, jugador, tile_list):
        buffer=50
        proximidad_rect=pygame.Rect(jugador.forma.x-buffer, jugador.forma.y-buffer, jugador.forma.width +2*buffer, jugador.forma.height +2*buffer)
        for tile_data in self.map_tiles:
            image, rect, x, y, tile_type=tile_data
            if proximidad_rect.colliderect(rect):
                if tile_type in puerta_cerrada:
                    if tile_type==36 or tile_type==66:
                        new_tile_type=57
                    elif tile_type==37 or tile_type==67:
                        new_tile_type=58

                    tile_data[-1]=new_tile_type
                    tile_data[0]=tile_list[new_tile_type]

                    #Eliminar el tile de la lista de colisiones 
                    if tile_data in self.obstaculos_tiles:
                        self.obstaculos_tiles.remove(tile_data)
                    return True
        return False

    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2]+=posicion_pantalla[0]
            tile[3]+=posicion_pantalla[1]
            tile[1].center=(tile[2],tile[3])

    
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])