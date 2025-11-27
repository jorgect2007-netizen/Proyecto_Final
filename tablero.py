from clases import Personaje
from clases import Camion
from clases import Paquete
from clases import Jefe
import pyxel

class Tablero:

    def __init__(self, ancho: int, alto: int):

        self.ancho = ancho
        self.alto = alto

        pyxel.init(self.ancho, self.alto, title="Demo Juego Mario Bros")
        pyxel.run(self.update, self.draw)
        pyxel.load("assets/resources.pyxres")

  self.mario = Personaje(x=None, y=None, sprites= mario_sprites, nivel=0,
                     tope_arriba=2, tope_abajo=0)
        self.luigi = Personaje(x=None, y=None, sprites= luigi_sprites , 
                               nivel=1,
                     tope_arriba=2, tope_abajo=0)

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.mario.mover("arriba")
        if pyxel.btn(pyxel.KEY_DOWN):
            self.mario.mover("abajo")

        if pyxel.btn(pyxel.KEY_W):
            self.luigi.mover("arriba")
        if pyxel.btn(pyxel.KEY_S):
            self.luigi.mover("abajo")

        self.mario.update()
        self.luigi.update()
        pass
        
        def draw(self):
        pyxel.cls(7)
        self.mario.draw()
        self.luigi.draw()

prueba = Tablero(256*2+16, 256)
