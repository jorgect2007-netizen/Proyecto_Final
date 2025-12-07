#Con esta clase definiremos a Mario y a Luigi
class Personaje:
    def __init__(self, nombre: str, x: int, y: int, sprites: dict, nivel: int, tope_arriba: int, tope_abajo: int,
                 tablero):
        self.nombre = nombre
        #Donde aparece el personaje
        self.x = x
        self.y = y
        self.sprites = sprites #Sus posibles sprites
        self.nivel = nivel #Nivel en el que aparece
        #Nivel máximo y mínimo al que puede acceder
        self.tope_arriba = tope_arriba
        self.tope_abajo = tope_abajo
        #Implementamos el tablero para que el personaje tenga conocimiento del elemento del escenario
        self.tablero = tablero
        #Sprite con el que vemos al personaje
        self.sprite_actual = "abajo_der"

        #Valor inicial para el tiempo que va a estar durante otro sprite el personaje para las animaciones
        self.tiempo_animacion = 0

    #Definimos el movimiento de los personajes para que no puedan moverse más alla del tope que tienen por arriba y
    #por abajo
    def mover(self, direccion: str):
        if direccion.lower() == "arriba" and self.nivel < self.tope_arriba:
            #Si el jugador mueve arriba el personaje se mueve 2 niveles que es lo que le corresponde
            self.y -= 2 * self.tablero.dif_niveles
            self.nivel += 2


        elif direccion.lower() == "abajo" and self.nivel > self.tope_abajo:
            #Si el jugador mueve abajo el personaje se mueve 2 niveles que es lo que le corresponde
            self.y += 2 * self.tablero.dif_niveles
            self.nivel -= 2

    def animar(self, tipo: str):
        #Esta función cambia el sprite durante el tiempo que indiquemos cuando el personaje tenga que cambiar los
        #paquetes de cinta o cuando Luigi entregue las cajas en el paquete
        self.tiempo_animacion = 5  #Serían 5 frames que son 0.15 segundos más o menos
        #Si sube la caja se pone el sprite llamado "arriba"
        if tipo == "subir":
            self.sprite_actual = "arriba"
        #Si Luigi entrega el paquete se pone el sprite llamado "abajo_izq"
        elif tipo == "entregar":
            self.sprite_actual = "abajo_izq"

    def actualizar_sprite(self):
    #Se actualiza el sprite del personaje dependiendo de la situación
        if self.tablero.pausado_por_jefe:
        #Si se ha caido una caja y aparece el jefe el personaje tiene que tener el sprite "triste"
            self.sprite_actual = "triste"
            return

        #Usamos esta función para que cuando se haga una animación se pueda ver bien como se cambia de sprite
        if self.tiempo_animacion > 0:
            self.tiempo_animacion -= 1
            return

        #Usamos esto para que cuando Mario y Luigi estén en reposo en sus respectivas plataformas usen los sprites
        #correspondientes
        if self.nombre == "mario":
        #Si Mario está en la plataforma 0 tiene el sprite "abajo_der" para coger las cajas de la derecha y si no el
        #sprite "abajo_izq" para que coja las cajas de las cintas de su izquierda
            if self.nivel == 0:
                self.sprite_actual = "abajo_der"
            else:
                self.sprite_actual = "abajo_izq"

        elif self.nombre == "luigi":
        #A luigi esto no le hace falta porque siempre coge las cajas de la derecha
            self.sprite_actual = "abajo_der"

#Aquí definimos la clase camión
class Camion:
    def __init__(self, x: int, y: int, sprites: dict):
        self.x_inicial = x #En que x aparece el camion
        #Donde aparece el camión
        self.x = x
        self.y = y
        self.sprites = sprites  #Sus posibles sprites
        #Cantidad de cajas con las que el camión empieza y la máxima
        self.cajas = 0
        self.max_cajas = 8

        #Estado de la animación (que pase de estar en reposo a estar en reparto)
        self.animacion_salida = False
        self.velocidad_salida = -1
        self.temporizador = 0
        self.tiempo_espera = 3 * 30

    #Este método se usa para que se le vayan sumando cajas al camión conforme se las vayan entregando y que
    #cuando el camión este lleno empiece la animación de que está en reparto
    def llenar(self):
        if self.cajas < self.max_cajas:
            self.cajas += 1
            if self.cajas == self.max_cajas:
                self.iniciar_salida()
    #Cuando el camión está lleno se activa este método en el que el mapa se queda congelado durante el tiempo de espera
    #antes definido
    def iniciar_salida(self):
        self.animacion_salida = True
        self.temporizador = self.tiempo_espera

    #Aquí definimos el movimiento del camión cuando esté en reparto
    def update(self):
        if self.animacion_salida:
            self.x += self.velocidad_salida
            self.temporizador -= 1 #Para que cuando llegue a 0 el camión vuelva a la posición inicial
            if self.temporizador <= 0:
                self.reset()

    #Este método hace que cuando el camión termine de repartir vuelva a su posición inicial
    def reset(self):
        self.cajas = 0
        self.x = self.x_inicial
        self.animacion_salida = False

#Aquí definiremos las cintas del juego
class Cinta:
    def __init__(self, y, direccion, x_inicio, x_fin):
        self.y = y #La altura de las cintas
        self.direccion = direccion #Hacia donde se mueven
        #Donde empieza la cinta y donde acaba
        self.x_inicio = x_inicio
        self.x_fin = x_fin

#Aquí definiremos los paquetes/cajas del juego
class Paquete:
    def __init__(self, cinta_id: int, x: int, y: int, sprites: dict, nivel: int):
        self.cinta_id = cinta_id #En que cinta se encuentra el paquete
        #Donde aparecen los paquetes
        self.x = x
        self.y = y
        self.sprites = sprites #Sus posibles sprites
        self.fase = 1 #La fase en la que empieza el paquete
        self.nivel = nivel # El nivel en el que se encuentra el paquete
        self.activo = True #Para saber si los paquetes se tienen que mover o no
        self.en_borde = False #Para saber si los paquetes están en el borde de la cinta o no
        self.cayendo = False #Para saber si los paquetes se están cayendo o no
        self.velocidad_caida = 3 #La velocidad a la que se caen los paquete
        self.culpable = None #Para saber quien es el culpable de que se haya caido la caja si mario o luigi
        self.ha_cruzado = False #Para saber si ha pasado por el centro y asi cambiar de fase o no

    def actualizar_fase(self, centro):
    #Para que el paquete cambie de fase
        if not self.ha_cruzado and abs(self.x - centro) <= 2:
        #Si la distancia entre el centro y el paquete es <2 cambia de fase
            self.fase += 1
            if self.fase > 6:
                self.fase = 1
            self.ha_cruzado = True
    #Aquí definimos el movimiento de las cajas y los mecanismos de si se cae o si llega al borde, etc.
    def mover(self, cintas, centro, suelo_y):
        #Si el paquete no está activo está quieto
        if not self.activo:
            return
        #Si el paquete se está cayendo
        if self.cayendo:
            self.y += self.velocidad_caida
            if self.y > suelo_y + 50:
                self.activo = False
            return
        #Por si la cinta_id es mayor que la cantidad de cintas que hay
        if self.cinta_id < len(cintas):
            n_cinta = self.cinta_id
            cinta = cintas[n_cinta]

        #Definimos como se mueve el paquete
        nueva_x = self.x + (1 * cinta.direccion)
        #Hacemos esto para saber si el paquete está en el final de la cinta o no
        llegada_fin = False
        if cinta.direccion == -1 and nueva_x <= cinta.x_fin or cinta.direccion == 1 and nueva_x >= cinta.x_fin:
            llegada_fin = True
            self.x = cinta.x_fin

        if llegada_fin:
            self.en_borde = True
        #Si no está en el borde de la cinta se mueve normal y comprobamos si cambia de fase o no
        else:
            self.x = nueva_x
            self.en_borde = False
            self.actualizar_fase(centro)


class Jefe:
    def __init__(self, sprites: dict):
        #Donde aparece el jefe
        self.x = 0
        self.y = 0
        self.sprites = sprites #Sus posibles sprites
        self.activo = False #Si el jefe tiene que aparecer o no
        self.objetivo = None #Saber cual es el objetivo del jefe(luigi o mario).
        self.temporizador = 0 #Temporizador para hacer desaparecer al jefe
        self.duracion_enfado = 3 * 30 #Cuánto dura el enfado

    #Hacemos este método para cuando tenga que aparecer el jefe
    def activar(self, objetivo: str, x: int, y: int):
        self.activo = True
        self.objetivo = objetivo
        self.x = x
        self.y = y
        self.temporizador = self.duracion_enfado

    #Hacemos un update en la clase Jefe para que una vez se acabe el temporizador desaparezca otra vez
    def update(self):
        if self.activo:
            self.temporizador -= 1
            if self.temporizador <= 0:
                self.activo = False
                self.objetivo = None