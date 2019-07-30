import AI, Person


class Game:

    board = [0]*5 [0]*5
    agent1 = AI()
    agent2 = Person()

    def __init__(self):
        pass

    def gameLoop(self):
        gameOver = False

        while not gameOver:
            agent1.getNextMove()
            agent2.getNextMove()
            self.checkWin()

    def checkWin(self):
        for i in len(board):
            for j in len(board[i]):
                # vertical
                
                # horizontal
                # diagonal
                pass









