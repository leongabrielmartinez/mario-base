"""
Caracterisicas:
rectangulo 
tamaño
velocidad
contador_pasos
que_hace 
superficie

acciones: 
caminar
animar 
actualizar pantalla
"""
from configuraciones import*
from Class_Enemigo import *
import pygame
import time

class Personaje:
    def __init__(self,animaciones, tamaño, pos_x, pos_y, velocidad) -> None:
        self.animaciones = animaciones
        self.tamaño = tamaño
        reescalalar_imagenes(self.animaciones, self.tamaño[0],self.tamaño[1])#*tamaño desempaca la tupla == tamaño[0],tamaño[1] -> tamaño*

        self.rectangulo_principal = self.animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.velocidad = velocidad

        self.que_hace = "Quieto"
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["Quieto"]

        self.desplazamiento_y = 0
        self.potencia_salto = -15#se acerca al cero
        self.limite_velocidad_salto = 15
        self.gravedad = 1
        self.esta_saltando = False

        self.habilidad_especial = False
        self.tiempo_habilidad_especial = 3000 #10 seg
        self.tiempo_anterior = 0



    def actualizar(self, pantalla, piso, plataformas):

        tiempo_actual = pygame.time.get_ticks()#tomo el tiempo actual
        if tiempo_actual > self.tiempo_anterior + self.tiempo_habilidad_especial:
            self.habilidad_especial = False

        accion = ""

        if self.habilidad_especial:
            match self.que_hace:
                case "Derecha":
                    accion = "Super_Derecha"
                case "Izquierda":
                    accion = "Super_Izquierda"
                case "Quieto":
                    accion = "Super_Quieto"
                case "Salta":
                    accion = "Super_Salta"

            self.animacion_actual = self.animaciones[accion]
        else:
            self.animacion_actual = self.animaciones[self.que_hace]


        match self.que_hace:
            case "Derecha":
                if not self.esta_saltando:
                    self.animar(pantalla)
                self.caminar(pantalla)
            case "Izquierda":
                if not self.esta_saltando:
                    self.animar(pantalla)
                self.caminar(pantalla)
            case "Quieto":
                if not self.esta_saltando:
                    self.animar(pantalla)
            case "Salta":
                if not self.esta_saltando:
                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto

        self.aplicar_gravedad(pantalla,piso, plataformas)


    def animar(self, pantalla):        
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1
        

    def caminar(self, pantalla):
        velocidad_actual = self.velocidad
        if self.que_hace == "Izquierda":
            velocidad_actual *= -1
        nueva_x = self.rectangulo_principal.x + velocidad_actual
        if nueva_x >= 0 and nueva_x <= pantalla.get_width()- self.rectangulo_principal.width:
            self.rectangulo_principal.x += velocidad_actual


    def aplicar_gravedad(self, pantalla, piso, plataformas):
        if self.esta_saltando:
            self.animar(pantalla)
            self.rectangulo_principal.y += self.desplazamiento_y
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad
                
        for piso in plataformas:
            if not piso["premio"]:
                if self.rectangulo_principal.colliderect(piso["rectangulo"]):
                    self.desplazamiento_y = 0
                    self.esta_saltando = False
                    self.rectangulo_principal.bottom = piso["rectangulo"].top
                    break
                else:
                    self.esta_saltando = True


    def verificar_colision_enemigo(self, lista_enemigos:list["Enemigo"], pantalla):#lista_enemigos:list["Enemigo"] se typea la var de contx
        for enemigo in lista_enemigos:
            if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
                enemigo.muriendo = True
                enemigo.rectangulo_principal.y += 20

                enemigo.animacion_actual = enemigo.animaciones["aplasta"]
                #se puede trabajar mejor como un setter
                enemigo.animar(pantalla)

    def romper_bloque(self, lista_plataformas, flor):#esto deberia funcionar con los diferente rectangulos nomas
        for plataforma in lista_plataformas:
            if plataforma["premio"]:         
                if self.rectangulo_principal.colliderect(plataforma["rectangulo"]):
                    flor["descubierta"] = True
                    plataforma["premio"] = False

    def verificar_colision_flor(self, flor):
        if flor["descubierta"] == True and self.rectangulo_principal.colliderect(flor["rectangulo"]):
            flor["descubierta"] = False
            flor["tocada"] = True
            self.tiempo_anterior = pygame.time.get_ticks()#toma el tiempo de cuando colisiono con la flor
            self.habilidad_especial = True



