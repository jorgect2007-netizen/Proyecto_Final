# clases.py
import pyxel


class Personaje:
    def __init__(self, nombre: str, x: int, y: int, sprites: dict, nivel: int, tope_arriba: int, tope_abajo: int,
                 tablero):
        self.nombre = nombre  # "mario" o "luigi"
        self.x = x
        self.y = y
        self.sprites = sprites
        self.nivel = nivel
        self.tope_arriba = tope_arriba
        self.tope_abajo = tope_abajo
        self.tablero = tablero

        # Estado visual
        self.direccion_sprite = "abajo_der"

        # Sistema de animación temporal (acción de levantar/entregar)
        self.timer_animacion = 0
        self.sprite_accion = "arriba"

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero")
        self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La y debe ser un entero")
        self.__y = y

    def mover(self, direccion: str):
        if (direccion.lower() == "arriba" and self.nivel < self.tope_arriba):
            self.y -= 2 * self.tablero.dif_niveles
            self.nivel += 2
            # NOTA: Ya no cambiamos el sprite aquí directamente,
            # se encarga actualizar_sprite()

        elif (direccion.lower() == "abajo" and self.nivel > self.tope_abajo):
            self.y += 2 * self.tablero.dif_niveles
            self.nivel -= 2

    def animar(self, tipo: str):
        """
        Activa una animación breve.
        tipo: 'subir' (coger caja) o 'entregar' (camión)
        """
        self.timer_animacion = 5  # Duración en frames (aprox 0.15s, "microsegundo")

        if tipo == "subir":
            self.sprite_accion = "arriba"
        elif tipo == "entregar":
            if self.nombre == "luigi":
                self.sprite_accion = "abajo_izq"  # Luigi entregando al camión
            else:
                self.sprite_accion = "arriba"  # Mario entregando (si hubiera caso)

    def actualizar_sprite(self):
        """
        Determina qué sprite mostrar en cada frame según prioridad:
        1. Jefe regañando (Triste)
        2. Animación activa (Acción)
        3. Estado de reposo (Según nivel y personaje)
        """
        # 1. PRIORIDAD: JEFE REGAÑANDO
        if self.tablero.pausado_por_jefe:
            self.direccion_sprite = "triste"
            return

        # 2. PRIORIDAD: ANIMACIÓN DE ACCIÓN (Microsegundo al coger/soltar)
        if self.timer_animacion > 0:
            self.direccion_sprite = self.sprite_accion
            self.timer_animacion -= 1
            return

        # 3. PRIORIDAD: ESTADO NATURAL (REPOSO)
        if self.nombre == "mario":
            # Mario: Nivel 0 (Abajo) -> Mira derecha
            #        Niveles superiores -> Mira izquierda
            if self.nivel == 0:
                self.direccion_sprite = "abajo_der"
            else:
                self.direccion_sprite = "abajo_izq"

        elif self.nombre == "luigi":
            # Luigi: Siempre mira a la derecha en reposo en todas las plataformas
            self.direccion_sprite = "abajo_der"


class Camion:
    def __init__(self, x: int, y: int, sprites: dict):
        self.x_inicial = x
        self.x = x
        self.y = y
        self.sprites = sprites
        self.cajas = 0
        self.max_cajas = 8

        # Estado de animación
        self.animacion_salida = False
        self.velocidad_salida = -1
        self.temporizador = 0
        self.tiempo_espera = 3 * 30

    def llenar(self):
        if self.cajas < self.max_cajas:
            self.cajas += 1
            if self.cajas == self.max_cajas:
                self.iniciar_salida()

    def iniciar_salida(self):
        self.animacion_salida = True
        self.temporizador = self.tiempo_espera

    def update(self):
        if self.animacion_salida:
            self.x += self.velocidad_salida
            self.temporizador -= 1
            if self.temporizador <= 0:
                self.reset()

    def reset(self):
        self.cajas = 0
        self.x = self.x_inicial
        self.animacion_salida = False


class Cinta:
    def __init__(self, y, direccion, x_inicio, x_fin):
        self.y = y
        self.direccion = direccion
        self.x_inicio = x_inicio
        self.x_fin = x_fin
        self.limite_in = 500


class Paquete:
    def __init__(self, cinta_id: int, x: int, y: int, sprites: dict, nivel: int):
        self.cinta_id = cinta_id
        self.x = x
        self.y = y
        self.sprites = sprites
        self.fase = 1
        self.contador_anim = 0
        self.nivel = nivel
        self.activo = True
        self.en_borde = False
        self.cayendo = False
        self.velocidad_caida = 3
        self.culpable = None
        self.ha_cruzado = False

    def actualizar_fase(self, centro):
        if not self.ha_cruzado and abs(self.x - centro) <= 2:
            self.fase += 1
            if self.fase > 6:
                self.fase = 1
            self.ha_cruzado = True

    def mover(self, cintas, centro, suelo_y):
        if not self.activo: return

        if self.cayendo:
            self.y += self.velocidad_caida
            if self.y > suelo_y + 50:
                self.activo = False
            return

        idx = self.cinta_id if self.cinta_id < len(cintas) else len(cintas) - 1
        cinta = cintas[idx]

        nueva_x = self.x + (1 * cinta.direccion)

        llegada_fin = False
        if cinta.direccion == -1 and nueva_x <= cinta.x_fin:
            llegada_fin = True
            self.x = cinta.x_fin
        elif cinta.direccion == 1 and nueva_x >= cinta.x_fin:
            llegada_fin = True
            self.x = cinta.x_fin

        if llegada_fin:
            self.en_borde = True
        else:
            self.x = nueva_x
            self.en_borde = False
            self.actualizar_fase(centro)


class Jefe:
    def __init__(self, sprites: dict):
        self.x = 0
        self.y = 0
        self.sprites = sprites
        self.activo = False
        self.objetivo = None
        self.temporizador = 0
        self.duracion_enfado = 3 * 30

    def activar(self, objetivo: str, x: int, y: int):
        self.activo = True
        self.objetivo = objetivo
        self.x = x
        self.y = y
        self.temporizador = self.duracion_enfado

    def update(self):
        if self.activo:
            self.temporizador -= 1
            if self.temporizador <= 0:
                self.activo = False
                self.objetivo = None