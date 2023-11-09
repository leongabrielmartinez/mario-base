import pygame

def reescalalar_imagenes(diccionario_animaciones, ancho, alto):
    for clave in diccionario_animaciones:
        for i in range(len(diccionario_animaciones[clave])):
            img = diccionario_animaciones[clave][i]
            diccionario_animaciones[clave][i] = pygame.transform.scale(img, (ancho, alto))


def rotar_imagen(imagenes:list):
    lista_imagenes = []
    for i in range(len(imagenes)):
        imagen_rotada = pygame.transform.flip(imagenes[i],True,False)
        lista_imagenes.append(imagen_rotada)
    
    return lista_imagenes


personaje_quieto = [pygame.image.load("0.png")]
personaje_camina_derecha = [pygame.image.load("1.png"), pygame.image.load("2.png")]
personaje_salta = [pygame.image.load("3.png")]
personaje_camina_izquierda = rotar_imagen(personaje_camina_derecha)

enemigo_camina = [pygame.image.load("ene1.png"), pygame.image.load("ene2.png")]
enemigo_aplasta = [pygame.image.load("ene3.png")]

flor_fuego = [pygame.image.load("flor.png")]

super_mario_derecha = [pygame.image.load("sm1.png"),pygame.image.load("sm2.png"),pygame.image.load("sm3.png"),pygame.image.load("sm4.png")]

super_mario_izquierda  = rotar_imagen(super_mario_derecha)

super_mario_quieto = [pygame.image.load("smQuieto.png")]

super_mario_salta = [pygame.image.load("smSalta.png")]

