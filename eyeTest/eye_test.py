#!/usr/bin/python3

import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from random import random, randint
from kivy.core.window import Window
from kivy.uix.stacklayout import StackLayout

Window.fullscreen = True

class EyeTest(StackLayout):
    def __init__(self):
        super(EyeTest, self).__init__()
        self.cell = 2
        self.score = 0
        self.time = 15
        self.alpha = 0.2
        self.end = False
        self.btnList = []
        self.sizeHint = (.5, .45)
        self.layout = StackLayout()
        self.currentTime = time.time()
        self.luckyNumber = randint(0, 3)
        self.label = Button(text = 'Score: 0  Time - 15 sec.',
                            on_press = self.restart,
                            size_hint = (1, .1))

        self.add_widget(self.label)
        self.add_widget(self.layout)
        

    def checker(self, instance):
        if not self.end:
            # If chosen correct number
            if self.luckyNumber == int(instance.id):
                self.time = 15
                self.score += 1
                if self.cell < 5 and self.score % self.cell == 0:
                    self.cell += 1
                if self.score % 3 == 0 and self.alpha > 0.05:
                    self.alpha -= 0.01
                self.luckyNumber = randint(0, self.cell ** 2 - 1)
                self.sizeHint = (1 / self.cell, .9 / self.cell)

                # Delete old buttons
                for i in self.btnList:
                    self.layout.remove_widget(i)
                self.btnList = []

                self.addSetOfButton()

            # If chosen incorrect number
            else:
                self.time -= 3
                if self.time <= 0:
                    self.gameOver()
            
    def addSetOfButton(self):
        color = self.rgba()

        # Add new buttons
        for i in range(self.cell ** 2):
            btn = self.getButton(i, color)
            self.btnList.append(btn)
            self.layout.add_widget(btn)

        color[3] -= self.alpha
        # Change background_color random button
        btn = self.btnList[self.luckyNumber]
        btn.background_color = color

    def rgba(self):
        r, g, b = [random() for i in range(3)]
        return [r, g, b, 1]

    def getButton(self, id, color):
        return Button(id = str(id),
                      on_press = self.checker,
                      size_hint = self.sizeHint,
                      background_color = color)

    def updateTimer(self, dt):
        if not self.end:
            if time.time() - self.currentTime >= 1:
                self.currentTime = time.time()
                self.time -= 1

            self.label.text = 'Score: ' + str(self.score) + ' Time - ' + str(self.time) + ' sec.'
            if self.time <= 0:
                self.gameOver()

    def gameOver(self):
        self.end = True
        self.label.text = 'Game Over your score: <<< ' + str(self.score) + ' >>> - Press to play again'
        self.luckyNumber = randint(0, 3)
        self.sizeHint = (.5, .45)
        self.alpha = .2
        self.time = 16
        self.score = 0
        self.cell = 2

    def restart(self, instance):
        if self.end:
            # Delete old buttons
            for i in self.btnList:
                self.layout.remove_widget(i)
            self.btnList = []

            self.end = False
            self.addSetOfButton()


class EyeTestApp(App):
    def build(self):
        game = EyeTest()
        game.addSetOfButton()
        Clock.schedule_interval(game.updateTimer, .1)
        return game


if __name__ == '__main__':
    EyeTestApp().run()
