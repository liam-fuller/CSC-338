import sys
import math
import random
######################################
# Todo

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
        count_1 = sum(cc == 1 for row in bd for cc in row)
        count_2 = sum(cc == 2 for row in bd for cc in row)
        return 1 if count_1 == count_2 else 2
    
    def getmoves(self):
        return [(r,c) for r in range(3) for c in range(3) if self.entries[r][c]==0] # all possible position where the board is empty
    
    def copy(self):
        new_board = GameBoard()
        new_board.entries = [row[:] for row in self.entries]
        return new_board
         
            

class TicTacToeGame:

    def __init__(self, player):

        self.gameboard = GameBoard()
        self.turn = player
        self.ai = MCTS()
        if player == 1:
            self.ai.turn = 2
        else:
            self.ai.turn = 1
        self.turnnumber = 0


    def playturn(self):
        # print("Turn:", self.turn)
        print("Turn number: ", self.turnnumber)
        self.turnnumber += 1
        
        self.gameboard.print_bd()

        # print(self.turnnumber)
        legal_moves = [(r,c) for r in range(3) for c in range(3) if self.gameboard != 0]
        

        if self.turn == 1:
            print("Human, please choose a space!")
            validinput = False
            self.turn = 2
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
            #fix this for mcts
            print("AI is thinking...")
            move,_,next_bd = self.ai.MCTS_move(self.gameboard)
            if move is None:
                print("No valid moves left.")
                return  # don’t try to play a move
            print("AI chooses move: ", move,)
            self.gameboard.entries[move[0]][move[1]] = 2
            self.turn = 1




class MCTSNode:
    def __init__(self, bd: GameBoard, parent: None, action: None):
        self.bd = bd             
        self.parent = parent
        self.action = action # action that led to this node          
        self.children = [] # list of child nodes
        self.possible_moves = bd.getmoves()  # moves that can be played from this node
        self.visits = 0
        self.wins = 0.0         

    def is_fully_expanded(self):
        return len(self.possible_moves) == 0
    
    def is_terminal(self):
        return self.bd.checkwin() != 0
    
def apply_action(bd:GameBoard, action, player):
    r,c = action        
    new_bd = bd.copy()
    new_bd.entries[r][c] = player
    return new_bd

class MCTS:
    def __init__(self, c = math.sqrt(2)):
        self.c = c

    
    def uct_select(self, node:MCTSNode, c = None) -> MCTSNode:
        # node: current node
        # return: child node with highest UCT value
        if c is None:
            c = self.c
        return max(node.children, key=lambda child: (child.wins / child.visits) + c*math.sqrt(math.log(node.visits)/child.visits))

    def expand(self, node:MCTSNode) -> MCTSNode:
        # node: current node
        # return: new child node after applying one of the possible moves

        action = node.possible_moves.pop()
        r,c = action

        child_bd = node.bd.copy()
        player = child_bd.check_nextplayer(child_bd.entries)
        child_bd = apply_action(child_bd, action, player)

        child_node = MCTSNode(child_bd, parent=node, action = action)
        node.children.append(child_node)
        return child_node
    
    def rollout(self,bd:GameBoard) -> int:
        # bd: current board
        # return: score on the same (+1: for winner player)
        
        rollout_bd = bd.copy()

        while rollout_bd.checkwin() == 0:
            next_player = rollout_bd.check_nextplayer(rollout_bd.entries)
            actions = rollout_bd.getmoves()
            if not actions:
                break
            action =random.choice(actions)
            rollout_bd = apply_action(rollout_bd, action, next_player)
        
        winner = rollout_bd.checkwin()
        if winner ==1 or winner ==2:
            return +1
        else:
            return 0
        
    def backpropagate(self, node:MCTSNode, reward:int):
        current = node
        while current is not None:
            current.visits += 1
            current.wins += reward
            # switch perspective
            reward = -reward

            #propagate to parent
            current = current.parent
    
    def search(self,root:MCTSNode, iter = 2000):
        # based on the rood board, run MCTS and return the best action
        #root = MCTSNode(root_bd, parent=None, action=None)
        root_bd = root.bd
        if root_bd.checkwin() != 0:
            raise ValueError("Game is over")
        
        for _ in range(iter):
            node = root

            # selection
            while (not node.is_terminal()) and node.is_fully_expanded():
                node = self.uct_select(node, c= self.c)
            
            # expansion
            if (not node.is_terminal()) and (not node.is_fully_expanded()):
                node = self.expand(node)

            # simulation 
            reward = self.rollout(node.bd)

            # backpropagation
            self.backpropagate(node, reward)
        self.c = 0
        best_child = self.uct_select(root,c=0)
        return best_child.action

    

    def MCTS_move(self,root_state: GameBoard, iterations=2000):
        mcts = MCTS()
        root_node = MCTSNode(bd = root_state, parent= None, action=None)
            
        best_action = mcts.search(root_node, iter=iterations)
        player = root_state.check_nextplayer(root_state.entries)
        next_state = apply_action(root_state, best_action, player)
            
        return best_action, player, next_state

if not True:
    bd = GameBoard()
    print('-------- before move ----------')
    bd.entries = [[1,0,0],[0,2,0],[0,0,0]]
    bd.print_bd()
    print('-------- after MCTS move ----------')
    best_action, next_player, next_bd = MCTS_move(bd, iterations=1000)
    print("Best action:", best_action, "for player", next_player)
    next_bd.print_bd()
    print('----------------------------------')

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


while True:
    try:
        player = int(input("Do you wish to play as 1's or 2's: "))
        if player == 1 or player == 2:
            break
        else:
            raise ValueError
        
    except Exception:
        print("Please enter a 1 or a 2")

game = TicTacToeGame(player)

while True:
    game.gameboard.print_bd()
    if game.gameboard.checkwin() != 0:
        break
    #implement input checking and prinnting results
    game.playturn()

if game.gameboard.checkwin() != 3:
    print(f'The winner is player {game.gameboard.checkwin()}')
else:
    print(f"The game is a draw")