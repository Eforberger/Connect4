from abc import ABC, abstractmethod

class AbstractAgent(ABC):

    ID = 0

    def __init__(self):
        super().__init__()

    def setID(self, value):
        self.ID = value

    def getID(self):
        return self.ID

    @abstractmethod
    def getNextMove(self, boardArray):
        pass

    def checkSpace(self, x, y, boardArray):
        return True if (boardArray[x][y] == self.ID) else False

