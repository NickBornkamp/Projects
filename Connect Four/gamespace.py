class Board:
    def __init__(self):
        self.board = []
        for column in range(0,7): # 7 columns, 1 to 7
            col = []
            for row in range(0, 6): # 6 rows, 1 to 6
                col.append("E")
            
            self.board.append(col)
       

    def __str__(self):
        rotated = list(zip(*self.board[::-1]))
        output = []
        for column in rotated: # 6 rows, 1 to 6
                col = []
                for piece in column:
                    col.insert(0, piece)
                output.insert(0, " | ".join(col))
        return "\n".join(output)      

    def getRow(self, col):
        colList = []
        for row in self.board:
            colList.append(row[col])
        
        return colList

    def checkRow(self, piece, color):
        row = self.getRow(piece[1])
        try:
            nextThree = row[(piece[0] + 1):(piece[0]+4)]
        except:
            return False
        
        if(nextThree.count(color) == 3):
            #print("Row")
            return True
        return False
    
    def checkCol(self, piece, color):
        col = self.board[piece[0]]
        try:
            nextThree = col[(piece[1] + 1):(piece[1]+4)]
        except:
            return False
        
        if(nextThree.count(color) == 3):
            #print("Column")
            return True
        
        return False
    
    def checkDiag(self, piece, color):
        diagPos = []
        diagNeg = []
        try:
            for i in range(1, 4):
                diagPos.append(self.board[piece[0]+i][piece[1]+i])
        except:
            x = 1
        try:
            for i in range(1, 4):
                diagNeg.append(self.board[piece[0]-i][piece[1]+i])
        except:
            x = 1

        if(diagPos.count(color) == 3 or diagNeg.count(color) == 3):
            #print(diagPos)
            #print(diagNeg)
            return True
        return False

    

    def checkWin(self, color):
        for col in range(0, 7):
            for row in range(0, 6):
                piece = (col, row)
                if(self.board[col][row] == color and (self.checkRow(piece, color) or self.checkCol(piece, color) or self.checkDiag(piece, color))):
                    return True
        return False

    def checkFull(self):
        for col in self.board:
            if(col.count("E") != 0):
                return False
        return True

    def validMove(self, column):
        if(column < 1 or column > 7):
            return False
        col = self.board[column - 1]
        row = col.index("E") if "E" in col else -1
        if(row == -1):
            return False
        return True

    def insertPiece(self, column, color):
        row = -1
        if(self.validMove(column)):
            col = self.board[column - 1]
            row = col.index("E") if "E" in col else -1
            self.board[column - 1][row] = color
        return row
        
    
        

board = Board()