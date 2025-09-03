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

        return 0

gb = GameBoard()
gb.print()