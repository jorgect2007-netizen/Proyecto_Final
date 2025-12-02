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

class Cinta:
    def __init__(self, y, direccion, x_inicio, x_fin):
        self.y = y
        self.direccion = direccion
        self.x_inicio = x_inicio
        self.x_fin = x_fin

class Paquete:
    def __init__(self, cinta_id: int, x:int,y:int, sprites: dict, nivel: int):
        self.cinta_id = cinta_id   # en qué cinta está (0–4)
        self.x = x
        self.y = y
        self.sprites = sprites
        self.fase = 1
        self.contador_anim = 0
        self.nivel = nivel

    # -------------- ANIMACIÓN AL PASAR POR EL CENTRO --------------
    def actualizar_fase(self, centro):
        # si pasa por el centro:
        if abs(self.x - centro) < 2:
            self.fase += 1

    # -------------- MOVIMIENTO --------------
    def mover(self, cintas, centro):
        cinta = cintas[self.cinta_id]

        # mover horizontalmente
        self.x += 1 * cinta.direccion

        # actualizar animación
        self.actualizar_fase(centro)

        # si la caja llegó al final de la cinta → subir a la siguiente
        if cinta.direccion == -1 and self.x <= cinta.x_fin:
            self.cinta_id += 1  # sube a la cinta siguiente

        elif cinta.direccion == 1 and self.x >= cinta.x_fin:
            self.cinta_id += 1  # sube



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