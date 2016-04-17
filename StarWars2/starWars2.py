#!/usr/bin/python3
import pygame
import thsocket
from ship import Ship
from random import randint


class Asteroid:
    def __init__(self):
        self.x = randint(10, 490)
        self.y = 600

    def draw(self):
        self.y += 1
        if self.y > 510:
            if server.isServer():
                self.y = -10
                self.x = randint(10, 490)
                server.send('*asteroid ' + str(self.x) + ' ' + str(self.y) + '*')
        pygame.draw.circle(game.gameDisplay, (0,0,200), (self.x, self.y), 10)


class Shoot:
    def __init__(self):
        self.x = 0
        self.y = -1

    def createShoot(self):
        if self.y < 0 and (server.isServer() or client.isClient()):
            self.x = ship_1.x + 16
            self.y = ship_1.y
            if server.isServer():
                server.send('*shoot ' + str(self.x) + ' ' + str(self.y) + '*')
            if client.isClient():
                client.send('*shoot ' + str(self.x) + ' ' + str(self.y) + '*')
            self.playSong('shoot.mp3')

    def playSong(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    def draw(self):
        self.y -= 2
        if server.isServer():
            if ((shoot_1.x - asteroid.x) ** 2 + (shoot_1.y - asteroid.y) ** 2) ** .5 <= 12:
                shoot_1.x = -1
                shoot_1.y = -1
                asteroid.y = 600
                asteroid.x = randint(10, 490)
                server.send('*shoot -1 -1*asteroid ' + str(asteroid.x) + ' 600*')
                self.playSong('bang.mp3')
                game.player1 += 1
        elif client.isClient():
            if ((shoot_1.x - asteroid.x) ** 2 + (shoot_1.y - asteroid.y) ** 2) ** .5 <= 12:
                shoot_1.x = -1
                shoot_1.y = -1
                asteroid.y = 600
                asteroid.x = randint(10, 490)
                client.send('*shoot -1 -1*asteroid ' + str(asteroid.x) + ' 600*')
                self.playSong('bang.mp3')
                game.player2 += 1
        pygame.draw.circle(game.gameDisplay, (250,0,0), (self.x, self.y), 2)


class InputBox:
    def __init__(self):
        self.ip = ''
        self.visible = False
        self.white = (250, 250, 250)

    def check(self):
        # If pressed key 'ENTER'
        if event.key is pygame.K_RETURN:
            if self.visible:
                self.visible = False
                if self.ip == 'start' and not (server.is_alive() or client.is_alive()):
                    server.start()
                elif not (server.is_alive() or client.is_alive()):
                    client.connect(self.ip)
                    if client.isClient():
                        client.start()
                        print('start')
            else:
                self.visible = True

        # If pressed key 'BACKSPACE'
        elif event.key is pygame.K_BACKSPACE:
            if self.visible and self.ip:
                self.ip = self.ip[:-1]

        # If pressed keys '0-9 or a-z'
        else:
            if self.visible:
                if event.key is 46 and len(self.ip) < 15:
                    self.ip += '.'
                elif 47 < event.key < 58 or 96 < event.key < 123:
                    if len(self.ip) < 14:
                        self.ip += chr(event.key)

    def show(self):
        pygame.draw.rect(game.gameDisplay, self.white, (150, 250, 200, 30), 1)
        ip = game.font.render(self.ip, 1, self.white)
        game.gameDisplay.blit(ip, (157, 257))


class Screen:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.stop = False
        self.player1 = 0
        self.player2 = 0
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Star wars 2.0')
        self.gameDisplay = pygame.display.set_mode((500, 500))
        self.font = pygame.font.Font(None, 25)
        self.score1 = pygame.font.Font(None, 23)
        self.score2 = pygame.font.Font(None, 23)

    def gameOver(self):
        self.stop = True
        if server.is_alive():
            server.close()
            server.join()
        if client.is_alive():
            client.close()
            client.join()

    @staticmethod
    def restart(ship1, ship2):
        ship_1.x, ship_1.y = ship1
        ship_2.x, ship_2.y = ship2


inputBox = InputBox()
game = Screen()
ship_1 = Ship()
ship_2 = Ship()
shoot_1 = Shoot()
shoot_2 = Shoot()
asteroid = Asteroid()
server = thsocket.Server(game, ship_2, asteroid, shoot_2)
client = thsocket.Client(game, ship_2, asteroid, shoot_2)

while not game.stop:

    game.gameDisplay.fill((0, 0, 0))
    game.gameDisplay.blit(game.score1.render(str(game.player1), 1, inputBox.white), (15, 10))
    game.gameDisplay.blit(game.score2.render(str(game.player2), 1, inputBox.white), (480, 10))
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            game.gameOver()
            continue
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            ship_1.updatePosition(event)
            if server.isServer():
                server.send('*ship ' + str(ship_1.x_change) + ' ' + str(ship_1.y_change) + '*')
            if client.isClient():
                client.send('*ship ' + str(ship_1.x_change) + ' ' + str(ship_1.y_change) + '*')
            if event.type is pygame.KEYDOWN:
                inputBox.check()
                if event.key is pygame.K_SPACE:
                    shoot_1.createShoot()

    ship_1.draw(game)
    shoot_1.draw()
    asteroid.draw()

    if inputBox.visible:
        inputBox.show()
    if server.isServer() or client.isClient():
        ship_2.draw(game)
        shoot_2.draw()

    pygame.display.update()
    game.clock.tick(100)

pygame.quit()
