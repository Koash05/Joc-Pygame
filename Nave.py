#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame, random
from pygame.locals import *

# Constantes
WIDTH = 1280
HEIGHT = 720
BLACK = [255, 255, 255]
RECARGA = 10
VIDA = 5

from Shot import Shot


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/spaceship1.png")
        self.rect = self.image.get_rect()
        self.speed = 0.4
        self.rect.centery = HEIGHT/2
        self.rect.centerx = WIDTH/2
        self.mirando = 1
        self.shots = []
        self.recarga = RECARGA
        self.vida = VIDA
        self.score = 0
        self.multishot = False
        self.effectTimeMultiShot = 300


    def mover(self, time, keys):

        if not self.recarga == 0:
            self.recarga=self.recarga-1

        if self.rect.top >= 0:
            if keys[K_UP]:
                self.image = pygame.image.load("imagenes/spaceship1.png")
                self.rect.centery -= self.speed * time
                self.mirando = 1
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.image = pygame.image.load("imagenes/spaceship3.png")
                self.rect.centery += self.speed * time
                self.mirando = 2
        if self.rect.left >= 0:
            if keys[K_LEFT]:
                self.image = pygame.image.load("imagenes/spaceship4.png")
                self.rect.centerx -=self.speed * time
                self.mirando = 3
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.image = pygame.image.load("imagenes/spaceship2.png")
                self.rect.centerx +=self.speed * time
                self.mirando = 4


    def disparar(self, time, keys):
        if keys[K_SPACE]:
            if self.recarga == 0:
                if self.mirando == 1:
                    self.shots.append(Shot(self.rect.centerx, self.rect.centery-43, self.mirando))
                    if(self.multishot == True):
                        self.shots.append(Shot(self.rect.centerx, self.rect.centery - 43, 5))
                        self.shots.append(Shot(self.rect.centerx, self.rect.centery - 43, 6))

                if self.mirando == 2:
                    self.shots.append(Shot(self.rect.centerx, self.rect.centery+43, self.mirando))
                    if self.multishot == True:
                        self.shots.append(Shot(self.rect.centerx, self.rect.centery + 43, 7))
                        self.shots.append(Shot(self.rect.centerx, self.rect.centery+43, 8))

                if self.mirando == 3:
                    self.shots.append(Shot(self.rect.centerx-43, self.rect.centery, self.mirando))
                    if(self.multishot == True):
                        self.shots.append(Shot(self.rect.centerx - 43, self.rect.centery, 6))
                        self.shots.append(Shot(self.rect.centerx-43, self.rect.centery, 7))

                if self.mirando == 4:
                    self.shots.append(Shot(self.rect.centerx + 43, self.rect.centery, self.mirando))
                    if(self.multishot == True):
                        self.shots.append(Shot(self.rect.centerx + 43, self.rect.centery, 8))
                        self.shots.append(Shot(self.rect.centerx + 43, self.rect.centery, 5))

                self.recarga = RECARGA


        for shot in self.shots:
            speedTime = shot.speed * time
            if shot.mirando == 1:
                shot.rect.centery -= speedTime

            if shot.mirando == 2:
                shot.rect.centery += speedTime

            if shot.mirando == 3:
                shot.rect.centerx -= speedTime

            if shot.mirando == 4:
                shot.rect.centerx += speedTime

            if shot.mirando == 5:
                shot.rect.centerx += speedTime
                shot.rect.centery -= speedTime

            if shot.mirando == 6:
                shot.rect.centerx -= speedTime
                shot.rect.centery -= speedTime

            if shot.mirando == 7:
                shot.rect.centerx -= speedTime
                shot.rect.centery += speedTime

            if shot.mirando == 8:
                shot.rect.centerx += speedTime
                shot.rect.centery += speedTime

            shot.life = shot.life-1

            if(shot.life<=0):
                self.shots.remove(shot)


def cargarImagen(filename, transparent=True):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image
