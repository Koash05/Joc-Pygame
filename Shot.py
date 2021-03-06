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


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/shot.png")
        self.rect = self.image.get_rect()
        self.rect.centery=y
        self.rect.centerx=x
        self.mirando = direccion
        self.speed = 0.9
        self.life = 100

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
