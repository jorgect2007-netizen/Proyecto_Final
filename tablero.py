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

    def update(self):

        pass

    def draw(self):
        pyxel.cls(7)

prueba = Tablero(256*2+16, 256)
