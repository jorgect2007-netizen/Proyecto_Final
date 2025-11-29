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
        self.altura_cinta = 9
        self.margen_arriba = 45
        self.margen_abajo = 45
        espacio_util = self.alto - self.margen_arriba - self.margen_abajo
        self.dif_niveles = espacio_util // (self.num_niveles - 1)
        self.niveles_y = [
            self.margen_arriba + i * self.dif_niveles
            for i in range(self.num_niveles)
        ]
        #Definir personajes
        self.mario = Personaje(x=400, y=self.niveles_y[1], sprites = self.sprites_mario, nivel=0,
                               tope_arriba=4, tope_abajo=0)
        self.luigi = Personaje(x=100, y=self.niveles_y[4]-20, sprites = self.sprites_luigi,
                               nivel=0,
                               tope_arriba=4, tope_abajo=0)

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
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprites["abajo_izq"],0, scale=2.5)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprites["abajo_der"],0, scale=2.5)
        #Pilar que divide la pantalla
        for i in range(16):
            pyxel.blt(self.ancho//2, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho//2 + 16, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho//2 - 16, 0 + i * 16, 0, 0, 80, 16, 16)

        #Dibujos de las cintas
            #Cintas largas a la izquierda
        for y in self.niveles_y:
            if y % 2 == 0:
                pyxel.blt(132, y, 0, 8, 16, 80, 16, 11)
            else:
                pyxel.blt(124, y, 0, 0, 0, 96, 16, 11)


        pyxel.blt(124,0, 0,0, 96, 16, 11)
prueba = Tablero(456, 256)
