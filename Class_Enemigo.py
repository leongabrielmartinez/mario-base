from configuraciones import *


class Enemigo:
    def __init__(self, animaciones, pos_x, pos_y) -> None:#pasar por parametros, para evitar el acoplamiento
        self.animaciones = animaciones
        reescalalar_imagenes(self.animaciones, 50,50)
        self.rectangulo_principal = self.animaciones["Izquierda"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.esta_muerto = False
        self.pasos = 0
        self.animacion_actual = self.animaciones["Izquierda"]
        self.muriendo = False

    def avanzar(self):
        self.rectangulo_principal.x -= 5


    def animar(self, pantalla):        
        largo = len(self.animacion_actual)
        if self.pasos >= largo:
            self.pasos = 0
        pantalla.blit(self.animacion_actual[self.pasos], self.rectangulo_principal)
        self.pasos += 1
        if self.muriendo and self.pasos == largo:
            self.esta_muerto = True
        
        
    def actualizar(self, pantalla):
        if self.esta_muerto == False:
            self.animar(pantalla)
            self.avanzar()
        # elif self.muriendo == True:
        #     self.animacion_actual = self.animaciones["aplasta"]
        
