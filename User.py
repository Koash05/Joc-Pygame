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

class User():
    def __init__(self, nombre, puntacion):
        self.nombre = nombre
        self.puntuacion = puntacion

    def __repr__(self):
        return repr((self.nombre, self.puntuacion))


