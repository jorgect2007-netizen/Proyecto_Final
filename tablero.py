#Importamos las clases
from clases import Personaje
from clases import Camion
from clases import Paquete
from clases import Jefe
from clases import Cinta
import pyxel

#Creamos la clase tablero
class Tablero:
    #Aquí ponemos los posibles sprites de todos los personajes
    #Aquí los posibles sprites de mario
    sprites_mario = {
        'abajo_izq': (2, 0, 48, 16, 16),
        'abajo_der': (2, 0, 32, 16, 16),
        'arriba': (2, 0, 96, 16, 16),
        'triste': (2, 0, 64, 16, 16)
    }
    #Aquí los posibles sprites de luigi
    sprites_luigi = {
        'abajo_izq': (2, 16, 48, 16, 16),
        'abajo_der': (2, 16, 32, 16, 16),
        'arriba': (2, 16, 96, 16, 16),
        'triste': (2, 16, 80, 16, 16)
    }
    #Aquí los sprites de todas las fases de los paquetes
    sprites_paquete = {
        'fase1': (1, 0, 0, 16, 16),
        'fase2': (1, 0, 16, 16, 16),
        'fase3': (1, 0, 32, 16, 16),
        'fase4': (1, 0, 48, 16, 16),
        'fase5': (1, 0, 64, 16, 16),
        'fase6': (1, 0, 80, 16, 16),
    }
    #Aquí los posibles sprites del jefe
    sprites_jefe = {
        'jefe_luigi': (2, 32, 0, 16, 16),
        'jefe_mario': (2, 32, 16, 16, 16),
    }
    #Aquí los posibles sprites del camión
    sprites_camion = {
        'cam0': (1, 16, 0, 32, 24),
        'cam1': (1, 16, 24, 32, 24),
        'cam2': (1, 16, 48, 32, 24),
        'cam3': (1, 16, 72, 32, 24),
        'cam4': (1, 16, 96, 32, 24),
        'cam5': (1, 16, 120, 32, 24),
        'cam6': (1, 16, 144, 32, 24),
        'cam7': (1, 16, 168, 32, 24),
        'cam8': (1, 16, 192, 32, 24),
    }
    #En el init ponemos las propiedades del tablero (lo que mide)
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self.game_over = False #Para cuando se alcancen los 3 fallos
        self.puntos = 0 #Los puntos que lleve el jugador
        self.fallos = 0 #Los fallos que lleve el jugador
        self.max_fallos = 3 #Los fallos máximos que puede tener el jugador

        self.num_niveles = 5 #Los niveles que tiene el juego
        #Márgenes por arriba y abajo para que los sprites no se salgan de la pantalla
        self.margen_arriba = 45
        self.margen_abajo = 45
        espacio_util = self.alto - self.margen_arriba - self.margen_abajo
        #La diferencia de altura que hay entre niveles
        self.dif_niveles = espacio_util // (self.num_niveles - 1)
        #Una lista con la altura de todos los niveles
        self.niveles_y = []
        for i in range(self.num_niveles):
            self.niveles_y.append(self.margen_arriba + i * self.dif_niveles)

        self.x_base_mario = 390 #La posición x de mario
        self.x_base_luigi = 124 #La posición x de luigi
        #Definimos a mario y a luigi
        self.mario = Personaje("mario", x=self.x_base_mario, y=self.niveles_y[4] + 13, sprites=self.sprites_mario,
                               nivel=0, tope_arriba=4, tope_abajo=0, tablero=self)
        self.luigi = Personaje("luigi", x=self.x_base_luigi, y=self.niveles_y[4] - 28, sprites=self.sprites_luigi,
                               nivel=1, tope_arriba=5, tope_abajo=1, tablero=self)
        #Definimos al Jefe
        self.jefe = Jefe(sprites=self.sprites_jefe)
        self.pausado_por_jefe = False #Para saber si el juego se ha pausado por la aparición del jefe
        #Definimos al Camión
        self.camion = Camion(x=18, y=40, sprites=self.sprites_camion)
        self.pausado_por_camion = False #Para saber si el juego se ha pausado porque el camión se está llendo

        #Aquí definimos las cintas del juego
        self.cintas = [
            Cinta(self.niveles_y[4] + 17, -1, 512, 425), #Cinta 0
            Cinta(self.niveles_y[4], -1, 380, 148), #Cinta 1
            Cinta(self.niveles_y[3], +1, 148, 380), #Cinta 2
            Cinta(self.niveles_y[2], -1, 380, 148), #Cinta 3
            Cinta(self.niveles_y[1], +1, 148, 380), #Cinta 4
            Cinta(self.niveles_y[0], -1, 380, 155)  #Cinta 5
        ]

        self.paquetes = [] #Lista con los paquetes en pantalla
        self.min_paquetes = 1 #Los paquetes que tiene que haber mínimo en pantalla

        #Ponemos las funciones necesarias de pyxel para iniciar el juego
        pyxel.init(self.ancho, self.alto, title="PROYECTO FINAL MARIO BROSS")
        pyxel.load("assets/resources.pyxres")
        pyxel.run(self.update, self.draw)

    #Aquí vamos actualizando el mínimo de paquetes cada vez que el jugador haga puntos múltiplos de 50.
    def actualizar_min_paquetes(self):
        self.min_paquetes += (self.puntos // 50)
    #Usaremos esta función para generar los paquetes
    def generar_paquete(self):
        self.paquetes.append(Paquete(
            cinta_id=0,
            x=self.cintas[0].x_inicio,
            y=self.cintas[0].y - 4,
            sprites=self.sprites_paquete,
            nivel=0
        ))
    #Con este método comprobamos si los paquetes están a la misma altura que el personaje
    def verificar_colisiones(self):
        for paquete in self.paquetes:
            #Solo funciona si el paquete no se está cayendo, si está activo y si está en el borde
            if paquete.activo and not paquete.cayendo and paquete.en_borde:
                #En el caso de que ya haya que dejar el paquete en el camión
                if paquete.cinta_id == 5:
                    self.entregar_paquete(paquete)
                #Para el resto de los casos
                else:
                    #Si la cinta es par, es de mario
                    if paquete.cinta_id % 2 == 0:
                        personaje_encargado = self.mario
                    #Y si no lo es, es de luigi
                    else:
                        personaje_encargado = self.luigi
                    #Si están en el mismo nivel el paquete sube, y si no, se cae
                    if personaje_encargado.nivel == paquete.cinta_id:
                        self.subir_paquete(paquete, personaje_encargado)
                    else:
                        self.iniciar_caida(paquete, personaje_encargado.nombre)

    def subir_paquete(self, paquete, personaje):
        paquete.cinta_id += 1
        nueva_cinta = self.cintas[paquete.cinta_id]
        paquete.x = nueva_cinta.x_inicio
        paquete.y = nueva_cinta.y - 4
        paquete.en_borde = False
        paquete.ha_cruzado = False

        # ANIMACIÓN: Activar sprite "arriba"
        personaje.animar("subir")

        self.puntos += 10
        pyxel.play(0, 0)

    def iniciar_caida(self, paquete, culpable):
        paquete.cayendo = True
        paquete.en_borde = False
        paquete.culpable = culpable

    def registrar_fallo(self, paquete):
        self.fallos += 1
        pyxel.play(0, 1)

        if self.fallos >= self.max_fallos:
            self.game_over = True
        else:
            self.pausado_por_jefe = True

            if paquete.culpable == "luigi":
                x_jefe = 50
                y_jefe = self.niveles_y[4] - 20
                self.jefe.activar("jefe_luigi", x_jefe, y_jefe)
                self.luigi.x = x_jefe + 30
                self.luigi.y = self.niveles_y[4] - 28
                self.luigi.nivel = 1

            else:  # mario
                x_jefe = 450
                y_jefe = self.niveles_y[3] - 20
                self.jefe.activar("jefe_mario", x_jefe, y_jefe)
                self.mario.x = x_jefe - 30
                self.mario.y = self.niveles_y[3] - 28
                self.mario.nivel = 2

    def entregar_paquete(self, paquete):
        paquete.activo = False
        self.puntos += 10
        pyxel.play(0, 2)

        self.luigi.animar("entregar")

        # Lógica del camión
        self.camion.llenar()
        if self.camion.animacion_salida:
            self.pausado_por_camion = True

    def update(self):
        # --- ACTUALIZAR SPRITES SIEMPRE (Incluso en pausa) ---
        self.mario.actualizar_sprite()
        self.luigi.actualizar_sprite()

        # --- PRIORIDAD DE PAUSAS ---
        if self.pausado_por_camion:
            self.camion.update()
            if not self.camion.animacion_salida:
                self.pausado_por_camion = False
            return

        if self.pausado_por_jefe:
            self.jefe.update()
            if not self.jefe.activo:
                self.pausado_por_jefe = False
                self.mario.x = self.x_base_mario
                self.luigi.x = self.x_base_luigi
            return

            # --- JUEGO NORMAL ---
        if pyxel.btnp(pyxel.KEY_UP): self.mario.mover("arriba")
        if pyxel.btnp(pyxel.KEY_DOWN): self.mario.mover("abajo")
        if pyxel.btnp(pyxel.KEY_W): self.luigi.mover("arriba")
        if pyxel.btnp(pyxel.KEY_S): self.luigi.mover("abajo")

        self.actualizar_min_paquetes()

        if len(self.paquetes) < self.min_paquetes and pyxel.frame_count % 80 == 0:
            self.generar_paquete()

        for paquete in self.paquetes:
            estaba_activo = paquete.activo
            suelo_y = self.niveles_y[4]
            paquete.mover(self.cintas, self.ancho // 2, suelo_y)

            if estaba_activo and not paquete.activo and paquete.cayendo:
                self.registrar_fallo(paquete)

        self.paquetes = [p for p in self.paquetes if p.activo]
        self.verificar_colisiones()

    def draw(self):
        pyxel.cls(13)

        # Escaleras
        pyxel.blt(self.x_base_mario, self.niveles_y[4] - 25, 0, 0, 56, 16, 16, 0, scale=2)
        pyxel.blt(self.x_base_mario, self.niveles_y[2] - 25, 0, 0, 56, 16, 16, 0, scale=2)
        pyxel.blt(self.x_base_luigi, self.niveles_y[3] - 25, 0, 0, 56, 16, 16, 0, scale=2)
        pyxel.blt(self.x_base_luigi, self.niveles_y[1] - 25, 0, 0, 56, 16, 16, 0, scale=2)

        # Personajes
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprites[self.mario.sprite_actual], 0, scale=3)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprites[self.luigi.sprite_actual], 0, scale=3)

        # Paquetes
        for paquete in self.paquetes:
            sprite = paquete.sprites[f"fase{paquete.fase}"]
            pyxel.blt(paquete.x, paquete.y, *sprite, scale=3, colkey=0)

        # Pilar
        for i in range(16):
            pyxel.blt(self.ancho // 2, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho // 2 + 16, 0 + i * 16, 0, 0, 80, 16, 16)
            pyxel.blt(self.ancho // 2 - 16, 0 + i * 16, 0, 0, 80, 16, 16)

        # Cintas
        for i, y in enumerate(self.niveles_y):
            if i % 2 == 0:
                pyxel.blt(160, y, 0, 8, 16, 80, 16, 11)
            else:
                pyxel.blt(152, y, 0, 0, 0, 96, 16, 11)
            if i % 2 == 0:
                pyxel.blt(280, y, 0, 0, 0, -96, 16, 11)
            else:
                pyxel.blt(288, y, 0, 8, 16, -80, 16, 11)

        pyxel.blt(424, self.niveles_y[4] + 17, 0, 0, 0, 96, 16, 11)

        # Plataformas
        pyxel.blt(self.x_base_luigi - 90, self.niveles_y[4] + 9, 0, 0, 104, 90, 9, 0, scale=2)
        pyxel.blt(self.x_base_luigi - 30, self.niveles_y[2] + 9, 0, 0, 104, 35, 9, 0, scale=2)
        pyxel.blt(self.x_base_luigi - 30, self.niveles_y[0] + 9, 0, 0, 104, 35, 9, 0, scale=2)
        pyxel.blt(self.x_base_mario + 5, self.niveles_y[4] + 49, 0, 0, 104, 35, 9, 0, scale=2)
        pyxel.blt(self.x_base_mario + 23, self.niveles_y[3] + 9, 0, 0, 104, 72, 9, 0, scale=2)
        pyxel.blt(self.x_base_mario + 5, self.niveles_y[1] + 9, 0, 0, 104, 35, 9, 0, scale=2)

        # Plataforma Camión (Estática)
        pyxel.blt(71, 57, 0, 112, 0, 4, 17, 0, scale=2)
        pyxel.blt(0, 79, 0, 0, 104, 50, 9, 0, scale=2)

        # Camión (Dinámico)
        nombre_sprite = f"cam{self.camion.cajas}"
        if nombre_sprite in self.camion.sprites:
            pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprites[nombre_sprite],colkey=14, scale=2)

        if self.jefe.activo:
            sprite = self.jefe.sprites[self.jefe.objetivo]
            pyxel.blt(self.jefe.x, self.jefe.y, *sprite, scale=2, colkey=0)

        # UI
        pyxel.text(10, 10, f"PUNTOS: {self.puntos}", 7)
        texto_fallos = "FALLOS: " + "X " * self.fallos
        pyxel.text(300, 10, texto_fallos, 8 if self.fallos > 0 else 7)


        pyxel.text(10, 246, f"PISO LUIGI: {self.luigi.nivel}", 7)
        pyxel.text(450, 10, f"PISO MARIO: {self.mario.nivel}", 7)

        if self.game_over:
            pyxel.cls(13)
            pyxel.text(self.ancho // 2 - 30, self.alto // 2, "GAME OVER", 8)


prueba = Tablero(512, 256)