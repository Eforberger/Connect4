from AI import AI
from Person import Person
import operator, numpy

# https://gist.github.com/ABIR-JT/4704533
# TO DO: make it so that check sequence only checks for sequences at one spot, then change the looping to outside its call (so that cal can do the layer stuff)
# import stuff
# run code
# https://gist.github.com/ABIR-JT/4704533

class Game:

    # Constants
    ROWS = 6
    COLUMNS = 7
    DIRECTIONS = {  # for convenience
        'n': (-1, 0),
        'ne': (-1, 1),
        'e': (0, 1),
        'se': (1, 1),
        's': (1, 0),
        'sw': (1, -1),
        'w': (0, -1),
        'nw': (-1, -1)
    }

    # Make an empty board
    board = numpy.zeros(shape=(ROWS, COLUMNS), dtype=int)

    #board = [0]*5 [0]*5
    agent1 = AI()
    agent1.setID(123)
    agent2 = Person()
    agent2.setID(124)


    def __init__(self):
        pass

    def gameLoop(self):
        gameOver = False

        while not gameOver:
            self.agent1.getNextMove()
            self.agent2.getNextMove()
            self.checkWin()

    # <editor-fold desc="Description">
   # def checkWin(self):
       # for i in len(board):
          #  for j in len(board[i]):
                # vertical
                
                # horizontal
                # diagonal
              #  pass
    # </editor-fold>



    def print_board(self):
        # Flip the board upside down, so 0,0 is bottom left instead of top left, then print each row
        for line in reversed(self.board):
            print("|", end="", flush=True)
            for cell in line:
                print("Z" if cell == self.agent1.getID() else "X" if cell == self.agent2.getID() else cell, end="", flush=True)
            print("|")


    def add_disc(self, column, playerID):

        # Validate column and player numbers
        if not column < self.COLUMNS:
            print("Invalid column number! Try again.")
            return False

        # Swap the dimensions to make it easier to loop through
        sboard = numpy.swapaxes(self.board, 0, 1)
        # Put the piece in the first available spot in the specified column
        for row, cell in enumerate(sboard[column]):
            print("row", row) # testing
            #if not cell:
            if not cell:
                sboard[column, row] = playerID
                self.board = numpy.swapaxes(sboard,0,1)
                self.print_board() # testing
                print("----------") # testing
                return True

        # If we get here, then it should be because nothing can be placed here
        return False

    # Returns the player no. if someone has won
    def check_win(self):
        # Only time multiple wins are found should be when a token is placed in a spot
        # that completes two sequences, provided this function is called after every move
        # This means it should be fine to just take the first item in the 'wins' list to
        # determine the winner
        # TODO: win message
        wins = self.check_sequence(4)
        return wins[0]['player'] if wins else None

    # Very basic, easy-to-beat computer opponent
    def make_computer_move(self):
        self.check_win()

        # Check for any sequence of 3, then 2, then 1
        for i in range(1,4):
            nearWins = self.check_sequence(i)
            if nearWins:
                # Prioritize winning over blocking opponent, if possible
                for nearWin in nearWins:
                    if nearWin['player'] == 2 and not self.get_next_in_sequence(nearWin):
                        self.add_disc(nearWin['column'], 2)
                        return True

                # Otherwise, just block the first opponent move it finds.  In the future, it would be nice
                # if positions where multiple opponent sequences could be blocked were prioritised.
                for nearWin in nearWins:
                    if not self.get_next_in_sequence(nearWin):
                        self.add_disc(nearWin['column'], 2)
                        return True

        # If this point is reached, just randomly add tokens (I did mention this was basic)
        for column in range(self.COLUMNS):
            d = self.add_disc(column,2)
            if d: return True


    def get_next_in_sequence(self, sequence):
        (x, y) = tuple( map(
            operator.add,
            (sequence['row'], sequence['column']),
            tuple( map(
                operator.mul,
                (sequence['length'], sequence['length']),
                self.DIRECTIONS[sequence['direction']])
            )
        ))
        return self.board[x][y]

    def check_sequence(self, length):
        sequences = []
        for x,column in enumerate(self.board):
            for y,cell in enumerate(self.board[x]):
                if cell:
                    adjacentCells = self.get_next_values(x,y)
                    for direction,value in adjacentCells.iteritems():

                        # The function will check every spot, so no need to look upwards or backwards
                        if value and direction not in ("nw", "n", "ne", "w", "x"):

                            # Check if the same value is in the next cell, and that it's not already part of a sequence
                            # that has already been checked
                            (prevX, prevY) = tuple(map(operator.add, tuple(map(operator.mul, (-1,-1), self.DIRECTIONS[direction])), (x,y)))
                            if value == cell and self.board[prevX,prevY] != cell:
                                sLength = self.follow_sequence(x, y, direction)
                                if sLength >= length:
                                    sequences.append({"row": x, "column":y, "player": value, "direction": direction, "length": sLength})
        return sequences

    # Returns the length of sequence in the direction specified
    def follow_sequence(self, row, column, direction):
        if direction not in self.DIRECTIONS:
            print("Invalid direction in follow_sequence")
            return False

        if not (row < self.COLUMNS and column < self.ROWS):
            print("Invalid row/column.")
            return False

        player = self.board[row,column]
        v = player
        length = 0
        (x2, y2) = tuple(map(operator.add, (row,column), self.DIRECTIONS[direction]))
        while v == player:
            v = self.board[x2,y2]
            length += 1
            (x2, y2) = tuple(map(operator.add, (x2,y2), self.DIRECTIONS[direction]))
        return length


    # Returns a dictionary with the values of the surrounding points
    def get_next_values(self, column, row):
        if not (column < self.COLUMNS and row < self.ROWS):
            print("Invalid row/column.")
            return False

        # Pad board with -1, so we don't get any index errors
        paddedBoard = numpy.empty((self.ROWS+2, self.COLUMNS+2), dtype=int)
        paddedBoard[:,:] = -1
        paddedBoard[1:self.ROWS+1, 1:self.COLUMNS+1] = self.board.reshape(self.ROWS, self.COLUMNS)

        # Get the surrounding cells
        return dict(zip(["nw", "n", "ne", "w", "x", "e", "sw", "s", "se"], (paddedBoard[column:column+3, row:row+3]).ravel()))

game = Game()
game.board[0][0]=1 # testing
game.add_disc(1, 123)
game.add_disc(2, 124)
game.add_disc(2, 123)
game.add_disc(3, 124)
game.add_disc(3, 223)
game.add_disc(3, 224)
game.print_board()








