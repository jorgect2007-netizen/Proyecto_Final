#Esta clase hará referencia a los personajes Mario y Luigi
class Personaje:
    #Aqui definiremos los atributos de posición los sprites el nivel en el que se encuentran y los límites a los que
    #pueden llegar
    def __init__(self, x: int, y: int, sprites: dict, nivel: int, tope_arriba: int, tope_abajo: int, tablero):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.nivel = nivel
        self.tope_arriba = tope_arriba
        self.tope_abajo = tope_abajo
        self.tablero = tablero

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número positivo")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError ("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y debe ser un número positivo")
        else:
            self.__y = y


#Este método define el movimiento que van a tener los personajes, el cual solo les permitirá cambiar de nivel
    def mover(self, direccion: str):
       if (direccion.lower() == "arriba" and self.nivel < self.tope_arriba):
           self.y -= 2*self.tablero.dif_niveles
           self.nivel += 2
       elif (direccion.lower() == "abajo" and self.nivel > self.tope_abajo):
           self.y += 2*self.tablero.dif_niveles
           self.nivel -= 2


class Camion:
    # Aqui definiremos los atributos de posición los sprites y el número de cajas que tiene el camión
    def __init__(self, x: int, y: int, sprites: tuple, cajas_camion: int, esperando: bool):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.cajas_camion = cajas_camion
        self.esperando = True

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número positivo")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y debe ser un número positivo")
        else:
            self.__y = y


class Paquete:
    def __init__(self, x: int, y: int, sprites: dict, nivel: int, tablero, fase):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.nivel = nivel
        self.tablero = tablero
        self.fase = fase

        self.direccion = "izquierda"
        self.sprite_actual = "fase1"
        self.velocidad = 1

class Cinta:



    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número positivo")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y debe ser un número positivo")
        else:
            self.__y = y

    def movimiento_inicial(self, lado_mario: bool):
        self.x -= self.velocidad


    def mover(self):
        if self.direccion == "izquierda":
            self.x -= self.velocidad
            self.cambio_nivel()
        else:
            self.x += self.velocidad
            self.cambio_nivel()


    def cambio_nivel(self):
        if self.x == self.tablero.limite_in:
            if self.tablero.mario.nivel == self.nivel:
                self.y -= self.tablero.niveles_y[self.nivel] - 10
                self.x = self.tablero.limite_der
                self.nivel += 1
            else:
                self.caer()

        elif self.x <= self.tablero.limite_izq:
            if self.tablero.luigi.nivel == self.nivel:
                self.nivel += 1
                self.y -= self.tablero.niveles_y[self.nivel] - 45
                self.cambiar_sprite()
                self.direccion = "derecha"
            else:
                self.caer()


        elif self.x >= self.tablero.limite_der:
            if self.tablero.mario.nivel == self.nivel:
                self.y -= self.tablero.niveles_y[self.nivel]-45
                self.nivel += 1
                self.cambiar_sprite()
                self.direccion = "derecha"
            else:
                self.caer()

    def cambiar_sprite(self):
        if self.fase == 0 and self.x == self.tablero.centro:
            self.sprite_actual = "fase2"
            self.fase = 1
        elif self.fase == 1 and self.x == self.tablero.centro:
            self.sprite_actual = "fase3"
            self.fase = 2
        elif self.fase == 2 and self.x == self.tablero.centro:
            self.sprite_actual = "fase4"
            self.fase = 3
        elif self.fase == 3 and self.x == self.tablero.centro:
            self.sprite_actual = "fase5"
            self.fase = 4
        elif self.fase == 4 and self.x == self.tablero.centro:
            self.sprite_actual = "fase6"
            self.fase = 5

    def caer(self):
        self.y = self.tablero.alto



class Jefe:
    def __init__(self, x: int, y: int, sprites: tuple, enfadado: bool):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.enfadado = False

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número positivo")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y debe ser un número positivo")
        else:
            self.__y = y