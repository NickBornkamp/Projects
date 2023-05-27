import random
import copy
import math

class Agent:
    def __init__(self, color, name, oppColor):
        self.name = name
        self.color = color
        self.oppColor = oppColor
        self.multiplier = 1

        self.cap = 0
        self.multiplier = 3
        self.reducer = 1

    def moveChosen(self, board):
        scores = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.boardScore(board, scores, self.color, self.multiplier)    
        
        sortedScores = dict(sorted(scores.items(), key=lambda x:x[1], reverse=True))
        print(sortedScores)
        for move in sortedScores:
            if(board.validMove(move)):
                return move
        return 4

    
    def boardScore(self, board, scores, color, multiplier):
            #print(multiplier)
            if(multiplier <= self.cap):
                return
            
            #print(color)

            mult = multiplier * 1 if color == self.color else multiplier * 0.8
            for option in scores:
                nextBoard = copy.deepcopy(board)
                nextBoard.insertPiece(option, color)

                if(nextBoard.checkWin(color)):
                    scores[option] += round(10 * mult)
                else:
                    nextColor = self.color if color != self.color else self.oppColor
                    self.boardScore(nextBoard, scores, nextColor, multiplier - self.reducer)

                if(multiplier == self.multiplier and option == 4):
                    print("Thinking...")
                elif(scores[option] > 5000):
                    return


class RandAgent(Agent):

    def moveChosen(self, board):
        return random.randint(1, 7)
    


class ReinforcementAgent(Agent):

    def __init__(self, color, name, oppColor):
        super().__init__(color, name, oppColor)
        
        self.cap = 0
        self.multiplier = 3
        self.reducer = 1


    
    
               

class DeepAgent(Agent):
    def __init__(self, color, name, oppColor):
        super().__init__(color, name, oppColor)
        
        self.cap = 0
        self.multiplier = 6
        self.reducer = 1

        print("Mr. Deep can think ", math.ceil(self.multiplier/self.reducer), " moves ahead!")

    

    

class InfiniteAgent(Agent):
    def __init__(self, color, name, oppColor):
        super().__init__(color, name, oppColor)
        
        self.cap = 0
        self.multiplier = 25
        self.reducer = 5

        print("The Infinite can think ", math.ceil(self.multiplier/self.reducer), " moves ahead!")

    

    
    def moveChosen(self, board):
        scores = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.boardScore(board, scores, self.color, self.multiplier)    
        
        sortedScores = dict(sorted(scores.items(), key=lambda x:x[1], reverse=True))
        print(sortedScores)
        for move in sortedScores:
            if(board.validMove(move)):
                return move
        return 4
    

    def boardScore(self, board, scores, color, multiplier):
            #print(multiplier)
            if(multiplier <= self.cap):
                return
            
                
            #print(color)

            mult = multiplier
            for option in scores:
                if(scores[option] > 2000):
                    return
                if(multiplier == self.multiplier and option == 4):
                    print("Thinking...")
                nextBoard = copy.deepcopy(board)
                nextBoard.insertPiece(option, color)
                nextColor = self.color if color != self.color else self.oppColor
                for option in scores:
                    nextnextBoard = copy.deepcopy(nextBoard)
                    nextnextBoard.insertPiece(option, nextColor)

                    if(nextBoard.checkWin(self.color)):
                        scores[option] += mult
                    elif(nextnextBoard.checkWin(self.oppColor)):
                        scores[option] += mult * 2
                
                self.boardScore(nextnextBoard, scores, color, multiplier - self.reducer)    

                