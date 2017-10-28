import curses

RIGHT = curses.KEY_RIGHT
LEFT  = curses.KEY_LEFT
SPACE = 32
#
ALIEN  = "M"
ROCKET = "^"
SHOT   = "."
ERASE  = " "
#
X1 = 0
Y1 = 0
X2 = 80
Y2 = 23
#
startX = int((X2 - X1) / 2)
startY = int((Y2 - Y1) / 2)
