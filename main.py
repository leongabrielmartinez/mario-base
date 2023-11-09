import pygame
from pygame.locals import *
from configuraciones import *
from Class_Personaje import *
from modo import *
from Class_Enemigo import *

def crear_plataforma(visible,esPremio, tamaño,x, y, path="", ):
    plataforma = {}
    if visible:
        plataforma["superficie"] = pygame.image.load(path)
        print(plataforma["superficie"] )
        plataforma["superficie"] = pygame.transform.scale(plataforma["superficie"],tamaño)
    else:
        plataforma["superficie"] = pygame.Surface(tamaño)
    plataforma["rectangulo"] = plataforma["superficie"].get_rect()
    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y
    plataforma["premio"] = esPremio
    
    return plataforma


#CONFIGURACIONES GENERICAS
W, H = 1000, 800
FPS = 18


#FONDO
fondo = pygame.image.load("fondo.jpg")
fondo = pygame.transform.scale(fondo, (W, H))


#ANIMACIONES
diccionario_animaciones = {}
diccionario_animaciones["Quieto"] = personaje_quieto
diccionario_animaciones["Derecha"] = personaje_camina_derecha
diccionario_animaciones["Izquierda"] = personaje_camina_izquierda
diccionario_animaciones["Salta"] = personaje_salta

diccionario_animaciones["Super_Derecha"] = super_mario_derecha
diccionario_animaciones["Super_Izquierda"] = super_mario_izquierda
diccionario_animaciones["Super_Quieto"] = super_mario_quieto
diccionario_animaciones["Super_Salta"] = super_mario_salta


#PLATAFORMAS 
piso = crear_plataforma(False,False, (W,5), 0,733)#reposisionar
plataforma_caño = crear_plataforma(True,False, (125,125), 250,608, "Caño(2).png")
plataforma_invisible = crear_plataforma(False,False, (200,195), 735,542,"")
plataforma_premio = crear_plataforma(False,True, (53,53),550,485, "")

plataformas = [piso, plataforma_caño,plataforma_invisible, plataforma_premio]


#MARIO
mario = Personaje(diccionario_animaciones, (75,100), 0,500, 5) 
mario.rectangulo_principal.bottom = piso["rectangulo"].y #UBICAR A MARIO SOBRE EL PISO


#ENEMIGOS
diccionario_animaciones = {"Izquierda":enemigo_camina, "aplasta":enemigo_aplasta}
enemigo_uno = Enemigo(diccionario_animaciones, 500, (piso["rectangulo"].y - 50))
enemigo_dos = Enemigo(diccionario_animaciones, 1000, (piso["rectangulo"].y - 50))


d = {"aplasta":diccionario_animaciones["aplasta"]}
reescalalar_imagenes(d,50,20)
lista_enemigos = [enemigo_uno, enemigo_dos]


#FLOR
#TAREA AGREGAR ESTE COMPORTAMIENTO A UNA CLASE QUE SEA UNA CLASE QUE SEA PARA CREACION DE OBJETOS
flor = {}
flor["superficie"] = flor_fuego[0]
flor["superficie"] = pygame.transform.scale(flor["superficie"], (50,50))
flor["rectangulo"] = flor["superficie"].get_rect()
#UBICAR LA FLOR
flor["rectangulo"].midbottom = plataforma_premio["rectangulo"].midtop
flor["descubierta"] = False
flor["tocada"] = False





#PYGAME
pygame.init()
RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((W, H))
bandera = True


while bandera:
    RELOJ.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            bandera = False
        elif evento.type == MOUSEBUTTONDOWN:#PRINTEAR LA UBICACION DEL CLIKEO EN PANTALLA
            print(evento.pos)
        elif evento.type == KEYDOWN:
            if evento.key == K_TAB:
                cambiar_modo()
    
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        mario.que_hace = "Derecha"
    elif teclas[pygame.K_LEFT]:
        mario.que_hace = "Izquierda"
    elif(teclas[pygame.K_SPACE]):
        mario.que_hace = "Salta"
    else:
        mario.que_hace  = "Quieto"


    PANTALLA.blit(fondo, (0, 0))
    PANTALLA.blit(plataforma_caño["superficie"], plataforma_caño["rectangulo"])


    mario.romper_bloque(plataformas, flor)
    if flor["descubierta"] == True and flor["tocada"] == False:
        PANTALLA.blit(flor["superficie"], flor["rectangulo"])#la flor deberia tener su propio update


    enemigo_uno.actualizar(PANTALLA)
    enemigo_dos.actualizar(PANTALLA)


    mario.verificar_colision_flor(flor)
    mario.verificar_colision_enemigo(lista_enemigos, PANTALLA)

    for i in range(len(lista_enemigos)):#en ciertos casos se recorre asi porque el for es de solo lectura 
        if lista_enemigos[i].esta_muerto:
            del lista_enemigos[i]
            break#para no leer el elemento faltante y evitar que rompa


    mario.actualizar(PANTALLA,piso, plataformas)

    if obtener_modo():
        pygame.draw.rect(PANTALLA, "blue", mario.rectangulo_principal, 3)
        for plataforma in plataformas:
            pygame.draw.rect(PANTALLA, "red", plataforma["rectangulo"], 5)
            

    pygame.display.update()


