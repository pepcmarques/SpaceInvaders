#!/bin/env python

##################################
__author__ = "Paulo Marques"
__copyright__ = ""
__credits__ = ["Paulo Marques"]
               
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Paulo Marques"
__email__ = ""
__status__ = "Production"
##################################

import curses
import os
import random
import sys
import time
import threading
from time import sleep
from settings import RIGHT, LEFT, SPACE, ALIEN, ROCKET, SHOT, ERASE, X1, Y1, X2, Y2, startX, startY 


def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
     sys.stdout.flush()


class Position(object):
    def __init__(self, x, y):
        super(Position, self).__init__()
        self.x = x
        self.y = y


class PositionAlien(Position):
    def __init__(self, x, y, direction):
        super(PositionSnake, self).__init__(x, y)
        self.direction = direction
        self.sleep     = 0.5


class Rocket():
    def __init__(self):
        self.x = int((X2 - X1)/2)
        self.y = Y2
        self.direction = 0

    def move(self):
        print_there(self.x, self.y, ERASE)
        if self.direction == RIGHT:
           self.x = self.x + 1
        elif self.direction == LEFT:
           self.x = self.x - 1
        else:
           self.x = self.x # just to know it will be static
        print_there(self.x, self.y, ROCKET)
        self.hitTheWall()

    def hitTheWall(self):
        if (self.x == X1+2) or (self.x == X2-1):
           self.direction = 0

    def process_event(self, e):
        if (e == RIGHT):
           self.direction = RIGHT
        elif (e == LEFT):
           self.direction = LEFT


class Shot():
    def __init__(self, rocket):
       self.x = rocket.x
       self.y = rocket.y - 1

    def move(self):
       print_there(self.x, self.y, ERASE)
       self.y = self.y - 1
       print_there(self.x, self.y, SHOT)

    def hitAlien(self):
       global aliens
       i = 0
       for a in aliens.group:
           if ((self.x == a.x) and (self.y == a.y)):
              print_there(a.x, a.y, ERASE)
              aliens.group.pop(i)
              return True
           i += 1
       return False

    def hitTheWall(self):
       if (self.y == Y1+1):
         print_there(self.x, self.y, ERASE)
         return True
       return False

    def shotWorker(self):
        global aliens
        while (not self.hitAlien()) and (not self.hitTheWall()):
           self.move()
           sleep(0.1)


class Alien():
    def __init__(self, x, y, part):
        self.x = x
        self.y = y
        self.part = part


class AlienGroup(object):
    _instance = None

    def __init__(self):
        self.group = []
        self.direction = RIGHT
        for i in range(2,40,4):
            for j in range(2, 6):
                self.group.append(Alien(i, j, ALIEN))
        self.initialSize = len(self.group)

    @staticmethod
    def instance():
        if AlienGroup._instance == None:
           AlienGroup._instance = AlienGroup()
        return AlienGroup._instance

    def move(self):
        if self.direction == RIGHT:
           inc = 1
        elif self.direction == LEFT:
           inc = -1
        for a in self.group:
            print_there(a.x, a.y, ERASE)
            a.x += inc
            print_there(a.x, a.y, a.part)

    def hitTheWall(self):
        for a in self.group:
            if ((a.x == X1+2) or (a.x == X2-1)):
               if self.direction == RIGHT:
                  self.direction = LEFT
               else:
                  self.direction = RIGHT
               return True
        return False

    def invaded(self):
        for a in self.group:
            if (a.y == Y2):
               return True
        return False

    def goDown(self):
        inc = 1
        for a in self.group:
            print_there(a.x, a.y, ERASE)
            a.y += inc
        for a in self.group:
            print_there(a.x, a.y, a.part)

    def aliensWorker(self):
        global aliens
        global THE_END
        while (len(self.group) > 0) and (not self.invaded()):
            self.move()
            if self.hitTheWall():
               self.goDown()
            sleep(len(self.group)/(self.initialSize * 2.0))
        THE_END = True


def realtime(THE_END=False):

    global aliens
    aliens = AlienGroup.instance()

    alienThread = threading.Thread(target=aliens.aliensWorker, args=())
    alienThread.start()
    sleep(1)

    rocket = Rocket()

    counter = 0

    level = 1

    while not THE_END:

          rocket.move()

          if aliens.invaded():
             THE_END = True

          char = screen.getch()
          if (char == ord('q')):
             THE_END = True
          elif char in [RIGHT, LEFT]:
             rocket.process_event(char)
          elif char == SPACE:
             shot = Shot(rocket)
             shotThread = threading.Thread(target=shot.shotWorker, args=())
             shotThread.start()
          else:
             print_there(0,25, char)

          sleep(0.1)

    msg = "G   A   M   E     O   V   E   R"
    print_there(int((X2 - X1)/ 2) - int(len(msg))/2,int((Y2 - Y1)/2), msg)
    sleep(3)
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    os._exit(0)


#####################################
# BEGIN                             #
#####################################

# get the curses screen window
screen = curses.initscr()
#
# turn off input echoing
curses.noecho()
#
# respond to keys immediately (don't wait for enter)
screen.nodelay(True)
curses.cbreak()
#
# map arrow keys to special values
screen.keypad(True)
#
# DRAW FIELD
#
screen.addstr(Y1, X1, (X2-X1)*"-")
for y in range(Y1+1, Y2):
    screen.addstr(y, X1, "|")
    screen.addstr(y, X2-1, "|")
screen.addstr(Y2, X1, (X2-X1)*"-")

if __name__ == '__main__':
   os.system('clear')
   realtime()
