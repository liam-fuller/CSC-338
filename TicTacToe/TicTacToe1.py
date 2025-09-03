import sys

class GameBoard:

    def __init__(self):

        self.entries = [ [0,0,0], [0,0,0], [0,0,0] ] # 3x3 grid of 0s
        self.state = 0
        #State 0: Game playing
        #State 1: Player 1 wins
        #State 2: Player 2 wins
        #State 3: Draw

    def print(self):
        for i in range (3):
            for j in range (3):
                print(self.entries[i][j], end = '')
            print('')
       
            

    def checkwin(self) -> int:

        for line in WIN_LINES:
            vals = [self.entries[r][c] for r,c in line]
            if vals == [1,1,1]:
                self.state = 1
                return 1
            if vals == [2,2,2]:
                self.state = 2
                return 2
        if any(0 in row for row in self.entries):
            self.state = 0
            return 0
        self.state = 3
        return 3




gb = GameBoard()
gb.print()

