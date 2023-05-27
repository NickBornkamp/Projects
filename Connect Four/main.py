from gamespace import Board
from agent import *

from tkinter import *
from tkinter import messagebox
import numpy as np




size_of_board = 800
symbol_size = 30
symbol_thickness = 10

redColor = '#EE4035'
yellowColor = '#eeee00'


print("Welcome to connect four")





class ConnectFour():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self, numPlayers, goingFirst, agentName):
        self.numPlayers = numPlayers
        self.board = Board()

        self.colors = ["R", "Y"]
        self.guiColors = [redColor, yellowColor]


        self.playerColor = "R" if goingFirst else "Y"
        self.opponentColor = "Y" if goingFirst else "R"

        self.turnPlayer = "R"
        
        print(self.playerColor)

        self.turn = 0
        self.gameover = False
        print(self.board)


        agents = [RandAgent(self.opponentColor, "Randy", self.playerColor), 
                ReinforcementAgent(self.opponentColor, "Arnold", self.playerColor),
                DeepAgent(self.opponentColor, "Mr. Deep", self.playerColor),
                InfiniteAgent(self.opponentColor, "The Infinite", self.playerColor)]
        self.agent = [agent for agent in agents if agent.name == agentName][0]

        print("Challenger: ", self.agent.name)

        self.window = Tk()
        
        self.window.title(('Connect 4: '+ "R Turn"))
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.grid(row =0, column = 0, sticky = W, pady = 2)
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)
        self.window.protocol("WM_DELETE_WINDOW", self._quit)

        self.statusText = StringVar()
        self.state = Label(self.window, textvariable= self.statusText )        
        
        self.state.config(font=('Helvetica bold', 40))
        
        self.state.grid(row = 1, column = 1, sticky = W)
        self.statusText.set("Hello!")

        self.initialize_board()
        
        print("yeehaw")
        
        if(self.numPlayers == 1 and self.turnPlayer == self.agent.color):
            print("My turns")
            colorO = self.guiColors[self.turn % 2]
            self.checkStatus(self.agent.moveChosen(self.board), colorO)
        
        self.window.update()
        
    def _quit(self):
        self.window.quit()
        self.window.destroy()
        quit()


        


    def initialize_board(self):
        for i in range(7):
            self.canvas.create_line((i + 1) * size_of_board / 7, 0, (i + 1) * size_of_board / 7, size_of_board)

        for i in range(5, 0, -1):
            self.canvas.create_line(0, (i + 1) * size_of_board / 7, size_of_board, (i + 1) * size_of_board / 7)

    

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position, colorO):
        logical_position = np.array(logical_position)
        print(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        print(grid_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=colorO)

    

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board ) / 7 * logical_position + size_of_board / 15

    def convert_grid_to_logical_position(self, grid_position):
        
        return np.array(grid_position // (size_of_board / 7), dtype=int)


    def makeMove(self, column):
        self.turnPlayer = self.colors[self.turn % 2]
        colorO = self.guiColors[self.turn % 2]
        self.checkStatus(column, colorO)


    def checkStatus(self, col, colorO):
        if(self.board.validMove(col)):
            row = self.board.insertPiece(col,  self.turnPlayer)
            logical_position = [col-1, 6-row]
            self.draw_O(logical_position, colorO)
            self.turn+=1
            print(self.board)
            
        else:
            print("Invalid move, try again")
            self.turn -= 1
        
        if(self.board.checkFull()):
            print("It's a draw. Play something else!")

        elif(self.board.checkWin( self.turnPlayer)):
            print("Winner: ",  self.turnPlayer)
            messagebox.showinfo("Winner!", (self.turnPlayer + " Won!"))
            self.gameover = True
            self.updateStatus(self.turnPlayer)
            
        else:
            print("Nothing yet")
            self.turnPlayer = self.colors[self.turn % 2]
            colorO = self.guiColors[self.turn % 2]

            self.updateStatus(self.turnPlayer)
            if(self.numPlayers == 1 and self.turnPlayer == self.agent.color):
                print("My turns")
                colorO = self.guiColors[self.turn % 2]
                self.checkStatus(self.agent.moveChosen(self.board), colorO)

        

        

    def click(self, event):
        print(self.numPlayers, " ", self.turnPlayer)
        print(self.turnPlayer == self.agent.oppColor)
        colorO = self.guiColors[self.turn % 2]
        #print(self.numPlayers == 1 and self.turnPlayer == self.agent.oppColor)

        if(not self.gameover):
            if(self.numPlayers == 1 and self.turnPlayer == self.playerColor):
                placement = event.x
                logical_position = self.convert_grid_to_logical_position(placement)
                self.checkStatus(logical_position + 1, colorO)
            

            elif(self.numPlayers == 2):
                placement = event.x
                logical_position = self.convert_grid_to_logical_position(placement)
                self.checkStatus(logical_position + 1, colorO)
        
    

    def updateStatus(self, winColor):
        output = "Connect 4: " + winColor + " Turn"
        
        self.window.title(output)
        if(self.gameover):
            output = "Victory for " + winColor
        self.statusText.set(output)
        print(str(self.statusText.get()))
        self.window.update()


        
        
    
class Menu:

    def __init__(self) -> None:
        
        self.top = Tk()
        self.top.geometry("400x400")

        B = Button(self.top, text ="Begin", command = self.begin)
        B.grid(row =3, column = 3, sticky = E, pady = 2)

        self.radioPlayers()
        self.radioAgents()
        self.firstCheckbox()

        self.top.mainloop()


    def radioPlayers(self):
        self.players = IntVar()
        self.players.set(1)
        R1 = Radiobutton(self.top, text="1 Player", variable=self.players, value=1,
                command=self.sel(1))
        

        R2 = Radiobutton(self.top, text="2 Players", variable=self.players, value=2,
                command=self.sel(2))
        

        R1.grid(row = 0, column = 0, sticky = W, padx = 3, pady = 2)
        R2.grid(row = 1, column = 0, sticky = W, padx = 3, pady = 2)

    def radioAgents(self):
            self.agent = StringVar()
            self.agent.set("Randy")
            
            R1 = Radiobutton(self.top, text="Randy the Random", variable=self.agent, value="Randy")

            R2 = Radiobutton(self.top, text="Arnold (Easy)", variable=self.agent, value="Arnold",)

            R3 = Radiobutton(self.top, text="Mr. Deep (Hard)", variable=self.agent, value="Mr. Deep")

            R4 = Radiobutton(self.top, text="The Infinite (Weird)", variable=self.agent, value="The Infinite")

            R1.grid(row = 0, column = 1, sticky = W, pady = 2)
            R2.grid(row = 1, column = 1, sticky = W, pady = 2)
            R3.grid(row = 2, column = 1, sticky = W, pady = 2)
            R4.grid(row = 3, column = 1, sticky = W, pady = 2)

    def firstCheckbox(self):
        self.goFirst = IntVar()
        self.goFirst.set(1)
        c1 = Checkbutton(self.top, text="Go first?", variable=self.goFirst, onvalue=1, offvalue=0)
        c1.grid(row = 0, column = 2, sticky = W, pady = 2)



    def begin(self):
        self.top.withdraw()
        numPlayers = int(self.players.get())
        agent = str(self.agent.get())
        goFirst = int(self.goFirst.get())

        game_instance = ConnectFour(numPlayers, goFirst, agent)
        

    def sel(self, value):
        pass
        



if __name__ == "__main__":
    menu = Menu()






    
