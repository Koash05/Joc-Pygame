#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame, random, os
from pygame.locals import *

# Constantes
WIDTH = 1280
HEIGHT = 720
WHITE = [255, 255, 255]
RECARGA = 10
VIDA = 5


# Clases
# ---------------------------------------------------------------------
from Corazon import Corazon
from Moneda import Moneda
from MultiShot import MultiShot
from Nave import Nave
from Ovni import Ovni
from SpeedUp import SpeedUp
from SpeedDown import SpeedDown
from User import User

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


def calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots, deathOvnis, fase):
    for ovni in ovnis:
        for shot in naveJugador.shots:
            if(pygame.sprite.collide_mask(shot, ovni)):
                naveJugador.shots.remove(shot)
                posicionOvniMuertoX=ovni.rect.centerx
                posicionOvniMuertoY = ovni.rect.centery
                try:
                    deathOvnis=deathOvnis+1

                    if deathOvnis > 20 + (fase*2):
                        fase = fase + 1
                        deathOvnis = 0

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

    array_usuarios = []
    file1 = open('puntacion.txt', 'r')
    Lines = file1.readlines()
    count = 0
    for line in Lines:
        count += 1
        parsed_user = line.strip().split(":", 1)

        array_usuarios.append(User(parsed_user[0], parsed_user[1]))

    file1.close()

    for i in range(1,len(array_usuarios)):
        for j in range(0,len(array_usuarios)-i):
            if(array_usuarios[j+1].puntuacion > array_usuarios[j].puntuacion):
                aux=array_usuarios[j];
                array_usuarios[j]=array_usuarios[j+1];
                array_usuarios[j+1]=aux;

    if os.path.exists("puntacion.txt"):
        os.remove("puntacion.txt")


    f = open("puntacion.txt", "a")
    for i in array_usuarios:
        f.write(str(i.nombre + ":" + i.puntuacion + "\n"))

    f.close()

    return array_usuarios

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
    ranking = []

    isPlayerSpeedingUp = False
    isOvnisSpeedingDown = False
    speedUpEffectTime = 300
    speedDownEffectTime = 300
    mostrarPuntuacion = False

    deathOvnis = 0

    fase = 1
    background_image = pygame.image.load("./imagenes/fondo.png").convert()

    #myfont = pygame.font.SysFont('Comic Sans MS', 30)
    myfont = pygame.font.Font('./fonts/Moby-Regular.ttf', 30)
    myfont2 = pygame.font.Font('./fonts/Singa Serif Regular.ttf', 30)


    tiempoParaNuevoOvni = 50

    clock = pygame.time.Clock()

    fin = False
    timeToRead=0

    nombre=""

    pygame.mixer.music.load('./music/Jeremy Blake - Powerup!.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    while True:
        if fin:
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)
                if eventos.type == pygame.KEYDOWN:
                    if mostrarPuntuacion == False:
                        letra = pygame.key.name(eventos.key)
                        if letra == "return":
                            ranking = guardarPuntuacion(nombre, naveJugador.score)
                            mostrarPuntuacion = True
                        elif len(letra) == 1 and letra !=":":
                            nombre = nombre + letra

            #screen.fill(WHITE)
            screen.blit(background_image, [0,0])

            if mostrarPuntuacion:
                distancia=20
                top=1
                for x in ranking:
                    if not top > 10:
                        screen.blit(myfont2.render(str(top) + " - " + x.nombre + ": " + x.puntuacion, False, (0, 0, 0)),(350, distancia))
                        distancia=distancia+35
                    top=top+1
            else:
                textGetName = myfont.render('Introduce tu nombre:', False, (0, 0, 0))
                screen.blit(textGetName, (500, 250))
                textGetName = myfont.render(nombre, False, (0, 0, 0))
                screen.blit(textGetName, (500, 300))
        pygame.display.flip()

        if not fin:
            time = clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            naveJugador.mover(time, keys)
            naveJugador.disparar(time, keys)
            #screen.fill(WHITE)
            screen.blit(background_image, [0,0])
            screen.blit(naveJugador.image, naveJugador.rect)

            tiempoParaNuevoOvni = tiempoParaNuevoOvni-1
            if tiempoParaNuevoOvni <= 0:
                nuevoOvni(ovnis, tiempoParaNuevoOvni)
                tiempoParaNuevoOvni = 50 - fase

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
            calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots, deathOvnis, fase)

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