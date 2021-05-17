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
        self.life = 100


class Corazon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagenes/corazon.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifeTime = 300


class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = cargarImagen("imagenes/moneda.png")
        self.image = pygame.image.load("imagenes/moneda.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifeTime = 300


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


class Ovni(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargarImagen("imagenes/ovni.png")
        self.rect = self.image.get_rect()
        self.speed = 0.2
        self.rect.centery = y
        self.rect.centerx = x


class MultiShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagenes/Multishot.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifeTime = 300


class SpeedUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagenes/speedUp.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifeTime = 300


class SpeedDown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagenes/speedDown.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifeTime = 300


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

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


def dibujarBalas(naveJugador, screen):
    for shot in naveJugador.shots:
        screen.blit(shot.image, shot.rect)


def dibujarOvnis(ovnis, screen):
    for ovni in ovnis:
        screen.blit(ovni.image, ovni.rect)


def calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots):
    for ovni in ovnis:
        for shot in naveJugador.shots:
            if(pygame.sprite.collide_mask(shot, ovni)):
                naveJugador.shots.remove(shot)
                posicionOvniMuertoX=ovni.rect.centerx
                posicionOvniMuertoY = ovni.rect.centery
                try:
                    ovnis.remove(ovni)
                except:
                    print("")
                naveJugador.score=naveJugador.score+1
                item = random.randint(0, 7)

                if item == 2:
                    monedas.append(Moneda(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 3:
                    vidas.append(Corazon(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 3:
                    speedUp.append(SpeedUp(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 4:
                    speedDown.append(SpeedDown(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 5:
                    multiShots.append(MultiShot(posicionOvniMuertoX, posicionOvniMuertoY))


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

        if naveJugador.vida < 0:
            naveJugador.vida=0

        naveJugador.score = naveJugador.score-10

        if naveJugador.score < 0:
            naveJugador.score=0

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


def calcularTiempoDeVidaItems(monedas, vidas, speedUp, multiShots):

    for moneda in monedas:
        moneda.lifeTime=moneda.lifeTime-1

        if moneda.lifeTime <=0:
            monedas.remove(moneda)

    for vida in vidas:
        vida.lifeTime = vida.lifeTime-1

        if vida.lifeTime <=0:
            vidas.remove(vida)

    for speedup in speedUp:
        speedup.lifeTime = speedup.lifeTime-1

        if speedup.lifeTime <=0:
            speedUp.remove(speedup)

    for multishot in multiShots:
        multishot.lifeTime = multishot.lifeTime-1

        if multishot.lifeTime <=0:
            multiShots.remove(multishot)



def dibujarItems(monedas, vidas, speedUp, speedDown, multiShots, screen):
    for moneda in monedas:
        screen.blit(moneda.image, moneda.rect)

    for vida in vidas:
        screen.blit(vida.image, vida.rect)

    for speedup in speedUp:
        screen.blit(speedup.image, speedup.rect)

    for speeddown in speedDown:
        screen.blit(speeddown.image, speeddown.rect)

    for multishot in multiShots:
        screen.blit(multishot.image, multishot.rect)



def calcularColisionItems(monedas, vidas, multiShots, naveJugador):
    for moneda in monedas:
        if pygame.sprite.collide_mask(naveJugador, moneda):
            naveJugador.score += 100
            monedas.remove(moneda)

    for vida in vidas:
        if pygame.sprite.collide_mask(naveJugador, vida):
            if naveJugador.vida < 5:
                naveJugador.vida += 1
            else:
                naveJugador.score +=50

            vidas.remove(vida)

    for multishot in multiShots:
        if pygame.sprite.collide_mask(naveJugador, multishot):
            naveJugador.multishot = True

            multiShots.remove(multishot)



def dibujarVidaRestante(screen, naveJugador):
    imagenVida = pygame.image.load("imagenes/corazon.png")
    imagenCorazonUsado = pygame.image.load("imagenes/corazonOscuro.png")
    vidasJugador = naveJugador.vida
    vidasTotales = VIDA
    vidasUsadas = vidasTotales-vidasJugador
    distanciaDeDibujado = 40

    for x in range(0, vidasJugador):
        screen.blit(imagenVida, (WIDTH-distanciaDeDibujado, 20))
        distanciaDeDibujado += 40

    for x in range(0, vidasUsadas):
        screen.blit(imagenCorazonUsado, (WIDTH-distanciaDeDibujado, 20))
        distanciaDeDibujado += 40


def guardarPuntuacion(name, puntacion):
    f = open("puntacion.txt", "a")

    puntacionString=str(puntacion)
    f.write(str(name + ":" + puntacionString + "\n"))

    f.close()


def escribirNombre(keys):
    letra = pygame.key.key_code(keys)


def readFile(myfont, screen):
    f = open("puntacion.txt", "r")
    #print(f.readline())
    posicion = 100

    for x in f:
        textsurface = myfont.render(str(x), False, (0, 0, 0))
        screen.blit(textsurface, (100, posicion))
        posicion = posicion+50


# ---------------------------------------------------------------------

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Travelling around the space")

    naveJugador = Nave()

    ovnis = []
    vidas = []
    monedas = []
    speedUp = []
    speedDown = []
    multiShots = []

    isPlayerSpeedingUp = False
    isOvnisSpeedingDown = False
    speedUpEffectTime = 300
    speedDownEffectTime = 300

    fase = 1

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    tiempoParaNuevoOvni = 50

    clock = pygame.time.Clock()

    fin = False
    timeToRead=0

    nombre=""

    while True:

        if fin:
            textsurface = myfont.render('Introduce tu nombre:', False, (255, 255, 255))
            screen.blit(textsurface, (WIDTH / 2, HEIGHT / 2))

            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)
                if eventos.type == pygame.KEYDOWN:
                    letra= pygame.key.name(eventos.key)
                    if letra == "return":
                        guardarPuntuacion(nombre, naveJugador.score)
                        exit()
                    elif len(letra) == 1:
                        nombre = nombre + letra

            if timeToRead <= 300:
                readFile(myfont, screen)
                timeToRead=timeToRead+1

        if not fin:
            time = clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            naveJugador.mover(time, keys)
            naveJugador.disparar(time, keys)
            screen.fill(BLACK)
            screen.blit(naveJugador.image, naveJugador.rect)

            tiempoParaNuevoOvni = tiempoParaNuevoOvni-1
            if tiempoParaNuevoOvni <= 0:
                nuevoOvni(ovnis, tiempoParaNuevoOvni)
                tiempoParaNuevoOvni = 50

            dibujarOvnis(ovnis, screen)
            dibujarBalas(naveJugador, screen)
            dibujarItems(monedas, vidas, speedUp, speedDown, multiShots, screen)
            calcularColisionItems(monedas, vidas, multiShots, naveJugador)

            # SpeedUp
            for speedup in speedUp:
                if pygame.sprite.collide_mask(naveJugador, speedup):
                    naveJugador.speed = 0.6
                    isPlayerSpeedingUp = True

                    speedUp.remove(speedup)

            # SpeedDown
            for speeddown in speedDown:
                if pygame.sprite.collide_mask(naveJugador, speeddown):
                    for ovni in ovnis:
                        ovni.speed = 0.15

                    speedDown.remove(speeddown)


            seguirJugador(naveJugador, ovnis, time)
            calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots)

            calcularTiempoDeVidaItems(monedas, vidas, speedUp, multiShots)

            # SpeedUp
            if (isPlayerSpeedingUp == True):
                speedUpEffectTime = speedUpEffectTime - 1

                if (speedUpEffectTime <= 0):
                    isPlayerSpeedingUp = False
                    naveJugador.speed = 0.4
                    speedUpEffectTime = 300

            # SpeedDown
            if (isOvnisSpeedingDown == True):
                speedDownEffectTime = speedDownEffectTime - 1

                if (speedDownEffectTime <= 0):
                    isOvnisSpeedingDown = False
                    for ovni in ovnis:
                        ovni.speed = 0.2

                    speedDownEffectTime = 300

            # SpeedDown
            if (naveJugador.multishot == True):
                naveJugador.effectTimeMultiShot = naveJugador.effectTimeMultiShot - 1

                if (naveJugador.effectTimeMultiShot <= 0):
                    naveJugador.multishot = False
                    naveJugador.effectTimeMultiShot = 300



            imagenMoneda = pygame.image.load("imagenes/moneda.png")
            screen.blit(imagenMoneda, (20,20))

            textScore = myfont.render("Monedas: " + str(naveJugador.score), False, (0, 0, 0))
            screen.blit(textScore, (60, 13))

            textFase = myfont.render("Fase: " + str(fase), False, (0, 0, 0))
            screen.blit(textFase, ((WIDTH/2)-75, 13))

            dibujarVidaRestante(screen, naveJugador)

            if(naveJugador.vida == 0):

                fin = True

                ovnis = []
                vidas = []
                monedas = []
                speedUp = []
                speedDown = []
                multiShots = []

            pygame.display.flip()

    return 0


if __name__ == '__main__':
    pygame.init()
    main()