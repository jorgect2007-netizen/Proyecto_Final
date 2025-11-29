from clases import Personaje
from clases import Camion
from clases import Paquete
from clases import Jefe
import pyxel

class Tablero:

    sprites_mario = {
        'abajo_izq':(2,0,48,16,16),
        'abajo_der':(2,0,32,16,16),
        'arriba':(2,0,96,16,16),
        'triste':(2,0,64,16,16)
    }

    sprites_luigi = {
        'abajo_izq':(2,16,48,16,16),
        'abajo_der': (2, 16, 32, 16, 16),
        'arriba': (2, 16, 96, 16, 16),
        'triste': (2, 16, 80, 16, 16)
    }
    def __init__(self, ancho: int, alto: int):

        self.ancho = ancho
        self.alto = alto

        #Definir altura de las cintas
        self.num_niveles = 5
        self.altura_cinta = 16
        self.margen_arriba = 45
        self.margen_abajo = 45
        espacio_util = self.alto - self.margen_arriba - self.margen_abajo
        self.dif_niveles = espacio_util // (self.num_niveles - 1)
        self.niveles_y = [
            self.margen_arriba + i * self.dif_niveles
            for i in range(self.num_niveles)
        ]
        #Zona de mario
        self.zona_mario=self.ancho
        #Definir personajes
        self.mario = Personaje(x=390, y=self.niveles_y[4]+13, sprites = self.sprites_mario, nivel=0,
                               tope_arriba=4, tope_abajo=0, tablero=self)
        self.luigi = Personaje(x= 124, y=self.niveles_y[4]-28, sprites = self.sprites_luigi,
                               nivel=0, tope_arriba=4, tope_abajo=0, tablero=self)

        pyxel.init(self.ancho, self.alto, title="Demo Juego Mario Bros")
        pyxel.load("assets/resources.pyxres")
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover("arriba")
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover("abajo")

        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover("arriba")
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover("abajo")

    def draw(self):
        pyxel.cls(7)
        #Escaleras
        pyxel.blt(self.mario.x, self.niveles_y[4]-25,0,0,56, 16,16,0,scale=2)
        pyxel.blt(self.mario.x, self.niveles_y[2]-25,0,0,56, 16,16,0,scale=2)
        pyxel.blt(self.luigi.x, self.niveles_y[3] - 25, 0, 0, 56, 16, 16, 0, scale=2)
        pyxel.blt(self.luigi.x, self.niveles_y[1] - 25, 0, 0, 56, 16, 16, 0, scale=2)
        #Mario y Luigi
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprites["abajo_der"],0, scale=3)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprites["abajo_der"],0, scale=3)
        #Pilar que divide la pantalla
        for i in range(16):
            pyxel.blt(self.ancho//2, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho//2 + 16, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho//2 - 16, 0 + i * 16, 0, 0, 80, 16, 16)

        #Cintas a la izquierda
        for y in self.niveles_y:
            #Cintas cortas
            if y % 2 == 0:
                pyxel.blt(160, y, 0, 8, 16, 80, 16, 11)
            #Cintas largas
            else:
                pyxel.blt(152, y, 0, 0, 0, 96, 16, 11)

        #Cintas a la derecha
        for y in self.niveles_y:
            if y % 2 == 0:
                pyxel.blt(280, y, 0, 0, 0, -96, 16, 11)
            else:
                pyxel.blt(288, y, 0, 8, 16, -80, 16, 11)

        #Cinta de la que salen las cajas
        pyxel.blt(424,self.niveles_y[4]+17,0,0, 0, 96, 16, 11)

        #Plataformas luigi
        pyxel.blt(self.luigi.x - 90,self.niveles_y[4]+9,0,0,104, 90,9,0,scale = 2)
        pyxel.blt(self.luigi.x - 30, self.niveles_y[2] + 9, 0, 0, 104, 35, 9, 0, scale=2)
        pyxel.blt(self.luigi.x - 30, self.niveles_y[0] + 9, 0, 0, 104, 35, 9, 0, scale=2)
        #Plataformas mario
        pyxel.blt(self.mario.x + 5,  self.niveles_y[4]+49, 0, 0, 104, 35, 9, 0, scale=2)
        pyxel.blt(self.mario.x + 23,  self.niveles_y[3]+9, 0, 0, 104, 72, 9, 0, scale=2)
        pyxel.blt(self.mario.x + 5,  self.niveles_y[1]+9, 0, 0, 104, 35, 9, 0, scale=2)

        #Zona del camión
        pyxel.blt(71,57,0,112,0,4,17,0,scale=2)
        pyxel.blt(0, 79, 0, 0, 104, 50, 9, 0, scale=2)
        pyxel.blt(18,40,1, 16,0,32,24, 0,scale=2)
prueba = Tablero(512, 256)
