#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame, random, os, operator

from pygame.locals import *

# Constantes
WIDTH = 1280
HEIGHT = 720
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RECARGA = 10
VIDA = 5
REDBUTTON = [213, 56, 56]
REDBUTTONHOVER = [104, 28, 28]
GRIS = [236, 236, 236]


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


def calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots):
    for ovni in ovnis:
        for shot in naveJugador.shots:
            if(pygame.sprite.collide_mask(shot, ovni)):
                naveJugador.shots.remove(shot)
                posicionOvniMuertoX=ovni.rect.centerx
                posicionOvniMuertoY = ovni.rect.centery
                naveJugador.deathOvnis = naveJugador.deathOvnis + 1

                try:
                    ovnis.remove(ovni)
                except:
                    print("")
                naveJugador.score = naveJugador.score + 20
                item = random.randint(1, 10)

                if item == 1:
                    monedas.append(Moneda(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 2:
                    vidas.append(Corazon(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 3:
                    speedUp.append(SpeedUp(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 4:
                    speedDown.append(SpeedDown(posicionOvniMuertoX, posicionOvniMuertoY))

                if item == 5:
                    multiShots.append(MultiShot(posicionOvniMuertoX, posicionOvniMuertoY))


def seguirJugador(naveJugador, ovnis, time):
    for ovni in ovnis:

        if ovni.seguir == 0:
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

        else:
            distanciaX = naveJugador.rect.centerx - ovni.rect.centerx
            distanciaY = naveJugador.rect.centery - ovni.rect.centery

            if distanciaY < 0:
                ovni.rect.centery -= ovni.speed * time
            elif distanciaY > 0:
                ovni.rect.centery += ovni.speed * time

            if distanciaY ==0:
                if distanciaX < 0:
                    ovni.rect.centerx -= ovni.speed * time
                elif distanciaX > 0:
                    ovni.rect.centerx += ovni.speed * time

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


def nuevoOvni(ovnis, isOvnisSpeedingDown):
    posicion=random.randint(0, 5)
    seguir=random.randint(0, 2)
    if posicion == 0:
        newOvni = Ovni(0+20,0+20, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015
        ovnis.append(newOvni)

    if posicion == 1:
        newOvni = Ovni(0+20,WIDTH-10, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015
        ovnis.append(newOvni)

    if posicion == 2:
        newOvni = Ovni(0+20,WIDTH/2, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015
        ovnis.append(newOvni)

    if posicion == 3:
        newOvni = Ovni(HEIGHT-20,0+20, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015
        ovnis.append(newOvni)

    if posicion == 4:
        newOvni = Ovni(HEIGHT/2,0, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015
        ovnis.append(newOvni)

    if posicion == 5:
        newOvni = Ovni(HEIGHT,WIDTH, seguir)
        if (isOvnisSpeedingDown):
            newOvni.speed = 0.015

        ovnis.append(newOvni)


def calcularTiempoDeVidaItems(monedas, vidas, speedUp, multiShots, speedDown):

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

    for speeddown in speedDown:
        speeddown.lifeTime = speeddown.lifeTime-1

        if speeddown.lifeTime <=0:
            speedDown.remove(speeddown)




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


def guardarPuntuacion(name, puntacion, pedirNombre):
    if pedirNombre:
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

        array_usuarios.append(User(parsed_user[0], int(parsed_user[1])))

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
        f.write(i.nombre + ":" + str(i.puntuacion) + "\n")

    f.close()

    return array_usuarios

def escribirNombre(keys):
    letra = pygame.key.key_code(keys)


def readFile(myfont, screen):
    f = open("puntacion.txt", "r")
    posicion = 100

    for x in f:
        textsurface = myfont.render(str(x), False, (0, 0, 0))
        screen.blit(textsurface, (100, posicion))
        posicion = posicion+50

# ---------------------------------------------------------------------

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Hunters")

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

    fase = 1
    background_image = pygame.image.load("./imagenes/Cielo_estrellado.png").convert()

    myfont = pygame.font.Font('./fonts/nasalization-rg.otf', 30)

    tiempoParaNuevoOvni = 50

    clock = pygame.time.Clock()

    opcion = 0
    timeToRead=0
    pedirNombre = False

    nombre=""

    pygame.mixer.music.load('./music/Jeremy Blake - Powerup!.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    while True:
        if opcion == 0:
            click = False
            pedirNombre = False

            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            button_3 = pygame.Rect(50, 300, 200, 50)

            screen.blit(background_image, [0,0])
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)
                if eventos.type == MOUSEBUTTONDOWN:
                    if eventos.button == 1:
                        click = True

            if button_1.collidepoint((mx, my)):
                if click:
                    opcion = 1
                pygame.draw.rect(screen, REDBUTTONHOVER, button_1)
                screen.blit(myfont.render("Jugar", False, WHITE), (70, 100))

            else:
                pygame.draw.rect(screen, REDBUTTON, button_1)
                screen.blit(myfont.render("Jugar", False, BLACK), (70, 100))

            if button_2.collidepoint((mx, my)):
                if click:
                    opcion = 2
                pygame.draw.rect(screen, REDBUTTONHOVER, button_2)
                screen.blit(myfont.render("Ranking", False, WHITE), (60, 200))

            else:
                pygame.draw.rect(screen, REDBUTTON, button_2)
                screen.blit(myfont.render("Ranking", False, BLACK), (60, 200))

            if button_3.collidepoint((mx, my)):
                if click:
                    opcion = 3
                pygame.draw.rect(screen, REDBUTTONHOVER, button_3)
                screen.blit(myfont.render("Salir", False, WHITE), (60, 300))

            else:
                pygame.draw.rect(screen, REDBUTTON, button_3)
                screen.blit(myfont.render("Salir", False, BLACK), (60, 300))

            pygame.display.update()
            clock.tick(60)

        if opcion == 2:
            for eventos in pygame.event.get():

                if not pedirNombre:
                    ranking = guardarPuntuacion(nombre, naveJugador.score, pedirNombre)
                    mostrarPuntuacion = True

                if eventos.type == QUIT:
                    sys.exit(0)
                if eventos.type == pygame.KEYDOWN:
                    if mostrarPuntuacion == False:
                        letra = pygame.key.name(eventos.key)
                        if letra == "return":
                            ranking = guardarPuntuacion(nombre, naveJugador.score, pedirNombre)
                            mostrarPuntuacion = True
                        elif len(letra) == 1 and letra !=":":
                            nombre = nombre + letra
                        elif letra == "backspace":
                            nombre = nombre[0:len(nombre)-1]
                    elif mostrarPuntuacion == True:
                        if pygame.key.name(eventos.key) == "return":
                            opcion = 0
                            naveJugador = Nave()
                            isPlayerSpeedingUp = False
                            isOvnisSpeedingDown = False
                            speedUpEffectTime = 300
                            speedDownEffectTime = 300
                            mostrarPuntuacion = False
                            naveJugador.deathOvnis = 0
                            fase = 1
                            tiempoParaNuevoOvni = 50

            #screen.fill(WHITE)
            screen.blit(background_image, [0,0])

            if mostrarPuntuacion:
                distancia=200
                top=1
                screen.blit(myfont.render("Space Hunters", False, GRIS),
                            (300, 20))
                screen.blit(myfont.render("Ranking", False, GRIS),
                            (300, 120))

                for x in ranking:
                    if not top > 10:
                        screen.blit(myfont.render(str(top) + " - " + x.nombre + ": " + str(x.puntuacion), False, GRIS),(350, distancia))
                        distancia=distancia+35
                    top = top+1
                screen.blit(myfont.render("Pulsa intro para volver a empezar", False, GRIS),
                            (300, distancia+80))
            else:
                textGetName = myfont.render('Introduce tu nombre:', False, GRIS)
                screen.blit(textGetName, (300, 250))
                textGetName = myfont.render(nombre, False, GRIS)
                screen.blit(textGetName, (300, 300))
        pygame.display.flip()

        if opcion == 1:
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
                nuevoOvni(ovnis, isOvnisSpeedingDown)
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
            calculaDisparos(naveJugador, ovnis, monedas, vidas, speedUp, speedDown, multiShots)

            calcularTiempoDeVidaItems(monedas, vidas, speedUp, multiShots, speedDown)

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

                if naveJugador.deathOvnis > 20 + fase:
                    fase = fase + 1
                    naveJugador.deathOvnis = 0

            imagenMoneda = pygame.image.load("imagenes/moneda.png")
            screen.blit(imagenMoneda, (20,20))

            textScore = myfont.render("Monedas: " + str(naveJugador.score), False, GRIS)
            screen.blit(textScore, (60, 13))

            textFase = myfont.render("Fase: " + str(fase), False, GRIS)
            screen.blit(textFase, ((WIDTH/2)-75, 13))

            dibujarVidaRestante(screen, naveJugador)

            if(naveJugador.vida == 0):

                pedirNombre = True
                mostrarPuntuacion = False
                opcion = 2
                ovnis = []
                vidas = []
                monedas = []
                speedUp = []
                speedDown = []
                multiShots = []

            pygame.display.flip()

        if opcion == 3:
            sys.exit()

    return 0


if __name__ == '__main__':
    pygame.init()
    main()