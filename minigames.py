import numpy as np
from PIL import Image, ImageDraw, ImageStat
import random

# gameBoard = np.zeros((7, 6))

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.move = 1 # 1 is X, 2 is O.

    def draw(self):
        print(self.board)

    def place(self, x, y):
        if t.check(x, y) not in (1, 2): # Checks if X or O already placed there
            t.board[y - 1, x - 1] = self.move

            return 0
        else:
            return 1
    def check(self, x, y):
        return t.board[y -1, x - 1]

    def checkForWin(self):
        if self.check(1, 1) == self.check(2, 1) == self.check(3, 1):      # Check if won on the first horizontal row
            return self.check(1, 1)
        elif self.check(1, 2) == self.check(2, 2) == self.check(3, 2):    # Check if won on the second horizontal row
            return self.check(1, 2)
        elif self.check(1, 3) == self.check(2, 3) == self.check(3, 3):    # Check if won on the third horizontal row
            return self.check(1, 3)

        elif self.check(1, 1) == self.check(1, 2) == self.check(1, 3):    # Check if won on the first vertical row
            return self.check(1, 1)
        elif self.check(2, 1) == self.check(2, 2) == self.check(2, 3):    # Check if won on the second vertical row
            return self.check(2, 1)
        elif self.check(3, 1) == self.check(3, 2) == self.check(3, 3):    # Check if won on the third vertical row
            return self.check(3, 1)

        elif self.check(1, 1) == self.check(2, 2) == self.check(3, 3):    # Check if won diagonally 1
            return self.check(1, 1)
        elif self.check(3, 1) == self.check(2, 2) == self.check(1, 3):    # Check if won diagonally 2
            return self.check(1, 1)
        else:
            return None

    def isFull(self):
        a = 0
        for list in self.board:
            if 0 in list:
                a += 1
        if a == 0:
            return "tie"
        else:
            return "not full"

    def next(self):
        win = self.checkForWin()
        if win:
            return win
        elif self.isFull():
            return self.isFull()

        if self.move == 1:
            self.move = 2
        elif self.move == 2:
            self.move = 1

"""if __name__ == "__main__":
    t = TicTacToe()

    running = True
    while running:
        t.draw() # Draw the game board
        a = input().split(" ") # Gets x and y and puts it into a tuple
        placed = t.place(int(a[0]), int(a[1])) # Returns 1 if no space there, otherwise 0
        if placed == 1:
            print("There's no space there! Try again!")
        else:
            win = t.next() # Next move, and checks if someone won
            if win in (1, 2): # If someone won
                print(str(win), "wins!")
                input()
                running = False
            elif win == "tie": # Otherwise if it was a tie...
                print("It was a tie.")
                input()
                running = False"""

class FloodIt:
    def __init__(self):
        self.colors = {
            "blue":      (90, 192, 234),
            "orange":    (230, 89, 50),
            "green":     (156, 198, 58),
            "yellow":    (250, 231, 75),
            "pink":      (247, 150, 218),
            "dark_blue": (34, 122, 160)
        }

        self.field = Image.new("RGB", (14, 14))
        pixels = self.field.load()

        for y in range(self.field.height):
            for x in range(self.field.width):
                pixels[y, x] = random.choice(tuple(self.colors.values()))

        self.field = self.field.resize((256, 256))

    def next(self, fill):
        ImageDraw.floodfill(self.field, (0, 0), self.colors[fill])
        # self.field.show()

    def isFull(self):
        extrema = ImageStat.Stat(self.field)._getextrema()
        return extrema.count(extrema[0]) == len(extrema)

if __name__ == "__main__":
    game = FloodIt()
    game.isFull()