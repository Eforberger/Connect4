from abs import ABC, abstractmethod

class AbstractAgent(ABC):

    ID = 0

    def __init__(self,value):
        self.value = value
        super().__init__()

    @abstractmethod
    def getID(self):
        pass

    @abstractmethod
    def getNextMove(self, boardArray):
        pass

    def checkSpace(self, x, y, boardArray):
        return (boardArray[x][y] == self.ID?) True : False

