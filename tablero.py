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
        'triste': (2, 16, 64, 16, 16)
    }
    def __init__(self, ancho: int, alto: int):

        self.ancho = ancho
        self.alto = alto
        self.mario = Personaje(x=20, y=20, sprites = self.sprites_mario, nivel=0,
                               tope_arriba=2, tope_abajo=0)
        self.luigi = Personaje(x=40, y=40, sprites = self.sprites_luigi,
                               nivel=1,
                               tope_arriba=2, tope_abajo=0)

        pyxel.init(self.ancho, self.alto, title="Demo Juego Mario Bros")
        pyxel.run(self.update, self.draw)
        pyxel.load("assets/resources.pyxres")

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

prueba = Tablero(256*2+16, 256)
