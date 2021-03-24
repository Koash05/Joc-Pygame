#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame, random
from pygame.locals import *

# Constantes
WIDTH = 1280
HEIGHT = 720
BLACK = [0, 0, 0]
RECARGA = 10
VIDA = 5


# Clases
# ---------------------------------------------------------------------

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/shot.png")
        self.rect = self.image.get_rect()
        self.rect.centery=y
        self.rect.centerx=x
        self.mirando = direccion
        self.speed = 0.9
        self.life= 100

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/spaceship1.png")
        self.rect = self.image.get_rect()
        self.speed = 0.4
        self.rect.centery=HEIGHT/2
        self.rect.centerx=WIDTH/2
        self.mirando = 1
        self.shots = []
        self.recarga=RECARGA
        self.vida = VIDA


    def mover(self, time, keys):

        if not self.recarga == 0:
            self.recarga=self.recarga-1

        if self.rect.top >= 0:
            if keys[K_UP]:
                self.image = cargarImagen("imagenes/spaceship1.png")
                self.rect.centery -= self.speed * time
                self.mirando = 1
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.image = cargarImagen("imagenes/spaceship3.png")
                self.rect.centery += self.speed * time
                self.mirando = 2
        if self.rect.left >= 0:
            if keys[K_LEFT]:
                self.image = cargarImagen("imagenes/spaceship4.png")
                self.rect.centerx -=self.speed * time
                self.mirando = 3
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.image = cargarImagen("imagenes/spaceship2.png")
                self.rect.centerx +=self.speed * time
                self.mirando = 4

    def disparar(self, time, keys):
        if keys[K_SPACE]:
            if self.recarga == 0:
                if self.mirando == 1:
                    self.shots.append(Shot(self.rect.centerx, self.rect.centery-43 , self.mirando))
                if self.mirando == 2:
                    self.shots.append(Shot(self.rect.centerx, self.rect.centery+43, self.mirando))
                if self.mirando == 3:
                    self.shots.append(Shot(self.rect.centerx-43, self.rect.centery, self.mirando))
                if self.mirando == 4:
                    self.shots.append(Shot(self.rect.centerx+43, self.rect.centery, self.mirando))

                self.recarga=RECARGA

        for shot in self.shots:
            if shot.mirando == 1:
                shot.rect.centery -= shot.speed * time
            if shot.mirando == 2:
                shot.rect.centery += shot.speed * time
            if shot.mirando == 3:
                shot.rect.centerx -= shot.speed * time
            if shot.mirando == 4:
                shot.rect.centerx += shot.speed * time

            shot.life=shot.life-1
            if(shot.life<=0):
                self.shots.remove(shot)

class Ovni(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/ovni.png")
        self.rect = self.image.get_rect()
        self.speed = 0.2
        self.rect.centery=y
        self.rect.centerx=x


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def cargarImagen(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def dibujarBalas(naveJugador, screen):
    for shot in naveJugador.shots:
        screen.blit(shot.image, shot.rect)

def dibujarOvnis(ovnis, screen):
    for ovni in ovnis:
        screen.blit(ovni.image, ovni.rect)

def calculaDisparos(naveJugador, ovnis):
    for ovni in ovnis:
        for shot in naveJugador.shots:
            if(pygame.sprite.collide_mask(shot, ovni)):
                naveJugador.shots.remove(shot)
                ovnis.remove(ovni)

def seguirJugador(naveJugador, ovnis, time):
    for ovni in ovnis:
        distanciaX= naveJugador.rect.centerx-ovni.rect.centerx
        distanciaY= naveJugador.rect.centery-ovni.rect.centery

        if distanciaX < 0:
            ovni.rect.centerx -= ovni.speed * time
        if distanciaX > 0:
            ovni.rect.centerx += ovni.speed * time
        if distanciaY < 0:
            ovni.rect.centery -= ovni.speed * time
        if distanciaY > 0:
            ovni.rect.centery += ovni.speed * time

        colisionNaveOvni(naveJugador, ovni, ovnis)

def colisionNaveOvni(naveJugador, ovni, ovnis):
    if pygame.sprite.collide_mask(naveJugador, ovni):
        naveJugador.vida = naveJugador.vida - 1

        ovnis.remove(ovni)

def nuevoOvni(ovnis, tiempoParaNuevoOvni):
    posicion=random.randint(0, 5)

    if posicion == 0:
        ovnis.append(Ovni(0,0))
    if posicion == 1:
        ovnis.append(Ovni(0,WIDTH))
    if posicion == 2:
        ovnis.append(Ovni(0,WIDTH/2))
    if posicion == 3:
        ovnis.append(Ovni(HEIGHT,0))
    if posicion == 4:
        ovnis.append(Ovni(HEIGHT/2,0))
    if posicion == 5:
        ovnis.append(Ovni(HEIGHT,WIDTH))


# ---------------------------------------------------------------------
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Travelling around the space")

    naveJugador = Nave()

    ovnis = []

    tiempoParaNuevoOvni = 50

    ovni = Ovni(500, 500)
    ovnis.append(ovni)


    clock = pygame.time.Clock()

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)

        naveJugador.mover(time, keys)
        naveJugador.disparar(time, keys)
        screen.fill(BLACK)
        screen.blit(naveJugador.image, naveJugador.rect)

        tiempoParaNuevoOvni=tiempoParaNuevoOvni-1
        if tiempoParaNuevoOvni<=0:
            nuevoOvni(ovnis, tiempoParaNuevoOvni)
            tiempoParaNuevoOvni=50

        dibujarOvnis(ovnis, screen)
        dibujarBalas(naveJugador, screen)
        seguirJugador(naveJugador, ovnis, time)
        calculaDisparos(naveJugador, ovnis)


        if(naveJugador.vida == 0):
            print("has perdido")

        pygame.display.flip()

    return 0




if __name__ == '__main__':
    pygame.init()
    main()