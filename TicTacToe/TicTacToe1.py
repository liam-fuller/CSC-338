import sys
######################################
# Todo
# 1. rewrite the code under the class setting
# 2. add alpha-beta pruning
# 3. Monte Carlo Tree Search
######################################

WIN_LINES = [
    [(0,0),(0,1),(0,2)],  # rows
    [(1,0),(1,1),(1,2)],
    [(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],  # cols
    [(0,1),(1,1),(2,1)],
    [(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],  # diagonals
    [(0,2),(1,1),(2,0)]
]


class GameBoard:

    def __init__(self):

        self.entries = [[0, 0, 0], [0, 0, 0], [0, 0 ,0]]
        self.state = 0
        # State 0: Game playing
        # State 1: Player 1 wins
        # State 2: Player 2 wins
        # State 3: draw

    def print_bd(self):

        for i in range(3):
            for j in range(3):
                print(self.entries[i][j],end='')
            print('')



    def checkwin(self) -> int:
        
        for line in WIN_LINES:
            vals = [self.entries[r][c] for r,c in line]
            if vals == [1, 1, 1]:   
                return 1
            if vals == [2, 2, 2]:
                return 2
            
        if any(0 in row for row in self.entries):
            return 0

        return 3
    
    def check_nextplayer(self, bd = None):
        #count how many 1 and 2 in bd
        count_1 = sum(cc == 1 for row in bd for cc in row)
        count_2 = sum(cc == 2 for row in bd for cc in row)
        
        if count_1 > count_2:
            return 2
        else:
            return 1
    

    def minmax(self, bd=None, depth=0):
        # set default player to 1(X) cause it is the first player
        # score for x: +, score for o:-
        # return (move, score)
        
        result = self.checkwin()
        if result == 1: 
            return None, 10-depth # x win, prefer faster wins 
        if result == 2: 
            return None, depth-10 # o win, prefer slower losses 
        if result == 3: 
            return None, 0 #draw
        


        moves = [(r,c) for r in range(3) for c in range(3) if bd[r][c]==0] # all possible position where the board is empty
        #So if these are valid moves then could we make the inverse of this containing all positons where the board is not empty then
        #When they input a move we can check if it is in illegal moves before we do anything
        #Or should we just check if the move isnt in the moves list then it must be an illegal move
        player = self.check_nextplayer(bd)
        

        if player == 1: # x's turn, maximize
            best = -1e9 # initilize to very small number
            move = None 
            for r,c in moves:
                bd[r][c]=1 # if x plays here
                _,score=self.minmax(bd,depth+1) # o's turn 
                bd[r][c]=0 # undo move
                
                if score>best: # pick the move with the largest score
                    best,move=score,(r,c)
            return move,best
        
        else: # o's turn, minimize     
            best = 1e9 # initilize to very large number
            move=None
            for r,c in moves:
                bd[r][c]=2
                _,score=self.minmax(bd,depth+1) # x's turn
                bd[r][c]=0
                
                if score<best: # pick the move with the smallest score
                    best,move=score,(r,c)
            return move,best
        
            

class TicTacToeGame:

    def __init__(self):

        self.gameboard = GameBoard()
        self.turn = 1
        self.turnnumber = 0


    def playturn(self):
        print("Turn number: ", self.turnnumber)
        self.turnnumber += 1
        
        self.gameboard.print_bd()

        print(self.turnnumber)
        legal_moves = [(r,c) for r in range(3) for c in range(3) if self.gameboard != 0]
        

        if self.turn == 1:
            print("Human, please choose a space!")
            validinput = False
            # print(legal_moves)
            legal_moves = [(r, c) for r in range(3) for c in range(3) if self.gameboard.entries[r][c] == 0]
            # print("Available moves:", legal_moves)

        while not validinput:
            user_input = input("Enter two numbers separated by a comma (row,col): ")

            try:
                move = tuple(map(int, user_input.split(',')))

                if move in legal_moves:
                    humanrow, humancol = move
                    self.gameboard.entries[humanrow][humancol] = 1
                    validinput = True
                else:
                    print("That space is already taken or invalid. Try again.")

            except Exception:
                print("Invalid input. Please use format: row,col (e.g. 1,2)")

        else:
            print("AI is thinking...")
            move, score = self.gameboard.minmax(self.gameboard.entries)
            if move is None:
                print("No valid moves left.")
                return  # don’t try to play a move
            print("AI chooses move: ", move, " with score: ", score)
            self.gameboard.entries[move[0]][move[1]] = 2
            self.turn = 1





game = TicTacToeGame()

while game.gameboard.state == 0:
    game.playturn()
    game.gameboard.state = game.gameboard.checkwin()
    print(' ')

game.gameboard.print_bd()
if game.gameboard.state == 1:
    print("Player 1 wins!")
elif game.gameboard.state == 2:
    print("Player 2 wins!")
else:
    print("The game is a draw!")

