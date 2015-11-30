#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame
import random
import time

WIDTH = 500
HEIGHT = 500

pygame.init()
pygame.mixer.init()
pygame.font.init()
gameDisplay = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Star wars')
clock = pygame.time.Clock()

class Object:
    def __init__(self, path_to_image):
        self.x = 250
        self.y = 468
        self.x_change = 0
        self.y_change = 0
        self.image = pygame.image.load(path_to_image)
    def create(self):
        if 0 < self.x + self.x_change < 473:
            self.x += self.x_change
        if 200 < self.y + self.y_change < 468:
            self.y += self.y_change
        gameDisplay.blit(self.image, (self.x, self.y))

def display_score():
    global score
    score += 1
    pygame.display.set_caption('Star wars: ' + str(score))
def check_key(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            ship.x_change = -1
        if event.key == pygame.K_RIGHT:
            ship.x_change = 1
        if event.key == pygame.K_DOWN:
            ship.y_change = 1
        if event.key == pygame.K_UP:
            ship.y_change = -1
        if event.key == pygame.K_SPACE:
            BST.append([ship.x, ship.y])
            pygame.mixer.music.load("fire.mp3")
            pygame.mixer.music.play()

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and ship.x_change != 1:
            ship.x_change = 0
        if event.key == pygame.K_RIGHT and ship.x_change != -1:
            ship.x_change = 0
        if event.key == pygame.K_UP and ship.y_change != 1:
            ship.y_change = 0
        if event.key == pygame.K_DOWN and ship.y_change != -1:
            ship.y_change = 0
def check_bang():
    global TG, BST
    for j, i in enumerate(TG):
        x1 = i[0]
        y1 = i[1]
        for j1, i1 in enumerate(BST):
            x2 = i1[0] + 14
            y2 = i1[1] - 3
            if ((x1-x2)**2 + (y1-y2)**2) ** .5 <= 10:
                TG[j] = ()
                BST[j1] = ()
                display_score()
                pygame.mixer.music.load("bang.mp3")
                pygame.mixer.music.play()
            BST = [i for i in BST if i]
    TG = [i for i in TG if i]
def bluster():
    for j, i in enumerate(BST):
        x = i[0]
        y = i[1]
        pygame.draw.line(gameDisplay,
                         (250, 0, 0),
                         (x+14, y), (x+14, y-3),  1)
        if y < 0:
            BST.pop(j)
        else:
            BST[j][1] = y-2
def target():
    global tg_clock
    if time.time() > tg_clock and len(TG) < 3:
        TG.append([random.randint(10, WIDTH-10), 0])
        tg_clock = time.time() + random.random()
    for j, i in enumerate(TG):
        pygame.draw.circle(gameDisplay,
                           (250, 250, 250), i, 10)
        if TG[j][1] > 510:
            TG.pop(j)
        else:
            TG[j][1] += 1


TG = []
BST = []
score = 0
tg_clock = time.time()
ship = Object('ship.png')

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            continue
        check_key(event)

    gameDisplay.fill((0, 0, 0))
    ship.create()
    check_bang()
    bluster()
    target()

    pygame.display.update()
    clock.tick(100)
