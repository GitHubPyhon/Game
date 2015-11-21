#!/usr/bin/python3
import tkinter
import random
import time

WIDTH = 500
HEIGHT = 400

class Window:
    def __init__(self):
        self.direction = 'right'
        self.food = []
        self.worm = [[10, 10], [15, 10], [20, 10]]
        self.canvas = tkinter.Canvas(root,
                                width=WIDTH,
                                height=HEIGHT)
        root.bind('<Key>', self.direct)
        root.title('Snake')
        self.canvas.pack()
    def direct(self, event = None):
        if event:
            if event.keycode == 111 and self.direction != 'down':
                self.direction = 'up'
            elif event.keycode == 116 and self.direction != 'up':
                self.direction = 'down'
            elif event.keycode == 113 and self.direction != 'right':
                self.direction = 'left'
            elif event.keycode == 114 and self.direction != 'left':
                self.direction = 'right'

        if self.direction == 'down':
            self.x = self.worm[-1][0]
            self.y = self.worm[-1][1] + 6
        elif self.direction == 'up':
            self.x = self.worm[-1][0]
            self.y = self.worm[-1][1] - 6
        elif self.direction == 'right':
            self.x = self.worm[-1][0] + 6
            self.y = self.worm[-1][1]
        elif self.direction == 'left':
            self.x = self.worm[-1][0] - 6
            self.y = self.worm[-1][1]
    def reset(self):
        self.canvas.delete('all')
        self.worm = [[10, 10], [15, 10], [20, 10]]
        self.direction = 'right'
        self.end = False
        self.food = []
        self.x = 10
        self.y = 10


class Point(Window):
    def draw(self, xy):
        x = (WIDTH + xy[0]) % WIDTH
        y = (HEIGHT + xy[1]) % HEIGHT
        return self.canvas.create_oval(x-3, y+3, x+3, y-3, fill='black')
    def eat(self):
        if not self.food:
            x = random.randint(5, WIDTH - 5)
            y = random.randint(5, HEIGHT - 5)
            self.food.append([x, y, self.draw((x,y))])
        if ((self.x - self.food[0][0])**2 + (self.y - self.food[0][1])**2) ** .5 < 6:
            return True
        else:
            return False


class Snake(Point):
    def move(self):
        self.direct()
        if self.x < 0 or self.y < 0 or self.x > WIDTH - 1 or self.y > HEIGHT - 1:
            for i in range(5):
                s = 'Game over - ' + str(5 - i) + ' sec'
                root.title(s)
                root.update()
                time.sleep(1)
                if i == 4:
                    root.title('Snake')
                    root.update()
            self.reset()
        self.worm.append([self.x, self.y, self.draw([self.x, self.y])])
        if self.eat():
            self.canvas.delete(self.food[0][-1])
            self.food.pop(0)
        else:
            self.worm.pop(0)
        root.update()
        time.sleep(0.1)
        self.canvas.delete(self.worm[0][-1])


if __name__ == '__main__':
    root = tkinter.Tk()
    snake = Snake()
    while True:
        snake.move()
    root.mainloop()
