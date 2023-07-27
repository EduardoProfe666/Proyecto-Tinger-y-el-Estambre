import pygame
from tkinter import messagebox as mb
import random

print("Tinger y el Estambre. v2023.07.26. EduardoProfe")

class Juego:
    puntuacion = 0  # Puntuación del jugador
    velocidad_estambre = []  # Velocidad en x e y del estambre
    velocidad_gato = 0  # Velocidad del gato
    img_punt = None  # Imagen de la puntuación
    rect_punt = None  # Rectángulo de la puntuación
    ventana = None  # Ventana del juego
    estambre = None  # Imagen del estambre
    estambre_recta = None  # Recta de trayectoria del estambre
    gato = None  # Imagen del gato
    gato_recta = None  # Recta de trayectoria del gato
    fondos = []  # Fondos del juego
    fondo_seleccionado = None  # Fondo del juego seleccionado
    tam_pantalla = []  # Tamaño en x e y de la pantalla
    sonidos_gato = []  # Sonidos de maullidos de gatos al tocar el estambre
    sonido_gato_cheat = None  # Sonido de maullido de gato al presionar espacio
    soundtrack = None  # Sonido de fondo
    sonido_cheat_activo = False  # Comprobar si el sonido_cheat se encuentra activo

    def __init__(self, tam_pantalla: [int, int]):
        self.tam_pantalla = tam_pantalla

    def inicializar_juego(self):
        self.puntuacion = 0
        pygame.init()
        # Puntuación
        self.img_punt = pygame.font.SysFont("Roboto", 40).render(str(self.puntuacion), True, pygame.Color('violet'))
        self.rect_punt = self.img_punt.get_rect()
        self.rect_punt.top = 20
        self.rect_punt.left = 30
        # Ventana
        self.ventana = pygame.display.set_mode(self.tam_pantalla)
        pygame.display.set_caption("Tinger y el estambre")
        pygame.display.set_icon(pygame.image.load("image/icono.png"))
        self.velocidad_estambre = [4, 4]
        # Cargar estambre
        self.estambre = pygame.image.load("image/estambre.png")
        self.estambre_recta = self.estambre.get_rect()
        self.estambre_recta.move_ip(0, 0)
        # Cargar gato
        self.gato = pygame.image.load("image/gato.png")
        self.gato_recta = self.gato.get_rect()
        self.gato_recta.move_ip(self.tam_pantalla[0] / 2, self.tam_pantalla[1] - self.gato_recta.height)
        # Cargar audio
        self.sonido_gato_cheat = pygame.mixer.Sound(file="audio/gato_2.wav")
        self.sonidos_gato = [pygame.mixer.Sound(file="audio/gato_1.wav"), pygame.mixer.Sound(file="audio/gato_2.wav"),
                             pygame.mixer.Sound(file="audio/gato_3.wav"), pygame.mixer.Sound(file="audio/gato_4.wav"),
                             pygame.mixer.Sound(file="audio/gato_5.wav")]
        self.soundtrack = pygame.mixer.Sound(file="audio/sountrack.wav")
        self.soundtrack.play(loops=-1)
        self.soundtrack.set_volume(0.3)
        self.sonido_gato_cheat.set_volume(0.5)
        for i in self.sonidos_gato:
            i.set_volume(0.5)
        # Cargar fondo
        self.fondos = [pygame.image.load('image/fondo_1.jpg'), pygame.image.load('image/fondo_2.jpg'),
                       pygame.image.load('image/fondo_3.jpg'), pygame.image.load('image/fondo_4.jpg'),
                       pygame.image.load('image/fondo_5.jpg'), pygame.image.load('image/fondo_6.jpg'),
                       pygame.image.load('image/fondo_7.jpg')]
        for i in range(len(self.fondos)):
            self.fondos[i] = pygame.transform.smoothscale(self.fondos[i], self.tam_pantalla)
        self.fondo_seleccionado = self.fondos[random.randint(0, len(self.fondos) - 1)]

    def jugar(self):
        jugando = True
        while jugando:
            self.inicializar_juego()
            aux = self.iniciar_juego()
            self.soundtrack.stop()
            self.sonido_gato_cheat.stop()
            if aux == -1:
                mb.showinfo("Fin del juego", "Gracias por jugar :)")
                jugando = False
            else:
                mb.showinfo("Game Over", "Perdiste :(\n\n" + "Puntuación: " + str(self.puntuacion))
                if not mb.askyesno("Seguir jugando", "Quieres seguir jugando?"):
                    mb.showinfo("Fin del juego", "Gracias por jugar :)")
                    jugando = False

    def iniciar_juego(self):
        retorno = -1
        jugando = True
        while jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False
            self.comprobar_teclas_presionadas()
            if not self.comprobar_colisiones():
                jugando = False
                retorno = self.puntuacion
            self.actualizar_visual()

        return retorno

    def comprobar_teclas_presionadas(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.gato_recta.left > 0:  # Flecha Izquierda
            self.gato_recta = self.gato_recta.move(-8, 0)
        if keys[pygame.K_RIGHT] and self.gato_recta.right < self.ventana.get_width():  # Flecha Derecha
            self.gato_recta = self.gato_recta.move(8, 0)
        if keys[pygame.K_SPACE]:  # Espacio
            if not self.sonido_cheat_activo:
                self.sonido_cheat_activo = True
                self.sonido_gato_cheat.play(-1)
            self.puntuacion += 3
            self.img_punt = pygame.font.SysFont("Roboto", 40).render(str(self.puntuacion), True, pygame.Color('red'))
        else:
            self.sonido_cheat_activo = False
            self.sonido_gato_cheat.stop()

    def comprobar_colisiones(self):
        jugando = True
        if self.gato_recta.colliderect(self.estambre_recta):
            self.velocidad_estambre[1] = -self.velocidad_estambre[1]
            self.puntuacion += 1
            self.img_punt = pygame.font.SysFont("Roboto", 40).render(str(self.puntuacion), True,
                                                                     pygame.Color('violet'))
            self.sonidos_gato[random.randint(a=0, b=len(self.sonidos_gato) - 1)].play()
        if self.estambre_recta.left < 0 or self.estambre_recta.right > self.ventana.get_width():
            self.velocidad_estambre[0] = -self.velocidad_estambre[0]
        if self.estambre_recta.top < 0:
            self.velocidad_estambre[1] = -self.velocidad_estambre[1]
        if self.estambre_recta.bottom > self.ventana.get_height():
            jugando = False
        self.estambre_recta = self.estambre_recta.move(self.velocidad_estambre)
        return jugando

    def actualizar_visual(self):
        self.ventana.blit(self.fondo_seleccionado, (0, 0))
        self.ventana.blit(self.img_punt, self.rect_punt)
        self.ventana.blit(self.estambre, self.estambre_recta)
        self.ventana.blit(self.gato, self.gato_recta)
        pygame.display.flip()
        pygame.time.Clock().tick(70)


if __name__ == "__main__":
    Juego((640, 480)).jugar()
